# session-history

A self-contained CLI that indexes every Claude Code session transcript into a
full-text-searchable SQLite (FTS5) database, so past sessions become greppable
across projects.

- **Standard library only** (`sqlite3` + FTS5). No pip installs. macOS, the
  python.org builds, and the Microsoft Store build all ship SQLite with FTS5;
  Anaconda/Miniconda does not. On startup the tool probes for FTS5 and, if it is
  missing, fails soft with a plain-language fix (use python.org Python, not
  Anaconda) instead of a cryptic `no such module: fts5`.
- **`~/.claude/projects/` is read strictly read-only.** This tool never writes,
  moves, or modifies anything there. All state (the database, and with it the
  harvest bookmark) lives in `~/.my-second-brain/session-history.db`,
  deliberately outside any repo or skill directory so a code update or skill
  reinstall can never wipe the index or the bookmark.
- **Purely local.** Nothing is uploaded anywhere; there is no network code in
  this package at all.

## Usage

```bash
# Index (incremental + idempotent, safe to run before every search)
python3 -m session_history ingest        # or: ./sh ingest

# Cross-session full-text search (ranked, with snippets)
./sh search "rm -rf symlink"
./sh search "GHL order form product picker"

# One session, chronological
./sh show <session-id>          # accepts a uuid prefix

# The N most recent sessions
./sh recent 15

# Just the tool calls a session made
./sh actions <session-id>

# WS2: weekly harvest pass (PROPOSE long-term memory candidates)
./sh harvest --now 2026-07-11            # writes ONE review report to the vault Inbox
./sh harvest commit <report-path>        # AFTER human approval: consume the bookmark
```

## Configuration

Owner-specific paths come from config, never from code. Precedence per path:
CLI flag > environment variable > config file > generic default. The config
file is optional JSON at `~/.my-second-brain/session-history.json` (move it
with `SESSION_HISTORY_CONFIG`):

```json
{
  "vault": "/Users/me/Documents/My-Second-Brain"
}
```

Recognised keys: `vault` (harvest reports default to `<vault>/00_Inbox/`),
`inbox` (explicit report directory, wins over `vault`), `db`, `projects`.
Environment variables `SESSION_HISTORY_DB` / `SESSION_HISTORY_PROJECTS` /
`SESSION_HISTORY_INBOX` override the file. Without any of these, `ingest` and
`search` work out of the box (`~/.claude/projects` in,
`~/.my-second-brain/session-history.db` out) and `harvest` asks for an
explicit `--out`.

## What gets indexed

Each transcript line is one JSON object. Only conversational lines (`user`,
`assistant`) are indexed; metadata lines (`mode`, `last-prompt`, `system`,
`queue-operation`, `attachment`) are skipped, and a session's title is pulled
from a `custom-title` line if present. For every message the indexer emits:

- one row of concatenated `text` + `thinking` blocks,
- one row per `tool_use` block (`tool_name` + truncated JSON input),
- one row per `tool_result` block (truncated result text).

Nested subagent transcripts (`<slug>/<session>/subagents/agent-*.jsonl`) are
indexed too. Internal `journal.jsonl` workflow-bookkeeping files are skipped.
Any single payload is truncated to ~2 KB so base64/huge blobs never enter FTS.

## The incremental cursor (how re-ingest stays correct)

The cursor is a **byte offset**, not a line count: each session row stores the
number of bytes consumed so far, and re-ingest seeks to that offset and reads
forward, indexing only whole lines up to the last `\n` (a partial trailing line
from a live session flushing mid-write is never indexed until it completes).
Change detection compares current file size against the stored offset (**not
mtime**, since same-second appends and sync tools touching mtime both defeat mtime),
so a file whose mtime moved backwards is still re-read. If the file is smaller
than the stored offset (compaction/rewrite/truncation) its rows are deleted and
it is re-ingested from offset 0, so running `ingest` twice on an unchanged
corpus yields byte-identical row and FTS-match counts.

## Harvest (WS2): propose, never auto-write

Once a week, `harvest` reads sessions that have not yet been "harvested" and drafts
candidate long-term memories / decisions / notes for a human to approve. The AI
only proposes; nothing is written to memory automatically, and the output is one
review report in the vault Inbox (`<date>-Harvest-Report.md`).

Selection is `harvested = 0` AND **quiescent** (file mtime older than 24h relative
to `--now`, so a session still being written is never harvested) AND carries real
conversation (at least one user turn; `journal.jsonl` bookkeeping is already
skipped at ingest) AND is a **main session**: subagent transcripts stay fully
searchable but are never harvested, because they are machine-to-machine (their
"user" turns are an orchestrator's brief, and their text is dominated by task
material that reads as false signal). Each pass is capped at the 30 most-recent
qualifiers; the rest are reported as `sessions_capped_out`, never silently
dropped. Each selected session is compressed to a small view (title + date +
project + the user's corrections, explicit decisions, and gotchas) read from
the indexed `messages` table, never by re-parsing jsonl.

Three noise filters keep the proposals honest: lines inside injected
`<system-reminder>` context are never mined (standing house rules are not new
signal); cue matching uses word boundaries on English cues (so "locked" cannot
fire inside "blocked"); and any line repeating verbatim across 3+ sessions of
one batch is dropped as boilerplate echo (a human rephrases; injected context
repeats byte-identical).

**Bookmark discipline is the whole point.** `harvest` does **not** flip
`harvested`; proposal is idempotent and re-runnable, so a garbage first report can
be regenerated without silently burning the sessions it covered. The report's
frontmatter lists the exact session ids it covers. Only after a human approves
does a Command Base session run `harvest commit <report-path>`, which reads those
ids back and sets `harvested = 1` / `harvested_at` for exactly them (idempotent).
`--now` takes an explicit reference instant so a run is deterministic rather than
clock-dependent.

## Schema

`schema_version` (single integer row) gates future migrations. `sessions` holds
one row per transcript with the `byte_offset`/`size_at_ingest` cursor and a
`harvested`/`harvested_at` bookmark for a later weekly pass; `harvest_state` holds
that pass's bookkeeping. `messages` is the FTS5 virtual table. Full DDL lives in
`session_history/core.py`.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

The suite (`tests/`) runs against a tiny hand-made fixture corpus
(`tests/fixtures/`), never the live corpus, and specifically covers the
incremental hazards: mtime rolled backwards, partial-then-completed trailing
lines, truncation/rewrite dedup, idempotency, and search-count stability across
a single-file change.

## Layout

```
session_history/      package (core.py = logic, __main__.py = CLI)
sh                     thin entrypoint (./sh <verb>)
tests/                 unittest suite
tests/fixtures/        small committed jsonl corpus + generator
```

## Two copies, one source

This package lives in two places: a standalone dev-bench repo (where
development happens) and a vendored copy inside the `my-second-brain` skill
payload at `scripts/session-history/` (what installs ship). If you are reading
this inside the skill payload, you have the vendored copy; it is complete and
self-contained, nothing else to fetch.

Every product release re-syncs the package from the dev bench into the payload
as a fixed release step, so the two copies never drift:

```bash
rsync -av --delete \
  --exclude .git --exclude data --exclude __pycache__ --exclude .DS_Store \
  <dev-bench>/session-history/ \
  <product-repo>/my-second-brain/scripts/session-history/
```

Run the tests in BOTH locations after syncing, then the product repo's
pre-push scans.
