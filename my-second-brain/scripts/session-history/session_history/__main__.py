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
import sys

from . import (
    FTS5Unavailable,
    IndexNotBuilt,
    actions,
    connect,
    default_db_path,
    default_projects_dir,
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

    # ⛔ There is no `harvest` subcommand and there has not been one since
    # 2026-08-20. It ran a weekly pass that guessed at what a week of
    # sessions was worth keeping; that judgement now happens at each
    # session's own closeout, by whoever was in it. See core.py's note.
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
    except IndexNotBuilt as e:
        print(str(e), file=sys.stderr)
        return 4
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
