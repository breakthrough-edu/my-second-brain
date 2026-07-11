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
    # 07_/08_ business wings). Anything else at the top level is surfaced.
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
    # required keys. Left EMPTY on purpose: the public default enforces nothing
    # private. A vault supplies its own types map via .checkup.json to turn on
    # required-key enforcement. See structure-doctrine.md in the vault.
    "record_schema": {"marker": "cb", "types": {}},
    # Tag vocabulary: the markdown file the whitelist is parsed from, relative
    # to meta_dir. An explicit `tag_vocabulary` list in config overrides parsing.
    "tag_vocabulary_file": "tagging-vocabulary.md",
    # Also scan note BODIES for inline #tags, not just frontmatter `tags:`.
    # Inline scanning is inherently noisier; set False to check frontmatter only.
    "scan_inline_tags": True,
    # Dirs whose notes are skipped when scanning for tags / schema (archive and
    # template shapes are not live content).
    "scan_skip_dirs": ["05_Archive", "99_Meta/Templates", "99_Meta/memory-archive"],
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


CHECKS = [
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
