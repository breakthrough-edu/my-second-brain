#!/usr/bin/env python3
"""
deck.py: the Command Deck generator.

WHAT IT IS
    Two subcommands over one vault:

      build   read the vault, render 02_Command-Base/Command-Deck.html
      doctor  read the vault, print the dark-cell case notes and fix nothing

    The deck is a GENERATED file. It holds zero hand-written state, every
    rebuild rewrites the whole thing, and nothing on the page is authoritative
    about anything: the vault is. That is the entire reason it may be
    overwritten without asking, and the reason a drag on the deck produces a
    proposal rather than a write (execution-backlog entry 46).

READ-ONLY ON THE VAULT, ALWAYS
    The one file this script writes is the deck itself, and it writes it
    ATOMICALLY: a temp file beside the target, then os.replace. A failed or
    half-finished run therefore leaves the PREVIOUS deck intact and honest,
    still carrying its own generation stamp, rather than a truncated page that
    looks current. Nothing else in the vault is ever touched, moved, renamed,
    or deleted. `doctor` writes nothing at all.

ZERO CONFIG FILE, ON PURPOSE
    There is no deck config to keep in sync with the vault, because the vault
    IS the config and it is re-derived on every run:

      wings    top-level folders (`03_Personal-Wing/`, `*-Business-Wing/`)
      lanes    the subfolders of a wing's `02_Work/`, ordered by doctrine
      brands   the `<Brand>-Brand-Assets/` folders under `01_Assets/`
      language `language:` in 99_Meta/bootstrap-progress.md

    A stored copy of any of those is a second thing to keep true, and the day
    it disagrees with the folders the deck starts lying quietly.

SHARED READING LAYER, NOT A SECOND DIALECT
    Frontmatter parsing and the markdown walk come from `checkup.py` by import,
    never re-implemented here. Two hand-rolled parsers over the same files are
    two dialects that grow their own bugs and eventually give two answers about
    one note. `checkup.py` judges whether a note is LEGAL; this file only asks
    whether it is FED. Those are different questions, which is why they are two
    commands, and the shared layer is where they must not differ.

    ⛔ Consequence worth stating: everything the deck reads is an OPTIONAL key
    in doctrine section 8 (`due`, `started`, `stage`, `priority`, `depends_on`).
    A project with none of them is perfectly legal, so the checker will never
    mention it and the frontmatter guard will never stop it. It is simply a dark
    row on the deck. `doctor` exists because that failure is in no other
    enforcement's jurisdiction, and it reports rather than repairs: the fix is a
    key in the owner's own file, which is the owner's call and the session's
    hands.

FAIL-SOFT IS THE CALLER'S CONTRACT
    This runs at the start of a session, so it must never be the thing that
    stops a morning brief. Exit codes: 0 built (or doctored), 2 could not run at
    all (no vault, no template). Any single unreadable note is counted and
    skipped, never fatal.

PYTHON ONLY, NO THIRD-PARTY IMPORTS
    Standard library only, so a machine with python3 can always run it. Unlike
    the schema reader this file does not need PyYAML: it reads a handful of
    scalar frontmatter keys, and `checkup.parse_frontmatter` already covers
    exactly that surface.
"""

import argparse
import datetime as _dt
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

try:
    from checkup import parse_frontmatter, iter_markdown_files, parse_date
except ImportError as exc:  # pragma: no cover - packaging accident, not a vault state
    sys.stderr.write(
        "deck.py could not import its reading layer from checkup.py (%s).\n"
        "Both files ship in the same scripts/ folder; a copy that separated them "
        "is the bug, not the vault.\n" % exc
    )
    sys.exit(2)


TEMPLATE_NAME = "deck-template.html"
DECK_RELPATH = os.path.join("02_Command-Base", "Command-Deck.html")
META_DIR = "99_Meta"
PROGRESS = "bootstrap-progress.md"

# Doctrine section 1 states the lane ladder in this order. Folders are the
# source of WHICH lanes exist; this list is only their reading order, and a lane
# folder the owner added that is not on it still ships, at the end.
LANE_ORDER = ["Deliver", "Grow", "Run", "Build"]

# Skipped for the same reason checkup skips them: templates are shapes, not
# records, and archive is retired. `99_Meta/Templates` in particular would
# otherwise put a `{{DATE}}` brief on the deck as a real project.
SKIP_DIRS = ["98_Archive", os.path.join("99_Meta", "Templates"),
             os.path.join("99_Meta", "memory-archive")]

PULSE_DAYS = 56  # eight weeks, the width of the sparkline in the template
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)")


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------

def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return None


def _fm_looks_broken(text):
    """True when a file opens a frontmatter block and never closes it.

    This is the one YAML failure the shared parser cannot report by itself: it
    returns {} both for "no frontmatter" and for "frontmatter that never ended",
    and only the second is a broken file. To the deck a broken file does not
    exist, which is the hardest kind of absence for an owner to notice on their
    own, so doctor names them.
    """
    if not text:
        return False
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return False
    for ln in lines[1:]:
        if ln.strip() == "---":
            return False
    return True


def _slug(name):
    return re.sub(r"[^A-Za-z0-9]+", "-", name).strip("-").lower()


def _int_or_none(v):
    try:
        return int(str(v).strip())
    except (TypeError, ValueError):
        return None


def _truthy(v):
    return str(v).strip().lower() in ("true", "yes", "1")


def _listify(v):
    if v in (None, ""):
        return []
    if isinstance(v, list):
        return [str(x).strip() for x in v if str(x).strip()]
    return [p.strip() for p in str(v).split(",") if p.strip()]


def _link_target(raw):
    """`[[_Acme-Rebrand-Brief]]` or `Acme Rebrand` -> a comparable key."""
    raw = str(raw).strip().strip("'\"")
    m = WIKILINK_RE.search(raw)
    if m:
        raw = m.group(1)
    raw = raw.strip().lstrip("_")
    raw = re.sub(r"-Brief$", "", raw, flags=re.IGNORECASE)
    return _slug(raw)


def _title_from(text, fallback):
    if text:
        for ln in text.splitlines():
            if ln.startswith("# "):
                return ln[2:].strip()
    return fallback


def _body_lines(text):
    """The note's lines with any frontmatter block removed."""
    lines = text.splitlines() if text else []
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return lines[i + 1:]
        return []          # never closed: there is no body to speak of
    return lines


def _first_body_line(text, fallback):
    if not text:
        return fallback
    lines = text.splitlines()
    i = 0
    if lines and lines[0].strip() == "---":
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            i += 1
        i += 1
    while i < len(lines):
        ln = lines[i].strip()
        if ln and not ln.startswith("<!--") and not ln.startswith("#"):
            return ln.lstrip("-* ").strip()
        if ln.startswith("# "):
            return ln[2:].strip()
        i += 1
    return fallback


def _pretty(name):
    return name.replace("-", " ").replace("_", " ").strip()


# --------------------------------------------------------------------------
# Vault shape (all derived, nothing stored)
# --------------------------------------------------------------------------

class VaultShape(object):
    __slots__ = ("root", "personal_wing", "business_wings", "brands", "lanes",
                 "language", "business_name", "business_slug")

    def __init__(self):
        self.root = None
        self.personal_wing = None
        self.business_wings = []
        self.brands = []
        self.lanes = []
        self.language = "en"
        self.business_name = ""
        self.business_slug = ""


def read_shape(vault):
    shape = VaultShape()
    shape.root = vault

    for entry in sorted(os.listdir(vault)):
        full = os.path.join(vault, entry)
        if not os.path.isdir(full):
            continue
        if entry.endswith("_Personal-Wing") or entry == "03_Personal-Wing":
            shape.personal_wing = entry
        elif entry.endswith("-Business-Wing"):
            shape.business_wings.append(entry)

    lanes = []
    for wing in shape.business_wings:
        work = os.path.join(vault, wing, "02_Work")
        if os.path.isdir(work):
            for lane in sorted(os.listdir(work)):
                if os.path.isdir(os.path.join(work, lane)) and lane not in lanes:
                    lanes.append(lane)
        assets = os.path.join(vault, wing, "01_Assets")
        if os.path.isdir(assets):
            for room in sorted(os.listdir(assets)):
                if room.endswith("-Brand-Assets") and os.path.isdir(os.path.join(assets, room)):
                    brand = room[: -len("-Brand-Assets")]
                    if brand not in shape.brands:
                        shape.brands.append(brand)
    ordered = [l for l in LANE_ORDER if l in lanes]
    ordered += [l for l in lanes if l not in LANE_ORDER]
    shape.lanes = ordered

    progress = os.path.join(vault, META_DIR, PROGRESS)
    fm = parse_frontmatter(_read(progress) or "")
    lang = str(fm.get("language", "")).strip().lower()
    shape.language = "zh" if lang.startswith("zh") or lang == "中文" else "en"
    shape.business_name = str(fm.get("business_name", "")).strip()
    shape.business_slug = str(fm.get("business_tag", "")).strip()
    if not shape.business_name and shape.business_wings:
        w = shape.business_wings[0]
        shape.business_name = _pretty(re.sub(r"^\d+_", "", w).replace("-Business-Wing", ""))
    return shape


# --------------------------------------------------------------------------
# Scan
# --------------------------------------------------------------------------

class Scan(object):
    def __init__(self):
        self.projects = []
        self.decisions = []
        self.renewals = []
        self.pulse = {"touched": 0, "days": [], "top": [], "silent": []}
        self.scanned = 0
        self.unreadable = []      # (relpath, why)
        self.notes = []           # doctor observations, (kind, subject, detail)


def _project_dirs(vault, shape):
    """Yield (wing_kind, lane_or_None, project_dir) for every project folder.

    A project folder is any folder directly under `Personal-Projects/` or under
    one lane of a business wing's `02_Work/`. Doctrine section 1: lanes hold
    projects, never loose materials.
    """
    if shape.personal_wing:
        pp = os.path.join(vault, shape.personal_wing, "Personal-Projects")
        if os.path.isdir(pp):
            for name in sorted(os.listdir(pp)):
                full = os.path.join(pp, name)
                if os.path.isdir(full) and not name.startswith("."):
                    yield ("personal", None, full)
    for wing in shape.business_wings:
        work = os.path.join(vault, wing, "02_Work")
        if not os.path.isdir(work):
            continue
        for lane in sorted(os.listdir(work)):
            lane_dir = os.path.join(work, lane)
            if not os.path.isdir(lane_dir):
                continue
            for name in sorted(os.listdir(lane_dir)):
                full = os.path.join(lane_dir, name)
                if os.path.isdir(full) and not name.startswith("."):
                    yield ("business", lane, full)


def _find_brief(project_dir):
    base = os.path.basename(project_dir)
    exact = os.path.join(project_dir, "_%s-Brief.md" % base)
    if os.path.isfile(exact):
        return exact
    for name in sorted(os.listdir(project_dir)):
        if name.startswith("_") and name.endswith("-Brief.md"):
            return os.path.join(project_dir, name)
    return None


def _read_tasks(scan, project_dir, vault):
    tasks = []
    tdir = os.path.join(project_dir, "Tasks")
    if not os.path.isdir(tdir):
        return tasks
    for name in sorted(os.listdir(tdir)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(tdir, name)
        text = _read(path)
        scan.scanned += 1
        rel = os.path.relpath(path, vault)
        if _fm_looks_broken(text):
            scan.unreadable.append((rel, "frontmatter block never closes"))
            continue
        fm = parse_frontmatter(text or "")
        if str(fm.get("cb", "")).strip() != "task":
            continue
        tasks.append({
            "id": "t-" + _slug(rel),
            "title": _title_from(text, _first_body_line(text, _pretty(name[:-3]))),
            "status": str(fm.get("status", "")).strip() or "not-started",
            "start": str(fm.get("start", "")).strip() or None,
            "due": str(fm.get("due", "")).strip() or None,
            "waiting_on": str(fm.get("waiting_on", "")).strip() or None,
            "priority": _int_or_none(fm.get("priority")),
            "_path": rel,
        })
    return tasks


def scan_vault(vault, shape):
    scan = Scan()

    # ---- projects -------------------------------------------------------
    for kind, lane, pdir in _project_dirs(vault, shape):
        name = _pretty(os.path.basename(pdir))
        brief = _find_brief(pdir)
        rel_dir = os.path.relpath(pdir, vault)
        fm = {}
        brief_broken = False
        if brief:
            text = _read(brief)
            scan.scanned += 1
            if _fm_looks_broken(text):
                brief_broken = True
                scan.unreadable.append((os.path.relpath(brief, vault),
                                        "frontmatter block never closes"))
                # The project still ships onto the deck, with every key at its
                # default. A project that silently vanished would be the one
                # failure an owner could never spot from the page itself.
                name = _title_from(text, name)
            else:
                fm = parse_frontmatter(text or "")
                name = _title_from(text, name)
        else:
            scan.notes.append(("no-brief", rel_dir,
                               "folder sits in a lane with no _<Project>-Brief.md, "
                               "so the deck cannot see it as a project at all"))
            continue

        tasks = _read_tasks(scan, pdir, vault)
        proj = {
            "id": "p-" + _slug(rel_dir),
            "name": name,
            "wing": kind,
            "lane": lane.lower() if lane else None,
            "brand": str(fm.get("brand", "")).strip() or None,
            "status": str(fm.get("status", "")).strip() or "active",
            "stage": str(fm.get("stage", "")).strip() or None,
            "started": str(fm.get("started", "")).strip() or None,
            "due": str(fm.get("due", "")).strip() or None,
            "priority": _int_or_none(fm.get("priority")),
            # A Brief may carry renew_by. It then belongs to What expires rather
            # than to Countdown, and the template routes it there (JW 2026-08-16).
            "renew_by": str(fm.get("renew_by", "")).strip() or None,
            "depends_on": [_link_target(x) for x in _listify(fm.get("depends_on"))],
            "hide_on_deck": _truthy(fm.get("hide_on_deck")),
            "tasks": tasks,
            "_path": os.path.relpath(brief, vault),
            "_key": _slug(os.path.basename(pdir)),
            "_broken": brief_broken,
        }
        scan.projects.append(proj)

    # depends_on carries names or brief links; the template wants ids.
    by_key = {}
    for p in scan.projects:
        by_key[p["_key"]] = p["id"]
        by_key[_slug(p["name"])] = p["id"]
    for p in scan.projects:
        resolved, missing = [], []
        for dep in p["depends_on"]:
            if dep in by_key and by_key[dep] != p["id"]:
                resolved.append(by_key[dep])
            else:
                missing.append(dep)
        p["depends_on"] = resolved
        if missing:
            scan.notes.append(("dep-unresolved", p["_path"],
                               "depends_on names nothing the deck can find: %s"
                               % ", ".join(missing)))

    # ---- decisions ------------------------------------------------------
    dec_dir = os.path.join(vault, "02_Command-Base", "Decisions")
    if os.path.isdir(dec_dir):
        for name in sorted(os.listdir(dec_dir)):
            if not name.endswith(".md"):
                continue
            path = os.path.join(dec_dir, name)
            text = _read(path)
            scan.scanned += 1
            rel = os.path.relpath(path, vault)
            if _fm_looks_broken(text):
                scan.unreadable.append((rel, "frontmatter block never closes"))
                continue
            fm = parse_frontmatter(text or "")
            if str(fm.get("cb", "")).strip() != "decision":
                continue
            scan.decisions.append({
                "date": str(fm.get("date", "")).strip(),
                "title": _title_from(text, _pretty(name[:-3])),
                "lane": str(fm.get("lane", "")).strip() or "",
                "domain": str(fm.get("domain", "")).strip() or "",
                "status": str(fm.get("status", "")).strip() or "active",
                "supersedes": str(fm.get("supersedes", "")).strip() or None,
                "_path": rel,
            })

    # ---- renewals (any family that carries renew_by) --------------------
    for path in iter_markdown_files(vault, SKIP_DIRS):
        text = _read(path)
        rel = os.path.relpath(path, vault)
        if _fm_looks_broken(text):
            if not any(r == rel for r, _ in scan.unreadable):
                scan.unreadable.append((rel, "frontmatter block never closes"))
            continue
        fm = parse_frontmatter(text or "")
        renew = str(fm.get("renew_by", "")).strip()
        if not renew:
            continue
        parts = rel.split(os.sep)
        room = parts[-2] if len(parts) >= 2 else ""
        wing = "personal"
        if parts and parts[0].endswith("-Business-Wing"):
            wing = "business"
        scan.renewals.append({
            "name": _title_from(text, _pretty(os.path.basename(path)[:-3])),
            "room": room,
            "wing": wing,
            "renew_by": renew,
            "_path": rel,
        })

    # ---- pulse (01_Daily backlinks) -------------------------------------
    scan.pulse = _read_pulse(vault, scan)
    return scan


def _read_pulse(vault, scan):
    today = _dt.date.today()
    days = [0] * PULSE_DAYS
    mentions = {}
    last_seen = {}
    daily = os.path.join(vault, "01_Daily")
    if os.path.isdir(daily):
        for name in sorted(os.listdir(daily)):
            if not name.endswith(".md"):
                continue
            d = parse_date(name[:-3])
            if not d:
                continue
            offset = (today - d).days
            text = _read(os.path.join(vault, "01_Daily", name)) or ""
            scan.scanned += 1
            # Journal lines only: "- something" in the BODY. ⛔ The frontmatter
            # delimiters are `---`, which starts with a dash, so a naive dash
            # test scores every daily note two lines it does not have and the
            # whole sparkline reads high.
            lines = [l for l in _body_lines(text)
                     if re.match(r"^\s*[-*]\s+\S", l)]
            if 0 <= offset < PULSE_DAYS:
                days[PULSE_DAYS - 1 - offset] = len(lines)
            for m in WIKILINK_RE.finditer(text):
                target = m.group(1).strip()
                key = _link_target(target)
                kind = "brief" if "Brief" in target else "guide"
                mentions[key] = mentions.get(key, 0) + 1
                if key not in last_seen or d > last_seen[key]:
                    last_seen[key] = d
                mentions.setdefault("_kind:" + key, kind)

    names = {}
    for p in scan.projects:
        names[p["_key"]] = p["name"]
        names[_slug(p["name"])] = p["name"]

    top = []
    for key, n in sorted(((k, v) for k, v in mentions.items() if not k.startswith("_kind:")),
                         key=lambda kv: -kv[1])[:5]:
        top.append({"name": names.get(key, _pretty(key)),
                    "kind": mentions.get("_kind:" + key, "brief"), "n": n})

    week_ago = today - _dt.timedelta(days=7)
    touched = 0
    silent = []
    for p in scan.projects:
        if p["status"] == "done" or p["hide_on_deck"]:
            continue
        seen = last_seen.get(p["_key"]) or last_seen.get(_slug(p["name"]))
        if seen and seen >= week_ago:
            touched += 1
        elif seen:
            silent.append({"name": p["name"], "days": (today - seen).days})
        else:
            silent.append({"name": p["name"], "days": None})
    silent = [s for s in silent if s["days"] is not None]
    silent.sort(key=lambda s: -s["days"])
    return {"touched": touched, "days": days, "top": top, "silent": silent[:4]}


# --------------------------------------------------------------------------
# Payload for the template
# --------------------------------------------------------------------------

def _strip_private(obj):
    if isinstance(obj, dict):
        return {k: _strip_private(v) for k, v in obj.items() if not k.startswith("_")}
    if isinstance(obj, list):
        return [_strip_private(x) for x in obj]
    return obj


def build_payload(shape, scan, now):
    wing = shape.business_wings[0] if shape.business_wings else ""
    setup = {
        "business": {
            "name": shape.business_name or _pretty(wing) or "Second Brain",
            "slug": shape.business_slug,
            "wing": wing,
        },
        "brands": list(shape.brands),
        "lanes": [l.lower() for l in shape.lanes],
        "personalWing": shape.personal_wing or "",
    }
    data = {
        "meta": {
            "generated": now.strftime("%Y-%m-%d %H:%M"),
            "generatedDate": now.strftime("%Y-%m-%d"),
            "scanned": scan.scanned,
            "briefs": len(scan.projects),
            "tasks": sum(len(p["tasks"]) for p in scan.projects),
            "unreadable": len(scan.unreadable),
        },
        "projects": _strip_private(scan.projects),
        "decisions": _strip_private(scan.decisions),
        "renewals": _strip_private(scan.renewals),
        "pulse": scan.pulse,
    }
    return setup, data


# --------------------------------------------------------------------------
# build
# --------------------------------------------------------------------------

def render(template_text, setup, data, shape, now):
    out = template_text
    out = out.replace("{{TODAY}}", now.strftime("%Y-%m-%d"))
    out = out.replace("{{THIS_MONTH}}", now.strftime("%Y-%m"))
    out = out.replace("{{LANG}}", shape.language)
    out = out.replace("{{SETUP_JSON}}", json.dumps(setup, ensure_ascii=False, indent=2))
    out = out.replace("{{DATA_JSON}}", json.dumps(data, ensure_ascii=False, indent=2))
    return out


def cmd_build(vault, args):
    template = os.path.join(_HERE, TEMPLATE_NAME)
    if not os.path.isfile(template):
        sys.stderr.write("deck.py: display template missing at %s\n" % template)
        return 2
    template_text = _read(template)
    if template_text is None:
        sys.stderr.write("deck.py: display template unreadable at %s\n" % template)
        return 2

    now = _dt.datetime.now()
    shape = read_shape(vault)
    scan = scan_vault(vault, shape)
    setup, data = build_payload(shape, scan, now)
    html = render(template_text, setup, data, shape, now)

    target = os.path.join(vault, DECK_RELPATH)
    parent = os.path.dirname(target)
    if not os.path.isdir(parent):
        sys.stderr.write("deck.py: %s does not exist in this vault\n"
                         % os.path.dirname(DECK_RELPATH))
        return 2

    # Atomic: a failed write leaves the previous deck standing, stamp and all.
    tmp = target + ".tmp-%d" % os.getpid()
    try:
        with open(tmp, "w", encoding="utf-8") as fh:
            fh.write(html)
        os.replace(tmp, target)
    except OSError as exc:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        sys.stderr.write("deck.py: could not write the deck (%s)\n" % exc)
        return 2

    if args.json:
        print(json.dumps({"deck": DECK_RELPATH, "generated": data["meta"]["generated"],
                          "scanned": scan.scanned, "briefs": data["meta"]["briefs"],
                          "tasks": data["meta"]["tasks"],
                          "unreadable": len(scan.unreadable)}, ensure_ascii=False))
        return 0

    line = "Command Deck rebuilt: %d projects, %d tasks, %d notes scanned." % (
        data["meta"]["briefs"], data["meta"]["tasks"], scan.scanned)
    if scan.unreadable:
        line += " %d file(s) the deck could not read (run `deck.py doctor`)." % len(scan.unreadable)
    print(line)
    return 0


# --------------------------------------------------------------------------
# doctor
# --------------------------------------------------------------------------

def _dark_cells(scan, shape):
    """One row per dark cell: which cell, why, which key lights it.

    Every rule below is about an OPTIONAL key. Nothing here is a violation and
    nothing here should make anybody blush; the checker's findings are the ones
    that should.
    """
    out = []
    projects = [p for p in scan.projects
                if p["status"] != "done" and not p["hide_on_deck"]]

    # JW 2026-08-16: `due` with no `started` is a MILESTONE (a diamond on the
    # swimlane, and the only thing Countdown holds). `started` with `due` is a
    # runway (a bar). Both are complete shapes, so neither is dark. What IS dark
    # is a project carrying neither: it is not a point and not a span, and the
    # swimlane has to invent both edges to draw it at all.
    for p in projects:
        if p.get("_broken"):
            # One cause, not eight symptoms. Every key on this project reads as
            # missing because none of them can be read at all, and listing each
            # cell separately would bury the one fix under its own consequences.
            out.append({"cell": "Everything on this project", "subject": p["name"],
                        "path": p["_path"],
                        "why": "its Brief opens a frontmatter block and never closes it, so "
                               "the deck reads no keys from it and draws it at every default",
                        "fix": "close the frontmatter with a --- line; the other cells will "
                               "report themselves once it parses"})
            continue
        if not p["due"] and not p["started"]:
            out.append({"cell": "The whole timeline", "subject": p["name"],
                        "path": p["_path"],
                        "why": "the Brief carries neither started nor due, so this project is "
                               "neither a milestone (a diamond) nor a runway (a bar) and the "
                               "swimlane leaves it off entirely. It is still on the kanban, the "
                               "grid and the health ring",
                        "fix": "due: YYYY-MM-DD alone if it is a deadline, or started: plus due: "
                               "if it is a stretch of work"})
        if p["priority"] is None:
            out.append({"cell": "Top Priority", "subject": p["name"], "path": p["_path"],
                        "why": "no priority, so its open tasks can never reach the priority 1 and 2 list",
                        "fix": "priority: 1 to 5 in the Brief"})
        if p["renew_by"]:
            out.append({"cell": "The whole timeline", "subject": p["name"], "path": p["_path"],
                        "why": "its Brief carries renew_by, which is the expiry key and belongs "
                               "to What expires and nothing else. Section 8 declares that key on "
                               "the entity family, not on brief, so the deck shows this project "
                               "only under What expires and leaves it off the swimlane and "
                               "Countdown entirely",
                        "fix": "move renew_by onto the entity note that owns the expiring thing "
                               "(the licence, the lease, the policy) and leave the Brief to the "
                               "work: started, due, stage, priority"})
        if p["due"] and not p["started"] and any(t["start"] or t["due"] for t in p["tasks"]):
            out.append({"cell": "Swimlane shape", "subject": p["name"], "path": p["_path"],
                        "why": "it reads as a milestone (due, no started) so the swimlane draws a "
                               "diamond, yet its tasks carry dates that stretch out beside it. If "
                               "it is really a stretch of work, it is drawn as a point",
                        "fix": "started: YYYY-MM-DD in the Brief turns it into a bar; leaving it "
                               "out is legal and keeps the diamond"})
        if not p["stage"]:
            out.append({"cell": "Kanban by stage", "subject": p["name"], "path": p["_path"],
                        "why": "no stage, so it lands in the No stage yet column",
                        "fix": "stage: pending / planning / pursuing / executing / closed "
                               "(legal to leave unset; doctrine section 1 only expects it on client work)"})
        if not p["tasks"]:
            out.append({"cell": "Every task view", "subject": p["name"], "path": p["_path"],
                        "why": "the project has no Tasks/ notes, so nothing of it appears in "
                               "kanban, grid or the health ring",
                        "fix": "one cb: task note in <Project>/Tasks/"})
        for t in p["tasks"]:
            if not t["due"]:
                out.append({"cell": "Calendar", "subject": "%s / %s" % (p["name"], t["title"]),
                            "path": t["_path"],
                            "why": "the task carries no due date, so it never lands on a day",
                            "fix": "due: YYYY-MM-DD in the task note"})
            if t["status"] == "waiting" and not t["waiting_on"]:
                out.append({"cell": "Waiting on", "subject": "%s / %s" % (p["name"], t["title"]),
                            "path": t["_path"],
                            "why": "status is waiting but nothing names who or what is being waited on",
                            "fix": "waiting_on: <person or thing> in the task note"})

    if projects and not any(p["depends_on"] for p in projects):
        out.append({"cell": "Dependency arrows", "subject": "(vault-wide)", "path": None,
                    "why": "no Brief carries depends_on, so the swimlane view draws no arrows",
                    "fix": "depends_on: [<other project>] in a Brief that really waits on another"})
    if not scan.decisions:
        out.append({"cell": "Standing rules", "subject": "(vault-wide)", "path": None,
                    "why": "no cb: decision notes yet, so the sidebar's rulebook is empty",
                    "fix": "say \"log a decision\" once and the panel fills itself"})
    if not scan.renewals:
        out.append({"cell": "What expires", "subject": "(vault-wide)", "path": None,
                    "why": "nothing in the vault carries renew_by",
                    "fix": "renew_by: YYYY-MM-DD on any document that expires"})
    if not any(scan.pulse["days"]):
        out.append({"cell": "What is moving", "subject": "(vault-wide)", "path": None,
                    "why": "no daily notes in the last %d days, so the pulse has nothing to plot" % PULSE_DAYS,
                    "fix": "say \"compile\" at the end of a day"})
    return out


def cmd_doctor(vault, args):
    template = os.path.join(_HERE, TEMPLATE_NAME)
    blockers = []
    if not os.path.isfile(template):
        blockers.append("display template missing at %s" % template)
    if not os.path.isdir(os.path.join(vault, "02_Command-Base")):
        blockers.append("02_Command-Base/ does not exist in this vault, "
                        "so there is nowhere to write the deck")

    shape = read_shape(vault)
    scan = scan_vault(vault, shape)
    dark = _dark_cells(scan, shape)
    deck_path = os.path.join(vault, DECK_RELPATH)
    stamp = None
    if os.path.isfile(deck_path):
        stamp = _dt.date.fromtimestamp(os.path.getmtime(deck_path)).isoformat()

    if args.json:
        print(json.dumps({
            "blockers": blockers,
            "unreadable": [{"path": p, "why": w} for p, w in scan.unreadable],
            "dark": dark,
            "deck_exists": os.path.isfile(deck_path),
            "deck_stamp": stamp,
            "projects": len(scan.projects),
            "no_brief": [{"path": s, "why": d} for k, s, d in scan.notes if k == "no-brief"],
        }, ensure_ascii=False, indent=2))
        return 0

    print("Command Deck doctor: %s" % vault)
    print("")

    print("1 · Can it run")
    if blockers:
        for b in blockers:
            print("   BLOCKED  %s" % b)
    else:
        print("   ok       generator, template and 02_Command-Base/ are all in place")
        print("   deck     %s" % ("%s, stamped %s" % (DECK_RELPATH, stamp)
                                  if stamp else "not built yet"))
    print("")

    print("2 · Can it read")
    if scan.unreadable:
        print("   %d file(s) whose frontmatter the deck cannot read. Every key in them is"
              % len(scan.unreadable))
        print("   invisible to it (a task note like this does not reach the deck at all;")
        print("   a Brief still ships its project, drawn at every default):")
        for path, why in scan.unreadable:
            print("   - %s  (%s)" % (path, why))
    else:
        print("   ok       every note scanned parsed cleanly (%d scanned)" % scan.scanned)
    for kind, subject, detail in scan.notes:
        if kind == "no-brief":
            print("   - %s  (%s)" % (subject, detail))
    print("")

    print("3 · Dark cells")
    if not dark:
        print("   Nothing dark. Every panel has something to draw.")
    else:
        by_cell = {}
        for row in dark:
            by_cell.setdefault(row["cell"], []).append(row)
        for cell in by_cell:
            rows = by_cell[cell]
            print("   %s (%d)" % (cell, len(rows)))
            for row in rows:
                print("     · %s" % row["subject"])
                print("       why: %s" % row["why"])
                print("       fix: %s" % row["fix"])
                if row["path"]:
                    print("       in : %s" % row["path"])
        print("")
        print("   Nothing above is a law the vault broke. Every key named here is OPTIONAL in")
        print("   doctrine section 8, which is exactly why no other check mentions them; an")
        print("   unparseable file is the one exception, and it is a typo rather than a ruling.")
        print("   This report proposes; it changes nothing.")
    return 0


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="deck.py",
        description="Build the Command Deck from a My Second Brain vault, or "
                    "diagnose why part of it is dark.")
    ap.add_argument("command", choices=["build", "doctor"])
    ap.add_argument("vault", help="path to the vault root")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)

    vault = os.path.abspath(os.path.expanduser(args.vault))
    if not os.path.isdir(vault):
        sys.stderr.write("deck.py: no such vault: %s\n" % vault)
        return 2

    if args.command == "build":
        return cmd_build(vault, args)
    return cmd_doctor(vault, args)


if __name__ == "__main__":
    sys.exit(main())
