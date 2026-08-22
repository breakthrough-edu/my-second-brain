#!/usr/bin/env python3
"""
doctrine_schema.py: the reader for section 8 of a vault's structure doctrine.

WHAT IT IS
    One function, load_schema(vault_path), that turns section 8 of
    99_Meta/structure-doctrine.md into a structure other tools can enforce.
    Section 8 calls itself "the single source, no copies anywhere"; this file
    is what makes that sentence true instead of aspirational. Before it, the
    checker shipped an empty record-schema config and the law sat unread
    beside it.

    Consumers so far: scripts/checkup.py (the weekly linter) and the
    frontmatter guard hook. Both read through here. Neither keeps a copy.

    CHANGING SECTION 8? Run the repo's acceptance harness, `dev/s8-accept.py`,
    and require exit 0. It does not ship (it sits outside this payload), it
    checks the block against the criteria six ways, and its last check hands
    the block to THIS file and demands the two walks agree.

WHAT IT READS, AND WHY IT HARD-CODES NO FAMILY OR FIELD NAMES
    Section 8 opens with a meta-rule comment that describes its own shape:
    which keys are reserved, and what an unreserved key means. This reader
    obeys that comment rather than a list of names baked in here. Two reasons,
    both measured rather than assumed (see the 2026-08-15 harness session):

      1. Walking by the meta-rule writes ZERO family names and ZERO field
         names into this file. Hard-coding those would have meant naming every
         family and every field section 8 declares.

         ⛔ It does NOT write zero key names, and the difference is the whole
         claim. Four of the six RESERVED keys are written here on purpose:
         `required`, `optional`, `marker` and `multi` are fixed slots on Spec
         (see its __slots__), and three of them are also read straight off a
         raw spec (`raw.get(...)`, four such reads) rather than through the
         reserved set; `grep -oE '"(required|optional|multi)"'` over this file
         counts them. Those four are structural rather than discovered: a Spec
         needs somewhere to keep required keys whatever section 8 decides to
         call them.

         What writing them here costs, measured on a rendered vault rather than
         reasoned about: rename `required` in the block and this reader ABORTS
         (the mounting key stops being derivable), but rename `optional` or
         `multi` and it runs QUIETLY with that slot empty, the same families
         and shapes as before. The quiet `multi` is the expensive one: a
         legal `lane: [deliver, run]` on an SOP is then reported as two values
         in a single-valued field. So renaming a reserved key is an edit to this
         file as well, which is the same contract the meta-rule comment has.
         The names that would rot in silence are the family names and the
         field names, and not one of them appears below.
      2. The reserved-key list is not a convenience, it is a correctness
         requirement. "Inside a family, a mapping is a subtype" stops being
         true the moment a reserved key's value is itself a mapping (`extends`
         and `cardinality` both are). A walk that does not know the reserved
         keys invents families that do not exist.

    A stale hard-coded list would also fail QUIETLY: family counts still
    match, nothing raises, and only the values that moved go unenforced. So
    there is no fallback anywhere in this file. If the meta-rule comment
    cannot be read, load_schema raises. It never guesses.

OPEN KEYS: DECLARED LEGAL HERE, VALUES NOT GOVERNED HERE
    Section 8 can also declare a key legal on every note while declaring
    nothing about its values. `tags` is the one that ships: which words are
    legal is the tag vocabulary's business, and section 8's business is only
    that the key itself is not something somebody invented on the spot.

    An open key is NOT a closed list with nothing in it. An empty list refuses
    every value while looking like law; an open key refuses none and says so.

    So the reader puts an open key on the KNOWN side of every spec (its
    `optional`) and keeps it OUT of `enums`, where a value would be measured
    against a list. What that buys is one sentence in section 8 instead of two
    laws: the frontmatter guard used to carry `k != "tags"` in its own source,
    a second place the law lived, which is the thing section 8's own title
    forbids. A name declared open here and given a closed list anywhere in the
    same block raises rather than resolves (see parse_block).

NO LINE NUMBERS, EVER
    Section 8 is found by its heading and the first ```yaml fence below it.
    Every edit inside the block shifts every line in it, so a line number is
    a reference that rots on the next edit.

PYYAML IS A REAL DEPENDENCY, AND ITS ABSENCE IS LOUD
    Section 8 uses flow mappings and inline comments. A hand-rolled parser for
    it would be a second dialect of YAML that drifts from the first, which is
    the exact failure this file exists to prevent, so it uses PyYAML.

    That is a departure from "standard library only", and it is deliberate:
    the alternative was a schema reader nobody could trust. The import failing
    raises SchemaUnavailable, which carries the exact install command for the
    interpreter that is running. Callers MUST surface that as an error.

    ⛔ A caller may NOT downgrade a missing PyYAML into "check skipped, 0
    findings". Zero findings is indistinguishable from a clean vault, and a
    vault that looks clean because nothing was checked is the precise disease
    this whole enforcement line was built to catch.
"""

import os
import re
import sys
import sysconfig


class SchemaError(Exception):
    """Section 8 was reachable but could not be read as the law it claims to be."""


class SchemaUnavailable(SchemaError):
    """The reader itself cannot run (PyYAML missing). Never a silent skip."""


# --------------------------------------------------------------------------
# PyYAML, and an install hint that is right for THIS interpreter
# --------------------------------------------------------------------------
def install_hint():
    """The pip command that actually works on the interpreter now running.

    Measured on macOS 2026-08-16 across the three interpreters a Mac commonly
    carries, because guessing here produces advice that fails in front of the
    user:

      * python.org and Apple's Command Line Tools python: `--user` works.
      * Homebrew python: PEP 668 marks it externally managed, and `--user`
        ALONE IS STILL REFUSED. Homebrew's own refusal text names
        `--break-system-packages` and then recommends adding `--user` on top
        of it, which is what the Homebrew branch below prints. That pair
        installs into the per-user site directory, so nothing under the
        Homebrew prefix is written to and no Homebrew package is replaced.

    The test is PEP 668's own: an EXTERNALLY-MANAGED marker sitting beside the
    standard library. Returns (command, user_site_dir, externally_managed).
    """
    exe = sys.executable or "python3"
    marker = os.path.join(sysconfig.get_paths()["stdlib"], "EXTERNALLY-MANAGED")
    managed = os.path.exists(marker)
    try:
        import site
        user_site = site.getusersitepackages()
    except Exception:
        user_site = "(per-user site directory could not be resolved)"
    if managed:
        cmd = "%s -m pip install --user --break-system-packages pyyaml" % exe
    else:
        cmd = "%s -m pip install --user pyyaml" % exe
    return cmd, user_site, managed


def _load_yaml_module():
    try:
        import yaml  # noqa: F401
        return yaml
    except ImportError:
        cmd, user_site, managed = install_hint()
        flavour = ("This interpreter is externally managed (PEP 668), so plain "
                   "`--user` is refused on its own and the command below adds "
                   "--break-system-packages. It writes into the per-user site "
                   "directory only; nothing the package manager owns is touched."
                   if managed else
                   "This interpreter accepts a plain per-user install.")
        raise SchemaUnavailable(
            "PyYAML is not installed for %s, so section 8 of the structure "
            "doctrine cannot be read and NOTHING it declares can be enforced. "
            "%s\n  install:   %s\n  lands in:  %s\n"
            "Ask before installing, then re-run. Do not treat this as a check "
            "that can be skipped: a report with no findings because nothing "
            "was read looks exactly like a healthy vault."
            % (sys.executable or "python3", flavour, cmd, user_site))


# --------------------------------------------------------------------------
# Locating the block
# --------------------------------------------------------------------------
_HEADING_RE = re.compile(r"^##\s+8(\s|·|$)")


def locate_block(doctrine_path):
    """Return (body_text, coords) for section 8's yaml body. No line numbers in,
    line numbers out only as a human-readable coordinate string for reports."""
    try:
        with open(doctrine_path, "r", encoding="utf-8", errors="replace") as fh:
            lines = fh.read().split("\n")
    except OSError as e:
        raise SchemaError("cannot read %s: %s" % (doctrine_path, e))

    heads = [i for i, l in enumerate(lines) if _HEADING_RE.match(l)]
    if len(heads) != 1:
        raise SchemaError(
            "expected exactly one '## 8' heading in %s, found %d. Section 8 is "
            "located by its heading, so this has to be unambiguous."
            % (doctrine_path, len(heads)))
    head = heads[0]

    opens = [i for i in range(head + 1, len(lines)) if lines[i].strip() == "```yaml"]
    if not opens:
        raise SchemaError("no ```yaml fence below the '## 8' heading in %s" % doctrine_path)
    open_i = opens[0]
    closes = [i for i in range(open_i + 1, len(lines)) if lines[i].strip() == "```"]
    if not closes:
        raise SchemaError("unterminated ```yaml fence under section 8 in %s" % doctrine_path)
    close_i = closes[0]

    body = lines[open_i + 1:close_i]
    coords = "heading line %d, body lines %d-%d (%d lines)" % (
        head + 1, open_i + 2, close_i, len(body))
    return "\n".join(body), coords


def reserved_keys(body_text):
    """Read the reserved-key list out of the block's own meta-rule comment.

    No fallback on purpose. A built-in list here would be the second copy that
    section 8's own title forbids, and it would go stale silently."""
    for line in body_text.split("\n"):
        s = line.strip()
        if s.startswith("#") and "are reserved" in s:
            names = re.findall(r"`([a-z_-]+)`", s)
            if names:
                return set(names)
    return None


# --------------------------------------------------------------------------
# The parsed shape
# --------------------------------------------------------------------------
class Spec(object):
    """One enforceable shape: a family with no subtypes, or one subtype of one.

    `name` is the dotted path used in reports ("brief", "record.task").
    `enums` maps a field name to its closed list, already resolved: a value
    declared on the spec wins over one declared on its family, which wins over
    a global list, and `extends` adds to a global list rather than replacing it.
    """

    __slots__ = ("name", "family", "subtype", "required", "optional",
                 "marker", "multi", "enums")

    def __init__(self, name, family, subtype):
        self.name = name
        self.family = family
        self.subtype = subtype
        self.required = []
        self.optional = []
        self.marker = None
        self.multi = []
        self.enums = {}

    def declares(self, field):
        return field in self.required or field in self.optional

    def __repr__(self):
        return "<Spec %s required=%s enums=%s>" % (
            self.name, self.required, sorted(self.enums))


class Schema(object):
    """Everything section 8 declares, in the six shapes it can express."""

    __slots__ = ("families", "specs", "globals", "open_keys", "by_marker",
                 "by_type", "marker_key", "type_key", "reserved", "source",
                 "coords")

    def __init__(self):
        self.families = []      # family names, in declaration order
        self.specs = {}         # dotted name -> Spec
        self.globals = {}       # field -> closed list, global to all families
        self.open_keys = {}     # field -> why it is open, values ungoverned
        self.by_marker = {}     # "cb: task" -> Spec
        self.by_type = {}       # "brief" / "client" -> Spec
        self.marker_key = None  # the frontmatter key markers are written on
        self.type_key = None    # the frontmatter key everything else mounts on
        self.reserved = set()
        self.source = None
        self.coords = None

    def spec_for(self, fm):
        """Which spec governs this frontmatter, or None if section 8 does not
        claim it. Marker first: a record declares itself with its marker key
        and does not carry the type key at all."""
        if self.marker_key and self.marker_key in fm:
            val = fm.get(self.marker_key)
            if isinstance(val, str) and val.strip():
                return self.by_marker.get("%s: %s" % (self.marker_key, val.strip()))
            return None
        if self.type_key and self.type_key in fm:
            val = fm.get(self.type_key)
            if isinstance(val, str):
                return self.by_type.get(val.strip())
        return None

    def __repr__(self):
        return "<Schema %d families, %d specs, globals=%s>" % (
            len(self.families), len(self.specs), sorted(self.globals))


# --------------------------------------------------------------------------
# The meta-rule walk
# --------------------------------------------------------------------------
def _derive_marker_key(specs_raw, reserved):
    """The frontmatter key a marker is written on, read out of the markers.

    Section 8 writes a marker as `marker: "cb: decision"`. The key is the part
    before the colon, and every marker in the block has to agree on it or the
    block is describing two conventions at once."""
    keys = set()
    for raw in specs_raw.values():
        for rk in reserved:
            v = raw.get(rk)
            if isinstance(v, str) and ":" in v:
                keys.add(v.split(":", 1)[0].strip())
    if not keys:
        return None
    if len(keys) > 1:
        raise SchemaError(
            "the markers in section 8 do not agree on one frontmatter key "
            "(saw %s), so there is no single way to recognise a record"
            % sorted(keys))
    return keys.pop()


def _derive_type_key(specs_raw, marker_key):
    """The frontmatter key every non-marker spec mounts on.

    Derived, not named here: it is the one required key that EVERY marker-less
    spec declares. Section 8 currently makes that `type`, but this reader never
    says so; if the block renames it, the rename carries."""
    marker_bearing = set()
    for name, raw in specs_raw.items():
        if any(isinstance(v, str) and marker_key and v.startswith(marker_key + ":")
               for v in raw.values()):
            marker_bearing.add(name)
    common = None
    for name, raw in specs_raw.items():
        if name in marker_bearing:
            continue
        req = set(raw.get("required") or [])
        common = req if common is None else (common & req)
    if not common:
        raise SchemaError(
            "no single required key is shared by every non-record shape in "
            "section 8, so there is no derivable way for a note to declare "
            "which family it belongs to")
    if len(common) > 1:
        raise SchemaError(
            "more than one required key is shared by every non-record shape in "
            "section 8 (%s), so which one a note mounts on is ambiguous"
            % sorted(common))
    return common.pop()


def _walk(families, reserved):
    """Reach every spec using only the meta-rule.

    Drop reserved keys. A remaining key whose value is a mapping is a subtype,
    so a family with subtypes contributes its subtypes and not itself. A family
    with none is its own spec. No key name is written into this function."""
    specs_raw, family_lists = {}, {}
    for fam, body in families.items():
        if not isinstance(body, dict):
            raise SchemaError(
                "family %r is a %s, not a mapping; section 8 cannot be walked"
                % (fam, type(body).__name__))
        subtypes = {k: v for k, v in body.items()
                    if k not in reserved and isinstance(v, dict)}
        family_lists[fam] = {k: v for k, v in body.items()
                             if k not in reserved and isinstance(v, list)}
        if subtypes:
            for sub, spec in subtypes.items():
                specs_raw["%s.%s" % (fam, sub)] = spec
        else:
            specs_raw[fam] = body
    return specs_raw, family_lists


def parse_block(body_text, source=None, coords=None):
    """Parse an already-extracted section 8 body into a Schema."""
    yaml = _load_yaml_module()
    try:
        doc = yaml.safe_load(body_text)
    except yaml.YAMLError as exc:
        raise SchemaError("section 8 is not parseable YAML: %s" % exc)
    if not isinstance(doc, dict):
        raise SchemaError("section 8 did not parse to a mapping (got %s)"
                          % type(doc).__name__)

    reserved = reserved_keys(body_text)
    if not reserved:
        raise SchemaError(
            "section 8 no longer says which of its keys are reserved, so nothing "
            "in it can be enforced.\n"
            "  WHAT WAS LOOKED FOR: one comment line inside section 8's ```yaml "
            "block (the lines above `families:`) that contains the words 'are "
            "reserved' and names each reserved key in backticks on that same "
            "line, like this one, which is what ships:\n"
            "      # Inside a family, `required` `optional` `marker` `multi` "
            "`extends` `cardinality` are reserved\n"
            "  WHAT PROBABLY HAPPENED: that comment was tidied up. It reads like "
            "prose and it is not: this reader takes the reserved-key list out of "
            "it instead of carrying its own copy, so removing the backticks, "
            "spreading the names over two lines, or losing the exact words 'are "
            "reserved' each make it unreadable, even though the section still "
            "looks perfectly fine to a person.\n"
            "  HOW TO FIX IT: put the names back in backticks on the same line as "
            "the words 'are reserved'. The prose around them is free, the names "
            "and those three words are not. If you are unsure what the line said, "
            "the shipped version is in the my-second-brain skill payload at "
            "templates/structure-doctrine.template.md, section 8; `git diff` on "
            "99_Meta/structure-doctrine.md shows what changed in yours.\n"
            "  WHY IT STOPS INSTEAD OF GUESSING: a built-in list of those key "
            "names here would be the second copy that section 8's own title "
            "forbids, and it would go stale without ever raising. Refusing to run "
            "is the loud failure; a fallback would be the quiet one.")

    # Top level: three shapes, told apart by the VALUE and never by the name,
    # the same way the families holder has never been named in this file.
    #   mapping of mappings  -> the families (exactly one such key)
    #   mapping of strings   -> the open-key table (at most one such key)
    #   list                 -> a closed list, global to all families
    family_holders = [k for k, v in doc.items()
                      if isinstance(v, dict) and v
                      and all(isinstance(x, dict) for x in v.values())]
    open_holders = [k for k, v in doc.items()
                    if isinstance(v, dict) and v
                    and all(isinstance(x, str) for x in v.values())]
    if len(family_holders) != 1:
        raise SchemaError(
            "expected exactly one top-level key holding the families, found %d "
            "(%s). A top-level mapping is the families when every value in it "
            "is itself a mapping, and the open-key table when every value in it "
            "is a one-line string saying what governs that key instead, so an "
            "open-key entry written as a mapping is one way to land here."
            % (len(family_holders), sorted(family_holders)))
    if len(open_holders) > 1:
        raise SchemaError(
            "expected at most one top-level key holding the open keys, found %d "
            "(%s); which one a reader should believe is not decidable"
            % (len(open_holders), sorted(open_holders)))
    families = doc[family_holders[0]]
    open_keys = dict(doc[open_holders[0]]) if open_holders else {}
    globals_ = {k: v for k, v in doc.items()
                if k != family_holders[0] and isinstance(v, list)}

    specs_raw, family_lists = _walk(families, reserved)
    marker_key = _derive_marker_key(specs_raw, reserved)
    type_key = _derive_type_key(specs_raw, marker_key)

    schema = Schema()
    schema.families = list(families.keys())
    schema.globals = globals_
    schema.marker_key = marker_key
    schema.type_key = type_key
    schema.reserved = reserved
    schema.source = source
    schema.coords = coords

    for name, raw in specs_raw.items():
        fam = name.split(".", 1)[0]
        sub = name.split(".", 1)[1] if "." in name else None
        spec = Spec(name, fam, sub)
        spec.required = list(raw.get("required") or [])
        spec.optional = list(raw.get("optional") or [])
        spec.multi = list(raw.get("multi") or [])
        for rk in reserved:
            v = raw.get(rk)
            if isinstance(v, str) and marker_key and v.startswith(marker_key + ":"):
                spec.marker = v.strip()

        # Closed lists, weakest source first so the strongest wins.
        for field, values in globals_.items():
            spec.enums[field] = list(values)
        for field, values in family_lists.get(fam, {}).items():
            spec.enums[field] = list(values)
        for k, v in raw.items():
            if k in reserved:
                continue
            if isinstance(v, list):
                spec.enums[k] = list(v)
        # `extends` adds to a global list rather than replacing it.
        for rk in reserved:
            v = raw.get(rk)
            if isinstance(v, dict) and all(isinstance(x, list) for x in v.values()):
                for field, extra in v.items():
                    base = list(spec.enums.get(field, []))
                    for item in extra:
                        if item not in base:
                            base.append(item)
                    spec.enums[field] = base

        schema.specs[name] = spec
        if spec.marker:
            schema.by_marker[spec.marker] = spec

    # How a note names the spec it belongs to. Two cases, both read off the
    # block: a family that gives the mounting field its own closed list is
    # naming its legal values; otherwise the spec's own name is the value.
    for name, spec in schema.specs.items():
        own = family_lists.get(spec.family, {}).get(type_key)
        raw_own = specs_raw[name].get(type_key)
        values = raw_own if isinstance(raw_own, list) else own
        if values:
            for v in values:
                schema.by_type[v] = spec
        elif not spec.marker:
            schema.by_type[spec.subtype or spec.family] = spec

    # Open keys, applied last so nothing above can be read through them.
    # Two halves, and the second one refuses instead of resolving:
    #   1. the name joins every spec's `optional`, which is the side an
    #      enforcer counting undeclared keys reads. That is what lets the
    #      exemption live in section 8 rather than in an enforcer's source.
    #   2. the name may not also carry a closed list, anywhere. A key declared
    #      open here and closed there is section 8 saying two things about one
    #      key, and because the name now sits in `optional`, `Spec.declares`
    #      returns True for it, so picking the closed list would silently start
    #      enforcing a list the same block calls ungoverned. Raising is the
    #      loud failure; choosing a winner is the quiet one.
    schema.open_keys = open_keys
    for spec in schema.specs.values():
        for field in open_keys:
            if field in spec.enums:
                raise SchemaError(
                    "section 8 declares %r an open key (its values are not "
                    "governed there) and also gives it a closed list on %s, so "
                    "the block says two different things about one key. Keep "
                    "one: drop the closed list, or drop the name from the "
                    "open-key table." % (field, spec.name))
            if field not in spec.required and field not in spec.optional:
                spec.optional.append(field)

    return schema


def load_schema(vault, meta_dir="99_Meta", doctrine_name="structure-doctrine.md"):
    """Read section 8 out of a vault's own doctrine. Raises on anything unclear."""
    path = os.path.join(vault, meta_dir, doctrine_name)
    if not os.path.isfile(path):
        raise SchemaError(
            "no %s/%s in this vault, so there is no record schema to read"
            % (meta_dir, doctrine_name))
    body, coords = locate_block(path)
    return parse_block(body, source=os.path.join(meta_dir, doctrine_name), coords=coords)


def validate(fm, spec, schema):
    """Check one note's frontmatter against its spec.

    Returns a list of (kind, message). `kind` is "missing" or "value", so the
    caller decides severity. Values are only checked when present: a missing
    key is already reported once as missing and does not need a second line."""
    problems = []
    missing = [k for k in spec.required
               if k not in fm or fm.get(k) in ("", None, [])]
    if missing:
        problems.append(("missing", "missing required key(s): %s" % ", ".join(missing)))
    for field, allowed in spec.enums.items():
        if field not in fm or not spec.declares(field):
            continue
        raw = fm.get(field)
        if raw in ("", None, []):
            continue
        values = raw if isinstance(raw, list) else [raw]
        if len(values) > 1 and field not in spec.multi:
            problems.append((
                "value",
                "'%s:' carries %d values but section 8 declares it single-valued"
                % (field, len(values))))
        for v in values:
            if str(v).strip() not in allowed:
                problems.append((
                    "value",
                    "'%s: %s' is not in the closed list section 8 declares for "
                    "%s (%s)" % (field, v, spec.name, ", ".join(str(a) for a in allowed))))
    return problems


# --------------------------------------------------------------------------
# Run it directly to see what a vault's section 8 actually says.
# --------------------------------------------------------------------------
def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        sys.stderr.write("usage: doctrine_schema.py /path/to/vault\n")
        return 2
    try:
        schema = load_schema(os.path.abspath(os.path.expanduser(argv[0])))
    except SchemaUnavailable as e:
        sys.stderr.write("BLOCKED: %s\n" % e)
        return 3
    except SchemaError as e:
        sys.stderr.write("ABORT: %s\n" % e)
        return 1
    print("source: %s (%s)" % (schema.source, schema.coords))
    print("reserved keys (read from the block): %s" % sorted(schema.reserved))
    print("mounting keys: marker=%r type=%r" % (schema.marker_key, schema.type_key))
    print("families (%d): %s" % (len(schema.families), ", ".join(schema.families)))
    print("global closed lists: %s" % {k: v for k, v in schema.globals.items()})
    print("open keys (legal on every note, values not governed by section 8): %s"
          % sorted(schema.open_keys))
    for k in sorted(schema.open_keys):
        print("    %s: %s" % (k, schema.open_keys[k]))
    print("\nspecs (%d):" % len(schema.specs))
    for name in sorted(schema.specs):
        s = schema.specs[name]
        bits = ["required=%s" % s.required]
        if s.optional:
            bits.append("optional=%s" % s.optional)
        if s.marker:
            bits.append("marker=%r" % s.marker)
        if s.multi:
            bits.append("multi=%s" % s.multi)
        if s.enums:
            bits.append("enums={%s}" % ", ".join(
                "%s:%d" % (k, len(v)) for k, v in sorted(s.enums.items())))
        print("  %-24s %s" % (name, "  ".join(bits)))
    print("\nmounted by marker (%d): %s" % (len(schema.by_marker), sorted(schema.by_marker)))
    print("mounted by %r (%d): %s" % (schema.type_key, len(schema.by_type), sorted(schema.by_type)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
