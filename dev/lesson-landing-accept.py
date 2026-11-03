#!/usr/bin/env python3
"""
lesson-landing-accept.py - acceptance harness for the Lesson landing: a
Lesson's rules land where the work runs, and a second fall into the same pit
rewrites the old Lesson instead of opening a new one.

WHAT THIS IS
    The half of the acceptance a machine can judge. It reads the shipped text
    and answers six questions:

      1. Does the session report skill's first question carry, in this order,
         the search of the Lessons room, the trigger line, the ask of where
         each rule lives (with its four homes and its refusals), and the
         memory reminder (with its no-path rule and its one fallback)?
      2. Does the Lesson template open its living half with a trigger line and
         show a rule ending with where it lives?
      3. Does the doctrine template's section 7 carry the landing and the
         second-fall rule, and does its table say where a Lesson lands?
      4. Does the CLAUDE.md template carry the closeout search and the
         pointer as the trigger line?
      5. Does the product skill carry the retrofit for existing vaults, with
         its trigger phrase, the guardian route for the law, and no sweep?
      6. Branch only: do the added lines keep the product's red lines, does
         section 8 of the doctrine template stay byte-identical, and did
         nothing outside the expected files change?

WHAT THIS IS NOT
    ⛔ It does not judge whether the words work. Whether a session that has
    never seen this text searches before it writes, recognises the same pit,
    rewrites the old Lesson and moves its rule into the file that ran, is a
    question only a clean session answers, against a vault built to trip it.
    A green run here means the text is in place and clean, nothing more.

WHEN TO RUN IT
    After any edit to the files listed in TARGETS, before calling the edit
    done.

    $ python3 dev/lesson-landing-accept.py                    # standing checks
    $ python3 dev/lesson-landing-accept.py --base origin/main # plus branch checks
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

REPORT = "my-second-brain/skills/breakthrough-session-report/SKILL.md"
NOTES = "my-second-brain/templates/note-templates.md"
DOCTRINE = "my-second-brain/templates/structure-doctrine.template.md"
CLAUDE = "my-second-brain/templates/CLAUDE.template.md"
ROUTER = "my-second-brain/SKILL.md"
GUIDE = "my-second-brain/references/operating-the-second-brain-student-guide.md"

TARGETS = [REPORT, NOTES, DOCTRINE, CLAUDE, ROUTER, GUIDE]

# Maintainer files allowed to change beside the targets.
ALLOWED_EXTRA = ["dev/lesson-landing-accept.py"]

# Words that would put the author's own house into the public text.
PRIVATE = [r"Jia Wei", r"\bJW\b", r"/Users/", r"jiawei", r"Breakthrough"]

failures = []


def check(ok, what):
    print(("PASS  " if ok else "FAIL  ") + what)
    if not ok:
        failures.append(what)


def read(rel):
    return (REPO / rel).read_text(encoding="utf-8")


def section(text, start, stop):
    a = text.find(start)
    if a < 0:
        return ""
    b = text.find(stop, a + len(start))
    return text[a:] if b < 0 else text[a:b]


def standing():
    # 1 · the closeout's first question
    q1 = section(read(REPORT), '### 1 · "Did anything bite us?"', "### 2 ·")
    check(bool(q1), "report: first question found")
    marks = [
        ("search", "Before writing, search `04_Methodology/Lessons/`"),
        ("trigger", "The living half opens with one trigger line"),
        ("landing", "ask where it lives"),
        ("reminder", "Then leave the reminder"),
    ]
    pos = [q1.find(m) for _, m in marks]
    for (name, m), p in zip(marks, pos):
        check(p >= 0, f"report: {name} paragraph present")
    check(all(p >= 0 for p in pos) and pos == sorted(pos),
          "report: search, trigger, landing, reminder in that order")
    for phrase in ["it gets no second note", "`## Related`", "widen the trigger line",
                   "no counter and no flag"]:
        check(phrase in q1, f"report: second-fall wording has {phrase!r}")
    check("never a list of past scenes" in q1.replace("Never", "never"),
          "report: trigger line refuses a list of past scenes")
    check("do not hand them a blank line" in q1, "report: AI drafts the trigger line")
    for home in ["step of the SOP", "command-base skill", "door of the playbook folder",
                 "doctrine section 8", "breakthrough-vault-guardian"]:
        check(home in q1, f"report: landing home {home!r} named")
    check("Never a skill that ships with this product" in q1 and "never a hook" in q1,
          "report: product skills and hooks refused as homes")
    check("(lives in: memory only)" in q1 and "(lives in: [[" in q1,
          "report: both shapes of the lives-in tail shown")
    check('never "see Lesson X"' in q1, "report: no see-Lesson pointer in the home")
    check("On a second fall the rule moves" in q1 and "file that did" in q1,
          "report: second fall moves the rule up, or onto the path that ran")
    check("No path to that memory is written here" in q1, "report: memory path never guessed")
    check("`99_Meta/memory.md`" in q1 and "One home, never both" in q1,
          "report: one fallback for the reminder, never both")
    check("not the title" in q1, "report: pointer is the trigger line, not the title")

    # 2 · the Lesson template
    lesson = section(read(NOTES), "## Lesson.md", "## Method.md")
    living = section(lesson, "## What we now do differently", "<!--\n04_Methodology")
    check("**Trigger:**" in living, "template: trigger line in the living half")
    check("(lives in:" in living, "template: rule ends with where it lives")
    check("second fall" in living.lower(), "template: second fall rewrites here")
    head = lesson.split("---")[1] if lesson.count("---") >= 2 else ""
    check(all(k in head for k in ["type: lesson", "date:", "source:", "lane:",
                                  "confirmed_by_owner:"]) and "enforced_in" not in head,
          "template: frontmatter keys unchanged, no new key")

    # 3 · the doctrine template
    doc = read(DOCTRINE)
    s7 = section(doc, "## 7 ·", "## 8 ·")
    lesson_line = next((l for l in s7.splitlines() if l.startswith("- **Lesson = a pit.**")), "")
    for phrase in ["Lesson's rules land where the work runs", "trigger line",
                   "not a second Lesson", 'never as "see Lesson X"', "## Related"]:
        check(phrase in lesson_line, f"doctrine §7: Lesson line has {phrase!r}")
    check("each rule linked to the file it now lives in" in s7,
          "doctrine §7: table says where a Lesson lands")

    # 4 · the CLAUDE.md template
    cl = read(CLAUDE)
    check("search `04_Methodology/Lessons/` first" in cl, "CLAUDE: closeout search line")
    check("A Lesson's pointer is its trigger line" in cl, "CLAUDE: pointer is the trigger line")

    # 5 · the retrofit
    router = read(ROUTER)
    r12 = section(router, "12. **Retrofit the Lesson landing", "\n## ")
    check(bool(r12), "router: retrofit 12 present")
    check('"upgrade my lessons"' in r12 and "upgrade my lessons" in router.split("---")[1],
          "router: trigger phrase in the rule and the description")
    check("breakthrough-vault-guardian" in r12, "router: the law goes through the guardian")
    check("not swept" in r12, "router: written Lessons are not swept")
    check("**Trigger:**" in r12, "router: retrofit keyed on the trigger line")
    check(re.search(r"⛔ touching no other template", r12) is not None,
          "router: only the Lesson template is replaced")

    guide = read(GUIDE)
    check("改旧的那份, 不开新的" in guide, "student guide: second fall rewrites the old Lesson")


def branch(base):
    def git(*a):
        return subprocess.run(["git", "-C", str(REPO), *a], capture_output=True,
                              text=True, check=True).stdout

    changed = [l for l in git("diff", "--name-only", base).splitlines() if l]
    untracked = [l for l in git("ls-files", "--others", "--exclude-standard").splitlines() if l]
    stray = [f for f in changed + untracked if f not in TARGETS + ALLOWED_EXTRA]
    check(not stray, f"branch: nothing outside the expected files changed {stray or ''}")

    added = []
    for f in TARGETS:
        for l in git("diff", "-U0", base, "--", f).splitlines():
            if l.startswith("+") and not l.startswith("+++"):
                added.append((f, l[1:]))
    check(bool(added), "branch: there are added lines to judge")
    bad = [(f, l) for f, l in added if "—" in l or " -- " in l or re.search(r"\w - \w", l)]
    check(not bad, "branch: no em dash, double dash or spaced hyphen on added lines"
          + (f" {bad[0]}" if bad else ""))
    priv = [(f, l) for f, l in added for p in PRIVATE if re.search(p, l)]
    check(not priv, "branch: no author's name, path or house on added lines"
          + (f" {priv[0]}" if priv else ""))

    old8 = section(git("show", f"{base}:{DOCTRINE}"), "## 8 ·", "## 9 ·")
    new8 = section(read(DOCTRINE), "## 8 ·", "## 9 ·")
    check(bool(old8) and old8 == new8, "branch: doctrine §8 byte-identical")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", help="git ref to diff against for the branch checks")
    args = parser.parse_args()
    standing()
    if args.base:
        branch(args.base)
    print()
    print(f"{len(failures)} failure(s)" if failures else "ALL PASS")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
