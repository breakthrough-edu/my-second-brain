#!/usr/bin/env python3
"""
checkup.py: the machine-enforcement counterpart to the human Distill/Tidy pass.

WHAT IT IS
    A read-only vault linter. It inspects a My Second Brain vault and prints a
    report grouped by severity. It is the mechanical half of the weekly Tidy
    ritual (modes/distill.md, Half 1): the checks a script can run every time,
    so the human distill can spend its attention on judgment instead of hygiene.

READ-ONLY, ALWAYS
    This script NEVER modifies, moves, renames, or deletes anything in any
    vault. It opens files for reading only. There is not a single write to the
    target vault anywhere in this file. It reports; the owner (or the Distill
    mode) decides what to fix.

PUBLIC, GENERIC BY DESIGN
    This ships in a public skill, so it hardcodes no single owner's private
    conventions (no private folder names, client names, or private frontmatter
    schema). It ships sensible generic defaults drawn from the skill's own
    documented structure (references/scaffold-spec.md, templates/), and reads
    every vault-specific specific (room whitelist, required meta files, record
    schema, tag vocabulary, staleness thresholds) from config at runtime:

      1. An explicit --config PATH (JSON), if given.
      2. An auto-discovered `.checkup.json` at the vault root or in `99_Meta/`.
      3. Parsed from the vault's own control files where possible
         (tag vocabulary from `99_Meta/tagging-vocabulary.md`, staleness dates
         from `99_Meta/maintenance-state.md`).
      4. Generic built-in defaults.

    Every check degrades gracefully: if the config or file it needs is absent,
    it skips with a note instead of crashing.

USAGE
    python3 checkup.py /path/to/vault
    python3 checkup.py /path/to/vault --config my-checkup.json
    python3 checkup.py /path/to/vault --json

    Exit code is 0 even when problems are found (report-only). It is non-zero
    only when the vault itself cannot be read (bad path).

Python 3 standard library only.
"""

import argparse
import datetime as _dt
import json
import os
import re
import sys

# --------------------------------------------------------------------------
# Generic built-in defaults. NONE of these are private to any one owner; they
# come straight from the skill's documented scaffold (references/scaffold-spec.md).
# Every one of them is overridable by config read from inside the target vault.
# --------------------------------------------------------------------------
DEFAULTS = {
    # A top-level entry is an expected "room" if its name matches this pattern
    # (the numbered-room convention: 00_Inbox, 01_Daily, ... 99_Meta, plus the
    # 04_/05_ business wings). Anything else at the top level is surfaced.
    "room_pattern": r"^\d{2}_[A-Za-z]",
    # Extra top-level names that are allowed even though they do not match the
    # room pattern. Default covers the one file the scaffold writes to root.
    "allowed_rooms": ["CLAUDE.md"],
    # Top-level entries never worth reporting (tool/OS clutter).
    "ignore": [".git", ".obsidian", ".trash", ".DS_Store", ".gitignore",
               ".stfolder", ".stversions"],
    # The system control area and the files the scaffold guarantees live in it.
    "meta_dir": "99_Meta",
    "required_meta_files": [
        "structure-doctrine.md",
        "filing-log.md",
        "maintenance-state.md",
        "tagging-vocabulary.md",
    ],
    # Record-schema (the "cb:" frontmatter contract). Marker is the frontmatter
    # key that flags a governed record. `types` maps each marker VALUE to its
    # required keys.
    #
    # SOURCE OF TRUTH: section 8 of structure-doctrine.md inside the vault, and
    # nowhere else. Whatever this checker reads is DERIVED from that section; it
    # is never a second list maintained by hand. A vault may extend it through
    # .checkup.json (private families the public product knows nothing about),
    # but it may not contradict it.
    #
    # The shipped families are NOT optional. Every vault this product builds is
    # born with guide / brief / menu / entity / record / process / hypothesis /
    # lab / ritual / resources / brand-strategy already in it, so "the public
    # default enforces nothing" (the old posture here, correct back when section
    # 8 was only a table of precedents) would mean shipping structure with no
    # enforcement behind it at all.
    #
    # NOT YET IMPLEMENTED: reading section 8 directly. Until that lands, this
    # default stays empty rather than hardcoding a copy of the schema, because a
    # hardcoded copy is exactly the drift this comment exists to prevent.
    "record_schema": {"marker": "cb", "types": {}},
    # Tag vocabulary: the markdown file the whitelist is parsed from, relative
    # to meta_dir. An explicit `tag_vocabulary` list in config overrides parsing.
    "tag_vocabulary_file": "tagging-vocabulary.md",
    # Also scan note BODIES for inline #tags, not just frontmatter `tags:`.
    # Inline scanning is inherently noisier; set False to check frontmatter only.
    "scan_inline_tags": True,
    # Dirs whose notes are skipped when scanning for tags / schema (archive and
    # template shapes are not live content).
    "scan_skip_dirs": ["98_Archive", "99_Meta/Templates", "99_Meta/memory-archive"],
    # Freshness. Fields read from maintenance-state.md frontmatter, and the day
    # threshold past which each is called stale. If the file carries its own
    # `cadence_days`, that wins over staleness_days for the maintenance fields.
    "freshness_fields": ["last_tidy", "last_distill"],
    "staleness_days": 7,
    "filing_log_file": "filing-log.md",
    "filing_log_stale_days": 14,
    # Safety-lock (the optional rm -rf delete-guard installed by Setup Step 6.8).
    # Informational only. Matched by this substring in a PreToolUse Bash hook
    # command in ~/.claude/settings.json. macOS-only, like the guard itself.
    "safety_lock_check": True,
    "safety_lock_marker": "rm-guard",
}

# Severity ordering for grouping/printing.
ERROR, WARN, INFO = "ERROR", "WARN", "INFO"
_SEV_ORDER = {ERROR: 0, WARN: 1, INFO: 2}


class Finding:
    __slots__ = ("severity", "check", "message", "path")

    def __init__(self, severity, check, message, path=None):
        self.severity = severity
        self.check = check
        self.message = message
        self.path = path

    def as_dict(self):
        d = {"severity": self.severity, "check": self.check, "message": self.message}
        if self.path:
            d["path"] = self.path
        return d


# --------------------------------------------------------------------------
# Small helpers (all read-only)
# --------------------------------------------------------------------------
_FM_DELIM = re.compile(r"^---\s*$")
_DATE_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
# backtick-wrapped hashtag, e.g. `#marketing`, as used in vocabulary tables
_VOCAB_TAG_RE = re.compile(r"`#([A-Za-z0-9][A-Za-z0-9/_-]*)`")
# an inline tag in note bodies: start-of-line or space/paren before '#', then a
# tag that must start with a LOWERCASE letter. Lowercase-hyphen is the tag
# format both the public template and the doctrine mandate, so this restriction
# is generic (not private) and it drops the common false positives: markdown
# headings ('# ' has a space), hex colors (#FF6600), and C#/PascalCase anchors.
_INLINE_TAG_RE = re.compile(r"(?:^|[\s(\[])#([a-z][a-z0-9/_-]*)")
# Inline code spans (`...`) and markdown link targets (](url)) are stripped
# before inline-tag scanning: both routinely carry a '#' that is NOT a tag,
# e.g. a lowercase hex color `#e60012` or a table-of-contents anchor link
# [Section](#section-anchor). Both are generic markdown, not private to any vault.
_INLINE_CODE_RE = re.compile(r"`[^`]*`")
_MD_LINK_TARGET_RE = re.compile(r"\]\([^)]*\)")
# A lowercase hex color the tag regex would otherwise accept (#c1272d). Requiring
# a digit keeps real 3/6-letter words (deface, facade) from being dropped.
_HEX_COLOR_RE = re.compile(r"[0-9a-f]{3}(?:[0-9a-f]{3})?$")


def _read_text(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except (OSError, UnicodeError):
        return None


def parse_frontmatter(text):
    """Minimal, dependency-free YAML-frontmatter reader.

    Returns a dict of top-level keys. Values are strings, or lists for inline
    (`[a, b]`) and block (`- a`) sequences. Enough for lint purposes: we only
    ever check key presence, simple scalars, and the `tags` list.
    """
    if not text:
        return {}
    lines = text.splitlines()
    if not lines or not _FM_DELIM.match(lines[0]):
        return {}
    fm = {}
    key = None
    for raw in lines[1:]:
        if _FM_DELIM.match(raw):
            break
        # block-list continuation: "  - value"
        m = re.match(r"^\s*-\s+(.*)$", raw)
        if m and key is not None:
            fm.setdefault(key, [])
            if not isinstance(fm[key], list):
                fm[key] = []
            fm[key].append(m.group(1).strip().strip("'\""))
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", raw)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if val == "":
            fm[key] = ""  # may be filled by following block list
        elif val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            fm[key] = [p.strip().strip("'\"") for p in inner.split(",") if p.strip()] if inner else []
        else:
            fm[key] = val.strip("'\"")
    return fm


def strip_code_and_frontmatter(text):
    """Remove YAML frontmatter, fenced code blocks, inline code spans, and
    markdown link targets so inline-tag scanning does not trip over a `#` that
    is not a tag: code, hex colors, or table-of-contents anchor links."""
    lines = text.splitlines()
    out = []
    i = 0
    n = len(lines)
    if lines and _FM_DELIM.match(lines[0]):
        i = 1
        while i < n and not _FM_DELIM.match(lines[i]):
            i += 1
        i += 1  # skip closing delimiter
    in_fence = False
    while i < n:
        ln = lines[i]
        if ln.lstrip().startswith("```") or ln.lstrip().startswith("~~~"):
            in_fence = not in_fence
            i += 1
            continue
        if not in_fence:
            # drop inline code spans and markdown link targets so a '#' inside
            # them (hex color, TOC anchor) is not later mistaken for a tag
            ln = _INLINE_CODE_RE.sub(" ", ln)
            ln = _MD_LINK_TARGET_RE.sub("]", ln)
            out.append(ln)
        i += 1
    return "\n".join(out)


def iter_markdown_files(vault, skip_dirs):
    """Yield absolute paths to .md files, skipping configured dirs and dotdirs."""
    skip_abs = {os.path.normpath(os.path.join(vault, d)) for d in skip_dirs}
    for root, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        # prune configured skip dirs
        pruned = []
        for d in dirs:
            full = os.path.normpath(os.path.join(root, d))
            if full in skip_abs:
                continue
            pruned.append(d)
        dirs[:] = pruned
        for f in files:
            if f.endswith(".md"):
                yield os.path.join(root, f)


def today():
    return _dt.date.today()


def parse_date(s):
    if not s:
        return None
    m = _DATE_RE.search(str(s))
    if not m:
        return None
    try:
        return _dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


# --------------------------------------------------------------------------
# Config resolution
# --------------------------------------------------------------------------
def load_config(vault, explicit_path):
    """Layer config over defaults. Returns (config, source_note)."""
    cfg = dict(DEFAULTS)
    source = "built-in generic defaults"
    candidate = None
    if explicit_path:
        candidate = explicit_path
    else:
        for rel in (".checkup.json", os.path.join(DEFAULTS["meta_dir"], ".checkup.json")):
            p = os.path.join(vault, rel)
            if os.path.isfile(p):
                candidate = p
                break
    if candidate and os.path.isfile(candidate):
        raw = _read_text(candidate)
        try:
            user = json.loads(raw) if raw else {}
            cfg.update(user)
            # deep-merge record_schema so a partial override keeps the marker
            if "record_schema" in user:
                merged = dict(DEFAULTS["record_schema"])
                merged.update(user["record_schema"])
                cfg["record_schema"] = merged
            source = "config file: " + candidate
        except (ValueError, TypeError) as e:
            source = "built-in defaults (config at %s failed to parse: %s)" % (candidate, e)
    return cfg, source


# --------------------------------------------------------------------------
# Checks. Each returns (list[Finding], note_str_or_None). A note means the
# check was skipped or partially ran; it is surfaced in the report.
# --------------------------------------------------------------------------
def check_rooms(vault, cfg):
    findings = []
    try:
        entries = sorted(os.listdir(vault))
    except OSError as e:
        return findings, "could not list vault root: %s" % e
    pattern = re.compile(cfg.get("room_pattern", DEFAULTS["room_pattern"]))
    allowed = set(cfg.get("allowed_rooms", []))
    ignore = set(cfg.get("ignore", []))
    for name in entries:
        if name in ignore or name.startswith("."):
            continue
        if name in allowed or pattern.match(name):
            continue
        full = os.path.join(vault, name)
        kind = "folder" if os.path.isdir(full) else "file"
        sev = WARN if os.path.isdir(full) else INFO
        findings.append(Finding(
            sev, "rooms",
            "unexpected top-level %s outside the numbered-room structure: %s" % (kind, name),
            name))
    return findings, None


def check_required_meta(vault, cfg):
    findings = []
    meta_dir = cfg.get("meta_dir", DEFAULTS["meta_dir"])
    meta_abs = os.path.join(vault, meta_dir)
    if not os.path.isdir(meta_abs):
        return findings, "meta dir '%s' not found; skipped required-file check" % meta_dir
    required = cfg.get("required_meta_files", DEFAULTS["required_meta_files"])
    for fname in required:
        if not os.path.isfile(os.path.join(meta_abs, fname)):
            findings.append(Finding(
                ERROR, "meta-files",
                "required control file missing: %s/%s" % (meta_dir, fname),
                "%s/%s" % (meta_dir, fname)))
    return findings, None


def check_record_schema(vault, cfg):
    findings = []
    schema = cfg.get("record_schema", DEFAULTS["record_schema"]) or {}
    marker = schema.get("marker", "cb")
    types = schema.get("types", {}) or {}
    skip = cfg.get("scan_skip_dirs", DEFAULTS["scan_skip_dirs"])
    marked = 0
    for path in iter_markdown_files(vault, skip):
        text = _read_text(path)
        if text is None:
            continue
        fm = parse_frontmatter(text)
        if marker not in fm:
            continue
        marked += 1
        rel = os.path.relpath(path, vault)
        mval = fm.get(marker)
        if not mval:
            findings.append(Finding(
                WARN, "record-schema",
                "record has empty '%s:' marker" % marker, rel))
            continue
        if not types:
            continue  # presence-only mode; nothing private to enforce
        required = types.get(mval)
        if required is None:
            findings.append(Finding(
                WARN, "record-schema",
                "'%s: %s' is not a configured record type" % (marker, mval), rel))
            continue
        missing = [k for k in required if k not in fm or fm.get(k) in ("", None, [])]
        if missing:
            findings.append(Finding(
                ERROR, "record-schema",
                "'%s: %s' record missing required key(s): %s" % (marker, mval, ", ".join(missing)),
                rel))
    if marked == 0:
        return findings, "no '%s:' records found; schema check idle" % marker
    if not types:
        return findings, ("record_schema.types not configured: ran marker-presence "
                          "check on %d '%s:' record(s), no required-key enforcement" % (marked, marker))
    return findings, None


def load_tag_vocabulary(vault, cfg):
    """Return (set_of_tags, source_note_or_None)."""
    explicit = cfg.get("tag_vocabulary")
    if explicit:
        return set(t.lstrip("#") for t in explicit), "explicit list in config"
    meta_dir = cfg.get("meta_dir", DEFAULTS["meta_dir"])
    fname = cfg.get("tag_vocabulary_file", DEFAULTS["tag_vocabulary_file"])
    path = os.path.join(vault, meta_dir, fname)
    text = _read_text(path)
    if text is None:
        return None, "vocabulary file %s/%s not found" % (meta_dir, fname)
    tags = set(m.lower() for m in _VOCAB_TAG_RE.findall(text))
    if not tags:
        return None, "no `#tag` entries parsed from %s/%s" % (meta_dir, fname)
    return tags, None


def check_tags(vault, cfg):
    vocab, note = load_tag_vocabulary(vault, cfg)
    if vocab is None:
        return [], "tag check skipped: " + note
    skip = cfg.get("scan_skip_dirs", DEFAULTS["scan_skip_dirs"])
    offenders = {}  # tag -> first path
    counts = {}
    for path in iter_markdown_files(vault, skip):
        text = _read_text(path)
        if text is None:
            continue
        rel = os.path.relpath(path, vault)
        found = set()
        fm = parse_frontmatter(text)
        fmtags = fm.get("tags")
        if isinstance(fmtags, list):
            for t in fmtags:
                found.add(str(t).lstrip("#").lower())
        elif isinstance(fmtags, str) and fmtags:
            for t in re.split(r"[,\s]+", fmtags):
                if t:
                    found.add(t.lstrip("#").lower())
        if cfg.get("scan_inline_tags", DEFAULTS["scan_inline_tags"]):
            body = strip_code_and_frontmatter(text)
            for m in _INLINE_TAG_RE.findall(body):
                if _HEX_COLOR_RE.match(m) and any(c.isdigit() for c in m):
                    continue  # a hex color, not a tag
                found.add(m.lower())
        for t in found:
            if t not in vocab:
                counts[t] = counts.get(t, 0) + 1
                offenders.setdefault(t, rel)
    findings = []
    for t in sorted(offenders, key=lambda x: (-counts[x], x)):
        findings.append(Finding(
            WARN, "tags",
            "off-vocabulary tag #%s (used in %d note(s), e.g. %s)" % (t, counts[t], offenders[t]),
            offenders[t]))
    return findings, ("checked against %d vocabulary tag(s)" % len(vocab))


def check_freshness(vault, cfg):
    findings = []
    meta_dir = cfg.get("meta_dir", DEFAULTS["meta_dir"])
    # maintenance-state.md
    ms_path = os.path.join(vault, meta_dir, "maintenance-state.md")
    ms_text = _read_text(ms_path)
    note = None
    if ms_text is None:
        note = "maintenance-state.md not found; skipped maintenance freshness"
    else:
        fm = parse_frontmatter(ms_text)
        cadence = None
        try:
            cadence = int(str(fm.get("cadence_days")).strip()) if fm.get("cadence_days") else None
        except (ValueError, TypeError):
            cadence = None
        threshold = cadence if cadence else cfg.get("staleness_days", DEFAULTS["staleness_days"])
        for field in cfg.get("freshness_fields", DEFAULTS["freshness_fields"]):
            val = fm.get(field)
            d = parse_date(val)
            if d is None:
                findings.append(Finding(
                    WARN, "freshness",
                    "maintenance-state '%s' missing or unparseable" % field,
                    "%s/maintenance-state.md" % meta_dir))
                continue
            age = (today() - d).days
            if age > threshold:
                findings.append(Finding(
                    WARN, "freshness",
                    "%s is %d days old (threshold %d): %s" % (field, age, threshold, d.isoformat()),
                    "%s/maintenance-state.md" % meta_dir))
    # filing-log.md
    fl_name = cfg.get("filing_log_file", DEFAULTS["filing_log_file"])
    fl_path = os.path.join(vault, meta_dir, fl_name)
    fl_text = _read_text(fl_path)
    if fl_text is not None:
        found = [parse_date(x) for x in re.findall(r"\d{4}-\d{2}-\d{2}", fl_text)]
        found = [d for d in found if d]
        fl_threshold = cfg.get("filing_log_stale_days", DEFAULTS["filing_log_stale_days"])
        if found:
            latest = max(found)
            age = (today() - latest).days
            if age > fl_threshold:
                findings.append(Finding(
                    WARN, "freshness",
                    "filing-log last entry is %d days old (threshold %d): %s"
                    % (age, fl_threshold, latest.isoformat()),
                    "%s/%s" % (meta_dir, fl_name)))
    return findings, note


def check_safety_lock(vault, cfg):
    """Informational: is the optional rm -rf delete-guard (Setup Step 6.8)
    registered? Reads ~/.claude/settings.json read-only. macOS-only, matching
    the guard's own platform support; INFO severity, never an error."""
    if not cfg.get("safety_lock_check", True):
        return [], "disabled in config"
    if sys.platform != "darwin":
        return [], "non-macOS; safety-lock check skipped"
    settings = os.path.expanduser(os.path.join("~", ".claude", "settings.json"))
    text = _read_text(settings)
    hint = "optional delete-guard not detected; see Setup Step 6.8 to add the rm -rf accident net"
    if text is None:
        return [Finding(INFO, "safety-lock", hint)], "no ~/.claude/settings.json"
    try:
        data = json.loads(text)
    except (ValueError, TypeError):
        return [], "~/.claude/settings.json did not parse; skipped"
    marker = cfg.get("safety_lock_marker", "rm-guard")
    pre = (data.get("hooks", {}) or {}).get("PreToolUse", []) or []
    for entry in pre:
        for h in (entry.get("hooks", []) or []):
            cmdv = h.get("command", "")
            if isinstance(cmdv, str) and marker in cmdv:
                return [], "delete-guard installed"
    return [Finding(INFO, "safety-lock", hint)], None


# --------------------------------------------------------------------------
# House vintage: which generation of this product built the vault.
#
# WHY THIS CHECK EXISTS, stated bluntly because it is the dangerous one.
# Every other check in this file is blind between generations. `room_pattern`
# is r"^\d{2}_[A-Za-z]", which matches the old house's `07_Acme` exactly as
# happily as the current `04_Acme-Business-Wing`; `required_meta_files` names
# four files that both generations write; the record-schema check ships with
# no types configured. So an older vault, whose shape this checker's rules no
# longer describe, runs clean and walks away with a health certificate. A
# linter that says nothing about the one thing it cannot check is worse than
# one that was never run, because now there is a report to point at.
#
# The version is read, never guessed. Shape reading happens ONLY when no
# version is recorded anywhere, because shape alone convicts the innocent:
# PARA folders, numbered rooms and MOC files are ordinary Obsidian conventions,
# and Setup can adopt a vault that already had all three (see setup.md step 3).
#
# SEVERITY, and why every mismatch is an ERROR. modes/distill.md stops the tidy
# on a house-vintage ERROR, and the banner at the foot of this report prints on
# one; both read severity, not message text. So severity here is not a mood, it
# is the switch. Anything that leaves the generation of this house in doubt
# gets ERROR: a recorded version that is not the one this skill ships (older OR
# newer, the two-shapes accident is symmetrical), two records that disagree,
# and shapes from another generation. What stays a WARN is bookkeeping the
# owner can fix without the verdict changing: an unreadable value, one record
# where there should be two, shapes too thin to call.
#
# GATE ORDER IS LOAD-BEARING and it is mirrored in SKILL.md's gate 2, bullet for
# bullet. "The two records disagree" is tested BEFORE "a record carries the
# current number", because a house whose two records differ, one of them being
# the current number, matches both, and whichever runs first wins. Change the
# order in one place and the skill and the script rule differently on the same
# vault. (No version literal appears in this file on purpose; the number lives
# in the doctrine template, see current_doctrine_version.)
# --------------------------------------------------------------------------
_VERSION_NUM_RE = re.compile(r"^v?(\d+)")


def read_doctrine_version(text):
    """Read `doctrine_version:` out of a file's frontmatter.

    Returns (value, raw). `value` is an int when the key is present AND its
    value is a number (`2` and `v2` both read as 2); otherwise None. `raw` is
    the literal text of the value when the key was present at all; otherwise
    None.

    Two states a single None cannot tell apart, and the report has to: the key
    is NOT THERE, versus the key is there and says `two`. The second used to be
    reported as the first, which sent the owner hunting for a key that was
    sitting in front of them. An unreadable value is still not guessed at: a
    wrong number here is more damaging than no number."""
    fm = parse_frontmatter(text or "")
    if "doctrine_version" not in fm:
        return None, None
    raw = fm["doctrine_version"]
    if isinstance(raw, list):
        raw = ", ".join(str(x) for x in raw)
    raw = str(raw).strip()
    if raw == "":
        return None, raw
    m = _VERSION_NUM_RE.match(raw)
    return (int(m.group(1)) if m else None), raw


def doctrine_version_of(text):
    """The int only, for callers that have no file to blame (the template)."""
    return read_doctrine_version(text)[0]


def current_doctrine_version():
    """The version this copy of the product ships, read from the doctrine
    TEMPLATE beside this script in the skill payload.

    Deliberately NOT a constant in this file. A constant would be a second
    place to bump, and the two would disagree the first time somebody forgot,
    which is the exact class of bug this whole check is about. Returns None
    when the template is not reachable (script copied out of the payload); the
    'marked but older' comparison is then skipped and the report says so, while
    the important branch, no marker at all, still works without it."""
    here = os.path.dirname(os.path.abspath(__file__))
    return doctrine_version_of(
        _read_text(os.path.join(here, os.pardir, "templates",
                                "structure-doctrine.template.md")))


def _shape_evidence(vault):
    """Read the folder shapes and return TWO lists: `old`, where an old name is
    here and its current counterpart is not, and `both`, where the two names are
    sitting beside each other.

    The names come from what each generation's scaffold actually wrote: a
    `07_<Business>/` wing holding `01_Assets` / `02_SOP` / `03_Methodology`,
    `06_Command-Base/`, `05_Archive/`, `04_Resources/Skills/`, `_<Name>-MOC.md`
    doors and `function:` on decisions, against today's `04_<Business>-Business-Wing/`
    with `03_SOP`, `02_Command-Base/`, `98_Archive/`, `99_Meta/Skills/`,
    `_<Name>-Guide.md` doors and `lane:`.

    ⚠️ WHY THE SECOND LIST EXISTS. Every signal here used to be "old name AND
    current counterpart absent", which is the right shape for convicting on old
    names that are not rare on their own. But it silences itself on the one
    house this whole check was written to catch: a half-migrated vault wearing
    BOTH shapes at once (`02_SOP/` beside `03_SOP/`, `05_Archive/` beside
    `98_Archive/`). Every counterpart is present there, so every signal drops
    out and the house reads as unremarkable. Both-present is not weaker evidence
    than old-only; for a half-migration it is the only evidence there is.

    ⛔ ONE PAIR IS DELIBERATELY NOT IN `both`: MOC doors beside guide doors.
    Setup step 3 adopts somebody's existing vault by keeping their `*-MOC.md`
    files untouched and adding our `_*-Guide.md` doors for the folders we
    create, so that combination is the NORMAL end state of a legitimate,
    perfectly current adoption. It stays a one-directional signal (MOC files and
    not one guide file) and never counts as two shapes at once."""
    old, both = [], []

    def isdir(*parts):
        return os.path.isdir(os.path.join(vault, *parts))

    def pair(old_here, new_here, old_desc, both_desc):
        if old_here and new_here:
            both.append(both_desc)
        elif old_here:
            old.append(old_desc)

    try:
        top = sorted(os.listdir(vault))
    except OSError:
        return old, both
    topdirs = [n for n in top if os.path.isdir(os.path.join(vault, n))]

    pair("05_Archive" in topdirs, "98_Archive" in topdirs,
         "05_Archive/ at top level and no 98_Archive/",
         "05_Archive/ and 98_Archive/ both at top level")
    pair("06_Command-Base" in topdirs, "02_Command-Base" in topdirs,
         "06_Command-Base/ at top level and no 02_Command-Base/",
         "06_Command-Base/ and 02_Command-Base/ both at top level")

    old_wings = [n for n in topdirs if re.match(r"^(0[7-9]|[1-9]\d)_", n)
                 and n not in ("98_Archive", "99_Meta")]
    new_wings = [n for n in topdirs if n.endswith("-Business-Wing")]
    if old_wings:
        pair(True, bool(new_wings),
             "business wing at %s/ and no <NN>_<Business>-Business-Wing/" % old_wings[0],
             "a wing at %s/ and another at %s/" % (old_wings[0], new_wings[0] if new_wings else ""))

    for n in topdirs:
        if not isdir(n, "02_SOP"):
            continue
        pair(True, isdir(n, "03_SOP"),
             "%s/02_SOP/ (the current house calls that layer 03_SOP/)" % n,
             "%s/ holds 02_SOP/ and 03_SOP/ at the same time" % n)
        break

    pair(isdir("04_Resources", "Skills"), isdir("99_Meta", "Skills"),
         "generated skills under 04_Resources/Skills/ and no 99_Meta/Skills/",
         "generated-skill folders under both 04_Resources/Skills/ and 99_Meta/Skills/")

    moc = guide = False
    for path in iter_markdown_files(vault, []):
        base = os.path.basename(path)
        if base.endswith("-MOC.md"):
            moc = True
        elif base.startswith("_") and base.endswith("-Guide.md"):
            guide = True
        if moc and guide:
            break
    if moc and not guide:
        # one-directional on purpose; see the ⛔ note in the docstring
        old.append("*-MOC.md door files and not one _*-Guide.md")

    # Decisions: read every command-base folder that exists, not just the first.
    # On a half-migration both exist, and stopping at the first one is how the
    # mixed-field evidence goes missing.
    n_fn = n_lane = 0
    seen = []
    for cb in ("06_Command-Base", "02_Command-Base"):
        ddir = os.path.join(vault, cb, "Decisions")
        if not os.path.isdir(ddir):
            continue
        seen.append(cb)
        try:
            names = [x for x in sorted(os.listdir(ddir)) if x.endswith(".md")][:60]
        except OSError:
            names = []
        for name in names:
            fm = parse_frontmatter(_read_text(os.path.join(ddir, name)))
            if "function" in fm:
                n_fn += 1
            if "lane" in fm:
                n_lane += 1
    if n_fn:
        where = " and ".join("%s/Decisions/" % c for c in seen)
        pair(True, bool(n_lane),
             "decision notes in %s carry function: and none carries lane:" % where,
             "decision notes in %s carry function: (%d) and lane: (%d), two generations "
             "of the same field" % (where, n_fn, n_lane))

    return old, both


def check_house_vintage(vault, cfg):
    findings = []
    meta_dir = cfg.get("meta_dir", DEFAULTS["meta_dir"])
    doctrine_p = os.path.join(vault, meta_dir, "structure-doctrine.md")
    bootstrap_p = os.path.join(vault, meta_dir, "bootstrap-progress.md")
    filing_p = os.path.join(vault, meta_dir,
                            cfg.get("filing_log_file", DEFAULTS["filing_log_file"]))

    # Gate 1: is this vault this product's at all? Getting this wrong is the
    # expensive direction: telling a stranger their own vault is a broken
    # install of something they have never used.
    if not os.path.isfile(doctrine_p) or not (os.path.isfile(bootstrap_p)
                                              or os.path.isfile(filing_p)):
        return findings, ("no %s/structure-doctrine.md beside a state file, so this "
                          "does not look like a vault this product built; vintage not judged"
                          % meta_dir)

    doc_v, doc_raw = read_doctrine_version(_read_text(doctrine_p))
    if os.path.isfile(bootstrap_p):
        boot_v, boot_raw = read_doctrine_version(_read_text(bootstrap_p))
        boot_exists = True
    else:
        boot_v, boot_raw, boot_exists = None, None, False
    cur = current_doctrine_version()

    # A key that is present but unreadable is its own fact, and it is reported
    # as one. Saying "no doctrine_version recorded" about a file where the key
    # is plainly sitting there is the report lying to the person fixing it.
    for label, raw, val in (("structure-doctrine.md", doc_raw, doc_v),
                            ("bootstrap-progress.md", boot_raw, boot_v)):
        if raw is not None and val is None:
            findings.append(Finding(
                WARN, "house-vintage",
                "%s/%s carries doctrine_version: %s, which is not a number this script can "
                "read (it takes `2` or `v2`). The key is there; its value is unusable, so it "
                "counts for nothing below." % (meta_dir, label, raw or "(empty)"),
                "%s/%s" % (meta_dir, label)))

    # Gate 2, and its FIRST branch is the two records disagreeing. This order is
    # the whole point: "either place carries the current number" and "the two
    # places disagree" both match a house whose records differ with one of them
    # current, so whichever is tested first decides the verdict. Testing
    # agreement first calls that house current. It is not. SKILL.md's gate 2
    # lists its bullets in this same order, and the two have to move together.
    if doc_v is not None and boot_v is not None and doc_v != boot_v:
        findings.append(Finding(
            ERROR, "house-vintage",
            "the two version records disagree: %s/structure-doctrine.md says v%d, "
            "bootstrap-progress.md says v%d. One was hand-edited, or a migration stopped "
            "halfway. ⛔ No winner is picked here and none should be picked elsewhere: until "
            "the owner says which is true, the generation of this house is unknown, so treat "
            "every other check in this report as untested and change nothing structural."
            % (meta_dir, doc_v, boot_v),
            "%s/bootstrap-progress.md" % meta_dir))
        return findings, "records disagree: v%d vs v%d" % (doc_v, boot_v)

    known = doc_v if doc_v is not None else boot_v

    # Gate 2 proper: a recorded version decides it, and shape is never consulted.
    if known is not None:
        # Two records exist so that they can corroborate each other. One record
        # carrying the number is a silent pass with nothing to corroborate, and
        # the day the surviving one gets edited there is no second opinion left.
        if doc_v is None or boot_v is None:
            missing = "structure-doctrine.md" if doc_v is None else "bootstrap-progress.md"
            if missing == "bootstrap-progress.md" and not boot_exists:
                why = "%s/bootstrap-progress.md does not exist" % meta_dir
            else:
                why = "%s/%s carries no readable doctrine_version:" % (meta_dir, missing)
            findings.append(Finding(
                WARN, "house-vintage",
                "only one of the two version records carries a number (v%d); %s. A scaffolded "
                "house writes both, and they exist to check each other; with one, a later "
                "hand-edit has nothing to disagree with. Copy the number into the other."
                % (known, why),
                "%s/%s" % (meta_dir, missing)))
        if cur is None:
            return findings, ("vault declares doctrine v%d; the doctrine template is not "
                              "beside this script, so there was nothing to compare it against"
                              % known)
        if known < cur:
            # ERROR, not WARN, and this is the correction that matters most.
            # The stop-work gate in modes/distill.md and the banner at the foot
            # of this report both key on a house-vintage ERROR. While this was a
            # WARN, a house that DECLARED itself old sailed through both, and a
            # house whose age was merely inferred from folder names (below) was
            # stopped. Honesty bought the owner weaker protection than silence.
            findings.append(Finding(
                ERROR, "house-vintage",
                "this vault records doctrine v%d; this copy of the product ships v%d. The other "
                "checks in this report describe the v%d shape, so treat their silence as "
                "untested here rather than as a pass. There is no migration tool: report the "
                "differences, change nothing structural." % (known, cur, cur),
                "%s/structure-doctrine.md" % meta_dir))
            return findings, "declared v%d, shipped v%d" % (known, cur)
        if known > cur:
            # The same mismatch pointing the other way, and the same danger: a
            # skill that scaffolds v%d shapes into a v%d house builds the
            # two-shapes accident just as surely. The thing to update here is
            # the skill, not the vault.
            findings.append(Finding(
                ERROR, "house-vintage",
                "this vault records doctrine v%d; this copy of the product ships v%d, so the "
                "OLDER thing here is the skill, not the house. Its checks and its scaffold "
                "describe v%d shapes, which would land beside the v%d ones already here. "
                "Update the skill (`npx skills update`) before any structural write; reading "
                "and answering are unaffected." % (known, cur, cur, known),
                "%s/structure-doctrine.md" % meta_dir))
            return findings, "declared v%d, shipped v%d (skill is older)" % (known, cur)

        # The number says current, so nothing below may overturn that: the whole
        # point of letting a house declare its version is that someone who
        # adopted this law by hand can say so once and stop being asked. But
        # "do not overrule the owner" and "do not mention what is plainly here"
        # are different promises, and only the first one was made. A house can
        # declare itself current AND be sitting on both shapes at once, and that
        # is exactly the state worth a sentence. So: report, never gate. WARN,
        # so the banner and the stop-work rule in modes/distill.md (both keyed
        # on ERROR) stay quiet and structural work proceeds.
        _, both = _shape_evidence(vault)
        if both:
            findings.append(Finding(
                WARN, "house-vintage",
                "this vault records doctrine v%d, which is current, so nothing here is "
                "blocked. Worth knowing anyway: some folders from the older shape are still "
                "sitting beside their current counterparts (%s). If this vault adopted the "
                "law by hand, that is expected and you can ignore this line. If a migration "
                "stopped part-way, these are the leftovers."
                % (known, "; ".join(both)),
                "%s/structure-doctrine.md" % meta_dir))
            return findings, "doctrine v%d, current (%d old-shape leftover(s))" % (
                known, len(both))
        return findings, "doctrine v%d, current" % known

    # Gate 3: no number anywhere. Only now does shape get a vote, and a shape is
    # evidence of a shape, never of who built the house or when. State what was
    # seen; the owner knows the provenance and this script never will.
    old, both = _shape_evidence(vault)
    verstr = ("v%d" % cur) if cur is not None else "the version this skill ships"
    seen = ("no doctrine_version: key in %s/structure-doctrine.md" % meta_dir
            if doc_raw is None else
            "doctrine_version: in %s/structure-doctrine.md is unreadable" % meta_dir)
    if not boot_exists:
        seen += ", and no %s/bootstrap-progress.md" % meta_dir
    elif boot_raw is None:
        seen += ", none in bootstrap-progress.md"
    else:
        seen += ", and bootstrap-progress.md's is unreadable"

    if both and (len(both) + len(old)) >= 2:
        findings.append(Finding(
            ERROR, "house-vintage",
            "%s, and this vault is wearing two shapes at once (%s). That is the state this "
            "check exists to catch: a layout part-way between generations, where a session "
            "that keeps scaffolding makes it worse and nobody can tell afterwards which "
            "session started it. Everything else in this report was written for %s and does "
            "not describe a house in this state, so a low finding count above is NOT a clean "
            "bill of health. There is no migration tool: report the differences, change "
            "nothing structural."
            % (seen, "; ".join(both + old), verstr),
            "%s/structure-doctrine.md" % meta_dir))
        return findings, "two shapes at once: %d both-present, %d old-only" % (len(both), len(old))

    if not both and len(old) >= 2:
        findings.append(Finding(
            ERROR, "house-vintage",
            "%s, and the folder shapes here are the ones this product's earlier generation "
            "used (%s). Everything else in this report was written for %s and does not "
            "describe this vault, so a low finding count above is NOT a clean bill of health. "
            "There is no migration tool: report the differences, change nothing structural."
            % (seen, "; ".join(old), verstr),
            "%s/structure-doctrine.md" % meta_dir))
        return findings, "%d old-shape signal(s)" % len(old)

    findings.append(Finding(
        WARN, "house-vintage",
        "%s, and the shapes are not conclusive (%s). Which generation this house belongs to "
        "cannot be settled from here; ask the owner rather than assuming either way. If they "
        "confirm it is current, writing doctrine_version: into the doctrine frontmatter "
        "settles it permanently."
        % (seen, "; ".join(both + old) if (both or old) else "no old-shape signal found"),
        "%s/structure-doctrine.md" % meta_dir))
    return findings, "unmarked, %d both-present + %d old-only signal(s)" % (len(both), len(old))


CHECKS = [
    # First on purpose: it decides whether the rest of the report means anything.
    ("House vintage", check_house_vintage),
    ("Top-level rooms", check_rooms),
    ("Required 99_Meta files", check_required_meta),
    ("Record (cb:) schema", check_record_schema),
    ("Tag vocabulary", check_tags),
    ("Freshness", check_freshness),
    ("Safety lock (delete-guard)", check_safety_lock),
]


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------
def run(vault, cfg):
    all_findings = []
    notes = []
    for label, fn in CHECKS:
        try:
            found, note = fn(vault, cfg)
        except Exception as e:  # a broken check never sinks the whole run
            found, note = [], "check errored (skipped): %s" % e
        all_findings.extend(found)
        notes.append((label, note, len(found)))
    return all_findings, notes


def print_report(vault, cfg, source, findings, notes):
    print("=" * 70)
    print("My Second Brain: vault checkup (read-only)")
    print("Vault:  %s" % vault)
    print("Config: %s" % source)
    print("Date:   %s" % today().isoformat())
    print("=" * 70)

    print("\nChecks run:")
    for label, note, count in notes:
        line = "  - %-26s %d finding(s)" % (label, count)
        if note:
            line += "   [%s]" % note
        print(line)

    by_sev = {ERROR: [], WARN: [], INFO: []}
    for f in findings:
        by_sev.get(f.severity, by_sev[INFO]).append(f)

    for sev in (ERROR, WARN, INFO):
        items = by_sev[sev]
        if not items:
            continue
        print("\n%s  (%d)" % (sev, len(items)))
        print("-" * 70)
        for f in sorted(items, key=lambda x: (x.check, x.message)):
            loc = ("  <%s>" % f.path) if f.path else ""
            print("  [%s] %s%s" % (f.check, f.message, loc))

    ne = len(by_sev[ERROR])
    nw = len(by_sev[WARN])
    ni = len(by_sev[INFO])
    print("\n" + "=" * 70)
    print("Summary: %d error(s), %d warning(s), %d info; %d finding(s) total."
          % (ne, nw, ni, ne + nw + ni))
    # The summary line is what gets skimmed, so the one finding that invalidates
    # the rest of the report says so here rather than trusting it to be read
    # twenty lines up. ASCII only: this has to survive a Windows console.
    # It says what was OBSERVED and stops there. A vintage error now covers four
    # different situations (a recorded version that is not this one, in either
    # direction; two records that disagree; folder shapes from another
    # generation), and none of them tells this script who built the vault or
    # when, so no sentence here may claim to know.
    if any(f.check == "house-vintage" and f.severity == ERROR for f in findings):
        print("NOT A CLEAN BILL: the house-vintage check did not clear, so the shape")
        print("every check above tests for may not be the shape this vault has, and a")
        print("low count is not evidence of health. Read the house-vintage error first.")
    print("Report-only: nothing in the vault was changed.")
    print("=" * 70)


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Read-only vault linter for a My Second Brain vault. "
                    "Reports hygiene problems; changes nothing.")
    ap.add_argument("vault", help="path to the vault root")
    ap.add_argument("--config", help="path to a .checkup.json config (overrides auto-discovery)")
    ap.add_argument("--json", action="store_true", help="emit findings as JSON instead of a text report")
    args = ap.parse_args(argv)

    vault = os.path.abspath(os.path.expanduser(args.vault))
    if not os.path.isdir(vault):
        sys.stderr.write("checkup: cannot read vault (not a directory): %s\n" % vault)
        return 2

    cfg, source = load_config(vault, args.config)
    findings, notes = run(vault, cfg)

    if args.json:
        out = {
            "vault": vault,
            "config_source": source,
            "date": today().isoformat(),
            "checks": [{"label": l, "note": n, "count": c} for (l, n, c) in notes],
            "findings": [f.as_dict() for f in findings],
            "summary": {
                "error": sum(1 for f in findings if f.severity == ERROR),
                "warn": sum(1 for f in findings if f.severity == WARN),
                "info": sum(1 for f in findings if f.severity == INFO),
            },
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print_report(vault, cfg, source, findings, notes)

    return 0  # report-only: always 0 when the vault was readable


if __name__ == "__main__":
    sys.exit(main())
