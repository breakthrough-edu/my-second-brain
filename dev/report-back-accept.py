#!/usr/bin/env python3
"""
report-back-accept.py - acceptance harness for two pieces of written behaviour:
the report-back loop (a handoff carries a return address, the closing session
sends the report's path back) and the playbook memory-pointer check in the
weekly maintenance pass.

WHAT THIS IS
    The half of the acceptance a machine can judge. It reads the shipped text
    and the diff against a base ref, and answers four questions:

      1. Are the new sections where they were meant to land, under the
         headings they were meant to land under?
      2. Does the delivery step name exactly the four results, and no fifth?
      3. Do the lines this change ADDED keep the product's red lines (no em
         dash, no double hyphen, no spaced hyphen as a separator, no product
         or person names, no path into anybody's private vault)?
      4. Did the change stay out of the files it promised not to touch?

WHAT THIS IS NOT
    ⛔ It does not judge whether the words work. Whether a session that has
    never seen this text can actually write the block, send the path and name
    the result honestly is a question only a clean session answers, by doing
    it. A green run here means the text is in place and clean, nothing more.

WHEN TO RUN IT
    After any edit to the five files listed in TARGETS, before calling the
    edit done.

    $ python3 dev/report-back-accept.py            # diff against origin/main
    $ python3 dev/report-back-accept.py --base v4.1.0

WHY THE RED-LINE CHECK READS ADDED LINES, NOT WHOLE FILES
    The files already carry YAML fences, table rules and one quoted list line
    that would trip a whole-file scan forever. A check that is red on day one
    for reasons nobody will fix is a check people stop reading. Added lines
    are the only lines this change is answerable for.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PAYLOAD = REPO / "my-second-brain"

CONSULTANT = "my-second-brain/skills/breakthrough-project-consultant/SKILL.md"
REPORT = "my-second-brain/skills/breakthrough-session-report/SKILL.md"
METHOD = "my-second-brain/skills/breakthrough-method-builder/SKILL.md"
MAINT = "my-second-brain/modes/maintenance.md"
GUIDE = "my-second-brain/references/operating-the-second-brain-student-guide.md"

TARGETS = [CONSULTANT, REPORT, METHOD, MAINT, GUIDE]

# Files and folders this change promised to leave alone.
FROZEN = [
    "my-second-brain/templates",
    "my-second-brain/modes/setup.md",
    "my-second-brain/modes/capture.md",
    "my-second-brain/modes/distill.md",
    "my-second-brain/SKILL.md",
    "my-second-brain/scripts",
]

# Maintainer files allowed to change beside the five targets.
ALLOWED_EXTRA = ["dev/report-back-accept.py", "README.md"]

RESULT_WORDS = ["delivered", "queued", "held", "not sent"]

# Names that must never appear in shipped text. Case-sensitive and bounded on
# purpose: an unbounded match on a short name fires on ordinary English.
NAME_PATTERNS = [
    r"\b2BI\b",
    r"2nd Brain Intensive",
    r"\bBLOC\b",
    r"\bBuild Day\b",
    r"Breakthrough Live",
    r"Breakthrough Circle",
    r"Breakthrough EDU",
    r"\bSKOOL\b",
    r"\bKaloz\b",
    r"Jia Wei",
    r"\bJW\b",
    r"\bFable\b",
    r"/Users/",
    r"breakthrough-vault",
]

failures = []
passes = []


def ok(name, detail=""):
    passes.append((name, detail))


def fail(name, detail):
    failures.append((name, detail))


def git(*args):
    out = subprocess.run(
        ["git", "-C", str(REPO), *args], capture_output=True, text=True
    )
    return out.returncode, out.stdout, out.stderr


def read(rel):
    return (REPO / rel).read_text(encoding="utf-8")


def section(text, heading_prefix):
    """Body of the first heading line starting with heading_prefix, up to the
    next heading of the same or a higher level. None when the heading is gone."""
    lines = text.splitlines()
    start = None
    level = None
    for i, line in enumerate(lines):
        if line.startswith(heading_prefix):
            start = i
            level = len(line) - len(line.lstrip("#"))
            break
    if start is None:
        return None
    body = []
    for line in lines[start + 1:]:
        m = re.match(r"^(#+) ", line)
        if m and len(m.group(1)) <= level:
            break
        body.append(line)
    return "\n".join(body)


def added_lines(base, rel):
    """Lines the working tree adds to rel, measured against base."""
    code, out, err = git("diff", "--unified=0", base, "--", rel)
    if code not in (0, 1):
        fail("diff readable", f"{rel}: git diff failed: {err.strip()}")
        return []
    return [
        line[1:]
        for line in out.splitlines()
        if line.startswith("+") and not line.startswith("+++")
    ]


# ---------------------------------------------------------------- 1 · handoff


def check_handoff_block():
    text = read(CONSULTANT)
    body = section(text, "## The handoff entry")
    if body is None:
        fail("handoff section", "the handoff section heading is gone")
        return
    if "Report back to" not in body:
        fail("report-back block", "`Report back to` is not in the handoff section")
        return
    ok("report-back block", "`Report back to` sits inside the handoff section")

    wanted = {
        "environment": r"environment",
        "address": r"address",
        "title": r"title",
        "machine": r"machine",
    }
    missing = [k for k, pat in wanted.items() if not re.search(pat, body, re.I)]
    if missing:
        fail("report-back block fields", f"not named in the handoff section: {missing}")
    else:
        ok("report-back block fields", "environment, address, title, machine all named")

    if not re.search(r"cannot receive messages", body, re.I):
        fail(
            "honest no-address line",
            "the handoff section never says what to write when there is no address",
        )
    else:
        ok("honest no-address line")

    if "00_Inbox/" not in body:
        fail(
            "no-project handoff",
            "the handoff section never says where a handoff with no project lives",
        )
    else:
        ok("no-project handoff", "`00_Inbox/` named inside the handoff section")


# ------------------------------------------------------------- 2 · deliver


def check_deliver():
    text = read(REPORT)
    baton = section(text, "## The baton")
    if baton is None:
        fail("baton section", "the baton section heading is gone")
        return

    m = re.search(r"^#{3,4} Deliver the baton.*$", baton, re.M)
    if not m:
        fail("deliver heading", "no `Deliver the baton` heading inside the baton section")
        return
    ok("deliver heading", m.group(0).strip())

    log_at = baton.find("99_Meta/filing-log.md")
    if log_at == -1 or log_at > m.start():
        fail("deliver order", "`Deliver the baton` does not come after the filing-log line")
    else:
        ok("deliver order", "after the filing-log line")

    deliver = baton[m.start():]
    for word in RESULT_WORDS:
        if f"`{word}`" not in deliver:
            fail("four results", f"`{word}` is not named in the delivery step")
    if all(f"`{w}`" in deliver for w in RESULT_WORDS):
        ok("four results", ", ".join(RESULT_WORDS))

    # A fifth result word offered in backticks would quietly widen the set.
    extra = sorted(
        w
        for w in set(re.findall(r"`([a-z][a-z ]{2,14})`", deliver))
        if w in {"sent", "received", "read", "refused", "expired", "failed", "pending", "dropped"}
    )
    if extra:
        fail("no fifth result", f"extra result words offered in backticks: {extra}")
    else:
        ok("no fifth result")

    if "Report back to" not in deliver:
        fail("deliver condition", "the delivery step never names the `Report back to` block")
    else:
        ok("deliver condition", "names the block it depends on")

    close = section(text, "## Close")
    if close is None:
        fail("close section", "the Close section heading is gone")
    elif not all(w in close for w in RESULT_WORDS):
        fail("close names the result", "the Close section does not carry all four results")
    else:
        ok("close names the result")


# ------------------------------------------------------- 3 · student guide


def check_guide():
    text = read(GUIDE)
    if "做完回主 session 的方式是贴 baton 路径" in text:
        fail("guide line", "the old paste-only sentence is still there")
        return
    line = next(
        (l for l in text.splitlines() if "session report" in l and "00_Inbox/" in l),
        None,
    )
    if line is None:
        fail("guide line", "no line names the session report in `00_Inbox/` any more")
        return
    if "发" not in line or "贴" not in line:
        fail("guide line", "the line does not carry both the send and the paste fallback")
    else:
        ok("guide line", "send first, paste as the fallback")
    if "读过才准归档" not in line:
        fail("guide line keeps the archive rule", "the read-before-archive rule fell off")
    else:
        ok("guide line keeps the archive rule")


# ----------------------------------------------------- 4 · pointer's home


def check_pointer_home():
    text = read(METHOD)
    if "drop a one-line pointer into the vault's working memory" in text:
        fail("pointer home", "method-builder still sends the pointer to the vault file first")
    elif "Claude's own memory" not in text:
        fail("pointer home", "method-builder never names Claude's own memory")
    else:
        ok("pointer home", "Claude's own memory named in method-builder")

    if "99_Meta/memory.md" not in text:
        fail("pointer fallback", "the fallback file is no longer named at all")
    else:
        ok("pointer fallback", "`99_Meta/memory.md` kept as the fallback")

    template = read("my-second-brain/templates/CLAUDE.template.md")
    if "Claude's own memory" not in template:
        fail("template agrees", "the vault template no longer says Claude's own memory")
    else:
        ok("template agrees", "both files use the same phrase")


def check_maintenance():
    text = read(MAINT)
    checks = section(text, "## The checks")
    if checks is None:
        fail("checks section", "the checks section heading is gone")
        return
    para = next(
        (
            p
            for p in re.split(r"\n\s*\n", checks)
            if "Claude's own memory" in p and "Playbooks/" in p
        ),
        None,
    )
    if para is None:
        fail(
            "pointer check",
            "no check pairs `04_Methodology/Playbooks/` with Claude's own memory",
        )
        return
    ok("pointer check", para.strip().splitlines()[0][:80])

    # Existing check numbers are cross-referenced by number; none may move.
    for number, anchor in [
        ("1.", "Doors and the directory, four things at once"),
        ("12.", "Inbox drain"),
        ("13.", "Memory weight"),
        ("14.", "Weekly rollup, and the two things that close it"),
        ("16.", "Stamp `maintenance-state.md`"),
        ("18.", "Do not close the ritual here"),
    ]:
        if not re.search(rf"^{re.escape(number)} .*{re.escape(anchor)}", text, re.M):
            fail("check numbers stand still", f"check {number} no longer opens with: {anchor}")
    if not any(n == "check numbers stand still" for n, _ in failures):
        ok("check numbers stand still")


# --------------------------------------------------------- 5 · red lines


def check_red_lines(base):
    clean = True
    for rel in TARGETS + ["README.md"]:
        for line in added_lines(base, rel):
            where = f"{rel}: {line.strip()[:90]}"
            if "—" in line or "–" in line:
                fail("no em or en dash", where)
                clean = False
            if "--" in line and not re.fullmatch(r"\s*\|?[-:| ]+\|?\s*", line):
                fail("no double hyphen", where)
                clean = False
            if re.search(r"\S - \S", line):
                fail("no spaced hyphen", where)
                clean = False
            for pat in NAME_PATTERNS:
                if re.search(pat, line):
                    fail("no names, no private paths", f"{pat} in {where}")
                    clean = False
            if re.search(r"\[\[\d{4}-\d{2}-\d{2}-", line):
                fail("no link into a private vault", where)
                clean = False
    if clean:
        ok("red lines on added lines", "dashes, double hyphens, spaced hyphens, names, private links")


# ------------------------------------------------------------ 6 · scope


def check_scope(base):
    for rel in FROZEN:
        code, _, _ = git("diff", "--quiet", base, "--", rel)
        if code != 0:
            fail("frozen files", f"{rel} differs from {base}")
        code, out, _ = git("status", "--porcelain", "--", rel)
        if out.strip():
            fail("frozen files", f"{rel} has uncommitted or untracked changes")
    if not any(n == "frozen files" for n, _ in failures):
        ok("frozen files", "templates, setup, capture, distill, router, scripts untouched")

    code, out, _ = git("diff", "--name-only", base)
    _, untracked, _ = git("ls-files", "--others", "--exclude-standard")
    changed = sorted(set(out.split()) | set(untracked.split()))
    stray = [c for c in changed if c not in TARGETS + ALLOWED_EXTRA]
    if stray:
        fail("only the expected files changed", f"unexpected: {stray}")
    else:
        ok("only the expected files changed", f"{len(changed)} file(s)")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="origin/main")
    args = parser.parse_args()

    code, _, err = git("rev-parse", "--verify", args.base)
    if code != 0:
        print(f"cannot resolve base ref {args.base}: {err.strip()}")
        return 2

    check_handoff_block()
    check_deliver()
    check_guide()
    check_pointer_home()
    check_maintenance()
    check_red_lines(args.base)
    check_scope(args.base)

    for name, detail in passes:
        print(f"  ok    {name}" + (f"  ({detail})" if detail else ""))
    if failures:
        print(f"\nFAILURES: {len(failures)}")
        for name, detail in failures:
            print(f"  FAIL  {name}: {detail}")
        return 1
    print("\nFAILURES: none")
    print("PASS, the text is in place and clean. Whether it works is the clean session's question.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
