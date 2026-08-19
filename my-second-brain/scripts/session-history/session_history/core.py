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
# The harvest pipeline lived here until 2026-08-20 and it is retired.
# --------------------------------------------------------------------------
#
# WHAT IT WAS: a weekly pass that read every session not yet marked harvested,
# mined candidate memories out of them by cue-word matching, and wrote a draft
# for a human to approve. It reached the owner through a doorbell that ran it
# on a timer.
#
# WHY IT IS GONE: what a session was worth keeping is now decided AT THE
# CLOSEOUT OF THAT SESSION, by whoever was in it, while they still remember
# what happened. A machine re-reading a week of transcripts to guess at the
# same thing was measured against that and lost badly.
#
# ⭐ WHAT THIS TOOL IS FOR NOW, so nobody mistakes the retirement for a verdict
# on the whole tool: it is the archive drawer. A session that crashed or was
# never closed out leaves nothing in the vault, and the transcript plus this
# index is the only trace of it that survives. `search` and `show` answer
# 'when did I work on that' at the moment somebody asks. That is the accepted
# cost of closeout-time capture, and this tool is what keeps it from being a
# permanent loss.
#
# ⛔ THE DATABASE KEEPS ITS COLUMNS. `sessions.harvested`, `harvested_at` and
# the `harvest_state` table are still created and still migrated, untouched.
# Dropping them would force every installed database through a migration to
# delete bookmarks that cost nothing to carry, and SCHEMA_VERSION would move
# for a change no reader would notice. ⛔ Do not 'clean them up'.
