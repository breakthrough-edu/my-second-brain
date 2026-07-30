"""Core logic for session-history: schema, incremental ingest, and queries.

Python 3 standard library only. Reads Claude Code session transcripts
(`~/.claude/projects/<slug>/<uuid>.jsonl`) strictly read-only and indexes
conversational text + tool calls into a FTS5 SQLite database.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import os
import re
import sqlite3
import sys
import time
from typing import Iterable, Iterator, Optional

SCHEMA_VERSION = 2

# Cap on how much of any single text/tool payload we index. Never shove
# base64 blobs or huge tool results into FTS.
MAX_TEXT_BYTES = 2048

# Filenames that are not conversation transcripts and must not be indexed.
_SKIP_FILENAMES = {"journal.jsonl"}


# --------------------------------------------------------------------------
# Paths + config
# --------------------------------------------------------------------------
#
# All owner-specific paths come from config, never from code. Precedence for
# each path: CLI flag > environment variable > config file > generic default.
# The config file is optional JSON at ~/.my-second-brain/session-history.json
# (override the location itself with SESSION_HISTORY_CONFIG). Recognised keys:
#
#   vault      absolute path to the owner's vault; harvest reports default to
#              <vault>/00_Inbox/
#   inbox      explicit report directory (wins over vault-derived inbox)
#   db         database path
#   projects   Claude Code transcripts directory
#
# State (the database, and with it the harvest bookmark) defaults to
# ~/.my-second-brain/, deliberately OUTSIDE any skill or repo directory, so a
# skill update or reinstall can never wipe the index or the bookmark.

DEFAULT_CONFIG_PATH = "~/.my-second-brain/session-history.json"
DEFAULT_STATE_DIR = "~/.my-second-brain"


def load_config() -> dict:
    path = os.environ.get("SESSION_HISTORY_CONFIG") or DEFAULT_CONFIG_PATH
    try:
        with open(os.path.expanduser(path), encoding="utf-8") as f:
            cfg = json.load(f)
        return cfg if isinstance(cfg, dict) else {}
    except (OSError, ValueError):
        return {}


def _resolve(env_var: str, cfg_key: str, fallback: Optional[str]) -> Optional[str]:
    env = os.environ.get(env_var)
    if env:
        return os.path.abspath(os.path.expanduser(env))
    cfg = load_config().get(cfg_key)
    if cfg:
        return os.path.abspath(os.path.expanduser(str(cfg)))
    if fallback:
        return os.path.abspath(os.path.expanduser(fallback))
    return None


def default_db_path() -> str:
    return _resolve(
        "SESSION_HISTORY_DB", "db", os.path.join(DEFAULT_STATE_DIR, "session-history.db")
    )


def default_projects_dir() -> str:
    return _resolve("SESSION_HISTORY_PROJECTS", "projects", "~/.claude/projects")


def default_inbox_dir() -> Optional[str]:
    """Directory harvest reports land in, or None if unconfigured.

    No baked-in default: the report belongs in the owner's vault Inbox, and
    only config (or SESSION_HISTORY_INBOX / the vault key) knows where that is.
    Callers must ask for an explicit --out when this returns None.
    """
    explicit = _resolve("SESSION_HISTORY_INBOX", "inbox", None)
    if explicit:
        return explicit
    vault = load_config().get("vault")
    if vault:
        return os.path.join(os.path.abspath(os.path.expanduser(str(vault))), "00_Inbox")
    return None


# --------------------------------------------------------------------------
# FTS5 runtime probe
# --------------------------------------------------------------------------
#
# The entire index is a FTS5 virtual table, so a SQLite build without the FTS5
# extension cannot run this tool at all. Most Python builds ship FTS5
# (python.org, the Microsoft Store build, macOS system Python, Homebrew); the
# one common exception is Anaconda / Miniconda, whose bundled SQLite is
# compiled without it. Rather than let `init_db` die on a cryptic
# `no such module: fts5`, we probe once at connect time and fail soft with a
# plain-language fix. This is a cross-platform defensive check, not a
# Windows-only one; Windows students just hit it most often.

FTS5_MISSING_MESSAGE = (
    "session-history needs SQLite built with the FTS5 full-text extension, and "
    "this Python does not have it.\n"
    "This almost always means you are on Anaconda or Miniconda, whose bundled "
    "SQLite is compiled without FTS5.\n"
    "Fix: run session-history with Python from python.org (or the Microsoft "
    "Store build on Windows), not Anaconda. Both ship SQLite with FTS5.\n"
    "To see which Python you are on, run: "
    'python -c "import sys; print(sys.executable)"'
)


class FTS5Unavailable(RuntimeError):
    """Raised when the runtime SQLite lacks FTS5, carrying a human-readable fix."""

    def __init__(self, message: str = FTS5_MISSING_MESSAGE):
        super().__init__(message)


def fts5_available() -> bool:
    """True if this Python's SQLite was compiled with the FTS5 extension.

    Probed against a throwaway in-memory database so the check never creates
    files or touches the real index. Microseconds; safe to call on every run.
    """
    try:
        probe = sqlite3.connect(":memory:")
    except sqlite3.Error:
        return False
    try:
        probe.execute("CREATE VIRTUAL TABLE _fts5_probe USING fts5(x)")
        return True
    except sqlite3.Error:
        return False
    finally:
        probe.close()


# --------------------------------------------------------------------------
# Schema / connection
# --------------------------------------------------------------------------

_SCHEMA = """
CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS sessions (
    id            TEXT PRIMARY KEY,   -- session uuid (jsonl filename stem)
    project       TEXT,               -- project slug (parent dir name)
    path          TEXT,               -- absolute path to the .jsonl file
    title         TEXT,               -- from custom-title line if present
    started_at    TEXT,               -- min timestamp seen
    last_ts       TEXT,               -- max timestamp seen
    line_count    INTEGER DEFAULT 0,  -- complete jsonl lines consumed
    byte_offset   INTEGER DEFAULT 0,  -- bytes consumed (incremental cursor)
    size_at_ingest INTEGER DEFAULT 0, -- file size observed at last ingest
    harvested     INTEGER DEFAULT 0,  -- per-session bookmark for WS2 "harvest"
    harvested_at  TEXT                -- nullable
);

CREATE VIRTUAL TABLE IF NOT EXISTS messages USING fts5(
    session_id,
    ts,
    role,
    text,
    tool_name,
    line_index UNINDEXED,
    block_index UNINDEXED,
    tokenize = 'unicode61'
);

CREATE TABLE IF NOT EXISTS harvest_state (
    id        INTEGER PRIMARY KEY CHECK (id = 1),
    last_run  TEXT,               -- last time a harvest pass ran
    sessions_harvested INTEGER DEFAULT 0,
    notes     TEXT
);
"""


def connect(db_path: Optional[str] = None) -> sqlite3.Connection:
    # Probe FTS5 before creating the state directory or opening the file, so a
    # SQLite without FTS5 fails soft with a fix instead of a cryptic
    # `no such module: fts5` the first time the schema builds the virtual table.
    if not fts5_available():
        raise FTS5Unavailable()
    path = db_path or default_db_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(_SCHEMA)
    row = conn.execute("SELECT version FROM schema_version LIMIT 1").fetchone()
    if row is None:
        conn.execute("INSERT INTO schema_version(version) VALUES (?)", (SCHEMA_VERSION,))
    row = conn.execute("SELECT id FROM harvest_state WHERE id=1").fetchone()
    if row is None:
        conn.execute(
            "INSERT INTO harvest_state(id, last_run, sessions_harvested, notes) VALUES (1, NULL, 0, NULL)"
        )
    conn.commit()


def _maybe_migrate(conn: sqlite3.Connection) -> int:
    """Re-parse the sessions whose stored rows predate the current message shape.

    v1 folded tool_result and thinking blocks into the same text the miner
    reads, so a v1 row cannot be told apart from a v2 row by inspecting it.
    Re-parsing is the only honest fix, and the only sessions that CAN be
    re-parsed are the ones whose transcript is still on disk (Claude Code
    deletes them after about 30 days). Orphans keep their v1 rows on purpose:
    a stale shape beats no content, `search` still finds them, and their
    `harvested` bookmarks stay exactly where they were.

    Deliberately NOT hung off `init_db`. `harvest` and `harvest_commit` call
    that too, and the distill has a path that reviews an existing report
    without ever ingesting; wiping messages there would empty the index with
    nothing queued to rebuild it.

    The deletes and the version stamp share one transaction, so an interrupted
    run self-heals rather than half-migrating: a session left at byte_offset 0
    against a non-zero file size is exactly what the ordinary change detector
    picks up on the next ingest, no re-run of the migration and no double
    delete. Never migrates downward, a database written by a newer version is
    left alone.

    Returns the number of sessions queued for re-parse.
    """
    row = conn.execute("SELECT version FROM schema_version LIMIT 1").fetchone()
    version = row["version"] if row else SCHEMA_VERSION
    if version >= SCHEMA_VERSION:
        return 0

    stale = [
        r["id"]
        for r in conn.execute("SELECT id, path FROM sessions").fetchall()
        if r["path"] and os.path.exists(r["path"])
    ]
    try:
        for sid in stale:
            conn.execute("DELETE FROM messages WHERE session_id=?", (sid,))
            conn.execute(
                "UPDATE sessions SET byte_offset=0, line_count=0 WHERE id=?", (sid,)
            )
        conn.execute("UPDATE schema_version SET version=?", (SCHEMA_VERSION,))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    return len(stale)


# --------------------------------------------------------------------------
# Parsing helpers
# --------------------------------------------------------------------------

def _truncate(text: str, limit: int = MAX_TEXT_BYTES) -> str:
    if text is None:
        return ""
    b = text.encode("utf-8", errors="replace")
    if len(b) <= limit:
        return text
    return b[:limit].decode("utf-8", errors="ignore") + " …[truncated]"


# Pseudo tool_name marking an assistant `thinking` block. Not a real tool; it
# parks reasoning in a row the harvest query skips while `sh search` still finds
# it. Changing this string requires a re-ingest to take effect on old rows.
THINKING_TOOL_NAME = "__thinking__"


def _flatten_tool_result(content) -> str:
    """tool_result content may be a string or a list of blocks."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for b in content:
            if isinstance(b, dict):
                if b.get("type") == "text":
                    parts.append(str(b.get("text", "")))
                elif "text" in b:
                    parts.append(str(b.get("text", "")))
            elif isinstance(b, str):
                parts.append(b)
        return "\n".join(parts)
    if content is None:
        return ""
    return str(content)


def _rows_for_line(obj: dict) -> Iterator[tuple]:
    """Yield (role, text, tool_name, block_index) FTS rows for one jsonl line.

    Only conversational line types (user/assistant) produce rows. Metadata
    lines yield nothing. A single message may yield several rows: one for its
    concatenated text/thinking, plus one per tool_use / tool_result block.
    """
    ltype = obj.get("type")
    if ltype not in ("user", "assistant"):
        return

    msg = obj.get("message")
    if not isinstance(msg, dict):
        return
    role = msg.get("role") or ltype
    content = msg.get("content")

    # Plain-string content (common for user prompts).
    if isinstance(content, str):
        txt = content.strip()
        if txt:
            yield (role, _truncate(txt), None, 0)
        return

    if not isinstance(content, list):
        return

    text_parts = []
    extra_rows = []  # (role, text, tool_name, block_index)
    for i, block in enumerate(content):
        if not isinstance(block, dict):
            if isinstance(block, str) and block.strip():
                text_parts.append(block.strip())
            continue
        btype = block.get("type")
        if btype == "text":
            t = str(block.get("text", "")).strip()
            if t:
                text_parts.append(t)
        elif btype == "thinking":
            # Own row, tagged, NOT concatenated into the visible-prose row.
            # Merged in, the assistant's private reasoning was indistinguishable
            # from what it actually said, and harvest mined it as owner signal.
            # The THINKING_TOOL_NAME marker keeps it fully searchable while the
            # harvest query (tool_name IS NULL) skips it.
            t = str(block.get("thinking", "")).strip()
            if t:
                extra_rows.append((role, _truncate(t), THINKING_TOOL_NAME, i))
        elif btype == "tool_use":
            name = block.get("name") or "unknown"
            inp = block.get("input", {})
            try:
                inp_str = json.dumps(inp, ensure_ascii=False)
            except (TypeError, ValueError):
                inp_str = str(inp)
            extra_rows.append((role, _truncate(inp_str), name, i))
        elif btype == "tool_result":
            res = _flatten_tool_result(block.get("content"))
            res = res.strip()
            if res:
                extra_rows.append(("tool_result", _truncate(res), None, i))

    joined = "\n".join(text_parts).strip()
    if joined:
        yield (role, joined, None, -1)  # block_index -1 = the message's text row
    for r in extra_rows:
        yield r


def _iter_complete_lines(data: bytes) -> tuple[list[bytes], int]:
    """Split `data` into complete lines (ending in \\n) plus bytes consumed.

    A trailing partial line (no newline) is left unconsumed so live sessions
    flushing mid-line are never indexed.
    """
    last_nl = data.rfind(b"\n")
    if last_nl == -1:
        return [], 0
    consumed = last_nl + 1
    complete = data[:consumed]
    lines = complete.split(b"\n")
    # split leaves a trailing empty string because complete ends in \n
    if lines and lines[-1] == b"":
        lines.pop()
    return lines, consumed


# --------------------------------------------------------------------------
# Ingest
# --------------------------------------------------------------------------

def _iter_transcript_files(projects_dir: str) -> Iterator[tuple[str, str, str]]:
    """Yield (session_id, project_slug, abs_path) for every .jsonl transcript.

    Walks recursively so nested subagent transcripts
    (`<slug>/<session>/subagents/agent-*.jsonl`) are indexed too. The project
    slug is always the first path component under `projects_dir`; the
    session_id is the filename stem (uuids and `agent-<id>` names are unique).
    """
    if not os.path.isdir(projects_dir):
        return
    seen_ids: dict[str, str] = {}
    for slug in sorted(os.listdir(projects_dir)):
        pdir = os.path.join(projects_dir, slug)
        if not os.path.isdir(pdir):
            continue
        for dirpath, dirnames, filenames in os.walk(pdir):
            dirnames.sort()
            for fn in sorted(filenames):
                if not fn.endswith(".jsonl"):
                    continue
                # `journal.jsonl` files are internal workflow bookkeeping
                # (started/result records), not conversation transcripts, and
                # every workflow reuses the same name. Skip them.
                if fn in _SKIP_FILENAMES:
                    continue
                path = os.path.join(dirpath, fn)
                session_id = fn[: -len(".jsonl")]
                # Defense-in-depth: filename stems are unique in practice, but
                # never let two files collide onto one primary key.
                if seen_ids.get(session_id, path) != path:
                    h = hashlib.sha1(path.encode("utf-8")).hexdigest()[:8]
                    session_id = f"{session_id}__{h}"
                seen_ids[session_id] = path
                yield session_id, slug, path


def _ingest_file(
    conn: sqlite3.Connection,
    session_id: str,
    project: str,
    path: str,
) -> int:
    """Ingest one transcript file incrementally. Returns rows inserted."""
    try:
        size = os.path.getsize(path)
    except OSError:
        return 0

    existing = conn.execute(
        "SELECT byte_offset, line_count, started_at, last_ts, title FROM sessions WHERE id=?",
        (session_id,),
    ).fetchone()

    start = 0
    base_line_index = 0
    prev_started = None
    prev_last = None
    prev_title = None
    truncated = False

    if existing is not None:
        stored_offset = existing["byte_offset"] or 0
        if size == stored_offset:
            # No new complete-or-partial bytes since last ingest: unchanged.
            return 0
        if size < stored_offset:
            # File shrank: truncation / compaction / rewrite. Re-ingest from 0.
            conn.execute("DELETE FROM messages WHERE session_id=?", (session_id,))
            truncated = True
            start = 0
            base_line_index = 0
        else:
            start = stored_offset
            base_line_index = existing["line_count"] or 0
            prev_started = existing["started_at"]
            prev_last = existing["last_ts"]
            prev_title = existing["title"]

    with open(path, "rb") as fh:
        fh.seek(start)
        data = fh.read()

    lines, consumed = _iter_complete_lines(data)
    new_offset = start + consumed

    inserted = 0
    line_index = base_line_index
    started_at = prev_started
    last_ts = prev_last
    title = prev_title

    insert_rows = []
    for raw in lines:
        idx = line_index
        line_index += 1
        if not raw.strip():
            continue
        try:
            obj = json.loads(raw.decode("utf-8", errors="replace"))
        except (ValueError, UnicodeDecodeError):
            continue

        if obj.get("type") == "custom-title":
            ct = obj.get("customTitle") or obj.get("title")
            if ct:
                title = ct
            continue

        ts = obj.get("timestamp")
        if ts:
            if started_at is None or ts < started_at:
                started_at = ts
            if last_ts is None or ts > last_ts:
                last_ts = ts

        for (role, text, tool_name, block_index) in _rows_for_line(obj):
            insert_rows.append(
                (session_id, ts or "", role, text, tool_name, idx, block_index)
            )
            inserted += 1

    if insert_rows:
        conn.executemany(
            "INSERT INTO messages(session_id, ts, role, text, tool_name, line_index, block_index) "
            "VALUES (?,?,?,?,?,?,?)",
            insert_rows,
        )

    # Upsert session metadata.
    conn.execute(
        """
        INSERT INTO sessions(id, project, path, title, started_at, last_ts,
                             line_count, byte_offset, size_at_ingest)
        VALUES (?,?,?,?,?,?,?,?,?)
        ON CONFLICT(id) DO UPDATE SET
            project=excluded.project,
            path=excluded.path,
            title=COALESCE(excluded.title, sessions.title),
            started_at=excluded.started_at,
            last_ts=excluded.last_ts,
            line_count=excluded.line_count,
            byte_offset=excluded.byte_offset,
            size_at_ingest=excluded.size_at_ingest
        """,
        (
            session_id,
            project,
            path,
            title,
            started_at,
            last_ts,
            line_index,
            new_offset,
            size,
        ),
    )
    return inserted


def ingest(
    conn: sqlite3.Connection,
    projects_dir: Optional[str] = None,
    progress: bool = True,
) -> dict:
    """Incremental, idempotent ingest across all transcript files.

    Returns a stats dict: {files_scanned, files_changed, rows_inserted, seconds}.
    """
    projects_dir = projects_dir or default_projects_dir()
    init_db(conn)
    migrated = _maybe_migrate(conn)
    if migrated and progress:
        print(f"session-history: index format v1 to v2, re-reading {migrated} "
              f"conversation(s). One time only.", file=sys.stderr)

    t0 = time.time()
    files = list(_iter_transcript_files(projects_dir))

    # Cheap pre-pass: figure out which files actually have new bytes so we can
    # print an honest "indexing N changed files" line before a long first run.
    changed = []
    existing = {
        r["id"]: r["byte_offset"]
        for r in conn.execute("SELECT id, byte_offset FROM sessions").fetchall()
    }
    for session_id, project, path in files:
        try:
            size = os.path.getsize(path)
        except OSError:
            continue
        if existing.get(session_id) != size:  # unknown, grew, or shrank
            changed.append((session_id, project, path))

    if progress and changed:
        print(f"session-history: indexing {len(changed)} changed file(s) "
              f"of {len(files)} total…", file=sys.stderr)

    rows_inserted = 0
    for i, (session_id, project, path) in enumerate(changed, 1):
        rows_inserted += _ingest_file(conn, session_id, project, path)
        if progress and len(changed) > 50 and i % 100 == 0:
            print(f"  … {i}/{len(changed)} files, {rows_inserted} rows", file=sys.stderr)
            conn.commit()

    conn.commit()
    stats = {
        "files_scanned": len(files),
        "files_changed": len(changed),
        "rows_inserted": rows_inserted,
        "seconds": round(time.time() - t0, 2),
    }
    return stats


# --------------------------------------------------------------------------
# Query helpers
# --------------------------------------------------------------------------

_TOKEN_RE = re.compile(r"[^\W_]+", re.UNICODE)


def _fts_query(raw: str) -> str:
    """Turn arbitrary user input into a safe FTS5 MATCH expression.

    We quote each token as a phrase term (implicit AND) so punctuation like
    `rm -rf` or `S09` never trips FTS5's query syntax.
    """
    tokens = _TOKEN_RE.findall(raw)
    if not tokens:
        # Fall back to a quoted literal of the whole string.
        return '"' + raw.replace('"', '""') + '"'
    return " ".join('"' + t.replace('"', '""') + '"' for t in tokens)


def search(conn: sqlite3.Connection, query: str, limit: int = 20) -> list[dict]:
    match = _fts_query(query)
    sql = """
        SELECT m.session_id AS session_id,
               s.project AS project,
               s.title AS title,
               s.started_at AS started_at,
               s.last_ts AS last_ts,
               m.role AS role,
               m.tool_name AS tool_name,
               m.ts AS ts,
               snippet(messages, 3, '«', '»', ' … ', 12) AS snippet,
               bm25(messages) AS score
        FROM messages m
        JOIN sessions s ON s.id = m.session_id
        WHERE messages MATCH ?
        ORDER BY score
        LIMIT ?
    """
    try:
        rows = conn.execute(sql, (match, limit)).fetchall()
    except sqlite3.OperationalError:
        # Last-ditch: quote the whole thing literally.
        safe = '"' + query.replace('"', '""') + '"'
        rows = conn.execute(sql, (safe, limit)).fetchall()
    return [dict(r) for r in rows]


def show(conn: sqlite3.Connection, session_id: str, limit: int = 1000) -> dict:
    sess = conn.execute("SELECT * FROM sessions WHERE id=?", (session_id,)).fetchone()
    if sess is None:
        # Allow prefix match on the uuid for convenience.
        sess = conn.execute(
            "SELECT * FROM sessions WHERE id LIKE ? LIMIT 1", (session_id + "%",)
        ).fetchone()
        if sess is None:
            return {}
        session_id = sess["id"]
    rows = conn.execute(
        """
        SELECT ts, role, tool_name, text, line_index, block_index
        FROM messages WHERE session_id=?
        ORDER BY line_index, block_index
        LIMIT ?
        """,
        (session_id, limit),
    ).fetchall()
    return {"session": dict(sess), "messages": [dict(r) for r in rows]}


def recent(conn: sqlite3.Connection, n: int = 10) -> list[dict]:
    rows = conn.execute(
        """
        SELECT id, project, title, started_at, last_ts, line_count
        FROM sessions
        ORDER BY COALESCE(last_ts, started_at) DESC
        LIMIT ?
        """,
        (n,),
    ).fetchall()
    out = []
    for r in rows:
        d = dict(r)
        if not d.get("title"):
            # Fall back to the first user prompt as a summary.
            fr = conn.execute(
                """
                SELECT text FROM messages
                WHERE session_id=? AND role='user'
                ORDER BY line_index LIMIT 1
                """,
                (d["id"],),
            ).fetchone()
            d["summary"] = (fr["text"].splitlines()[0][:100] if fr else "(no title)")
        else:
            d["summary"] = d["title"]
        out.append(d)
    return out


def actions(conn: sqlite3.Connection, session_id: str, limit: int = 500) -> list[dict]:
    sess = conn.execute("SELECT id FROM sessions WHERE id=?", (session_id,)).fetchone()
    if sess is None:
        sess = conn.execute(
            "SELECT id FROM sessions WHERE id LIKE ? LIMIT 1", (session_id + "%",)
        ).fetchone()
        if sess is None:
            return []
        session_id = sess["id"]
    rows = conn.execute(
        """
        SELECT ts, tool_name, text
        FROM messages
        WHERE session_id=? AND tool_name IS NOT NULL
        ORDER BY line_index, block_index
        LIMIT ?
        """,
        (session_id, limit),
    ).fetchall()
    return [dict(r) for r in rows]


# --------------------------------------------------------------------------
# WS2: Harvest pipeline
# --------------------------------------------------------------------------
#
# Once a week, read sessions that have not yet been "harvested" and PROPOSE
# candidate long-term memories / decisions / notes for the human to APPROVE.
# The AI only proposes; nothing is written to memory automatically, and the
# proposal run NEVER flips the `harvested` bookmark. Only human approval, replayed
# through `harvest_commit`, consumes the bookmark. This keeps proposal idempotent
# and re-runnable: a garbage first report can be regenerated without silently
# burning the sessions it covered.

# How recent a session's file mtime may be and still be considered "quiescent".
# A session whose transcript was touched within this window may still be live
# (mid-write), so it is never harvested.
QUIESCENT_SECONDS = 24 * 3600

# Deliberate cap on the first pass so the report stays reviewable for signal /
# noise. Qualifying sessions beyond this are reported as capped-out, never
# silently dropped, and (because no flag flips) are re-proposed next run.
HARVEST_MAX_DEFAULT = 30

_UTC = datetime.timezone.utc


def _parse_now(now) -> datetime.datetime:
    """Normalise a caller-supplied reference instant to a tz-aware UTC datetime.

    Accepts a `datetime`, a full ISO-8601 string, or a bare `YYYY-MM-DD` date
    (interpreted as that date at 00:00:00 UTC). We take an explicit reference
    instant rather than calling the system clock so a harvest run is
    deterministic and reproducible.
    """
    if isinstance(now, datetime.datetime):
        dt = now
    else:
        s = str(now).strip()
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        try:
            dt = datetime.datetime.fromisoformat(s)
        except ValueError:
            dt = datetime.datetime.fromisoformat(s[:10])  # bare date
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=_UTC)
    return dt.astimezone(_UTC)


def _now_date(now) -> str:
    return _parse_now(now).date().isoformat()


def _project_label(slug: Optional[str]) -> str:
    """Turn a project-dir slug into a short human label.

    Claude Code slugs are the cwd with separators flattened to dashes
    (`-Users-<name>-Documents-My-Vault-...`). We keep the last few meaningful
    path-ish components so the report reads like a place, not a mangle.
    """
    if not slug:
        return "(unknown)"
    parts = [p for p in slug.strip("-").split("-") if p]
    # Drop home-prefix noise: whatever this machine's home path contributes
    # (e.g. Users/<name>) plus the usual home-folder waypoints.
    drop = {p for p in os.path.expanduser("~").split(os.sep) if p}
    drop.update({"Users", "home", "Documents", "Desktop"})
    meaningful = [p for p in parts if p not in drop]
    tail = meaningful[-4:] if meaningful else parts[-2:]
    return "-".join(tail) if tail else slug


def _session_message_stats(conn: sqlite3.Connection, session_id: str) -> tuple[int, int]:
    """Return (user_text_rows, assistant_text_rows) for a session."""
    row = conn.execute(
        """
        SELECT
          SUM(CASE WHEN role='user'      AND tool_name IS NULL THEN 1 ELSE 0 END) AS u,
          SUM(CASE WHEN role='assistant' AND tool_name IS NULL THEN 1 ELSE 0 END) AS a
        FROM messages WHERE session_id=?
        """,
        (session_id,),
    ).fetchone()
    return (row["u"] or 0, row["a"] or 0)


def _is_quiescent(path: Optional[str], cutoff_epoch: float) -> bool:
    """True if the transcript file was last modified before the cutoff.

    A missing file is treated as quiescent (it cannot be mid-write); the
    view-builder simply finds no live bytes for it.
    """
    if not path:
        return True
    try:
        return os.path.getmtime(path) < cutoff_epoch
    except OSError:
        return True


def _dedupe_forked_sessions(qualifying: list[dict]) -> list[dict]:
    """Collapse transcript twins produced by resuming or forking a conversation.

    Resuming a session writes a SECOND jsonl for the same conversation: same
    project, same `started_at` to the millisecond, near-identical content. Both
    get indexed, so both reach the report and the reader sees the same evidence
    printed twice under two different session ids (6 such pairs in the
    2026-07-29 batch). Keep the richest twin, which is the one with the most
    user rows (tie broken by the later `last_ts`), and hang the losers on it as
    `_fork_twins` so the report's frontmatter still lists them: they were
    genuinely covered, and a commit must flip them too or they return every pass
    forever.
    """
    groups: dict[tuple, list[dict]] = {}
    order: list[tuple] = []
    for d in qualifying:
        key = (d.get("project"), d.get("started_at"))
        if not d.get("started_at"):  # no reliable fork key, never collapse
            key = ("__unique__", id(d))
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(d)

    survivors: list[dict] = []
    for key in order:
        members = groups[key]
        if len(members) == 1:
            survivors.append(members[0])
            continue
        members.sort(
            key=lambda m: (m.get("_user_rows") or 0, m.get("last_ts") or ""),
            reverse=True,
        )
        winner, losers = members[0], members[1:]
        winner["_fork_twins"] = [m["id"] for m in losers]
        survivors.append(winner)
    return survivors


def select_harvest_candidates(
    conn: sqlite3.Connection,
    now,
    max_sessions: int = HARVEST_MAX_DEFAULT,
) -> dict:
    """Select sessions eligible for a harvest pass.

    Eligible = `harvested = 0` AND quiescent (mtime older than QUIESCENT_SECONDS
    relative to `now`) AND carries real conversation (at least one user text
    message; internal `journal.jsonl` bookkeeping is already excluded at ingest)
    AND is a main session, not a subagent transcript. Subagent transcripts stay
    fully indexed and searchable, but they are machine-to-machine: no owner
    voice to mine, and their assistant text is dominated by task material
    (quoted articles, fetched pages) that reads as false gotchas. Anything that
    mattered was relayed through the main session that spawned them, which does
    qualify.

    Returns {selected, qualified, in_report, capped_out, cutoff}. `selected` is
    the `max_sessions` most-recent qualifying session rows (as dicts); the rest
    are counted as `capped_out`, never dropped silently.
    """
    ref = _parse_now(now)
    cutoff_epoch = ref.timestamp() - QUIESCENT_SECONDS

    rows = conn.execute(
        """
        SELECT id, project, path, title, started_at, last_ts, line_count,
               harvested, harvested_at
        FROM sessions
        WHERE harvested = 0
        ORDER BY COALESCE(last_ts, started_at) DESC
        """
    ).fetchall()

    qualifying: list[dict] = []
    for r in rows:
        if "/subagents/" in (r["path"] or "") or str(r["id"]).startswith("agent-"):
            continue
        if not _is_quiescent(r["path"], cutoff_epoch):
            continue
        u, a = _session_message_stats(conn, r["id"])
        if u < 1:  # no real user conversation: bookkeeping / empty transcript
            continue
        d = dict(r)
        d["_user_rows"] = u
        d["_assistant_rows"] = a
        qualifying.append(d)

    qualifying = _dedupe_forked_sessions(qualifying)

    selected = qualifying[:max_sessions]
    return {
        "selected": selected,
        "qualified": len(qualifying),
        "in_report": len(selected),
        "capped_out": len(qualifying) - len(selected),
        "cutoff": datetime.datetime.fromtimestamp(cutoff_epoch, _UTC).isoformat(),
    }


# --- compressed-view extraction ------------------------------------------

# Signal lexicons, bilingual: English plus common Chinese phrasings (owners who
# code-switch are first-class). Matched case-insensitively against message text
# lines.
# Cues that only signal a correction when the line STARTS with them ("No, use
# X"). Matched mid-line they hit street addresses ("No.4, Unit 6") and prose.
_CORRECTION_START_CUES = ("no,", "no.", "wait,")

_CORRECTION_CUES = (
    "not that", "don't ", "do not ", "instead", "actually",
    "rather", "wrong", "revert", "undo", "stop", "that's not",
    "isn't what", "i said", "please don't", "avoid", "never ", "prefer ",
    "should be", "shouldn't", "try option", "sry", "sorry",
    # "let's go with" / "let's use" / "go with option" used to live here AND in
    # _DECISION_CUES verbatim. With independent buckets that printed one line as
    # both a correction and a decision, which is where the report's duplicated
    # evidence came from. They are decision phrasings; a real correction carries
    # its own marker ("no, instead let's go with B" still trips "instead").
    "不是", "不要", "别 ", "应该", "其实", "错了", "改成", "而是", "换成", "不对",
)
_DECISION_CUES = (
    "we decided", "i decided", "let's go with", "lets go with", "going with",
    "let's use", "lets use", "we'll use", "i'll go with", "decision:",
    "final decision", "let's lock", "lock it", "locked", "approved", "let's do",
    "we should use", "the plan is", "go with option", "let's ship",
    "决定", "就用", "拍板", "定了", "改用", "就这样", "用这个",
)
_GOTCHA_CUES = (
    "error", "failed", "fails", "traceback", "exception", "gotcha",
    "doesn't work", "does not work", "not working", "broken", "bug",
    " 403", " 404", " 500", "permission denied", "turns out", "the issue is",
    "the problem is", "root cause", "workaround", "caveat", "careful",
    "报错", "失败", "不行", "问题是", "原来", "坑", "踩坑", "无法",
)

_IDEA_CUES = (
    "what if", "idea:", "how about", "i'm thinking", "im thinking",
    "worth exploring", "we could maybe", "could we maybe", "brainstorm",
    "有没有可能", "我在想", "有个想法", "点子", "或许可以", "可不可以考虑",
    "值得试", "值得探索", "有机会延伸", "延伸到",
)

_SENTINEL_PREFIXES = (
    "[image:", "[request interrupted", "<system-reminder", "caveat:",
    "[tool ", "this session is", "<command-", "<local-command-",
)

# Document markup, not speech. Pasting a handoff doc or a schema table into a
# message put its rows in front of the cue lexicons, and a table row that happens
# to contain "拍板" or "locked" then shipped as "a decision seems to have been
# locked here". Nobody says a markdown table out loud.
_MARKUP_PREFIXES = (
    "|", "```", "> |", "<td", "<tr", "<span", "<div",
    # Section headings from a pasted document. Nobody opens their mouth with
    # "## ", so dropping these costs no owner voice and stops a doc's own
    # headings ("## 拍板事项") shipping as decisions.
    "## ", "### ", "#### ",
)


def _is_markup(line: str) -> bool:
    s = line.lstrip()
    if s.startswith(_MARKUP_PREFIXES):
        return True
    # A row rendered without its leading pipe still reads as a table when it is
    # mostly cell separators.
    return s.count(" | ") >= 2


def _clean_line(text: str) -> str:
    return " ".join(text.split())


def _cue_regex(cues) -> "re.Pattern":
    """Compile a lexicon into one alternation with word-boundary discipline.

    ASCII-alphanumeric cue edges get boundary guards so "locked" cannot fire
    inside "blocked"/"unblocked" and "stop" cannot fire inside "stops". Cues
    with punctuation/space edges, and CJK cues (which have no word boundaries),
    keep plain substring semantics.
    """
    parts = []
    for c in cues:
        esc = re.escape(c)
        if c[0].isascii() and c[0].isalnum():
            esc = r"(?<![a-zA-Z0-9])" + esc
        if c[-1].isascii() and c[-1].isalnum():
            esc += r"(?![a-zA-Z0-9])"
        parts.append(esc)
    return re.compile("|".join(parts), re.IGNORECASE)


_CORRECTION_RE = _cue_regex(_CORRECTION_CUES)
_DECISION_RE = _cue_regex(_DECISION_CUES)
_GOTCHA_RE = _cue_regex(_GOTCHA_CUES)
_IDEA_RE = _cue_regex(_IDEA_CUES)


def compressed_view(conn: sqlite3.Connection, session_id: str, per_bucket: int = 6) -> dict:
    """Build a compressed view of a session for harvest.

    NOT the full transcript: title + date + project plus up to `per_bucket`
    lines each of the user's corrections/redirections, explicit decision
    statements, and gotchas/errors. Reuses the indexed `messages` table (the
    tool's own query layer) rather than re-parsing jsonl.
    """
    sess = conn.execute("SELECT * FROM sessions WHERE id=?", (session_id,)).fetchone()
    if sess is None:
        return {}
    sess = dict(sess)

    # Subagent transcripts have no human in them: every user-role message is
    # the orchestrator's brief/instructions. Mining those as "corrections" (or
    # decisions) proposes the AI's own prompt back as the owner's voice, so
    # user rows in subagent transcripts feed no bucket (they still name the
    # session via first_user).
    is_subagent = "/subagents/" in (sess.get("path") or "") or str(
        sess.get("id", "")
    ).startswith("agent-")

    # Conversation text only. `tool_name IS NULL` alone is NOT enough: tool_result
    # rows are stored with tool_name NULL and role 'tool_result', so the old filter
    # let every file read, command dump and HTTP body into the buckets (measured
    # 2026-07-29 on a 2,679-session index: 70,653 tool_result rows vs 42,788
    # assistant and 8,258 user, i.e. 58% of everything the miner saw was raw tool
    # output). Pin the role explicitly.
    rows = conn.execute(
        """
        SELECT role, text FROM messages
        WHERE session_id=? AND tool_name IS NULL AND text IS NOT NULL
          AND role IN ('user','assistant')
        ORDER BY line_index, block_index
        """,
        (session_id,),
    ).fetchall()

    corrections: list[str] = []
    decisions: list[str] = []
    gotchas: list[str] = []
    ideas: list[str] = []
    first_user = None

    for r in rows:
        role = r["role"]
        raw = r["text"] or ""
        # Injected-context spans (<system-reminder>...</system-reminder>) carry
        # the harness's own text: house rules, loaded instructions, reminders.
        # Every line inside the span is skipped, not just the opening tag,
        # otherwise standing rules echo into the buckets as fresh signal. State
        # resets per message row; if truncation ate the closing tag, the rest
        # of the row is reminder content anyway.
        in_reminder = False
        in_fence = False
        for ln in raw.splitlines():
            ln = _clean_line(ln)
            low = ln.lower()
            if low.startswith("<system-reminder"):
                in_reminder = True
            if in_reminder:
                if "</system-reminder>" in low:
                    in_reminder = False
                continue
            # Fenced blocks are pasted material, never speech. `_is_markup` only
            # ever dropped the ``` markers, so everything between them still
            # reached the lexicons: `git commit -m 'fix: we decided to lock the
            # anchor scroll'` shipped as a decision. Toggle BEFORE the length
            # gate, a bare ``` is three characters and would never be seen.
            if ln.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            if len(ln) < 8:
                continue
            if any(low.startswith(p) for p in _SENTINEL_PREFIXES):
                continue
            if _is_markup(ln):
                continue
            snippet = ln[:220]
            if role == "user":
                if first_user is None:
                    first_user = snippet
                if is_subagent:
                    continue
                # Decisions and ideas are OWNER-VOICE ONLY. They used to accept
                # assistant rows, which meant the AI's own reasoning came back as
                # "a decision seems to have been locked here" ("I'm the top-level
                # coordinator managing JW's approval gates...", "Before modifying
                # the generator in phase 4, I need to..."). What the assistant
                # thought is not what the owner decided. Gotchas stay open to
                # assistant rows on purpose: "the render failed with a 500, turns
                # out the anchor was wrong" is real signal whoever says it.
                #
                # ONE LINE, ONE BUCKET, by an explicit priority chain:
                # corrections > decisions > ideas > gotchas. Only the gotcha end
                # of it was ever enforced, so a line tripping both the decision
                # and idea lexicons printed identical evidence under two
                # headings, which is the padding the report gets judged on. A
                # line whose bucket is already full stops here rather than
                # falling through, otherwise the overflow reappears one heading
                # down wearing a different label.
                if low.startswith(_CORRECTION_START_CUES) or _CORRECTION_RE.search(ln):
                    if len(corrections) < per_bucket and snippet not in corrections:
                        corrections.append(snippet)
                    continue
                if _DECISION_RE.search(ln):
                    if len(decisions) < per_bucket and snippet not in decisions:
                        decisions.append(snippet)
                    continue
                if _IDEA_RE.search(ln):
                    if len(ideas) < per_bucket and snippet not in ideas:
                        ideas.append(snippet)
                    continue
            # One line, one bucket. A sentence can trip several lexicons at once
            # ("是不是无法支援 HEIC 的照片?" reads as both a correction and a
            # gotcha), and printing it twice under two headings just pads the
            # report. Corrections win, they are the most specific read.
            if len(gotchas) < per_bucket and snippet not in corrections and _GOTCHA_RE.search(ln):
                if snippet not in gotchas:
                    gotchas.append(snippet)

    title = sess.get("title") or (first_user[:80] if first_user else "(untitled)")
    return {
        "id": sess["id"],
        "title": title,
        "date": (sess.get("last_ts") or sess.get("started_at") or "")[:10],
        "project": _project_label(sess.get("project")),
        "project_slug": sess.get("project"),
        "corrections": corrections,
        "decisions": decisions,
        "gotchas": gotchas,
        "ideas": ideas,
        "first_user": first_user,
    }


# --- cross-session echo filter --------------------------------------------

# A snippet is treated as boilerplate echo when it recurs verbatim in at least
# this many distinct sessions of one harvest batch.
ECHO_MIN_SESSIONS = 3

# A long line repeating byte-identical in even TWO sessions is injected context,
# not two independent human utterances: nobody retypes 60 characters the same way
# twice. Short lines keep the looser threshold, because "好, 就这样" legitimately
# recurs. Calibrated 2026-07-29 after CLAUDE.md house-rule text (present in only
# 2 sessions of the batch) survived the flat 3-session filter and shipped as a
# "feedback" candidate.
ECHO_LONG_LINE_CHARS = 60
ECHO_LONG_MIN_SESSIONS = 2

_ECHO_KEYS = ("corrections", "decisions", "gotchas", "ideas")


def filter_batch_echoes(views: list[dict], min_sessions: int = ECHO_MIN_SESSIONS) -> tuple[list[dict], int]:
    """Drop evidence lines that repeat verbatim across many sessions in a batch.

    A human rephrases; injected context (vault house rules, loaded skill text,
    harness boilerplate) repeats byte-identical in session after session. Any
    snippet found in `min_sessions`+ distinct sessions of the batch is standing
    context echoing through the transcript, not that session's own signal, so
    it is removed from every bucket of every view. Lines of at least
    `ECHO_LONG_LINE_CHARS` need only `ECHO_LONG_MIN_SESSIONS` repeats. Mutates
    and returns `views` plus the count of distinct echo lines dropped.
    """
    seen: dict[str, set] = {}
    for v in views:
        for key in _ECHO_KEYS:
            for s in v.get(key, ()):
                seen.setdefault(s, set()).add(v["id"])
    echo = set()
    for s, ids in seen.items():
        threshold = (
            ECHO_LONG_MIN_SESSIONS if len(s) >= ECHO_LONG_LINE_CHARS else min_sessions
        )
        if len(ids) >= threshold:
            echo.add(s)
    if echo:
        for v in views:
            for key in _ECHO_KEYS:
                if key in v:
                    v[key] = [s for s in v[key] if s not in echo]
    return views, len(echo)


# --- heuristic candidate mining ------------------------------------------
#
# `harvest` writes a deterministic, re-runnable report so tests and weekly
# automation have something concrete. These heuristics surface candidates from
# the compressed views; a human (or an AI reviewer) then curates the report's
# prose. The frontmatter session list is the contract `harvest_commit` reads back,
# and it never depends on the prose.

_STOPWORDS = {
    "the", "and", "for", "with", "this", "that", "from", "chat", "session",
    "help", "please", "about", "into", "your", "you", "how", "what", "why",
    "a", "an", "to", "of", "in", "on", "my", "me", "is", "it",
}


def _kebab(text: str, max_words: int = 5) -> str:
    words = re.findall(r"[a-z0-9]+", (text or "").lower())
    words = [w for w in words if w not in _STOPWORDS] or words
    return "-".join(words[:max_words]) or "candidate"


def mine_candidates(views: list[dict]) -> dict:
    """Derive heuristic candidate proposals from compressed views.

    Returns {"memory": [...], "decisions": [...], "notes": [...]}, each item a
    dict carrying the source pointer so the report can render a checkbox line.
    Kept intentionally conservative: at most one per bucket per session, so the
    scaffold favours signal over a 40-item wall.
    """
    memory: list[dict] = []
    decisions: list[dict] = []
    notes: list[dict] = []

    for v in views:
        ptr = {"id": v["id"], "title": v["title"]}
        if v["corrections"]:
            memory.append({
                **ptr,
                "tag": "feedback",
                "name": _kebab(v["title"]),
                "evidence": v["corrections"][0],
                "kind": "correction",
            })
        if v["gotchas"]:
            memory.append({
                **ptr,
                "tag": "reference",
                "name": _kebab(v["title"]),
                "evidence": v["gotchas"][0],
                "kind": "gotcha",
            })
        if v["decisions"]:
            decisions.append({
                **ptr,
                "evidence": v["decisions"][0],
            })
        # Section ③ used to re-print the SAME decision line as section ②, so one
        # candidate showed up twice under two different headings and the report
        # read three times longer than it had signal for. Ideas get their own
        # lexicon; when a session has none, ③ simply stays quiet for it.
        if v.get("ideas"):
            notes.append({
                **ptr,
                "evidence": v["ideas"][0],
            })
    return {"memory": memory, "decisions": decisions, "notes": notes}


# --- report rendering -----------------------------------------------------

def _fmt_pointer(item: dict) -> str:
    return f"(session {item['id'][:8]} · {item['title'][:60]})"


def render_report(now, stats: dict, views: list[dict], candidates: dict) -> str:
    date = _now_date(now)
    ids = [v["id"] for v in views] + list(stats.get("fork_twins") or [])
    fm_sessions = "[" + ", ".join(ids) + "]"

    lines: list[str] = []
    lines.append("---")
    lines.append("type: harvest-report")
    lines.append(f"date: {date}")
    lines.append("status: inbox-unprocessed")
    lines.append(f"sessions_qualified: {stats['qualified']}")
    lines.append(f"sessions_in_report: {stats['in_report']}")
    lines.append(f"sessions_capped_out: {stats['capped_out']}")
    lines.append(f"sessions: {fm_sessions}")
    lines.append("---")
    lines.append("")
    lines.append(f"# Harvest Report · {date}")
    lines.append("")
    lines.append(
        f"I read {stats['in_report']} of your past conversations (ones not yet "
        "reviewed) and pulled out what looks worth keeping. Nothing here is "
        "saved anywhere yet: tick the boxes you want to keep, and the next "
        "session that processes this report will write the keepers in and mark "
        "these conversations as reviewed."
    )
    lines.append("")
    echo = stats.get("echo_lines_filtered", 0)
    if echo:
        lines.append(
            f"_Noise filter: {echo} line(s) that repeated word-for-word across "
            "3+ conversations (standing rules, injected context) were set aside "
            "as boilerplate._"
        )
        lines.append("")

    _WHY = {
        "correction": "you corrected the AI here",
        "gotcha": "something broke or surprised here",
    }

    mem = candidates.get("memory", [])
    lines.append("## ① Worth remembering")
    lines.append("")
    if not mem:
        lines.append("_None surfaced this pass._")
    else:
        for m in mem:
            why = _WHY.get(m["kind"], m["kind"])
            lines.append(
                f"- [ ] **`{m['tag']}` · {m['name']}** {_fmt_pointer(m)}  \n"
                f"  Why it surfaced: {why}. Evidence: \"{m['evidence']}\""
            )
    lines.append("")

    dec = candidates.get("decisions", [])
    lines.append("## ② Decisions worth logging")
    lines.append("")
    if not dec:
        lines.append("_None surfaced this pass._")
    else:
        for d in dec:
            lines.append(
                f"- [ ] A decision seems to have been locked here {_fmt_pointer(d)}  \n"
                f"  Evidence: \"{d['evidence']}\""
            )
    lines.append("")

    note = candidates.get("notes", [])
    lines.append("## ③ Ideas worth a note")
    lines.append("")
    if not note:
        lines.append("_None surfaced this pass._")
    else:
        for n in note:
            lines.append(
                f"- [ ] An idea that could grow into its own note {_fmt_pointer(n)}  \n"
                f"  Evidence: \"{n['evidence']}\""
            )
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## The numbers (for the curious)")
    lines.append("")
    lines.append(
        f"- {stats['qualified']} conversation(s) qualified this pass: not yet "
        "reviewed, idle for 24h+, and a real conversation (subagent transcripts "
        "never qualify)."
    )
    lines.append(
        f"- {stats['in_report']} carried into this report; "
        f"{stats['capped_out']} held for a later pass. Held-over conversations "
        "are never dropped: they stay unreviewed and come back next time."
    )
    lines.append(
        "- The `sessions:` list in the frontmatter is the contract `harvest "
        "commit` reads back on approval; leave it untouched."
    )
    lines.append("")
    lines.append("## Evidence appendix (what was mined, per conversation)")
    lines.append("")
    for v in views:
        lines.append(f"### {v['title'][:70]}")
        lines.append(f"`{v['id']}` · {v['date']} · {v['project']}")
        lines.append("")
        for label, key in (("Corrections", "corrections"),
                           ("Decisions", "decisions"),
                           ("Gotchas", "gotchas"),
                           ("Ideas", "ideas")):
            if v.get(key):
                lines.append(f"- {label}:")
                for s in v[key]:
                    lines.append(f"  - {s}")
        lines.append("")

    return "\n".join(lines) + "\n"


# --- top-level harvest / harvest_commit ----------------------------------

def harvest(
    conn: sqlite3.Connection,
    now,
    out_path: str,
    max_sessions: int = HARVEST_MAX_DEFAULT,
) -> dict:
    """Run a harvest PROPOSAL pass and write the report to `out_path`.

    Selects candidate sessions, builds compressed views, mines candidate
    proposals, and writes ONE markdown report. Crucially, this does NOT flip the
    `harvested` bookmark on any session: proposals are idempotent and re-runnable.

    Returns a stats dict including the exact session ids covered by the report.
    """
    init_db(conn)
    sel = select_harvest_candidates(conn, now, max_sessions=max_sessions)
    views = [compressed_view(conn, r["id"]) for r in sel["selected"]]
    views = [v for v in views if v]
    kept = {v["id"] for v in views}
    # Fork twins were collapsed out of `selected` but ARE covered by the report,
    # so they ride along in the frontmatter contract that harvest_commit reads.
    sel["fork_twins"] = [
        t
        for r in sel["selected"]
        if r["id"] in kept
        for t in (r.get("_fork_twins") or [])
    ]
    views, echo_dropped = filter_batch_echoes(views)
    sel["echo_lines_filtered"] = echo_dropped
    candidates = mine_candidates(views)
    report = render_report(now, sel, views, candidates)

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)

    # Record that a pass ran, but do NOT touch sessions.harvested here.
    conn.execute(
        "UPDATE harvest_state SET last_run=?, notes=? WHERE id=1",
        (_now_date(now), f"proposed {len(views)} session(s) -> {os.path.basename(out_path)}"),
    )
    conn.commit()

    return {
        "qualified": sel["qualified"],
        "in_report": sel["in_report"],
        "capped_out": sel["capped_out"],
        "echo_lines_filtered": echo_dropped,
        "sessions": [v["id"] for v in views] + list(sel.get("fork_twins") or []),
        "cutoff": sel["cutoff"],
        "out_path": os.path.abspath(out_path),
        "candidate_counts": {
            "memory": len(candidates["memory"]),
            "decisions": len(candidates["decisions"]),
            "notes": len(candidates["notes"]),
        },
    }


_FM_SESSIONS_RE = re.compile(r"^sessions:\s*(.*)$", re.MULTILINE)


def _parse_report_sessions(report_text: str) -> list[str]:
    """Read the `sessions:` list back out of a report's YAML frontmatter.

    Supports the flow-list form we write (`sessions: [a, b, c]`) as well as a
    block-list fallback. Stdlib only, so no yaml dependency.
    """
    # Isolate frontmatter.
    if report_text.startswith("---"):
        end = report_text.find("\n---", 3)
        fm = report_text[:end] if end != -1 else report_text
    else:
        fm = report_text

    m = _FM_SESSIONS_RE.search(fm)
    if not m:
        return []
    rest = m.group(1).strip()
    ids: list[str] = []
    if rest.startswith("["):
        inner = rest.strip("[]")
        ids = [x.strip().strip("'\"") for x in inner.split(",")]
    else:
        # block list: lines starting with "- " after the sessions: key
        block = fm[m.end():]
        for ln in block.splitlines():
            ls = ln.strip()
            if ls.startswith("- "):
                ids.append(ls[2:].strip().strip("'\""))
            elif ls and not ls.startswith("-"):
                break
    return [i for i in ids if i]


def harvest_commit(conn: sqlite3.Connection, report_path: str, now) -> dict:
    """Consume the bookmark for a report the human has approved.

    Reads the covered session ids from the report's frontmatter and sets
    `harvested = 1`, `harvested_at = <now>` for exactly those sessions. Idempotent:
    re-running commits nothing new. This is the ONLY path that flips the flag.
    """
    init_db(conn)
    with open(report_path, "r", encoding="utf-8") as f:
        text = f.read()
    ids = _parse_report_sessions(text)
    if not ids:
        return {"requested": 0, "flipped": 0, "already": 0, "missing": 0, "ids": []}

    date = _now_date(now)
    flipped = 0
    already = 0
    missing = 0
    for sid in ids:
        row = conn.execute(
            "SELECT harvested FROM sessions WHERE id=?", (sid,)
        ).fetchone()
        if row is None:
            missing += 1
            continue
        if row["harvested"] == 1:
            already += 1
            continue
        conn.execute(
            "UPDATE sessions SET harvested=1, harvested_at=? WHERE id=?", (date, sid)
        )
        flipped += 1

    total_harvested = conn.execute(
        "SELECT COUNT(*) FROM sessions WHERE harvested=1"
    ).fetchone()[0]
    conn.execute(
        "UPDATE harvest_state SET sessions_harvested=?, notes=? WHERE id=1",
        (total_harvested, f"committed {os.path.basename(report_path)} on {date}"),
    )
    conn.commit()

    return {
        "requested": len(ids),
        "flipped": flipped,
        "already": already,
        "missing": missing,
        "ids": ids,
    }
