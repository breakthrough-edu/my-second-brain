"""CLI for session-history.

Usage:
    python -m session_history ingest
    python -m session_history search <query>
    python -m session_history show <session-id>
    python -m session_history recent [n]
    python -m session_history actions <session-id>
"""

from __future__ import annotations

import argparse
import datetime
import os
import sys

from .core import DEFAULT_STATE_DIR
from . import (
    FTS5Unavailable,
    actions,
    connect,
    default_db_path,
    default_projects_dir,
    harvest,
    harvest_commit,
    ingest,
    recent,
    search,
    show,
)


def _fmt_date(ts: str | None) -> str:
    if not ts:
        return "?"
    return ts[:10]


def cmd_ingest(conn, args) -> int:
    stats = ingest(conn, projects_dir=args.projects, progress=not args.quiet)
    print(
        f"ingested: {stats['files_changed']} changed / {stats['files_scanned']} files, "
        f"{stats['rows_inserted']} rows, {stats['seconds']}s"
    )
    return 0


def cmd_search(conn, args) -> int:
    hits = search(conn, args.query, limit=args.limit)
    if not hits:
        print("(no matches)")
        return 0
    for h in hits:
        title = h.get("title") or "(untitled)"
        tool = f" [{h['tool_name']}]" if h.get("tool_name") else ""
        print(
            f"{_fmt_date(h.get('last_ts') or h.get('started_at'))}  "
            f"{h['project'][:40]}\n"
            f"  {h['session_id']}  {title}{tool}\n"
            f"  {h['role']}: {h['snippet']}\n"
        )
    return 0


def cmd_show(conn, args) -> int:
    res = show(conn, args.session_id, limit=args.limit)
    if not res:
        print(f"session not found: {args.session_id}", file=sys.stderr)
        return 1
    s = res["session"]
    print(f"# {s.get('title') or '(untitled)'}")
    print(f"session: {s['id']}")
    print(f"project: {s['project']}")
    print(f"path:    {s['path']}")
    print(f"span:    {s.get('started_at')}  →  {s.get('last_ts')}")
    print(f"lines:   {s.get('line_count')}\n")
    for m in res["messages"]:
        ts = (m.get("ts") or "")[:19].replace("T", " ")
        role = m["role"]
        if m.get("tool_name"):
            print(f"[{ts}] {role} · {m['tool_name']}: {m['text'][:200]}")
        else:
            body = m["text"]
            print(f"[{ts}] {role}:")
            for ln in body.splitlines():
                print(f"    {ln}")
    return 0


def cmd_recent(conn, args) -> int:
    for r in recent(conn, n=args.n):
        print(
            f"{_fmt_date(r.get('last_ts') or r.get('started_at'))}  "
            f"{r['id'][:8]}  {r['project'][:34]:34}  {r['summary']}"
        )
    return 0


def cmd_actions(conn, args) -> int:
    acts = actions(conn, args.session_id, limit=args.limit)
    if not acts:
        print("(no tool calls)")
        return 0
    for a in acts:
        ts = (a.get("ts") or "")[:19].replace("T", " ")
        print(f"[{ts}] {a['tool_name']}: {a['text'][:160]}")
    return 0


def cmd_harvest(conn, args) -> int:
    now = args.now
    out = args.out
    if not out:
        # The draft lands in the tool's own state directory, never the vault
        # Inbox. The Inbox is for things the owner is meant to read, and a
        # machine sift is not one of them; putting it there made skipping
        # curation the path of least resistance. A curated proposal note is
        # what reaches the Inbox now, written by the session that read this.
        # Side benefit: harvest no longer needs a configured vault to run.
        out = os.path.join(
            os.path.expanduser(DEFAULT_STATE_DIR), f"{now}-harvest-draft.md"
        )
    stats = harvest(conn, now=now, out_path=out, max_sessions=args.max)
    print(
        f"harvest: {stats['qualified']} qualified, {stats['in_report']} in report, "
        f"{stats['capped_out']} capped out, "
        f"{stats['echo_lines_filtered']} echo line(s) filtered"
    )
    print(f"       quiescence cutoff (mtime older than): {stats['cutoff']}")
    cc = stats["candidate_counts"]
    print(
        f"       candidates mined: {cc['memory']} memory, "
        f"{cc['decisions']} decision, {cc['notes']} note"
    )
    print(f"       draft: {stats['out_path']}")
    print("       (a machine sift, NOT a report: curate it into a short proposal\n        note in the owner's Inbox, then `harvest commit` that note)")
    return 0


def cmd_harvest_commit(conn, args) -> int:
    res = harvest_commit(conn, args.report_path, now=args.now)
    print(
        f"harvest commit: {res['flipped']} flipped, {res['already']} already harvested, "
        f"{res['missing']} missing (of {res['requested']} in report)"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="session-history", description=__doc__)
    p.add_argument("--db", default=None,
                   help="database path (default: ~/.my-second-brain/session-history.db)")
    p.add_argument("--projects", default=None, help="projects dir (default: ~/.claude/projects)")
    sub = p.add_subparsers(dest="cmd", required=True)

    pi = sub.add_parser("ingest", help="incremental, idempotent index")
    pi.add_argument("-q", "--quiet", action="store_true")
    pi.set_defaults(func=cmd_ingest)

    ps = sub.add_parser("search", help="cross-session full-text search")
    ps.add_argument("query")
    ps.add_argument("-n", "--limit", type=int, default=20)
    ps.set_defaults(func=cmd_search)

    psh = sub.add_parser("show", help="chronological timeline of one session")
    psh.add_argument("session_id")
    psh.add_argument("-n", "--limit", type=int, default=1000)
    psh.set_defaults(func=cmd_show)

    pr = sub.add_parser("recent", help="most recent N sessions")
    pr.add_argument("n", nargs="?", type=int, default=10)
    pr.set_defaults(func=cmd_recent)

    pa = sub.add_parser("actions", help="tool calls made by one session")
    pa.add_argument("session_id")
    pa.add_argument("-n", "--limit", type=int, default=500)
    pa.set_defaults(func=cmd_actions)

    # WS2 harvest. `harvest` proposes (never flips the bookmark); `harvest commit`
    # consumes the bookmark for an approved report.
    today = datetime.date.today().isoformat()
    pd = sub.add_parser("harvest", help="weekly harvest pass: propose memory candidates")
    pd.add_argument("--now", default=today,
                    help="reference date/instant (default: today; deterministic if passed)")
    pd.add_argument("--out", default=None,
                    help="draft path (default: ~/.my-second-brain/<now>-harvest-draft.md)")
    pd.add_argument("--max", type=int, default=30, help="cap on sessions in the report")
    pd.set_defaults(func=cmd_harvest)

    pd_sub = pd.add_subparsers(dest="harvest_cmd")
    pdc = pd_sub.add_parser("commit",
                            help="after approval, flip harvested=1 for the report's sessions")
    pdc.add_argument("report_path")
    pdc.add_argument("--now", default=today,
                     help="harvested_at date to stamp (default: today)")
    pdc.set_defaults(func=cmd_harvest_commit)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    if args.projects is None:
        args.projects = default_projects_dir()
    try:
        conn = connect(args.db or default_db_path())
    except FTS5Unavailable as e:
        print(str(e), file=sys.stderr)
        return 3
    try:
        return args.func(conn, args)
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
