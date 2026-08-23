#!/usr/bin/env python3
"""
citations-accept.py - acceptance harness for the guardian's citation table.

WHAT THIS IS
    One check, on one habit: every citation in
    `skills/breakthrough-vault-guardian/references/what-each-rule-guards.md`
    must be a FILE plus an ANCHOR, and the anchor must appear verbatim in that
    file. The form is:

        `path/to/file.md` → `some string that is really in it`

    Several anchors into the same file follow one after another, each behind
    its own arrow, and each is read against the file named most recently on
    that line.

WHY IT EXISTS, WHICH IS THE PART WORTH READING
    Until 2026-08-24 that table cited by LINE NUMBER (`scripts/checkup.py:640`).
    Nothing checked them, every edit to a cited file slid them, and a measured
    audit found roughly four in five landing somewhere unrelated: the freshness
    check citation pointed at the tag-vocabulary loop, the brand-pillar citation
    pointed at the SOP menu heading, and a citation about keeping a price
    current pointed at a file that never mentions one.

    ⛔ The reason a line-number checker was NOT built instead: a line number can
    only be tested for landing on a non-blank line, so such a check passes green
    on every one of the wrong citations above. It would have certified a broken
    file as healthy, which is worse than no check. An anchor is testable for the
    thing that actually matters, so this harness can be short and still mean
    something.

WHEN TO RUN IT
    After editing any file that table cites, and after editing the table.

    $ python3 dev/citations-accept.py

    The table path defaults to this script's own repo-relative sibling and can
    be overridden with --table.
"""

import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PAYLOAD = os.path.join(REPO, "my-second-brain")
DEFAULT_TABLE = os.path.join(
    PAYLOAD, "skills", "breakthrough-vault-guardian",
    "references", "what-each-rule-guards.md")

# A backticked path, or an arrow followed by a backticked anchor.
TOKEN = re.compile(
    r'`([A-Za-z0-9_][A-Za-z0-9_./-]*\.(?:md|py|sh|json|html))`'
    r'|→ `((?:[^`]|`(?=[^`]*`))*?)`')


def bases(table_path):
    """Every root a citation could legally be written against."""
    d = os.path.dirname(table_path)
    return [PAYLOAD, d, os.path.dirname(d), os.path.join(PAYLOAD, "skills")]


def resolve(rel, roots):
    for root in roots:
        candidate = os.path.join(root, rel)
        if os.path.isfile(candidate):
            return candidate
    return None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--table", default=DEFAULT_TABLE)
    args = ap.parse_args(argv)

    try:
        with open(args.table, encoding="utf-8") as fh:
            lines = fh.read().split("\n")
    except OSError as exc:
        print("FAIL - the table could not be read: %s" % exc)
        return 1

    roots = bases(args.table)
    cache = {}
    checked = 0
    files_seen = set()
    failures = []
    stray = []

    for lineno, line in enumerate(lines, 1):
        current = None
        for m in TOKEN.finditer(line):
            if m.group(1):
                current = m.group(1)
                continue
            anchor = m.group(2)
            checked += 1
            if current is None:
                failures.append((lineno, "<no file named before this arrow>",
                                 anchor))
                continue
            path = resolve(current, roots)
            if path is None:
                failures.append((lineno, current, "THAT FILE DOES NOT EXIST"))
                continue
            files_seen.add(current)
            if path not in cache:
                with open(path, encoding="utf-8") as fh:
                    cache[path] = fh.read()
            if anchor not in cache[path]:
                failures.append((lineno, current, anchor))

        # ⛔ The habit this file replaced, caught on the way back in.
        for m in re.finditer(
                r'[A-Za-z0-9_][A-Za-z0-9_./-]*\.(?:md|py|sh|json|html):[0-9]+'
                r'|`:[0-9]+', line):
            stray.append((lineno, m.group(0)))

    print("CHECK - every citation is a file plus an anchor that really is in it")
    print("    table     %s" % os.path.relpath(args.table, REPO))
    print("    checked   %d anchored citations across %d files"
          % (checked, len(files_seen)))

    if stray:
        print()
        print("FAILURES: %d citation(s) written as a line number" % len(stray))
        for lineno, text in stray:
            print("  line %-5d %s" % (lineno, text))
        print("  ⛔ Line numbers slide when a cited file is edited and nothing "
              "reports it. Cite a string that is really in the file instead.")

    if failures:
        print()
        print("FAILURES: %d anchor(s) that do not land" % len(failures))
        for lineno, where, anchor in failures:
            print("  line %-5d %s  →  %r" % (lineno, where, anchor))
        print("  ⛔ Each one is a sentence in the table claiming something the "
              "cited file no longer says. Re-read the file and re-anchor.")

    if stray or failures:
        return 1

    print()
    print("FAILURES: none")
    print("PASS - every citation lands on text that is really there.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
