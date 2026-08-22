#!/usr/bin/env python3
"""
s8-accept.py - acceptance harness for section 8 of the structure doctrine
(the machine-readable record schema).

WHAT THIS IS
    Seven checks that section 8 is still the thing it claims to be: parseable,
    self-describing, and readable by the code that actually ships. It replaces
    the throwaway script that the 2026-08-15 shape-fix session wrote into a
    scratchpad and lost; that loss is the reason this file exists at all.

WHEN TO RUN IT
    Every time section 8 changes, before calling the change done. A rename, a
    new family, a new reserved key, a moved value: run this. It is the
    acceptance step, not a smoke test.

    $ python3 dev/s8-accept.py

    The template path defaults to this script's own repo-relative sibling and
    can be overridden with --template.

ONE COPY, WHICH IS WHY CHECK 5 IS NO LONGER A DIFF
    Until 2026-08-16 this harness checked TWO copies of section 8 against each
    other: the shipped template and an English draft in a personal vault. Check
    5 was that diff. The draft is now retired and the template is the single
    source, so that check lost its subject.

    ⛔ It was replaced rather than deleted, because deleting it would have left
    all five survivors reading section 8 through THIS FILE'S private walk
    (`reserved_keys`, `walk_specs`, `closed_lists` below), which is a second
    implementation of what my-second-brain/scripts/doctrine_schema.py does. A
    harness that only ever agrees with itself can pass green while the reader
    the product actually ships raises on the same block. The new check 5 loads
    the block through that shipped reader and demands the two walks agree.

    That is also the measured failure this harness already hid once: the two
    copies' YAML bodies were byte-identical (old check 5 passed on every run)
    while the section HEADING and an entire paragraph of its preamble had
    drifted apart. Both sit outside the ```yaml fence, and every check here
    reads inside it. The lesson kept: this harness sees the block, not the
    section, and it should not be trusted with prose.

IT DOES NOT SHIP
    This file sits at the repo root under dev/, outside my-second-brain/. The
    `npx skills` installer copies exactly one directory - the one holding
    SKILL.md - so everything beside my-second-brain/ stays in version control
    and never reaches a user's ~/.claude/skills/. That is also why this script
    is allowed to `import yaml`: the "Python 3 standard library only" promise
    in my-second-brain/scripts/checkup.py belongs to code that ships. This is
    a maintainer tool and is held to no such promise. If PyYAML is missing the
    import fails loudly, which is the correct failure for a dev harness.

WHAT IT DELIBERATELY DOES NOT DO
    No line numbers anywhere. Section 8 is located by finding the `## 8 `
    heading and taking the first ```yaml fence below it, because every edit to
    the block shifts every line inside it - that pit has already been fallen
    into once and is logged as entry 103 of the execution backlog.

    Reserved key names are not hard-coded either. They are read out of the
    block's own meta-rule comment, so the next rename of a reserved key does
    not silently invalidate checks 3c and 3d. If that comment cannot be read,
    the run fails; it does not fall back to a built-in list.

    The expected counts below ARE hard-coded, on purpose: they are the
    acceptance criteria. Change one only when section 8 legitimately changes
    shape, and say so in the commit.

EXIT CODES
    0  all seven checks ran and passed
    1  a check failed - the report says which check and what differs
"""

import argparse
import os
import re
import sys

import yaml

# The shipped reader, for check 5. Imported by path: this harness lives outside
# the skill payload on purpose (see IT DOES NOT SHIP), so it has to reach in.
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir,
    "my-second-brain", "scripts"))
import doctrine_schema  # noqa: E402

# --- acceptance criteria (see header: change only with a shape change) -------
EXPECT_FAMILIES = 13
EXPECT_SPECS = 35  # families with subtypes contribute their subtypes, not themselves
                   # 24 until 2026-08-20, when process.method was opened
                   # 25 until 2026-08-21, when entity's eleven types became eleven subtypes
EXPECT_IN_FAMILY_CLOSED_LISTS = 14  # 13 until 2026-08-19, when entity.status was closed;
                                    # 14 until 2026-08-20, when process.method.status opened;
                                    # 15 until 2026-08-21, when entity.type stopped being a list
                                    # and became the family's subtypes
EXPECT_GLOBAL_CLOSED_LISTS = 2  # lane, domain
EXPECT_PERSONAL_LANES = 7
EXPECT_DECISION_LANES = 11  # the four work lanes plus the seven personal ones
EXPECT_MULTI = {"process.sop": ["lane"], "process.playbook": ["references"]}
# process.playbook.references added 2026-08-20: the one pointer a playbook writes at birth
EXPECT_LAB_CARDINALITY = {"count": 1, "per": "lab-folder"}
RENDER_TAGS = ["aroma-coffee", "laowang-coffee", "noodlebar"]
PLACEHOLDER = "{{BUSINESS_TAG}}"

failures = []


def fail(check, where, detail):
    failures.append((check, where, detail))
    print(f"    FAIL [{check}] {where}: {detail}")


# --- locating the block ------------------------------------------------------

def locate_block(path):
    """Find section 8's yaml body without using a single line number.

    Returns (body_lines, coords_string). Raises SystemExit on a structural
    surprise, because every later check reads whatever this returns.
    """
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")

    heads = [i for i, l in enumerate(lines) if l.startswith("## 8 ")]
    if len(heads) != 1:
        sys.exit(f"ABORT: expected exactly one '## 8 ' heading in {path}, found {len(heads)}")
    head = heads[0]

    opens = [i for i in range(head + 1, len(lines)) if lines[i].strip() == "```yaml"]
    if not opens:
        sys.exit(f"ABORT: no ```yaml fence below the '## 8 ' heading in {path}")
    open_i = opens[0]

    closes = [i for i in range(open_i + 1, len(lines)) if lines[i].strip() == "```"]
    if not closes:
        sys.exit(f"ABORT: unterminated ```yaml fence in {path}")
    close_i = closes[0]

    body = lines[open_i + 1:close_i]
    coords = (f"heading :{head + 1} | fence open :{open_i + 1} close :{close_i + 1} | "
              f"body :{open_i + 2}-{close_i} = {len(body)} lines")
    return body, coords


def reserved_keys(body):
    """Read the reserved-key list out of the block's own meta-rule comment.

    The whole point of that comment is that a reader hard-codes nothing, so
    this harness eats its own dog food. No fallback: a missing comment is a
    failure, not a reason to guess.
    """
    for line in body:
        s = line.strip()
        if s.startswith("#") and "are reserved" in s:
            names = re.findall(r"`([a-z_-]+)`", s)
            if names:
                return set(names)
    return None


# --- check 4 needs its own loader --------------------------------------------

class DupDetectLoader(yaml.SafeLoader):
    pass


_dupes = []


def _construct_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            _dupes.append(key)
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


DupDetectLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)


# --- the meta-rule walk (shared by 3c and 3d) --------------------------------

def walk_specs(families, reserved):
    """Reach every spec using only the block's own meta-rule.

    Drop reserved keys; a remaining key whose value is a mapping is a subtype,
    so the family's specs are its subtypes; a family with no subtypes is its
    own spec. No key name is written into this function.
    """
    specs, errors = {}, []
    for fam, body in families.items():
        if not isinstance(body, dict):
            errors.append(f"{fam}: family body is {type(body).__name__}, not a mapping")
            continue
        subtypes = {k: v for k, v in body.items()
                    if k not in reserved and isinstance(v, dict)}
        if subtypes:
            for name, sub in subtypes.items():
                specs[f"{fam}.{name}"] = sub
        else:
            specs[fam] = body
    return specs, errors


def open_key_table(doc):
    """The block's open keys, derived the way the block says to derive them.

    An open key is a key section 8 declares legal on every note while declaring
    nothing about its values. The rule for finding the table is the same one the
    shipped reader uses (a top-level mapping whose values are all one-line
    strings), written independently here for the same reason check 5 exists: two
    implementations that must agree catch a drift that one cannot. No key name is
    typed into this harness, so a rename in the block carries.
    """
    tables = [v for v in doc.values()
              if isinstance(v, dict) and v and all(isinstance(x, str) for x in v.values())]
    if len(tables) != 1:
        return {}
    return dict(tables[0])


def closed_lists(families, reserved):
    """Every in-family closed list, as (path, owning-spec-name, field-name)."""
    out = []
    for fam, body in families.items():
        if not isinstance(body, dict):
            continue
        for k, v in body.items():
            if k in reserved:
                continue
            if isinstance(v, list):
                out.append((f"{fam}.{k}", fam, k))
            elif isinstance(v, dict):
                for k2, v2 in v.items():
                    if k2 in reserved:
                        continue
                    if isinstance(v2, list):
                        out.append((f"{fam}.{k}.{k2}", f"{fam}.{k}", k2))
    return out


# --- the seven checks ----------------------------------------------------------

def check1(parsed):
    print("CHECK 1 - the block parses with yaml.safe_load")
    for label, (doc, _) in parsed.items():
        if doc is None:
            fail("1", label, "parsed to None")
            continue
        keys = list(doc.keys())
        print(f"    {label:8s} OK   top-level keys = {keys}")
        if "families" not in doc:
            fail("1", label, f"no 'families' key; got {keys}")


def check2(template_body):
    print("CHECK 2 - three rendered variants of the template")
    text = "\n".join(template_body)
    if PLACEHOLDER not in text:
        fail("2", "template", f"{PLACEHOLDER} not present; nothing to render")
        return
    for tag in RENDER_TAGS:
        try:
            doc = yaml.safe_load(text.replace(PLACEHOLDER, tag))
        except yaml.YAMLError as exc:
            fail("2", f"template[{tag}]", f"parse error: {exc}")
            continue
        domain = doc.get("domain")
        want = ["#personal", f"#{tag}"]
        if domain != want:
            fail("2", f"template[{tag}]", f"domain = {domain}, expected {want}")
        else:
            print(f"    {tag:16s} OK   domain = {domain}")


def check3(parsed, reserved):
    print("CHECK 3 - the rules that were moved out of comments are reachable in the parsed structure")
    for label, (doc, _) in parsed.items():
        fams = doc.get("families", {})

        # 3a - the personal lanes, via the extending key
        decision = fams.get("record", {}).get("decision", {})
        ext = None
        for k in reserved:
            if k in decision and isinstance(decision[k], dict) and "lane" in decision[k]:
                ext = decision[k]["lane"]
                break
        if ext is None:
            fail("3a", label, "no reserved key on record.decision carries an extending lane list")
        elif len(ext) != EXPECT_PERSONAL_LANES:
            fail("3a", label, f"{len(ext)} personal lanes, expected {EXPECT_PERSONAL_LANES}: {ext}")
        else:
            legal = list(doc.get("lane", [])) + list(ext)
            if len(set(legal)) != EXPECT_DECISION_LANES:
                fail("3a", label,
                     f"a decision has {len(set(legal))} legal lane values, expected {EXPECT_DECISION_LANES}: {legal}")
            else:
                print(f"    3a {label:8s} personal lanes = {ext}")
                print(f"       {'':8s} legal lanes for a decision = {legal}")

        # 3b - multi-value fields
        specs, errors = walk_specs(fams, reserved)
        multi = {name: spec["multi"] for name, spec in specs.items()
                 if isinstance(spec, dict) and "multi" in spec}
        if multi != EXPECT_MULTI:
            fail("3b", label, f"multi fields = {multi}, expected {EXPECT_MULTI}")
        else:
            print(f"    3b {label:8s} multi fields = {multi}")

        # 3c - one uniform walk reaches every spec, no exceptions
        skipped = [n for n, s in specs.items() if not isinstance(s, dict) or "required" not in s]
        if errors:
            fail("3c", label, f"walk errors: {errors}")
        if skipped:
            fail("3c", label, f"specs with no reachable 'required': {skipped}")
        if len(specs) != EXPECT_SPECS:
            fail("3c", label, f"{len(specs)} specs reached, expected {EXPECT_SPECS}: {sorted(specs)}")
        if not errors and not skipped and len(specs) == EXPECT_SPECS:
            print(f"    3c {label:8s} {len(specs)} specs reached, 0 skipped, 0 exceptions")

        # 3d - every closed list is keyed by a field its own spec declares
        lists = closed_lists(fams, reserved)
        bad = []
        for path, owner, field in lists:
            spec = specs.get(owner)
            if spec is None:
                # a family-level list on a family whose specs are its subtypes;
                # the field must be declared by every one of those subtypes
                subs = [s for n, s in specs.items() if n.startswith(owner + ".")]
                declared = subs and all(
                    field in (s.get("required", []) or []) + (s.get("optional", []) or [])
                    for s in subs)
            else:
                declared = field in (spec.get("required", []) or []) + (spec.get("optional", []) or [])
            if not declared:
                bad.append(path)
        if len(lists) != EXPECT_IN_FAMILY_CLOSED_LISTS:
            fail("3d", label,
                 f"{len(lists)} in-family closed lists, expected {EXPECT_IN_FAMILY_CLOSED_LISTS}: {[p for p, _, _ in lists]}")
        if bad:
            fail("3d", label, f"closed lists not keyed by a field their spec declares: {bad}")
        globals_ = [k for k, v in doc.items() if k != "families" and isinstance(v, list)]
        if len(globals_) != EXPECT_GLOBAL_CLOSED_LISTS:
            fail("3d", label,
                 f"{len(globals_)} global closed lists, expected {EXPECT_GLOBAL_CLOSED_LISTS}: {globals_}")
        if not bad and len(lists) == EXPECT_IN_FAMILY_CLOSED_LISTS and len(globals_) == EXPECT_GLOBAL_CLOSED_LISTS:
            print(f"    3d {label:8s} {len(lists)} in-family closed lists, all keyed by a declared field; "
                  f"{len(globals_)} global ({globals_})")

        # 3e - the lab cardinality
        card = None
        for k in reserved:
            v = fams.get("lab", {}).get(k)
            if isinstance(v, dict) and "count" in v:
                card = v
                break
        if card != EXPECT_LAB_CARDINALITY:
            fail("3e", label, f"lab cardinality = {card}, expected {EXPECT_LAB_CARDINALITY}")
        else:
            print(f"    3e {label:8s} lab cardinality = {card}")

        # 3f - a reserved key stranded at a family level that has subtypes.
        # The meta-rule says a family with subtypes contributes its subtypes and
        # not itself, so a `required` / `optional` / `multi` / `marker` written
        # beside the family NAME is dropped on the floor: it enforces nothing and
        # nothing raises, which is the quiet failure this check exists to make
        # loud. Which keys those are is derived, not typed: they are the reserved
        # keys the shipped reader keeps a slot for on one Spec. `cardinality` is
        # not among them and is legitimately family-level (see 3e); a family-level
        # closed LIST is legitimate too and still reaches every subtype, which is
        # why only the slot keys are looked at here.
        per_spec = set(doctrine_schema.Spec.__slots__) & set(reserved)
        stranded = []
        for fam, body in fams.items():
            if not isinstance(body, dict):
                continue
            has_subtypes = any(k not in reserved and isinstance(v, dict)
                               for k, v in body.items())
            if not has_subtypes:
                continue          # the family IS its own spec, so these are read
            stranded += [f"{fam}.{k}" for k in sorted(per_spec & set(body))]
        if stranded:
            fail("3f", label,
                 "reserved key(s) written at a family level that has subtypes, so "
                 f"the reader drops them and they enforce nothing: {stranded}. "
                 "Move each one onto every subtype's own line.")
        else:
            print(f"    3f {label:8s} nothing stranded at a family level "
                  f"({', '.join(sorted(per_spec))} checked on {len(fams)} families)")


def check4(bodies):
    print("CHECK 4 - duplicate keys silently swallowed?")
    for label, body in bodies.items():
        del _dupes[:]
        try:
            yaml.load("\n".join(body), Loader=DupDetectLoader)
        except yaml.YAMLError as exc:
            fail("4", label, f"parse error under the duplicate-detecting loader: {exc}")
            continue
        if _dupes:
            fail("4", label, f"duplicate keys silently collapsed: {sorted(set(_dupes))}")
        else:
            print(f"    {label:8s} duplicate keys: NONE")


def check5(body, reserved, specs, open_names):
    """The shipped reader agrees with this harness's own walk.

    Everything above walks the block using code written in THIS file. The
    product walks it using my-second-brain/scripts/doctrine_schema.py. Two
    implementations of one meta-rule can drift, and if they do, this harness is
    the one that lies (it goes green, the vault's checker raises). So the last
    check hands the same body to the real reader and compares what comes back.
    """
    print("CHECK 5 - the shipped reader (doctrine_schema.py) reaches the same shape")
    before = len(failures)
    text = "\n".join(body)
    try:
        schema = doctrine_schema.parse_block(text, source="template")
    except doctrine_schema.SchemaError as exc:
        fail("5", "doctrine_schema", f"the shipped reader could not read the block: {exc}")
        return
    print(f"    reader   {schema}")

    if schema.reserved != reserved:
        fail("5", "doctrine_schema",
             f"reserved keys differ: reader {sorted(schema.reserved)} vs "
             f"harness {sorted(reserved)}")
    if set(schema.specs) != set(specs):
        only_reader = sorted(set(schema.specs) - set(specs))
        only_harness = sorted(set(specs) - set(schema.specs))
        fail("5", "doctrine_schema",
             f"the two walks reach different specs; reader-only={only_reader}, "
             f"harness-only={only_harness}")
        return
    for name in sorted(specs):
        raw, spec = specs[name], schema.specs[name]
        for field in ("required", "optional", "multi"):
            mine = list(raw.get(field) or [])
            if field == "optional":
                # An open key is legal on every note, so the reader puts it on
                # every spec's optional: that is the side an enforcer reads when
                # it counts keys section 8 has not declared. The harness walk
                # reads the raw block, so it applies the same rule here rather
                # than expecting the two lists to differ. Same order as the
                # reader's, appended after what the spec itself declares.
                mine += [k for k in open_names
                         if k not in mine and k not in (raw.get("required") or [])]
            theirs = list(getattr(spec, field))
            if mine != theirs:
                fail("5", f"doctrine_schema[{name}]",
                     f"'{field}' differs: reader {theirs} vs harness {mine}")
    if not schema.marker_key or not schema.type_key:
        fail("5", "doctrine_schema",
             f"the reader derived no mounting key(s): marker={schema.marker_key!r} "
             f"type={schema.type_key!r}; nothing in a vault could be mounted")
    else:
        print(f"    reader   mounting keys derived: marker={schema.marker_key!r} "
              f"type={schema.type_key!r}")
        print(f"    reader   {len(schema.specs)} specs, "
              f"{len(schema.by_marker)} mounted by marker, "
              f"{len(schema.by_type)} values mounted by {schema.type_key!r}")
    if len(failures) == before:
        print(f"    agreement: {len(specs)} specs, identical required/optional/multi "
              f"on every one")


def _closed_list_slots(obj):
    """The slots on a parsed object where a closed list can actually sit.

    Derived, not typed, the same way 3f derives its slot names from
    `Spec.__slots__`: a slot holding a mapping of field name to a LIST of values
    IS a closed list, whatever it is called. Rename `enums` or `globals` and this
    follows the rename instead of going quietly blind.
    """
    out = []
    for slot in type(obj).__slots__:
        v = getattr(obj, slot, None)
        if isinstance(v, dict) and v and all(isinstance(x, list) for x in v.values()):
            out.append(slot)
    return out


def check7(body, open_names):
    """An open key is legal everywhere and closed nowhere.

    Section 8 can declare a key legal on every note while saying nothing about
    its values (`tags` is the one that ships). The whole worth of that sentence
    is WHERE the name lands inside the shipped reader, so this check reads the
    reader's own parse rather than the block:

      * on the known side of every spec, which is what lets the exemption live
        in section 8 instead of inside an enforcer. The frontmatter guard
        carried `k != "tags"` in its own source until 2026-08-21; that line is
        gone, and this is the check that keeps it gone.
      * in no closed list, anywhere. A closed list on an open key would mean the
        block declares the values ungoverned and then measures them against a
        list, and because the name sits in `optional` the reader's `declares()`
        says True for it, so such a list WOULD be enforced.

    The second half is proved twice: the shipped block is inspected, and then a
    doctored copy that gives an open key a closed list is handed to the reader,
    which has to refuse it. A rule nobody has watched refuse anything is a rule
    nobody has watched run.
    """
    print("CHECK 7 - open keys: known on every spec, closed nowhere")
    if not open_names:
        print("    template  no open keys declared in the block; nothing to check")
        return
    text = "\n".join(body)
    try:
        schema = doctrine_schema.parse_block(text, source="template")
    except doctrine_schema.SchemaError as exc:
        fail("7", "doctrine_schema", f"the shipped reader could not read the block: {exc}")
        return

    slots = sorted(set(_closed_list_slots(schema)) |
                   {s for spec in schema.specs.values() for s in _closed_list_slots(spec)})
    closed, unknown = [], []
    for name in open_names:
        for slot in _closed_list_slots(schema):
            if name in getattr(schema, slot):
                closed.append(f"schema.{slot}[{name!r}]")
        for spec_name in sorted(schema.specs):
            spec = schema.specs[spec_name]
            for slot in _closed_list_slots(spec):
                if name in getattr(spec, slot):
                    closed.append(f"{spec_name}.{slot}[{name!r}]")
            if not spec.declares(name):
                unknown.append(f"{spec_name}:{name}")
    if closed:
        fail("7", "template",
             "open key(s) also carry a closed list, so the block declares their "
             f"values ungoverned and enforces them anyway: {sorted(set(closed))}")
    if unknown:
        fail("7", "template",
             "open key(s) missing from the known side of some spec(s), so an "
             "enforcer counting undeclared keys still reports them there: "
             f"{unknown[:8]}{' ...' if len(unknown) > 8 else ''}")
    if not closed and not unknown:
        print(f"    template  {sorted(open_names)} known on all {len(schema.specs)} specs, "
              f"in 0 closed lists (slots checked: {', '.join(slots)})")

    # The refusal, run rather than described.
    name = sorted(open_names)[0]
    doctored = f"{text}\n{name}: [{name}-closed-by-a-doctored-block]\n"
    try:
        doctrine_schema.parse_block(doctored, source="doctored")
    except doctrine_schema.SchemaError as exc:
        print(f"    doctored  '{name}:' given a closed list -> reader refuses: "
              f"{str(exc).split('.')[0]}.")
    else:
        fail("7", "doctrine_schema",
             f"a block declaring {name!r} open AND giving it a closed list was "
             "accepted; the reader picked one meaning silently, and the closed "
             "list would be enforced on every note")


def check6(parsed, bodies):
    print(f"CHECK 6 - family count is still {EXPECT_FAMILIES}")
    for label, body in bodies.items():
        by_indent = [l for l in body if re.match(r"^  [a-z-]+:", l)]
        by_parse = len(parsed[label][0].get("families", {}))
        if len(by_indent) != EXPECT_FAMILIES or by_parse != EXPECT_FAMILIES:
            fail("6", label,
                 f"exactly-two-space keys = {len(by_indent)}, len(families) = {by_parse}, "
                 f"expected {EXPECT_FAMILIES} both ways")
        else:
            names = list(parsed[label][0]["families"].keys())
            print(f"    {label:8s} exactly-two-space keys = {len(by_indent)}   "
                  f"len(families) = {by_parse}   match=True")
            print(f"    {'':8s} {names}")


# --- main --------------------------------------------------------------------

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    default_template = os.path.join(
        here, os.pardir, "my-second-brain", "templates", "structure-doctrine.template.md")

    ap = argparse.ArgumentParser(description="Acceptance harness for doctrine section 8.")
    ap.add_argument("--template", default=os.path.normpath(default_template),
                    help="the doctrine template to check (default: this repo's)")
    args = ap.parse_args()

    print(f"PyYAML {yaml.__version__} at {yaml.__file__}")
    print(f"reader  {doctrine_schema.__file__}")
    print()

    print("COORDINATES (located at run time, never hard-coded)")
    body, coords = locate_block(args.template)
    bodies = {"template": body}
    print(f"    template  {coords}")
    print(f"              {args.template}")
    print()

    reserved = reserved_keys(body)
    if not reserved:
        sys.exit(
            "ABORT: the block no longer says which of its keys are reserved, so this run would "
            "be checking something other than what the block says.\n"
            "  LOOKED FOR: one comment line inside the ```yaml block, above `families:`, holding "
            "the words 'are reserved' and every reserved key in backticks on that same line:\n"
            "      # Inside a family, `required` `optional` `marker` `multi` `extends` "
            "`cardinality` are reserved\n"
            "  LIKELY CAUSE: that comment was reworded. It is an interface, not prose (both this "
            "harness and the shipped reader take the reserved-key list out of it), so dropping the "
            "backticks, splitting the names over two lines, or losing the exact words 'are "
            "reserved' each break it while the section still looks fine.\n"
            "  FIX: restore the names in backticks on the 'are reserved' line; the surrounding "
            "wording is free. `git diff` on the template shows what changed.\n"
            "  NO FALLBACK ON PURPOSE: a built-in copy of those names here would be the second "
            "copy section 8 forbids, and it would rot without raising. Same message and same "
            "reasoning as the shipped reader, scripts/doctrine_schema.py.")
    print(f"RESERVED KEYS (read from the block's own comment, not hard-coded): {sorted(reserved)}")
    print()

    parsed = {}
    try:
        parsed["template"] = (yaml.safe_load("\n".join(body)), body)
    except yaml.YAMLError as exc:
        fail("1", "template", f"parse error: {exc}")
        parsed["template"] = (None, body)

    check1(parsed)
    print()
    check2(body)
    print()
    check3({k: v for k, v in parsed.items() if v[0]}, reserved)
    print()
    check4(bodies)
    print()
    specs, _ = walk_specs((parsed["template"][0] or {}).get("families", {}), reserved)
    open_names = open_key_table(parsed["template"][0] or {})
    check5(body, reserved, specs, open_names)
    print()
    check6(parsed, bodies)
    print()
    check7(body, open_names)
    print()

    if failures:
        print(f"FAILURES: {len(failures)}")
        for check, where, detail in failures:
            print(f"  [check {check}] {where}: {detail}")
        return 1

    print("FAILURES: none")
    print("PASS - seven checks against the single source.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
