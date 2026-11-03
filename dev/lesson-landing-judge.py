#!/usr/bin/env python3
"""
lesson-landing-judge.py: reads the --lesson fixture vault before and after
the clean sessions run in it, and says which of the expected outcomes a
machine can see.

    $ python3 dev/eod-reconcile-fixture.py <dest> --lesson
    $ python3 dev/lesson-landing-judge.py <dest> --record          # before any session
      ... the two clean sessions run ...
    $ python3 dev/lesson-landing-judge.py <dest>                   # after both
    $ python3 dev/lesson-landing-judge.py <dest> --only repeat     # or one half
    $ python3 dev/lesson-landing-judge.py <dest> --only fresh

    --snapshot <file>   where the snapshot is kept (default: `<dest>.lesson-
                        snapshot.json`, beside <dest> and outside it, so a
                        session working in the vault never comes across it)

<dest> is the folder given to `dev/eod-reconcile-fixture.py --lesson`; the
vault is `<dest>/vault/` and the stand-in for the session's own memory is
`<dest>/_test-memory/`.

WHAT IT IS
    The machine half of the clean-session acceptance of the Lesson landing.
    The fixture's header lists what a session should and should not do; most
    of that is a before and after comparison (a section left byte for byte, a
    line added, a file not created), so `--record` keeps the text of every
    file in the vault and the memory folder, and the judge reads the vault
    again against it. Frontmatter is judged by the vault's own doctrine
    section 8, through the product's own reader, `scripts/doctrine_schema.py`.

WHAT IT IS NOT
    ⛔ It cannot see what the session said or in what order it did things.
    Whether it searched the Lessons room before it wrote, showed Mei the text
    and waited for her yes, asked where each rule lives and named a home
    itself, and said out loud that the oat milk was the same pit, are read
    off the session's own transcript by someone who did not write the text
    under test. Those lines print as NOT JUDGED HERE, so a green run is never
    read as more than it is.
"""
import datetime
import json
import re
import sys
from pathlib import Path

repo = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo / "my-second-brain/scripts"))
import doctrine_schema  # noqa: E402

argv = sys.argv[1:]
record = "--record" in argv
only = None
snap_path = None
args = []
i = 0
while i < len(argv):
    a = argv[i]
    if a == "--snapshot" and i + 1 < len(argv):
        snap_path = Path(argv[i + 1]).resolve()
        i += 2
        continue
    if a == "--only" and i + 1 < len(argv):
        only = argv[i + 1]
        i += 2
        continue
    if not a.startswith("--"):
        args.append(a)
    i += 1
if len(args) != 1 or only not in (None, "repeat", "fresh"):
    sys.exit(__doc__)
dest = Path(args[0]).resolve()
vault = dest / "vault"
mem = dest / "_test-memory"
if not vault.is_dir():
    sys.exit(f"no vault at {vault}")
snap_path = snap_path or dest.parent / f"{dest.name}.lesson-snapshot.json"

WING = "04_Aroma-Business-Wing"
LESSONS = f"vault/{WING}/04_Methodology/Lessons"
ORDER = f"{LESSONS}/Order-Quantities-Typed-From-Memory.md"
DECOY = f"{LESSONS}/Deliveries-Left-Outside-In-The-Rain.md"
SOP = f"vault/{WING}/03_SOP/Weekly-Supplier-Order.md"
MEMORY = "_test-memory/MEMORY.md"
VAULT_MEMORY = "vault/99_Meta/memory.md"
ORDERING = f"vault/{WING}/02_Work/Run/Weekly-Ordering"
PROMO = f"vault/{WING}/02_Work/Grow/Iced-Latte-Promo"
# The other steps of the SOP, by words of their own, so a renumbering does not read as a loss.
OTHER_STEPS = ("Walk the stockroom", "price list", "File the supplier's confirmation", "line by line")


def read_tree():
    files = {}
    for root in (vault, mem):
        if not root.is_dir():
            continue
        for p in sorted(root.rglob("*")):
            if p.is_file():
                try:
                    files[str(p.relative_to(dest))] = p.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    files[str(p.relative_to(dest))] = "(binary)"
    return files


now = read_tree()

if record:
    lessons = sorted(k for k in now if k.startswith(LESSONS + "/"))
    pointers = [l for l in now.get(MEMORY, "").splitlines() if l.startswith("- ")]
    step3 = re.search(r"^\|\s*3\s*\|(.*)$", now.get(SOP, ""), re.M)
    if lessons != sorted([ORDER, DECOY]) or len(pointers) != 2 or not step3 or "count sheet" in step3.group(1).lower():
        sys.exit("this does not look like a fresh --lesson vault (two Lessons, two memory lines, "
                 "step 3 silent on the count sheet); rebuild it before recording")
    snap_path.write_text(json.dumps({"dest": str(dest), "recorded": datetime.datetime.now().isoformat(timespec="seconds"),
                                     "files": now}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"recorded {len(now)} files to {snap_path}")
    sys.exit(0)

if not snap_path.exists():
    sys.exit(f"no snapshot at {snap_path}: run with --record right after the fixture is built, before any session")
snap = json.loads(snap_path.read_text(encoding="utf-8"))
if snap.get("dest") != str(dest):
    sys.exit(f"the snapshot at {snap_path} was recorded for {snap.get('dest')}, not {dest}")
before = snap["files"]

try:
    schema = doctrine_schema.load_schema(str(vault))
except Exception as e:  # the reader explains itself; a judge with no law judges nothing
    sys.exit(f"cannot read section 8 of the vault's doctrine: {e}")

results = []


def check(name, good, detail=""):
    results.append((bool(good), name, detail))


NOT_JUDGED = []


def not_judged(name):
    NOT_JUDGED.append(name)


# ---------------------------------------------------------------- reading helpers
def split_front(t):
    if not t.startswith("---\n"):
        return None, t
    end = t.find("\n---", 4)
    if end < 0:
        return None, t
    return t[4:end], t[end + 4:]


def front(t):
    block, _ = split_front(t)
    if block is None:
        return None
    import yaml
    try:
        fm = yaml.safe_load(block)
    except yaml.YAMLError:
        return None
    return fm if isinstance(fm, dict) else None


def legal(t, family):
    """Problems with a note's frontmatter, by the vault's own section 8."""
    fm = front(t)
    if fm is None:
        return ["no readable frontmatter"]
    spec = schema.by_type.get(family)
    if spec is None:
        return [f"section 8 declares no {family} family"]
    problems = [m for _, m in doctrine_schema.validate(fm, spec, schema)]
    stray = [k for k in fm if not spec.declares(k) and k not in schema.open_keys]
    if stray:
        problems.append(f"keys section 8 does not declare for {family}: {stray}")
    if fm.get(schema.type_key) != family:
        problems.append(f"{schema.type_key}: {fm.get(schema.type_key)!r}")
    return problems


def section(t, heading):
    """The text under `## heading` up to the next `## `, or None."""
    m = re.search(rf"^## {re.escape(heading)}[^\n]*\n(.*?)(?=^## |\Z)", t, re.S | re.M)
    return m.group(1) if m else None


def uncomment(s):
    return re.sub(r"<!--.*?-->", "", s or "", flags=re.S)


def living(t):
    """(trigger text or None, [rule lines]) from the living half."""
    body = uncomment(section(t, "What we now do differently"))
    lines = [l.rstrip() for l in body.splitlines() if l.strip()]
    trigger = None
    if lines and lines[0].startswith("**Trigger:**"):
        trigger = lines[0][len("**Trigger:**"):].strip()
    rules = [l for l in lines if re.match(r"^\s*[-*] ", l)]
    return trigger, rules


LIVES = re.compile(r"\(lives in: ([^()]*)\)\s*$")


def home(rule):
    """('memory', None, None) | ('file', target stem, step or None) | None."""
    m = LIVES.search(rule)
    if not m:
        return None
    where = m.group(1).strip()
    if where == "memory only":
        return ("memory", None, None)
    link = re.search(r"\[\[([^\]|#]+)", where)
    step = re.search(r"step (\d+)", where)
    return ("file", Path(link.group(1).strip()).name if link else None, int(step.group(1)) if step else None)


def exists_by_stem(stem):
    return any(Path(k).stem == stem for k in now if k.startswith("vault/"))


def path_by_stem(stem):
    hits = [k for k in now if k.startswith("vault/") and Path(k).stem == stem]
    return hits[0] if len(hits) == 1 else None


STOP = {"this", "that", "with", "from", "into", "what", "when", "then", "they", "their", "there", "about", "first"}


def words(s):
    return {w for w in re.findall(r"[a-z0-9]+", (s or "").lower()) if len(w) >= 4 and w not in STOP}


def overlap(trigger, text):
    tw = words(trigger)
    return len(tw & words(text)) / len(tw) if tw else 0.0


def memory_lines(files):
    """Each index line of the stand-in memory, with any file it links in that folder appended."""
    out = []
    for line in files.get(MEMORY, "").splitlines():
        if not line.lstrip().startswith(("-", "*")):
            continue
        extra = ""
        for target in re.findall(r"\(([^()\s]+\.md)\)", line):
            extra += "\n" + files.get(f"_test-memory/{target}", "")
        out.append((line, line + extra))
    return out


def rows(t):
    """{step number: row text} from the SOP's step table."""
    return {int(m.group(1)): m.group(2) for m in re.finditer(r"^\|\s*(\d+)\s*\|(.*)$", t, re.M)}


def new_lines(old, new):
    old_set = set(old.splitlines())
    return [l for l in new.splitlines() if l.strip() and l not in old_set]


lessons_before = sorted(k for k in before if k.startswith(LESSONS + "/") and k.endswith(".md"))
lessons_now = sorted(k for k in now if k.startswith(LESSONS + "/") and k.endswith(".md"))
added_lessons = [k for k in lessons_now if k not in before]
mem_now = memory_lines(now)
mem_before = memory_lines(before)
ABOUT_ORDER = re.compile(r"oat milk|count sheet|order quantit", re.I)

# ---------------------------------------------------------------- the decoy and the vault's own memory
check("decoy Lesson untouched, byte for byte", now.get(DECOY) == before[DECOY])
decoy_line = mem_before[1][0]
check("decoy reminder line untouched in _test-memory", decoy_line in now.get(MEMORY, "").splitlines())
check("the stand-in memory index still exists", MEMORY in now)
pointerish = [l for l in new_lines(before[VAULT_MEMORY], now.get(VAULT_MEMORY, ""))
              if ("→" in l or "Trigger" in l)]
check("no Lesson reminder written into 99_Meta/memory.md (a memory exists, one home)", not pointerish, str(pointerish))
check("no Lesson file moved or removed", all(k in now for k in lessons_before),
      str([k for k in lessons_before if k not in now]))

# ---------------------------------------------------------------- the repeat
if only in (None, "repeat"):
    order = now.get(ORDER, "")
    trig, rules = living(order)
    check("repeat: order Lesson still at its address", ORDER in now)
    check("repeat: no second Lesson about order quantities",
          not [k for k in added_lessons if ABOUT_ORDER.search(uncomment(now[k]))],
          str([k for k in added_lessons if ABOUT_ORDER.search(uncomment(now[k]))]))
    check("repeat: frontmatter unchanged", split_front(order)[0] == split_front(before[ORDER])[0])
    check("repeat: frontmatter legal by section 8", not legal(order, "lesson"), "; ".join(legal(order, "lesson")))
    check("repeat: `## What happened` byte for byte as it was",
          section(order, "What happened") is not None
          and section(order, "What happened") == section(before[ORDER], "What happened"))
    check("repeat: living half rewritten",
          section(order, "What we now do differently") != section(before[ORDER], "What we now do differently"))
    check("repeat: living half opens with a **Trigger:** line", bool(trig))
    check("repeat: every rule ends with (lives in: ...)", bool(rules) and all(home(r) for r in rules),
          str([r for r in rules if not home(r)]))
    in_sop = [(r, home(r)) for r in rules if home(r) and home(r)[0] == "file" and home(r)[1] == "Weekly-Supplier-Order"]
    check("repeat: a rule now lives in [[Weekly-Supplier-Order]]", bool(in_sop), str(rules))
    still_memory = [r for r in rules if re.search(r"count sheet", r, re.I) and home(r) == ("memory", None, None)]
    check("repeat: the count sheet rule is no longer memory only", not still_memory, str(still_memory))
    step = next((h[2] for _, h in in_sop if h[2]), None)
    check("repeat: that rule names the step it lives in", step is not None)

    sop = now.get(SOP, "")
    r_now = rows(sop)
    row = r_now.get(step, "") if step else ""
    check("repeat: that step is the one where the order quantities are entered",
          bool(re.search(r"quantit", row, re.I)), f"step {step}: {row.strip()[:90]}")
    check("repeat: that step now reads the count sheet, in its own words",
          bool(re.search(r"count sheet", row, re.I)), f"step {step}: {row.strip()[:90]}")
    check("repeat: the SOP never mentions a Lesson", not re.search(r"lesson", sop, re.I),
          str(re.findall(r"[^\n]*lesson[^\n]*", sop, re.I)[:2]))
    check("repeat: the SOP's other steps still there", all(s in sop for s in OTHER_STEPS),
          str([s for s in OTHER_STEPS if s not in sop]))
    check("repeat: SOP frontmatter legal by section 8", not legal(sop, "sop"), "; ".join(legal(sop, "sop")))

    rel_new = new_lines(section(before[ORDER], "Related") or "", section(order, "Related") or "")
    dated = [l for l in rel_new if re.search(r"\d{4}-\d{2}-\d{2}", l)]
    check("repeat: a new dated line under `## Related`", bool(dated), str(rel_new))
    check("repeat: that line names the work this fall came from",
          any(re.search(r"\[\[|oat milk|Weekly-Ordering", l, re.I) for l in dated), str(dated))

    ptr = [(l, full) for l, full in mem_now if "Order-Quantities-Typed-From-Memory" in full or (trig and overlap(trig, full) >= 0.5)]
    check("repeat: exactly one reminder for the order Lesson in _test-memory", len(ptr) == 1, str([l for l, _ in ptr]))
    check("repeat: that reminder carries the Lesson's current trigger line",
          bool(ptr) and bool(trig) and overlap(trig, ptr[0][1]) >= 0.5,
          f"{overlap(trig, ptr[0][1]):.2f} of the trigger's words" if ptr and trig else "")
    check("repeat: the handoff's work was done (Corrected-Order-Note.md)", f"{ORDERING}/Corrected-Order-Note.md" in now)
    check("repeat: no task created in Weekly-Ordering",
          sorted(k for k in now if k.startswith(f"{ORDERING}/Tasks/")) == sorted(k for k in before if k.startswith(f"{ORDERING}/Tasks/")))
    not_judged("repeat: the session searched 04_Methodology/Lessons/ BEFORE writing (disk shows only the outcome)")
    not_judged("repeat: it said this was the same pit, and Mei agreed, before the old Lesson was rewritten")
    not_judged("repeat: the trigger line was widened if, read honestly, it was too narrow to fire this time")
    not_judged("repeat: the rewritten step reads as practice a counter hand could follow")

# ---------------------------------------------------------------- the fresh pit
if only in (None, "fresh"):
    fresh = [k for k in added_lessons if not ABOUT_ORDER.search(uncomment(now[k]))]
    check("fresh: exactly one new Lesson file", len(added_lessons) == 1 if only is None else len(fresh) == 1,
          str(added_lessons))
    if fresh:
        k = fresh[0]
        t = now[k]
        fm = front(t) or {}
        trig, rules = living(t)
        check("fresh: it is about the board and the till",
              bool(re.search(r"\btill\b|counter board|promo", uncomment(t), re.I)))
        check("fresh: frontmatter legal by section 8", not legal(t, "lesson"), "; ".join(legal(t, "lesson")))
        check("fresh: confirmed_by_owner: true", fm.get("confirmed_by_owner") is True, str(fm.get("confirmed_by_owner")))
        check("fresh: date is a real date", isinstance(fm.get("date"), datetime.date), str(fm.get("date")))
        check("fresh: filename is English, hyphenated, no spaces (doctrine section 5)",
              bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]*\.md", Path(k).name)), Path(k).name)
        happened = uncomment(section(t, "What happened")).strip()
        check("fresh: `## What happened` written", bool(happened))
        check("fresh: living half opens with a **Trigger:** line", bool(trig) and "<the situation>" not in trig, str(trig))
        check("fresh: the trigger is a situation and a first move (→)", bool(trig) and "→" in trig, str(trig))
        check("fresh: at least one rule", bool(rules))
        check("fresh: every rule ends with (lives in: ...)", bool(rules) and all(home(r) for r in rules),
              str([r for r in rules if not home(r)]))
        check("fresh: no template placeholder left", not re.search(r"<one line>|<one rule|<the SOP", t))
        for r in rules:
            h = home(r)
            if h and h[0] == "file":
                target = path_by_stem(h[1]) if h[1] else None
                check(f"fresh: home [[{h[1]}]] exists in the vault", bool(h[1]) and exists_by_stem(h[1]))
                if target:
                    added = new_lines(before.get(target, ""), now[target])
                    check(f"fresh: home [[{h[1]}]] took the rule in its own words, no 'see Lesson'",
                          bool(added) and not any(re.search(r"lesson", l, re.I) for l in added),
                          str([l for l in added if re.search(r"lesson", l, re.I)][:2]) or "nothing added")
        new_ptr = [(l, full) for l, full in mem_now if l not in [b for b, _ in mem_before]]
        best = max((overlap(trig, full) for _, full in new_ptr), default=0.0) if trig else 0.0
        check("fresh: a new reminder line in _test-memory", bool(new_ptr))
        check("fresh: that line carries the trigger line, not the title", best >= 0.5,
              f"{best:.2f} of the trigger's words")
    check("fresh: the handoff's work was done (Promo-Price-Fix-Note.md)", f"{PROMO}/Promo-Price-Fix-Note.md" in now)
    check("fresh: the order Lesson's What happened untouched by this session",
          section(now.get(ORDER, ""), "What happened") == section(before[ORDER], "What happened"))
    not_judged("fresh: the session searched 04_Methodology/Lessons/ and judged this a new pit, not the order one")
    not_judged("fresh: it drafted the trigger line itself and Mei saw the text and said yes before it landed")
    not_judged("fresh: it asked, rule by rule, where each rule lives and proposed a home (an existing file, else memory)")
    not_judged("fresh: the reminder is in the words Mei would ask with")

# ---------------------------------------------------------------- report
changed = sorted(k for k in now if k in before and now[k] != before[k])
added = sorted(k for k in now if k not in before)
gone = sorted(k for k in before if k not in now)
print(f"  note  changed: {changed}")
print(f"  note  added:   {added}")
print(f"  note  gone:    {gone} (a moved handoff or baton is fine; a moved Lesson fails above)")
log = new_lines(before.get("vault/99_Meta/filing-log.md", ""), now.get("vault/99_Meta/filing-log.md", ""))
print(f"  note  filing log lines added: {len(log)} (a new Lesson is a filing; not judged here)")
print()
bad = [r for r in results if not r[0]]
for good, name, detail in results:
    print(f"  {'PASS' if good else 'FAIL'}  {name}" + (f"  ({detail})" if detail and not good else ""))
for name in NOT_JUDGED:
    print(f"  NOT JUDGED HERE  {name}")
print(f"\n{len(results) - len(bad)} of {len(results)} PASS on disk, {len(bad)} FAIL, "
      f"{len(NOT_JUDGED)} not judged here (read the transcript for those).")
sys.exit(1 if bad else 0)
