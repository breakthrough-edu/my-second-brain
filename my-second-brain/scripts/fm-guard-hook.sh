#!/bin/bash
# fm-guard-hook.sh  (My Second Brain frontmatter guard)
# Claude Code and Codex PreToolUse hook (matchers: Write, apply_patch, Bash). READ-ONLY.
#
# MSB-GUARD: key=fm_guard_installed installs-as=my-second-brain-fm-guard.sh matchers=Write,Bash name=frontmatter-guard does=checks a new note's filename and frontmatter against the doctrine before it lands
# MSB-PROBE: expect=block stdin={"tool_name":"Write","tool_input":{"file_path":"{{VAULT}}/00_Inbox/Guard-Probe.md","content":"---\ntype: msb-install-probe-not-a-real-family\nstatus: active\n---\n"}}
# MSB-PROBE: expect=block stdin={"tool_name":"Bash","tool_input":{"command":"cat > {{VAULT}}/00_Inbox/Guard-Probe-Bash.md <<'EOF'\n---\ntype: x\n---\nEOF"},"cwd":"{{VAULT}}"}
# MSB-PROBE: expect=allow stdin={"tool_name":"Bash","tool_input":{"command":"cat {{VAULT}}/99_Meta/filing-log.md 2>/dev/null | head"},"cwd":"{{VAULT}}"}
#
# ⭐ THAT FIRST LINE IS THE REGISTRY ENTRY FOR THIS GUARD, AND THE THREE AFTER IT
#   ARE ITS BEHAVIOURAL PROBES (both formats, and why the probe exists at all, are
#   documented at the top of rm-guard-hook.sh). ⚠️ `matchers=Write,Bash` is the
#   one that has to be read rather than assumed: this guard is HALF-INSTALLED if
#   it is registered under only one of them, and half-installed reads as done to
#   everything except a check that knows there should be two.
#
# ⭐ WHY THE PROBE IS A FRONTMATTER CASE AND NOT A FILENAME CASE. This guard has
#   two gates and only one of them can die quietly. The filename gate is pure
#   string work and always runs; the frontmatter gate needs section 8, which
#   needs scripts/doctrine_schema.py, which needs PyYAML, and when PyYAML is
#   absent this guard FAILS OPEN (see the block below) and says so only in
#   injected context nobody reads during an install. So a probe with an illegal
#   NAME passes on a machine where the schema gate is stone dead, and reports
#   the guard as working. The declared probe therefore carries a legal name and
#   an undeclared `type:`: the only thing that can refuse it is section 8, read
#   live, just now. ⛔ Do not "simplify" it into a filename case.
#   The two Bash probes are a pair: a heredoc birth it must refuse, and a read
#   of an existing note (with `2>/dev/null`) it must let through. The second is
#   there because the old Bash rule blocked on MENTION, and a guard that blocks
#   reads passes every block probe while getting itself switched off.
#   scripts/fm_guard_probes.py runs the full case table against a copy.
#
# WHAT IT IS
#   The "blocks" layer of the three the doctrine names in §5: templates teach,
#   the frontmatter guard blocks, the checker sweeps. It sits between a session
#   and the vault and judges what is about to be written, which is the only
#   moment a bad shape is cheap to stop.
#
# FOUR SURFACES, ONE GUARD
#   Write or apply_patch   filename gate + frontmatter gate; on a pass it injects
#                          the filing protocol so the session files by the law
#                          rather than from memory.
#   Bash, new note         a shell command whose WRITE TARGET is a NEW .md inside
#                          the vault is BLOCKED and pointed back at Write: the
#                          target of `>` `>>` `>|` `&>`, a `tee` file, the
#                          destination of `cp` / `install`, a `mv` from outside
#                          the vault, and the same inside `bash -c '...'`,
#                          resolved against the payload cwd, `cd` and `$VAR`.
#                          Reads, edits and appends to notes that already
#                          exist, and writes outside the vault all pass. Not
#                          because shell is dirty, but because this guard can
#                          read a Write's content and cannot read a heredoc's, so
#                          a birth through the shell is where the frontmatter
#                          gate is blind. Blocking it keeps one door instead of
#                          two. A target it cannot resolve passes with a note.
#   Bash `mv`              allowed, with the link-rescan discipline injected
#                          (§3: a move rewrites its own inbound links).
#   Bash `mkdir`           allowed, with "update Home.md's directory; an empty
#                          room gets no door" injected.
#
# TWO SEVERITIES, AND THE LINE BETWEEN THEM IS THE DOCTRINE'S, NOT OURS
#   §0 item 3 draws it in one sentence: a hard schema violation (a bad filename,
#   a missing required key, a value outside a closed list) is blocked; a key §8
#   has not declared is a JUDGMENT CALL and gets flagged to the session instead.
#   So this guard blocks the first list and only ever injects context for the
#   second. A guard that blocks judgment calls gets switched off in week one, and
#   a switched-off guard enforces nothing.
#
# WHERE THE LAW COMES FROM
#   Section 8 of the vault's own 99_Meta/structure-doctrine.md, read live through
#   scripts/doctrine_schema.py, the same reader the weekly checker uses. There is
#   no copy of any family, required key or closed list in this file. Two enforcers
#   reading one source cannot drift apart; two enforcers with two copies always do.
#
# ⛔ IF THE LAW CANNOT BE READ, THIS GUARD DOES NOT BLOCK.
#   It fails OPEN on the frontmatter gate and says loudly in the injected context
#   that it did. The reasoning is not symmetrical with the checker's: the checker
#   REPORTS, so an unread schema must become an error nobody can mistake for a
#   clean bill. This guard STOPS WORK, and a guard that cannot read the law but
#   blocks anyway would wedge a session with no way forward. Loud and open beats
#   silent and stuck. The filename gate has no such dependency and still applies.
#
# INSTALL: setup replaces the two placeholder values below, then registers this
#   script under PreToolUse for both the Write and Bash matchers.
# UNINSTALL: remove those entries (and delete the file).
#
# Exit 0 = allow (stdout JSON may carry injected context). Exit 2 = block.

INPUT="$(cat)"

HOOK_STDIN="$INPUT" \
MSB_VAULT_PATHS="__MSB_VAULT_PATHS__" \
MSB_SKILL_DIR="__MSB_SKILL_DIR__" \
/usr/bin/env python3 <<'PYEOF'
import sys, json, os, re, shlex

def allow():
    sys.exit(0)

def allow_with(context):
    """Allow, and hand the session a note it has to read before it files."""
    json.dump({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "additionalContext": context}}, sys.stdout)
    sys.exit(0)

def block(reason):
    sys.stderr.write(reason + "\n")
    sys.exit(2)

try:
    data = json.loads(os.environ.get("HOOK_STDIN", "") or "{}")
except Exception:
    allow()

tool = data.get("tool_name") or ""
tin = data.get("tool_input") or {}

# --- where this vault is, and where the reader lives ------------------------
# Sentinels built by concatenation so the real placeholder token appears on the
# env lines above and nowhere else; a find-and-replace at install time therefore
# cannot corrupt this guard against a botched install.
_VP = "__MSB_" "VAULT_PATHS__"
_SD = "__MSB_" "SKILL_DIR__"

vault_roots = []
for part in (os.environ.get("MSB_VAULT_PATHS", "") or "").split(":"):
    part = part.strip()
    if part and part != _VP:
        vault_roots.append(os.path.realpath(os.path.expanduser(os.path.expandvars(part))))

skill_dir = (os.environ.get("MSB_SKILL_DIR", "") or "").strip()
if skill_dir == _SD:
    skill_dir = ""

# Not a vault path, not our business. This guard never speaks about files
# outside the vault it was installed for.
def in_vault(path):
    if not path or not vault_roots:
        return None
    p = os.path.realpath(os.path.abspath(os.path.expanduser(path)))
    for root in vault_roots:
        if p == root or p.startswith(root + os.sep):
            return root
    return None

# --- the exemption table, copied from nowhere -------------------------------
# ⛔ This is the checker's `scan_skip_dirs` default, and it is here because
# every enforcer that walks a vault has to agree on what is not live
# content, and this list is the shared answer. A template full
# of {{PLACEHOLDER}} is not a schema violation; blocking writes into Templates/
# would make the product unable to ship its own templates. 99_Meta/Skills/ is
# the same class of case from the other direction: a generated skill package's
# SKILL.md carries a skill's own frontmatter (`name`, `description`), which is
# not a section 8 family and was never meant to be one, so section 8 has no
# verdict to give on it and a guard that judged it anyway would refuse the
# product's own generated skills.
# ⚠️ references/scaffold-spec.md's `home-is-true` check carries an exempt list
# that reads much like this one, and they are two mechanisms answering two
# questions: that list decides whether Home.md has to name a folder, this one
# decides whether section 8 judges a note inside it. The membership overlaps
# because the same folders are machinery in both senses. ⛔ Keep the two apart.
EXEMPT_DIRS = ("98_Archive", "99_Meta/Skills", "99_Meta/Templates",
               "99_Meta/memory-archive", "99_Meta/auto-memory")

def exempt(root, path):
    rel = os.path.relpath(os.path.realpath(os.path.abspath(path)), root)
    return any(rel == d or rel.startswith(d + os.sep) for d in EXEMPT_DIRS)

# --- the one protocol sentence ----------------------------------------------
# ⭐ Fixed text, injected verbatim on every pass. Its whole value is that it is
# the same three lines every time: a session that has drifted gets re-pointed at
# the law rather than at this guard's opinion of the law.
PROTOCOL = (
    "Filing protocol (from the frontmatter guard, injected on every note this "
    "session creates):\n"
    "  1. Before this lands, run the doctrine's filing decision tree "
    "(99_Meta/structure-doctrine.md §0) top to bottom and stop at the first hit.\n"
    "  2. If the tree does not decide it, STOP and propose to the owner. Do not "
    "force a family, do not invent frontmatter.\n"
    "  3. Once it lands, append one line to 99_Meta/filing-log.md: "
    "date, what, where, which rule decided it.")

# --- filename law (doctrine §5) ---------------------------------------------
# Only the parts §5 states as absolutes are enforced here. "Dated records are
# YYYY-MM-DD-keyword-slug" is NOT among them: which families are dated records
# is a judgment §8 does not encode, so this guard leaves it to §5 and the owner
# instead of enforcing it.
BARE_NOUNS = {
    "notes", "note", "findings", "decisions", "tasks", "ideas", "misc",
    "stuff", "temp", "draft", "drafts", "untitled", "new", "doc", "docs",
    "readme", "index", "summary", "output", "data", "info",
}

def filename_problems(root, path):
    base = os.path.basename(path)
    stem = base[:-3] if base.endswith(".md") else base
    out = []
    if " " in base:
        out.append("the name contains a space. §5: names are English, "
                   "hyphenated, no spaces. Try %r." % (stem.replace(" ", "-") + ".md"))
    if stem.lstrip("_").lower() in BARE_NOUNS:
        out.append("%r is a bare generic noun, banned by §5: a name that could "
                   "belong to any note belongs to no note. Name it after what "
                   "this one specifically is." % base)
    if base.startswith("_"):
        folder = os.path.dirname(os.path.abspath(path))
        try:
            others = [f for f in os.listdir(folder)
                      if f.startswith("_") and f.endswith(".md") and f != base]
        except OSError:
            others = []
        if others:
            out.append("§5 allows at most one `_`-prefixed door per folder, and "
                       "%s already holds %s. A folder with two doors breaks the "
                       "glob every agent uses to find the one."
                       % (os.path.basename(folder) or "that folder", ", ".join(sorted(others))))
    return out

# --- the door doorbell (a folder that has earned a guide) -------------------
def doorbell(root, path):
    """Two or more .md files and not one door means this folder now needs one.

    ⚠️ The test is "no `_`-prefixed file", NOT "no `_*-Guide.md`": a project
    folder's door is its Brief, and a check that only looked for Guides would
    ring the bell forever on every project in the vault."""
    folder = os.path.dirname(os.path.abspath(path))
    if exempt(root, folder):
        return None
    try:
        entries = [f for f in os.listdir(folder) if f.endswith(".md")]
    except OSError:
        return None
    if os.path.basename(path) not in entries:
        entries.append(os.path.basename(path))
    if len(entries) >= 2 and not any(f.startswith("_") for f in entries):
        return ("This folder is about to hold %d notes and has no `_`-prefixed "
                "door. §5: a folder that needs explaining carries exactly one. "
                "Offer to add the right one (a `_<Name>-Guide.md` for a room or "
                "lane, a `_<Project>-Brief.md` for a project) before moving on."
                % len(entries))
    return None

# --- the schema gate ---------------------------------------------------------
def load_schema(root):
    """(schema, why_not). Never raises: a guard that crashes blocks everything."""
    if not skill_dir:
        return None, "the guard was installed without a path to the section 8 reader"
    sys.path.insert(0, os.path.join(skill_dir, "scripts"))
    try:
        import doctrine_schema
    except Exception as e:
        return None, "the section 8 reader could not be imported (%s)" % e
    try:
        return doctrine_schema.load_schema(root), None
    except Exception as e:
        return None, str(e)

def parse_fm(text):
    """Reuse the checker's frontmatter parser so the two agree byte for byte."""
    if not skill_dir:
        return {}
    sys.path.insert(0, os.path.join(skill_dir, "scripts"))
    try:
        import checkup
        return checkup.parse_frontmatter(text)
    except Exception:
        return {}

def schema_gate(root, path, content):
    """Returns (block_reason_or_None, context_note_or_None)."""
    fm = parse_fm(content)
    if not fm:
        return None, ("This note is about to land with no frontmatter. Every "
                      "family in §8 requires at least a type or a marker; check "
                      "§0 for which family this is and give it one.")

    schema, why_not = load_schema(root)
    if schema is None:
        # ⛔ Fails OPEN, loudly. See the header: this guard stops work, so an
        # unreadable law must not become an unopenable door.
        return None, ("⚠️ The frontmatter guard could not read section 8 of the "
                      "doctrine (%s), so it checked this note's NAME only and "
                      "let its frontmatter through unchecked. Do not read this "
                      "as approval. Verify the shape against §8 by hand, and "
                      "tell the owner the guard is running half-blind." % why_not)

    spec = schema.spec_for(fm)
    if spec is None:
        mkey, tkey = schema.marker_key, schema.type_key
        declared = fm.get(mkey) if mkey in fm else fm.get(tkey)
        return ("BLOCKED by the frontmatter guard: %r is not a shape section 8 "
                "declares, so this note has no law to be checked against and "
                "must not land (doctrine §0, item 3: if no family fits, STOP).\n"
                "The legal way to widen the schema, in order:\n"
                "  1. Re-read §0's decision tree; most notes are an existing "
                "family wearing an unfamiliar name.\n"
                "  2. If it genuinely is new: write a template for it, add its "
                "row to §8, get the owner's yes, then file. §8 is amended by "
                "propose-and-approve; it is never widened by a note that "
                "arrived first.\n"
                "  The breakthrough-vault-guardian skill, if this vault has it, carries "
                "that whole change, including the files outside §8 that it "
                "touches."
                % declared, None)

    try:
        import doctrine_schema
        problems = doctrine_schema.validate(fm, spec, schema)
    except Exception:
        return None, None
    if problems:
        lines = "\n".join("  - %s" % m for _, m in problems)
        legal = ("required: %s" % ", ".join(spec.required)) if spec.required else ""
        if spec.optional:
            legal += "\n  optional: %s" % ", ".join(spec.optional)
        for f in sorted(spec.enums):
            if spec.declares(f):
                legal += "\n  %s must be one of: %s" % (
                    f, ", ".join(str(v) for v in spec.enums[f]))
        return ("BLOCKED by the frontmatter guard: this note claims to be a %r "
                "but does not match what §8 declares for one.\n%s\n"
                "What §8 declares for a %s, read live from this vault's own "
                "doctrine just now:\n  %s\n"
                "Two legal ways forward, and filing around it is neither:\n"
                "  1. The note is wrong: correct it to the shape above.\n"
                "  2. The LAW is wrong (this shape genuinely needs a key or a "
                "value §8 does not have): say so to the owner and amend §8 "
                "first, propose-and-approve."
                % (spec.name, lines, spec.name, legal), None)

    # A key §8 has not declared: a judgment call, so it is flagged, not blocked.
    known = set(spec.required) | set(spec.optional) | set(spec.enums)
    if schema.marker_key:
        known.add(schema.marker_key)
    if schema.type_key:
        known.add(schema.type_key)
    extra = [k for k in fm if k not in known]
    notes = []
    if extra:
        notes.append("This %s carries key(s) §8 has not declared: %s. That is a "
                     "judgment call, not a violation. If this kind of note "
                     "always carries them, propose registering them in §8; if "
                     "they were invented just now, drop them."
                     % (spec.name, ", ".join(sorted(extra))))

    # Closeout: a brief going done or killed is the moment its reusable output
    # is still fresh enough to be worth distilling.
    st = fm.get("status")
    if isinstance(st, str) and st.strip() in ("done", "killed") and "status" in spec.enums:
        notes.append("This note's status is going to %r. Before closing it out, "
                     "offer the distillation pass: is there anything here that "
                     "graduates into a lesson, a playbook, or an entity note "
                     "that outlives the project? Closing without asking is how "
                     "the reusable half gets buried with the project."
                     % st.strip())
    return None, ("\n\n".join(notes) if notes else None)

# ===========================================================================
# Surface 1: Write or Codex apply_patch
# ===========================================================================
def check_new_markdown(path, content):
    """Returns (block_reason_or_None, context_or_None) for a new Vault note."""
    if not path.endswith(".md"):
        return None, None
    root = in_vault(path)
    if root is None:
        return None, None
    if exempt(root, path):
        return None, None  # templates, archives, and skill packages are not live content
    if os.path.exists(path):
        return None, None  # an edit, not a birth; this guard watches births

    problems = filename_problems(root, path)
    if problems:
        return ("BLOCKED by the frontmatter guard: the filename breaks doctrine §5.\n"
                + "\n".join("  - %s" % p for p in problems)
                + "\n§5 is the law on names; rename and write again."), None

    reason, note = schema_gate(root, path, content)
    if reason:
        return reason, None

    parts = [PROTOCOL]
    bell = doorbell(root, path)
    if bell:
        parts.append(bell)
    if note:
        parts.append(note)
    return None, "\n\n".join(parts)

def apply_patch_additions(command):
    """Yield (path, content) for each file born through Codex apply_patch."""
    path = None
    lines = []
    for line in command.splitlines():
        if line.startswith("*** Add File: "):
            if path is not None:
                yield path, "\n".join(lines)
            path = line[len("*** Add File: "):].strip()
            lines = []
        elif line.startswith("*** "):
            if path is not None:
                yield path, "\n".join(lines)
                path = None
                lines = []
        elif path is not None and line.startswith("+"):
            lines.append(line[1:])
    if path is not None:
        yield path, "\n".join(lines)

if tool == "Write":
    reason, context = check_new_markdown(
        tin.get("file_path") or "", tin.get("content") or "")
    if reason:
        block(reason)
    if context:
        allow_with(context)
    allow()

if tool == "apply_patch":
    command = tin.get("command") or ""
    if not isinstance(command, str) or not command.strip():
        allow()
    cwd = data.get("cwd") or os.getcwd()
    contexts = []
    for raw_path, content in apply_patch_additions(command):
        path = raw_path if os.path.isabs(raw_path) else os.path.join(cwd, raw_path)
        reason, context = check_new_markdown(path, content)
        if reason:
            block(reason)
        if context:
            contexts.append(context)
    if contexts:
        allow_with("\n\n".join(contexts))
    allow()

# ===========================================================================
# Surface 2-4: Bash
# ===========================================================================
if tool != "Bash":
    allow()

cmd = tin.get("command") or ""
if not isinstance(cmd, str) or not cmd.strip():
    allow()

# --- the shell analyser -------------------------------------------------------
# ⭐ The question surface 2 asks is narrow on purpose: does this command BRING A
# NEW .md INTO EXISTENCE inside the vault? Not "does it mention one". A guard
# that blocks on mention blocks reads (`cat note.md 2>/dev/null | head`),
# appends to existing state files, copies OUT of the vault, and scripts whose
# heredoc body happens to name a note, and a guard that blocks reads gets
# switched off. So the analyser finds WRITE TARGETS, resolves them the way the
# shell would (cwd, `cd`, `$VAR`), and only then asks the vault questions.
# ⛔ It is an accident net, not a sandbox. `python3 -c "open(...,'w')"`, `touch`,
# `sed -i`, `dd of=` and friends are not write targets here, by design.
WRITE_OPS = {">", ">>", ">|", "&>", "&>>"}
READ_OPS = {"<", "<<", "<<<"}          # consume one operand, never a target
DUP_OPS = {">&", "<&"}                 # fd duplication (2>&1, >&2): operand is an fd
SEPARATORS = {";", ";;", "&&", "||", "|", "|&", "&", "(", ")", "\n"}
# Longest first: shlex glues adjacent punctuation (`;\n`, `)|`, `&&\n`) into one
# token, and a glued separator that is not split back apart hides the command
# after it.
OPERATORS = ("&>>", "<<<", ";;", "&&", "||", "|&", ">>", ">|", "&>", ">&", "<&",
             "<<", ";", "&", "|", "(", ")", "<", ">", "\n")
PUNCT = "();<>|&\n"
WRAPPERS = {"sudo", "command", "nohup", "exec", "time", "builtin", "env"}
SHELLS = {"bash", "sh", "zsh", "dash"}
ASSIGN_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)=(.*)$", re.S)
HEREDOC_RE = re.compile(r"<<(-?)\s*(?:'([^']*)'|\"([^\"]*)\"|\\?([A-Za-z0-9_]+))")

def strip_heredoc_bodies(cmd):
    """Drop every heredoc BODY and every `#` comment at this shell level.

    Quote-aware: a `<<` inside quotes belongs to an inner shell (bash -c '...')
    and is left for the recursion. The `<< EOF` operator itself stays, so the
    tokenizer still sees a read op. ⚠️ Bodies go BEFORE tokenizing because a body
    is prose: one apostrophe in it and shlex refuses the whole command.
    Comments go here too, because shlex's own comment handling swallows the
    newline that ends the comment and glues the next command onto it."""
    out, pending, q, i, n = [], [], None, 0, len(cmd)
    while i < n:
        c = cmd[i]
        if c == "\\" and q != "'" and i + 1 < n:           # escape (outside '...')
            out.append(cmd[i:i + 2]); i += 2; continue
        if q is None and c in ("'", '"'):
            q = c
        elif q == c:
            q = None
        elif q is None and c == "#" and (i == 0 or cmd[i - 1] in " \t\n;&|()"):
            j = cmd.find("\n", i)                          # comment: keep the newline
            i = n if j < 0 else j
            continue
        elif q is None and cmd.startswith("<<", i) and not cmd.startswith("<<<", i):
            m = HEREDOC_RE.match(cmd, i)
            if m:
                pending.append((m.group(2) or m.group(3) or m.group(4), m.group(1) == "-"))
                out.append(m.group(0)); i = m.end(); continue
        elif c == "\n" and q is None and pending:
            out.append("\n"); i += 1
            while pending and i < n:                       # body lines: dropped
                j = cmd.find("\n", i)
                line = cmd[i:] if j < 0 else cmd[i:j]
                i = n if j < 0 else j + 1
                delim, dash = pending[0]
                if (line.lstrip("\t") if dash else line) == delim:
                    pending.pop(0)
            continue
        out.append(c); i += 1
    return "".join(out)

def _split_punct(tok):
    if not tok or any(ch not in PUNCT for ch in tok):
        return [tok]
    parts, i = [], 0
    while i < len(tok):
        for op in OPERATORS:
            if tok.startswith(op, i):
                parts.append(op); i += len(op); break
        else:
            parts.append(tok[i]); i += 1
    return parts

def tokenize(cmd):
    """Shell-ish tokens. Raises ValueError on unbalanced quotes."""
    cmd = cmd.replace("\\\n", " ")         # line continuation, before shlex sees it
    lx = shlex.shlex(cmd, posix=True, punctuation_chars=PUNCT)
    lx.whitespace = " \t\r"
    lx.whitespace_split = True
    lx.commenters = ""                     # comments were stripped, quote-aware
    out = []
    for t in lx:
        out.extend(_split_punct(t))
    return out

def segments(tokens):
    seg = []
    for t in tokens:
        if t in SEPARATORS:
            if seg:
                yield seg
            seg = []
        else:
            seg.append(t)
    if seg:
        yield seg

def analyse(cmd, cwd, env, depth=0, acc=None):
    """Walk a command the way the shell would, recording what it writes.

    acc["targets"]: (abs_path, via, sources) per write target, where sources
      holds each resolved source path or None for one that could not be
      resolved (cp/install/mv only).
    acc["unresolved"]: target words still holding `$`, a backtick or a glob.
    acc["moved"]: every resolved positional of every `mv` (surface 3).
    acc["parse_failed"]: True when some level could not be tokenized."""
    if acc is None:
        acc = {"targets": [], "unresolved": [], "moved": [], "parse_failed": False}
    if depth > 3:
        return acc
    try:
        tokens = tokenize(strip_heredoc_bodies(cmd))
    except ValueError:
        acc["parse_failed"] = True
        return acc
    vars_ = dict(env)
    vars_["PWD"] = cwd
    state = {"cur": cwd}

    def resolve(word):
        w = os.path.expanduser(word)
        w = re.sub(r"\$\{?([A-Za-z_][A-Za-z0-9_]*)\}?",
                   lambda m: vars_.get(m.group(1), m.group(0)), w)
        if "$" in w or "`" in w or any(ch in w for ch in "*?["):
            return None
        return os.path.normpath(w if os.path.isabs(w) else os.path.join(state["cur"], w))

    def add(word, via, srcs=()):
        p = resolve(word)
        if p is None:
            acc["unresolved"].append(word)
        else:
            acc["targets"].append((p, via, tuple(srcs)))

    def learn(word):
        m = ASSIGN_RE.match(word)
        if m:
            v = resolve(m.group(2))
            vars_[m.group(1)] = v if v is not None else m.group(2)
        return bool(m)

    for seg in segments(tokens):
        words, i = [], 0
        while i < len(seg):                                    # 1. redirections
            t = seg[i]
            if t in WRITE_OPS:
                if i + 1 < len(seg):
                    add(seg[i + 1], t)
                i += 2; continue
            if t in READ_OPS or t in DUP_OPS:
                i += 2; continue
            words.append(t); i += 1
        j = 0
        while j < len(words) and (learn(words[j]) or words[j] in WRAPPERS or
                                  (j > 0 and words[j - 1] in WRAPPERS
                                   and words[j].startswith("-"))):
            j += 1                                             # 2. VAR=x, wrappers
        words = [w for w in words[j:] if not w.isdigit()]     # fd digits from `2>`
        if not words:
            continue
        head, args = words[0], words[1:]
        if head in ("export", "declare", "local", "typeset"):
            for a in args:
                learn(a)
        elif head in ("cd", "pushd"):
            positional = [a for a in args if not a.startswith("-")]
            if "-" in args:
                pass                                           # `cd -`: unknown, keep
            elif positional:
                r = resolve(positional[0])
                if r is not None:
                    state["cur"] = r
                    vars_["PWD"] = r
            else:
                state["cur"] = os.path.expanduser("~")
                vars_["PWD"] = state["cur"]
        elif head == "tee":
            for a in args:
                if not a.startswith("-"):
                    add(a, "tee")
        elif head in ("cp", "install", "mv"):
            dest, positional, k = None, [], 0
            while k < len(args):
                a = args[k]
                if a == "-t" and k + 1 < len(args):
                    dest = args[k + 1]; k += 2; continue
                if a.startswith("--target-directory="):
                    dest = a.split("=", 1)[1]; k += 1; continue
                if not a.startswith("-"):
                    positional.append(a)
                k += 1
            if head == "mv":
                for a in positional + ([dest] if dest else []):
                    r = resolve(a)
                    if r is not None:
                        acc["moved"].append(r)
            if dest is None:
                if len(positional) < 2:
                    continue
                dest, srcs = positional[-1], positional[:-1]
            else:
                srcs = positional
            if not srcs:
                continue
            rs = [resolve(s) for s in srcs]
            d = resolve(dest)
            if d is not None and os.path.isdir(d):
                for word, s in zip(srcs, rs):
                    if s is None:
                        acc["unresolved"].append(os.path.join(dest, word))
                    else:
                        acc["targets"].append(
                            (os.path.join(d, os.path.basename(s)), head, (s,)))
            else:
                add(dest, head, rs)
        elif head in SHELLS:                                   # bash -c '...'
            for k, a in enumerate(args):
                if (a.startswith("-") and not a.startswith("--")
                        and "c" in a[1:] and k + 1 < len(args)):
                    analyse(args[k + 1], state["cur"], vars_, depth + 1, acc)
                    break
    return acc

payload_cwd = data.get("cwd") or os.getcwd()
shell = analyse(cmd, payload_cwd, os.environ)
notes = []

# Surface 2: a NEW note born through the shell. Blocked, and pointed at Write.
births = []
for p, via, srcs in shell["targets"]:
    if not p.endswith(".md"):
        continue
    root = in_vault(p)
    if root is None or exempt(root, p) or os.path.exists(p):
        continue                           # outside, machinery, or an edit
    if via == "mv" and any(s is None or in_vault(s) for s in srcs):
        continue                           # a move inside the vault: surface 3
    births.append(p)
if births:
    block("BLOCKED by the frontmatter guard: creating a note through the "
          "shell (%s).\nUse the Write tool instead.\nThe reason is not "
          "style. This guard reads a Write's content and checks the "
          "frontmatter against §8 before it lands; it cannot read a "
          "heredoc's, so a note written this way skips the only gate that "
          "would have caught a missing required key or an illegal value. "
          "Two doors where one is unwatched is the same as no door."
          % ", ".join(os.path.basename(t) for t in births))

unresolved = [u for u in shell["unresolved"] if u.endswith(".md")]
for p, via, srcs in shell["targets"]:
    # A `mv` whose source is a `$var` or a glob could be a rename inside the
    # vault or an import from outside; the guard cannot tell, so it says so.
    if (via == "mv" and p.endswith(".md") and in_vault(p) and not exempt(in_vault(p), p)
            and not os.path.exists(p) and any(s is None for s in srcs)):
        unresolved.append("the source of the move into %s" % p)
if unresolved:
    notes.append("The frontmatter guard could not resolve %s, so it let this "
                 "command through unchecked. If this creates a new vault note, "
                 "use the Write tool instead, so the note's frontmatter is "
                 "checked against §8 before it lands."
                 % ", ".join(sorted(set(unresolved))))
if shell["parse_failed"]:
    notes.append("The frontmatter guard could not parse this command (unbalanced "
                 "quotes), so it let it through unchecked. If this creates a new "
                 "vault note, use the Write tool instead.")

# Surface 3: mv. Allowed, with the link discipline attached.
if any(p.endswith(".md") and in_vault(p) for p in shell["moved"]):
    notes.append(
        "This move is allowed, and it carries a duty (doctrine §3): a move "
        "or rename rewrites its own inbound links. Scan the vault for links "
        "to the old name, rewrite them or leave a `_MOVED` stub, then verify "
        "zero dead links. Weekly maintenance is the backstop, not the "
        "mechanism: between now and then every one of those links is dead.\n"
        "If the destination folder is new, Home.md's directory needs the "
        "same update the mkdir rule below asks for.")

# Surface 4: mkdir. Allowed, with the directory duty attached.
if re.search(r"(^|[;&|])\s*mkdir\b", cmd):
    made = []
    try:
        tokens = shlex.split(cmd, posix=True)
    except ValueError:
        tokens = re.findall(r"[^\s;|&<>]+", cmd)
    for t in tokens:
        if t.startswith("-"):
            continue
        if in_vault(t) and not t.endswith(".md"):
            made.append(t)
    if made:
        notes.append(
            "New folder(s) allowed: %s. Two duties follow.\n"
            "  1. Update 02_Command-Base/Home.md's directory. Home is the only "
            "directory this vault has, so a folder missing from it is a folder "
            "nobody finds.\n"
            "  2. An empty room gets no door. Do not write a `_<Name>-Guide.md` "
            "now just because the folder exists; the guard will say when the "
            "folder has earned one (two notes and no door). A welcome sign on an "
            "empty room is a promise the room has not kept."
            % ", ".join(os.path.basename(m.rstrip("/")) for m in made))

if notes:
    allow_with("\n\n".join(notes))
allow()
PYEOF
