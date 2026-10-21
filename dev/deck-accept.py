#!/usr/bin/env python3
"""
deck-accept.py - acceptance harness for what the Command Deck derives from a
task's body, and for the pieces of the page that carry it.

WHAT THIS IS
    The deck reads more than frontmatter. A task card shows the meetings the
    task was discussed in (read from `[[YYYY-MM-DD-...-meeting-summary]]` links
    in the body, never from a key), the newest dated line of the body as its
    latest note, and a `cancelled` task is drawn beside `done` wherever the
    vault's own section 8 lists that value. None of that is a frontmatter key,
    so neither the checker nor the frontmatter guard will ever notice when it
    breaks. This harness is what notices.

    It builds two small vaults in a temporary folder, runs the shipped
    `scripts/deck.py` against each, and reads back both the payload and the
    page `build` writes:

      A  a vault whose section 8 lists `cancelled`, with tasks that link
         meetings, tasks that do not, a cancelled task and a done one
      B  a vault on the doctrine exactly as shipped, with no meeting links and
         no cancelled task, which is most vaults: it must come out the way it
         always did, apart from the new optional pieces

    ⛔ It never touches a real vault. Both are built from scratch under a temp
    directory and deleted at the end.

WHEN TO RUN IT
    After editing `scripts/deck.py` or `scripts/deck-template.html`.

    $ python3 dev/deck-accept.py

WHY IT IMPORTS YAML
    The deck itself needs no PyYAML; without it the build still runs and simply
    does not read section 8. That is the right failure for code that ships and
    the wrong one for this harness: vault A's `cancelled` tasks are drawn only
    because section 8 was read, so a run without PyYAML would test the fallback
    and report it as the real thing. The import below therefore fails loudly.
    This file sits under dev/, outside the payload, and never ships.

WHAT IT DELIBERATELY DOES NOT DO
    It does not judge whether the page works in a browser: the drag, the reason
    prompt and the paste-back text are a click-through's job. It checks that
    the pieces are in the page, that the page's script parses when `node` is on
    the PATH, and that nothing the build prints says a task was left off.

EXIT CODES
    0  every check passed
    1  a check failed (each FAIL line says which and what was found)
    2  could not run at all (PyYAML missing, the payload not where expected)
"""

import argparse
import contextlib
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

try:
    import yaml  # noqa: F401  (see WHY IT IMPORTS YAML)
except ImportError:
    sys.stderr.write(
        "FAIL - PyYAML is not installed for %s.\n"
        "This harness needs section 8 to be read, which is what PyYAML does for the\n"
        "deck. Run it with a python3 that has PyYAML, or install it there first.\n"
        % sys.executable)
    sys.exit(2)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PAYLOAD = os.path.join(REPO, "my-second-brain")
SCRIPTS = os.path.join(PAYLOAD, "scripts")
DOCTRINE_TEMPLATE = os.path.join(PAYLOAD, "templates", "structure-doctrine.template.md")
DECK_TEMPLATE = os.path.join(SCRIPTS, "deck-template.html")

sys.path.insert(0, SCRIPTS)
import deck  # noqa: E402

SHIPPED_TASK_LIST = "status: [not-started, in-progress, waiting, blocked, done]}"
WITH_CANCELLED = "status: [not-started, in-progress, waiting, blocked, done, cancelled]}"
WING = "04_Acme-Business-Wing"
PROJECT = WING + "/02_Work/Grow/Spring-Launch"
ORIGINAL_FIVE = ["not-started", "in-progress", "waiting", "blocked", "done"]

passes, failures = [], []


def ok(name, detail):
    passes.append((name, detail))


def fail(name, detail):
    failures.append((name, detail))


def check(cond, name, good, bad):
    (ok if cond else fail)(name, good if cond else bad)
    return cond


# ------------------------------------------------------------------ fixtures

def write(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def task(status, body, extra=""):
    return ("---\ncb: task\nstatus: %s\ncreated: 2026-03-01\n%s---\n\n%s\n"
            % (status, extra, body))


def build_vault(root, doctrine_text, tasks):
    for d in ("00_Inbox", "01_Daily", "02_Command-Base/Decisions",
              "03_Personal-Wing/Personal-Projects", WING + "/01_Assets"):
        os.makedirs(os.path.join(root, d), exist_ok=True)
    write(root, "99_Meta/bootstrap-progress.md",
          "---\nbusiness_name: Acme Bakery\nbusiness_tag: \"#acme\"\nsetup_complete: true\n---\n")
    write(root, "99_Meta/structure-doctrine.md", doctrine_text)
    write(root, PROJECT + "/_Spring-Launch-Brief.md",
          "---\ntype: brief\nstatus: active\nupdated: 2026-03-01\ndue: 2026-04-30\n---\n\n"
          "# Spring Launch\n\nA seasonal menu launch.\n")
    for name, text in tasks.items():
        write(root, PROJECT + "/Tasks/" + name, text)


def vault_a_tasks():
    return {
        "supplier-quote.md": task(
            "waiting",
            "# Supplier quote for the spring menu\n\n"
            "Asked two suppliers for a quote ([[2026-03-02-supplier-call-meeting-summary]]).\n\n"
            "- 2026-03-02 Asked for a quote on flour and butter "
            "([[2026-03-02-supplier-call-meeting-summary]])\n"
            "- **2026-03-09** Second supplier wants a visit first "
            "([[2026-03-09-weekly-sync-meeting-summary]])\n"
            "- Follow-up: 2026-03-20 is when the first supplier said he would reply\n",
            extra="waiting_on: \"[[Sam]]\"\ndue: 2026-03-16\n"),
        "print-flyers.md": task(
            "not-started",
            "# Print the launch flyers\n\nSee [[_Spring-Launch-Brief]] and the notes in "
            "[[2026-03-01-flyer-ideas]].\n",
            extra="due: 2026-03-25\n"),
        "old-tasting.md": task(
            "cancelled",
            "# Tasting evening\n\n> 2026-03-05 Dropped, the launch date moved.\n"),
        "menu-photos.md": task("done", "# Menu photos\n\nShot and delivered.\n",
                               extra="due: 2026-03-04\n"),
    }


def vault_b_tasks():
    return {
        "first-step.md": task("not-started", "# First step\n\nWrite the plan.\n",
                              extra="due: 2026-03-20\n"),
        "second-step.md": task("in-progress", "# Second step\n\nTalk to the landlord.\n",
                               extra="due: 2026-03-27\n"),
        "third-step.md": task("done", "# Third step\n\nDone and dusted.\n"),
    }


def run_build(vault):
    """The real `deck.py build`, its printed line captured, against a fixture."""
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = deck.cmd_build(vault, argparse.Namespace(json=False))
    html_path = os.path.join(vault, deck.DECK_RELPATH)
    html = open(html_path, encoding="utf-8").read() if os.path.isfile(html_path) else ""
    return code, out.getvalue().strip(), html


def payload(vault):
    import datetime as _dt
    shape = deck.read_shape(vault)
    scan = deck.scan_vault(vault, shape)
    setup, data = deck.build_payload(shape, scan, _dt.datetime(2026, 3, 18, 9, 0))
    tasks = {}
    for p in data["projects"]:
        for t in p["tasks"]:
            tasks[t["file"].rsplit("/", 1)[-1]] = t
    return scan, setup, data, tasks


def script_parses(html):
    """`node --check` on the page's inline script, when node is there."""
    node = shutil.which("node")
    if not node:
        return None, "node is not on the PATH, so the script was not parsed"
    m = re.search(r"<script>(.*?)</script>", html, re.S)
    if not m:
        return False, "the page has no inline <script>"
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as fh:
        fh.write(m.group(1))
        js = fh.name
    try:
        r = subprocess.run([node, "--check", js], capture_output=True, text=True)
        return r.returncode == 0, (r.stderr.strip().splitlines() or ["parses"])[0]
    finally:
        os.unlink(js)


# ------------------------------------------------------------------ checks

def check_vault_a(root, doctrine):
    vault = os.path.join(root, "vault-a")
    build_vault(vault, doctrine.replace(SHIPPED_TASK_LIST, WITH_CANCELLED), vault_a_tasks())
    scan, setup, data, tasks = payload(vault)

    check(scan.task_law is not None and "cancelled" in scan.task_law,
          "A: section 8 read", "the fixture's section 8 lists cancelled",
          "section 8 was not read or does not list cancelled: %r (%s)"
          % (scan.task_law, scan.task_law_unread))

    q = tasks.get("supplier-quote.md", {})
    got = [m["slug"] for m in q.get("meetings", [])]
    want = ["2026-03-09-weekly-sync-meeting-summary", "2026-03-02-supplier-call-meeting-summary"]
    check(got == want, "A: meeting links become the meeting list, newest first",
          "%d meetings, %s first, each linked meeting once" % (len(got), got[0] if got else "?"),
          "got %r, wanted %r" % (got, want))
    check(all(m.get("date") == m["slug"][:10] for m in q.get("meetings", [])),
          "A: each meeting carries its date", "date taken from the link",
          "dates %r" % [m.get("date") for m in q.get("meetings", [])])

    f = tasks.get("print-flyers.md", {})
    check(f.get("meetings") == [], "A: a task with no meeting link has none",
          "a brief link and a dated non-meeting link are not meetings",
          "got %r" % f.get("meetings"))

    last = q.get("last") or {}
    check(last.get("date") == "2026-03-09"
          and last.get("text", "").startswith("Second supplier wants a visit first")
          and "meeting-summary" not in last.get("text", ""),
          "A: the latest dated progress line is picked",
          "2026-03-09, its date, markup and the bracketed meeting link stripped from the text; the later date "
          "inside a sentence is not taken",
          "got %r" % last)
    check(f.get("last") is None, "A: no dated line means no latest note",
          "print-flyers has none", "got %r" % f.get("last"))
    cx = tasks.get("old-tasting.md", {})
    check((cx.get("last") or {}).get("date") == "2026-03-05",
          "A: a quoted dated line counts", "the > quote marker is skipped",
          "got %r" % cx.get("last"))

    statuses = sorted(t["status"] for t in tasks.values())
    check("cancelled" in statuses, "A: cancelled tasks are in the payload",
          "old-tasting.md is drawn", "statuses %r" % statuses)
    check(data["meta"]["tasks"] == 4 == len(tasks),
          "A: cancelled tasks are counted", "meta.tasks = 4 = tasks on the page",
          "meta.tasks %r, tasks on the page %d" % (data["meta"]["tasks"], len(tasks)))
    check(setup.get("taskStatuses") == ORIGINAL_FIVE + ["cancelled"],
          "A: the board offers a cancelled column", "taskStatuses ends with cancelled",
          "taskStatuses %r" % setup.get("taskStatuses"))
    check(q.get("file") == PROJECT + "/Tasks/supplier-quote.md"
          and os.path.isfile(os.path.join(vault, q.get("file", "x"))),
          "A: each task ships its real path", q.get("file"), "file %r" % q.get("file"))
    proj = data["projects"][0] if data["projects"] else {}
    check(proj.get("file") == PROJECT + "/_Spring-Launch-Brief.md" and proj.get("dir") == PROJECT,
          "A: each project ships its real Brief and folder", proj.get("file"),
          "file %r dir %r" % (proj.get("file"), proj.get("dir")))
    check(setup.get("vaultName") == "vault-a", "A: the vault's folder name reaches the page",
          "vaultName = vault-a", "vaultName %r" % setup.get("vaultName"))

    code, line, html = run_build(vault)
    check(code == 0 and line.startswith("Command Deck rebuilt: 1 projects, 4 tasks,"),
          "A: build prints its line", line, "exit %s, printed %r" % (code, line))
    check("left off the board" not in line and "could not read" not in line,
          "A: nothing left off the board", "the build line names no task left off",
          "printed %r" % line)
    pieces = {
        "reason prompt": 'id="rsnov"',
        "meeting chip": "chip meet",
        "meeting popover": "openMeetPop",
        "overdue chip": 'id="ovchip"',
        "snooze buttons": "data-snooze",
        "latest note": "lastq",
        "block grammar header": '"# Deck edits"',
        "stop conditions line": "pendGuide",
        "append line": '"+ append:"',
        "full-word chip label": 'meetChip:"meeting"',
        "cancelled colour": "--st-cx",
        "payload meetings": '"meetings": [',
        "payload statuses": '"taskStatuses"',
    }
    missing = [k for k, v in pieces.items() if v not in html]
    check(not missing, "A: the rendered page carries the new pieces",
          "%d pieces found" % len(pieces), "missing: %s" % ", ".join(missing))
    check("{{" not in html, "A: every placeholder filled", "no {{...}} left",
          "a placeholder survived: %s" % html[html.find("{{"):html.find("{{") + 30])
    parsed, why = script_parses(html)
    if parsed is None:
        ok("A: the page script parses", "skipped, " + why)
    else:
        check(parsed, "A: the page script parses", "node --check passed", why)


def check_vault_b(root, doctrine):
    vault = os.path.join(root, "vault-b")
    build_vault(vault, doctrine, vault_b_tasks())
    scan, setup, data, tasks = payload(vault)
    check(setup.get("taskStatuses") == ORIGINAL_FIVE,
          "B: a shipped section 8 offers the five original columns",
          "no cancelled column", "taskStatuses %r" % setup.get("taskStatuses"))
    check(all(t["meetings"] == [] and t["last"] is None for t in tasks.values()),
          "B: no meeting links, no dated lines, nothing derived",
          "every task has meetings [] and last null",
          "got %r" % {k: (t["meetings"], t["last"]) for k, t in tasks.items()})
    old_keys = {"id", "title", "status", "start", "due", "waiting_on", "priority"}
    extra = set().union(*(set(t) for t in tasks.values())) - old_keys
    check(extra == {"file", "meetings", "last"},
          "B: the task payload only gains the three new keys",
          "file, meetings, last", "extra keys %r" % sorted(extra))
    code, line, html = run_build(vault)
    check(code == 0 and line == "Command Deck rebuilt: 1 projects, 3 tasks, 4 notes scanned.",
          "B: the build line is the plain one", line, "exit %s, printed %r" % (code, line))

    # The same vault with one cancelled task: section 8 as shipped does not list
    # it, so it stays off the board and is reported, exactly as before.
    write(vault, PROJECT + "/Tasks/dropped.md", task("cancelled", "# Dropped\n"))
    scan, setup, data, tasks = payload(vault)
    check("dropped.md" not in tasks and len(scan.off_list) == 1,
          "B: cancelled stays off where section 8 does not list it",
          "reported, not drawn", "drawn %s, off_list %r" % ("dropped.md" in tasks, scan.off_list))
    code, line, html = run_build(vault)
    check("1 task(s) left off the board for a status section 8 does not list" in line,
          "B: and the build line says so", "the off-list line is printed", "printed %r" % line)


def check_template_clean():
    text = open(DECK_TEMPLATE, encoding="utf-8").read()
    py = open(os.path.join(SCRIPTS, "deck.py"), encoding="utf-8").read()
    cjk = [m.group(0) for m in re.finditer(r"[\u3000-\u9fff\uff00-\uffef]+", text + py)]
    check(not cjk, "product files carry no CJK text", "none in deck.py or the template",
          "found %r" % cjk[:5])
    leftovers = [w for w in ("DEMO", "demobar", "demo-try", "demo-reset", "mtg")
                 if re.search(r"\b%s\b" % re.escape(w), text + py)]
    check(not leftovers, "no demo leftovers", "no banner, demo buttons or abbreviated label",
          "found %r" % leftovers)


def main():
    for path in (DOCTRINE_TEMPLATE, DECK_TEMPLATE):
        if not os.path.isfile(path):
            print("FAIL - %s is not where this harness expects it" % path)
            return 2
    doctrine = open(DOCTRINE_TEMPLATE, encoding="utf-8").read()
    if doctrine.count(SHIPPED_TASK_LIST) != 1:
        print("FAIL - the shipped task status list is not written as %r in the "
              "doctrine template, so fixture A cannot add cancelled to it" % SHIPPED_TASK_LIST)
        return 1
    root = tempfile.mkdtemp(prefix="deck-accept-")
    try:
        check_vault_a(root, doctrine)
        check_vault_b(root, doctrine)
        check_template_clean()
    finally:
        shutil.rmtree(root, ignore_errors=True)

    for name, detail in passes:
        print("  PASS  %s  (%s)" % (name, detail))
    if failures:
        print("\nFAILURES: %d" % len(failures))
        for name, detail in failures:
            print("  FAIL  %s: %s" % (name, detail))
        return 1
    print("\nFAILURES: none")
    print("PASS - %d checks: the deck derives meetings, latest notes and cancelled "
          "from the vault, and a plain vault comes out plain." % len(passes))
    return 0


if __name__ == "__main__":
    sys.exit(main())
