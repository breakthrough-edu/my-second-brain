#!/usr/bin/env python3
"""
report-back-accept.py - acceptance harness for three pieces of written behaviour:
the report-back loop (a handoff carries a return address, the closing session
sends the report's path back), the chip (a handoff queued as the next
session's opening message still carries that address), and the playbook
memory-pointer check in the weekly maintenance pass.

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

    $ python3 dev/report-back-accept.py                      # standing checks
    $ python3 dev/report-back-accept.py --base origin/main   # plus branch checks

TWO MODES, AND WHY THE SECOND ONE IS OPT-IN
    The standing checks read the shipped text as it is: the sections are in
    place, the four results are the four results, and the sections this
    harness owns keep the red lines. They stay true after a merge, on any
    branch.

    The branch checks compare against a base ref: red lines on every ADDED
    line, the frozen files untouched, nothing outside the expected files
    changed. They are answerable only while a branch is being reviewed. Run
    by default they would go red on the first later branch that legitimately
    edits a template, for a reason that has nothing to do with this text, and
    a check that is red for reasons nobody will fix is a check people stop
    running. So they run only when a base is named.

WHY THE STANDING RED-LINE CHECK READS SECTIONS, NOT WHOLE FILES
    The files carry YAML fences, table rules and one quoted list line that
    would trip a whole-file scan forever. The sections this harness locates
    are the only text it is answerable for.
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
ALLOWED_EXTRA = [
    "dev/report-back-accept.py",
    "README.md",
    # Re-anchored in the same round: one citation had slid when deck.py changed.
    "my-second-brain/skills/breakthrough-vault-guardian/references/what-each-rule-guards.md",
]

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
        "permissions": r"\*\*Permissions:\*\*",
    }
    missing = [k for k, pat in wanted.items() if not re.search(pat, body, re.I)]
    if missing:
        fail("report-back block fields", f"not named in the handoff section: {missing}")
    else:
        ok("report-back block fields", "environment, address, title, machine, permissions all named")

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


# ---------------------------------------------------------- 1b · the chip


def check_chip():
    """A handoff queued as a chip goes through the handoff entry, and the
    session that picks it up meets the block before the work."""
    text = read(CONSULTANT)
    front = text.split("---")[1] if text.startswith("---") else ""
    for phrase in ("write a handoff", "写一个 handoff", "open a chip", "开一个 chip"):
        if phrase not in front:
            fail("description names the ask", f"`{phrase}` is not in the description")
    if all(p in front for p in ("write a handoff", "写一个 handoff", "open a chip", "开一个 chip")):
        ok("description names the ask", "handoff and chip, in both languages")
    flat = " ".join(line.strip() for line in front.splitlines())
    if "brain dump of a project" in flat:
        fail("description scope", "the old sentence tying a handoff to a project is back")
    elif "whether or not the work has a project" not in flat:
        fail("description scope", "the description no longer says a handoff needs no project")
    elif "the command-base one included" not in flat:
        fail("description scope", "the description no longer says the daily session counts")
    else:
        ok("description scope", "says outright: any session, with or without a project")
    m = re.search(r"description: >\s*(.*?)\s*$", flat)
    length = len(m.group(1)) if m else 0
    if not 0 < length <= 1024:
        fail("description length", f"{length} characters, the limit is 1024")
    else:
        ok("description length", f"{length} of 1024 characters")

    body = section(text, "## The handoff entry")
    if body is None:
        return
    chip = next((b for b in re.split(r"\n(?=- \*\*)", body) if "as a chip" in b), None)
    if chip is None:
        fail("chip bullet", "the handoff section has no bullet for a handoff queued as a chip")
        return
    ok("chip bullet", "sits inside the handoff section")
    wanted = {
        "chip is defined": r"a card holding the next session's opening message",
        "sentence: block before the work": r"meets the `Report back to` block before it meets the work",
        "sentence: one-shot card opens with the block": r"opens with the `Report back to` block",
        "sentence: one-shot makes no file": r"no file is made",
        "sentence: file case is one line": r"one line and no more",
        "sentence: no second copy in the card": r"Do not repeat the handoff in the card",
        "sentence: the click is the owner's": r"click stays the owner's",
        "sentence: never unattended": r"never start a session nobody is watching",
        "sentence: never unasked": r"never move work the owner gave this session onto a card they did not ask for",
        "sentence: the opening is only for things noticed in passing": r"something it noticed in passing",
        "sentence: an offered card carries the block too": r"opens with the block too",
        "sentence: judge the piece, not the project": r"judge the piece being handed over",
        "sentence: the project question stays off the card": r"not to a card",
        "sentence: no card is ordinary": r"Nobody asked for a card, or there is no way to queue one",
    }
    for name, pat in wanted.items():
        if re.search(pat, chip):
            ok(name)
        else:
            fail(name, "the chip bullet no longer says it")
    if "The owner opens it." in body:
        fail("old owner-only sentence", "the sentence saying only the owner opens the next session is back")
    elif "is the next bullet" not in body:
        fail("old owner-only sentence", "the block paragraph no longer hands off to the chip bullet")
    else:
        ok("old owner-only sentence", "gone, and the block paragraph points at the chip bullet")
    if "This entry does not pick its session" not in body:
        fail("entry serves any session", "the handoff section no longer says the daily session counts")
    else:
        ok("entry serves any session", "the sentence saying the entry does not pick its session is there")
    if "comes through here" not in body or "not the Braindump file" not in body:
        fail("brain dump for a successor", "the handoff section no longer says which door it takes")
    else:
        ok("brain dump for a successor", "named as a handoff, and told apart from the Braindump file")
    # Sentences that would undo the rule if somebody added them.
    undo = [
        r"start the session yourself",
        r"Only the owner ever prepares",
        r"a file is made as well",
    ]
    hit = [u for u in undo if re.search(u, body)]
    if hit:
        fail("nothing undoes the rule", f"found: {hit}")
    else:
        ok("nothing undoes the rule", "⚠️ three known phrasings only; this is not a proof")

    guide = read(GUIDE)
    need = ["开一个 chip", "按下去的永远是你", "卡本身就是 handoff", "卡上只有一行", "不必开档"]
    gone = [n for n in need if n not in guide]
    if gone or "除非主 session" in guide:
        fail("guide carries both shapes and the click", f"missing or undone: {gone}")
    else:
        ok("guide carries both shapes and the click")


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


def judge_line(rel, line):
    """True when the line keeps every red line; records a failure otherwise."""
    clean = True
    where = f"{rel}: {line.strip()[:90]}"
    if chr(0x2014) in line or chr(0x2013) in line:  # em dash, en dash
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
    return clean


def owned_text():
    """The sections this harness is answerable for, as (file, text) pairs.
    A section that has gone missing is reported by its own check, not here."""
    out = []
    handoff = section(read(CONSULTANT), "## The handoff entry")
    if handoff:
        out.append((CONSULTANT, handoff))
    report = read(REPORT)
    baton = section(report, "## The baton") or ""
    m = re.search(r"^#{3,4} Deliver the baton.*$", baton, re.M)
    if m:
        out.append((REPORT, baton[m.start():]))
    close = section(report, "## Close")
    if close:
        out.append((REPORT, close))
    pointer = [
        l
        for l in read(METHOD).splitlines()
        if "Claude's own memory" in l or "99_Meta/memory.md" in l
    ]
    out.append((METHOD, "\n".join(pointer)))
    maint = read(MAINT)
    start = maint.find("1b. **")
    end = maint.find("**Machine-layer self-check**")
    if start != -1 and end > start:
        out.append((MAINT, maint[start:end]))
    guide = [
        l
        for l in read(GUIDE).splitlines()
        if "session report" in l and "00_Inbox/" in l
    ]
    out.append((GUIDE, "\n".join(guide)))
    return out


def check_red_lines_standing():
    clean = True
    count = 0
    for rel, text in owned_text():
        for line in text.splitlines():
            count += 1
            clean = judge_line(rel, line) and clean
    if clean:
        ok("red lines on the owned sections", f"{count} lines")


def check_red_lines_added(base):
    clean = True
    for rel in TARGETS + ["README.md"]:
        for line in added_lines(base, rel):
            clean = judge_line(rel, line) and clean
    if clean:
        ok("red lines on added lines", f"against {base}")


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
    parser.add_argument(
        "--base",
        default=None,
        help="a ref to compare against; adds the branch checks (added lines, frozen files, scope)",
    )
    args = parser.parse_args()

    if args.base:
        code, _, err = git("rev-parse", "--verify", args.base)
        if code != 0:
            print(f"cannot resolve base ref {args.base}: {err.strip()}")
            return 2

    check_handoff_block()

    check_chip()
    check_deliver()
    check_guide()
    check_pointer_home()
    check_maintenance()
    check_red_lines_standing()
    if args.base:
        check_red_lines_added(args.base)
        check_scope(args.base)

    for name, detail in passes:
        print(f"  ok    {name}" + (f"  ({detail})" if detail else ""))
    if failures:
        print(f"\nFAILURES: {len(failures)}")
        for name, detail in failures:
            print(f"  FAIL  {name}: {detail}")
        return 1
    print("\nFAILURES: none")
    mode = f"standing and branch checks against {args.base}" if args.base else "standing checks"
    print(f"PASS ({mode}): the text is in place and clean. Whether it works is the clean session's question.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
