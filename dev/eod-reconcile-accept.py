#!/usr/bin/env python3
"""
eod-reconcile-accept.py - acceptance harness for one piece of written
behaviour that lives in two places: the end-of-day reconcile in the generated
command-base skill (the net), and the closing step in the session report skill
that patches the records a session finished (the road).

WHAT THIS IS
    The half of the acceptance a machine can judge. It reads the shipped text
    and answers five questions:

      1. Is the reconcile section in the command-base template, directly above
         the core rules, carrying exactly one version marker, and does the
         compile row send a session there before the daily note?
      2. Does that section name its three sources, its three kinds of
         mismatch, the owner's yes, and its own limits (today only, the
         touched projects only, never at the cost of the note)?
      3. Does the session report skill carry the closing step, between the
         decisions backstop and the baton, with its three refusals?
      4. Does the product skill carry the retrofit for vaults generated before
         this existed, keyed on the same marker, and does it protect what the
         owner wrote into the compile row?
      5. Do the sections this harness owns keep the product's red lines?

WHAT THIS IS NOT
    ⛔ It does not judge whether the words work. Whether a session that has
    never seen this text finds the task that should have been closed, leaves
    alone the one that only sounds related, and waits for a yes before it
    writes, is a question only a clean session answers, by doing it against a
    vault built to trip it. A green run here means the text is in place and
    clean, nothing more. `dev/eod-reconcile-fixture.py` builds that vault, and
    its header says what a session should and should not find in it.

WHEN TO RUN IT
    After any edit to the files listed in TARGETS, before calling the edit
    done.

    $ python3 dev/eod-reconcile-accept.py                      # standing checks
    $ python3 dev/eod-reconcile-accept.py --base origin/main   # plus branch checks

    The branch checks (red lines on every added line, nothing outside the
    expected files changed) are answerable only while a branch is being
    reviewed, so they run only when a base is named.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

TEMPLATE = "my-second-brain/templates/command-base-SKILL.template.md"
REPORT = "my-second-brain/skills/breakthrough-session-report/SKILL.md"
ROUTER = "my-second-brain/SKILL.md"
GUIDE = "my-second-brain/references/operating-the-second-brain-student-guide.md"

TARGETS = [TEMPLATE, REPORT, ROUTER, GUIDE]

# Maintainer files allowed to change beside the targets.
ALLOWED_EXTRA = [
    "dev/eod-reconcile-accept.py",
    "dev/eod-reconcile-fixture.py",
    "README.md",
]

SECTION_HEADING = "## End-of-day reconcile"
BACKSTOP_HEADING = "## The second backstop"

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


def headings(text, level=2):
    return [l for l in text.splitlines() if re.match(rf"^{'#' * level} ", l)]


def need(name, body, wanted):
    """Every (label, pattern) in wanted is found in body, or one failure names
    the ones that are not."""
    missing = [label for label, pat in wanted if not re.search(pat, body, re.I | re.S)]
    if missing:
        fail(name, f"not found: {missing}")
        return False
    ok(name, ", ".join(label for label, _ in wanted))
    return True


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


# ------------------------------------------------------- 1 · the net, placed


def check_template_placement():
    text = read(TEMPLATE)
    body = section(text, SECTION_HEADING)
    if body is None:
        fail("reconcile section", f"`{SECTION_HEADING}` is not in the template")
        return None
    ok("reconcile section", "present in the command-base template")

    h2 = headings(text)
    at = next(i for i, h in enumerate(h2) if h.startswith(SECTION_HEADING))
    after = h2[at + 1] if at + 1 < len(h2) else "(end of file)"
    if after.strip() != "## Core rules":
        fail(
            "reconcile placement",
            f"the section is followed by `{after.strip()}`, and the retrofit lands it directly above `## Core rules`",
        )
    else:
        ok("reconcile placement", "directly above `## Core rules`")

    markers = re.findall(r"<!-- eod-rev: (\S+) -->", text)
    if len(markers) != 1:
        fail("one eod-rev marker", f"found {len(markers)} in the template")
    elif not markers[0].isdigit():
        fail("one eod-rev marker", f"its value is `{markers[0]}`, not a number")
    elif f"<!-- eod-rev: {markers[0]} -->" not in body:
        fail("one eod-rev marker", "the marker sits outside the reconcile section")
    else:
        ok("one eod-rev marker", f"eod-rev: {markers[0]}, inside the section")

    # The two older markers this change had no business touching.
    for other in ("boot-gate-rev", "doorbell-rev"):
        if len(re.findall(rf"<!-- {other}: \d+ -->", text)) != 1:
            fail("older markers intact", f"`{other}` no longer appears exactly once")
    if not any(n == "older markers intact" for n, _ in failures):
        ok("older markers intact", "boot-gate-rev and doorbell-rev each appear once")

    row = next(
        (l for l in text.splitlines() if l.startswith('| "compile"')), None
    )
    if row is None:
        fail("compile row", "the router has no row opening with \"compile\"")
    else:
        send = row.find("End-of-day reconcile")
        note = row.find("daily note")
        if send == -1:
            fail("compile row", "the row never names the reconcile section")
        elif note == -1 or send > note:
            fail("compile row", "the row names the reconcile after the daily note, not before it")
        else:
            ok("compile row", "sends the session to the reconcile before the daily note")
        if "capture-buffer.md" not in row or "01_Daily/" not in row:
            fail("compile row keeps its old job", "the note or the buffer dropped out of the row")
        else:
            ok("compile row keeps its old job", "still writes the note and clears the buffer")
    return body


# ------------------------------------------------------ 2 · the net, content


def check_template_content(body):
    need(
        "three sources",
        body,
        [
            ("captures", r"99_Meta/capture-buffer\.md"),
            ("session reports", r"session-report\.md"),
            ("this session", r"\*\*This session:\*\*"),
        ],
    )
    need(
        "reports read from both shelves",
        body,
        [("00_Inbox/", r"`00_Inbox/`"), ("98_Archive/", r"`98_Archive/`")],
    )
    need(
        "a report read here is not used up",
        body,
        [
            ("says so", r"does not use it up"),
            ("left where it is", r"Leave it where it is"),
        ],
    )
    need(
        "three kinds of mismatch",
        body,
        [
            ("finished, still open", r"\*\*Finished, still open\.\*\*"),
            ("waiting, and it arrived", r"\*\*Waiting, and it arrived\.\*\*"),
            ("brief describing yesterday", r"\*\*A brief still describing yesterday\.\*\*"),
        ],
    )
    need(
        "the owner's yes",
        body,
        [
            ("nothing changes without the yes", r"Nothing changes without the yes"),
            ("a no is not raised again", r"do not raise it again"),
        ],
    )
    need(
        "its own limits",
        body,
        [
            ("that date only", r"that date only"),
            ("not the whole vault", r"Not the whole vault"),
            ("part done is not done", r"part done is not done"),
            ("said, not guessed", r"said, not guessed"),
            ("never costs the note", r"must never cost a day its note"),
            ("empty is the usual answer", r"Nothing to reconcile is the usual answer"),
        ],
    )
    # Statuses are the vault's own list. A list quoted here would be read as
    # the whole set, which is how an off-list status gets written.
    if "§8" not in body:
        fail("statuses read from the doctrine", "the section never sends the reader to §8")
    else:
        ok("statuses read from the doctrine", "§8 named, no list quoted")
    quoted = re.findall(r"`(not-started|blocked|cancelled|killed)`", body)
    if quoted:
        fail("no status list quoted", f"statuses spelled out in the section: {sorted(set(quoted))}")
    else:
        ok("no status list quoted")

    # Things this pass was deliberately not given.
    if re.search(r"deck\.py|rebuild", body, re.I):
        fail("no second dashboard rebuild", "the section mentions a rebuild; there is one, at session start")
    else:
        ok("no second dashboard rebuild")
    stray = sorted(set(re.findall(r"\{\{([A-Z_]+)\}\}", body)) - {"YOUR_NAME"})
    if stray:
        fail("placeholders", f"placeholders the generator may not fill here: {stray}")
    else:
        ok("placeholders", "only {{YOUR_NAME}}")


# ------------------------------------------------------------ 3 · the road


def check_report():
    text = read(REPORT)
    body = section(text, BACKSTOP_HEADING)
    if body is None:
        fail("closing step", f"`{BACKSTOP_HEADING}` is not in the session report skill")
        return None
    ok("closing step", "present in the session report skill")

    h2 = [h.strip() for h in headings(text)]
    at = next(i for i, h in enumerate(h2) if h.startswith(BACKSTOP_HEADING))
    before = h2[at - 1] if at else "(top of file)"
    after = h2[at + 1] if at + 1 < len(h2) else "(end of file)"
    if not before.startswith("## The backstop") or not after.startswith("## The baton"):
        fail(
            "closing step order",
            f"it sits between `{before}` and `{after}`; it belongs after the decisions backstop and before the baton",
        )
    else:
        ok("closing step order", "after the decisions backstop, before the baton")

    need(
        "closing step asks, then writes",
        body,
        [
            ("asks", r"close it\?"),
            ("on a yes", r"On a yes"),
            ("status from §8", r"§8"),
            ("waiting_on", r"`waiting_on`"),
            ("a dated line", r"one dated line"),
            ("the brief", r"`## Next step`"),
        ],
    )
    need(
        "three refusals",
        body,
        [
            ("part done is not done", r"\*\*Part done is not done\.\*\*"),
            ("only this session's records", r"\*\*Only the records this session worked on\.\*\*"),
            ("no task made to be closed", r"do not create one in order to close it"),
        ],
    )
    need(
        "the read-only way out",
        body,
        [("names the record in the report", r"cannot write to the vault")],
    )

    baton = section(text, "## The baton") or ""
    if not re.search(r"records it patched", baton):
        fail("outputs name the patched records", "the baton's outputs line never mentions them")
    else:
        ok("outputs name the patched records")

    front = text.split("---", 2)[1] if text.startswith("---") else ""
    if "finished but never closed" not in " ".join(front.split()):
        fail("description", "the frontmatter description does not name the new job")
    else:
        ok("description", "names the task finished but never closed")
    return body


# -------------------------------------------------------- 4 · the retrofit


def check_retrofit():
    text = read(ROUTER)
    numbered = re.findall(r"^(\d+)\. \*\*", text, re.M)
    runs = []
    for n in map(int, numbered):
        if runs and n == runs[-1][-1] + 1:
            runs[-1].append(n)
        else:
            runs.append([n])
    line = next(
        (l for l in text.splitlines() if re.match(r"^\d+\. \*\*Retrofit the end-of-day reconcile", l)),
        None,
    )
    if line is None:
        fail("retrofit step", "no numbered step opens with `Retrofit the end-of-day reconcile`")
        return None
    number = int(line.split(".", 1)[0])
    run = next(r for r in runs if number in r)
    if run != list(range(run[0], run[-1] + 1)) or number != run[-1]:
        fail("retrofit step numbering", f"step {number} is not the last of an unbroken run: {run}")
    else:
        ok("retrofit step", f"step {number}, last of an unbroken run from {run[0]}")

    need(
        "retrofit is keyed on the marker",
        line,
        [
            ("greps eod-rev", r"`eod-rev:`"),
            ("takes wording from the template", r"templates/command-base-SKILL\.template\.md"),
            ("verifies through the installed path", r"verify through the installed path"),
            ("both locations", r"both locations"),
            ("maintainer bump rule", r"bump `eod-rev:`"),
        ],
    )
    need(
        "retrofit protects the owner's row",
        line,
        [
            ("adds to the front of the row", r"front of the row"),
            ("leaves the rest as found", r"exactly as found"),
            ("honest stop on a rewritten skill", r"honest stop"),
        ],
    )
    if re.search(r"eod-rev: \d", line):
        fail("no number hardcoded in the retrofit", "the step quotes a marker number; it must read the template's")
    else:
        ok("no number hardcoded in the retrofit")

    front = text.split("---", 2)[1] if text.startswith("---") else ""
    if "upgrade my end of day" not in " ".join(front.split()):
        fail("router description", "the trigger phrase is not in the frontmatter description")
    else:
        ok("router description", "names the trigger phrase")
    return line


def check_guide():
    lines = [l for l in read(GUIDE).splitlines() if "EOD" in l and "session report" in l]
    if not lines:
        fail("student guide", "no line ties the end of day to the day's session reports")
        return ""
    ok("student guide", "one line explains the reconcile")
    return "\n".join(lines)


# --------------------------------------------------------- 5 · red lines


def judge_line(rel, line):
    """True when the line keeps every red line; records a failure otherwise."""
    clean = True
    where = f"{rel}: {line.strip()[:90]}"
    # A version marker is an HTML comment, and its delimiters are not prose.
    line = re.sub(r"<!--.*?-->", "", line)
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


def check_red_lines_standing(owned):
    clean = True
    count = 0
    for rel, text in owned:
        for line in (text or "").splitlines():
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


def check_scope(base):
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
        help="a ref to compare against; adds the branch checks (added lines, scope)",
    )
    args = parser.parse_args()

    if args.base:
        code, _, err = git("rev-parse", "--verify", args.base)
        if code != 0:
            print(f"cannot resolve base ref {args.base}: {err.strip()}")
            return 2

    net = check_template_placement()
    if net is not None:
        check_template_content(net)
    road = check_report()
    retrofit = check_retrofit()
    guide = check_guide()
    check_red_lines_standing(
        [(TEMPLATE, net), (REPORT, road), (ROUTER, retrofit), (GUIDE, guide)]
    )
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
