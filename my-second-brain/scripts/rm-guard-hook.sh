#!/bin/bash
# rm-guard-hook.sh  (My Second Brain safety lock)
# Claude Code PreToolUse hook (matcher: Bash). A READ-ONLY accident net.
#
# MSB-GUARD: key=rm_guard_installed installs-as=my-second-brain-rm-guard.sh matchers=Bash name=delete-guard does=stops a recursive delete aimed at your vault or at a skill symlink into it
# MSB-PROBE: expect=block stdin={"tool_name":"Bash","tool_input":{"command":"rm -rf {{VAULT}}/probe-target-that-does-not-exist"}}
#
# ⭐ THAT FIRST LINE IS THE REGISTRY ENTRY FOR THIS GUARD, AND THE ONLY ONE.
#   Three readers take these facts from here and none of them keeps a copy:
#   setup step 6.8 (which key to write, what to name the installed file, which
#   PreToolUse matchers to register it under), the wiring check
#   `guards-registered` (the same three, to verify what setup claims), and
#   scripts/checkup.py's weekly safety-lock check (name and `does=`, to say
#   which guard is missing in words the owner understands).
#   Format: `# MSB-GUARD:` then space-separated key=value fields in any order,
#   except `does=`, which is last and runs to the end of the line.
#   ⛔ A new guard joins the product by shipping a script with one of these
#   lines. It does not join by anyone editing a list, because there is no list.
#
# ⭐ AND THE SECOND LINE IS HOW THIS GUARD PROVES IT IS ALIVE, FOR THE SAME
#   REASON. A guard can be written, registered, placeholder-free and clean under
#   `bash -n` while doing nothing at all, so setup 6.8 ends by FEEDING each
#   installed guard a call it must refuse and checking that it did. The call has
#   to travel with the guard rather than live in setup's prose: whoever writes
#   the third guard would otherwise have to hand-compose a payload for it, and a
#   hand-composed payload is how the 2026-08-16 install session nearly filed a
#   healthy guard as broken (it invented one the guard was right to allow).
#   Format: `# MSB-PROBE:` then `expect=block` or `expect=allow`, then `stdin=`,
#   which is last and runs to the end of the line: one line of JSON, exactly the
#   PreToolUse payload Claude Code would hand this hook, with `{{VAULT}}` where
#   the vault's absolute path goes. A guard may declare more than one.
#   expect=block means exit 2; expect=allow means exit 0.
#   ⛔ The probe is PIPED TO THE HOOK, never run as a command. This one names a
#   recursive delete because that is the thing this guard exists to refuse; the
#   target is a path that does not exist, so a misreading that executes it
#   instead of piping it deletes nothing.
#   ⚠️ Write the payload to a file, or use `printf '%s'`. ⛔ Not `echo`: zsh's
#   builtin `echo` expands the `\n` inside a JSON string into real newlines, the
#   hook then fails to parse its own input, and every guard fails OPEN on
#   unparseable input by design - so the probe reports a dead guard on a healthy
#   one. Measured, on zsh, on this product.
#
# Blocks recursive deletes that target your Obsidian vault, ~/.claude/skills,
# or ~/.codex/skills, including the symlink-passthrough case: My Second Brain
# installs skills as symlinks that point
# INTO your vault, and a plain `rm -r ~/.claude/skills/<name>` or
# `rm -r ~/.codex/skills/<name>` follows the link
# and destroys the real vault content behind it. This guard stops that.
#
# It is an accident net, NOT a security boundary. It only catches recursive
# deletes whose target resolves to an absolute protected path; it fails OPEN
# (allows) on anything it cannot parse, so it never blocks unrelated work.
#
# INSTALL: Setup replaces the placeholder value on the MSB_VAULT_PATHS line
# below with your vault's absolute path, and registers this script in the
# PreToolUse "Bash" matcher of ~/.claude/settings.json. That placeholder token
# appears on exactly ONE line (the env assignment); nowhere else in this file
# carries it, so a global find-and-replace at install time is safe.
# UNINSTALL: remove this script's entry from that matcher (and delete the file).
#
# Exit 0 = allow. Exit 2 = block.

INPUT="$(cat)"

# The quoted value below is replaced at install time with your vault's absolute
# path. Multiple vaults: colon-separated. Both skills roots are always protected
# and need no injection.
HOOK_STDIN="$INPUT" MSB_VAULT_PATHS="__MSB_VAULT_PATHS__" /usr/bin/env python3 <<'PYEOF'
import sys, json, os, shlex, re

def allow():
    sys.exit(0)

try:
    data = json.loads(os.environ.get("HOOK_STDIN", "") or "{}")
except Exception:
    allow()

cmd = ((data.get("tool_input") or {}).get("command") or "")
if not isinstance(cmd, str) or not cmd.strip():
    allow()

HOME = os.path.expanduser("~")

# Protected roots: the injected vault path(s) plus both skills roots (always).
# A leftover, un-injected placeholder is dropped so a botched install cannot
# create a garbage protected root.
# Sentinel built by concatenation so the full placeholder token never appears
# as a contiguous literal here: install-time substitution rewrites only the env
# line above, never this guard.
_PLACEHOLDER = "__MSB_" "VAULT_PATHS__"
raw_vaults = os.environ.get("MSB_VAULT_PATHS", "") or ""
vault_roots = []
for part in raw_vaults.split(":"):
    part = part.strip()
    if not part or part == _PLACEHOLDER:
        continue
    vault_roots.append(os.path.expanduser(os.path.expandvars(part)))

PROTECTED = list(vault_roots) + [
    os.path.join(HOME, ".claude", "skills"),
    os.path.join(HOME, ".codex", "skills"),
]
PROTECTED_REAL = []
for r in PROTECTED:
    PROTECTED_REAL.append(os.path.normpath(r))
    try:
        PROTECTED_REAL.append(os.path.realpath(r))
    except Exception:
        pass
PROTECTED_REAL = list(dict.fromkeys(PROTECTED_REAL))

# Literal path forms for the normalized-substring net (handles odd tokenization
# / escaped spaces that shlex may fumble). Checked only inside a delete segment.
LITERALS = []
for r in vault_roots:
    LITERALS.append(r)
LITERALS += [
    os.path.join(HOME, ".claude", "skills"),
    "~/.claude/skills",
    "$HOME/.claude/skills",
    os.path.join(HOME, ".codex", "skills"),
    "~/.codex/skills",
    "$HOME/.codex/skills",
]
LITERALS = [x for x in dict.fromkeys(LITERALS) if x]

def is_protected_abs(path):
    cands = {os.path.normpath(path)}
    try:
        cands.add(os.path.realpath(path))
    except Exception:
        pass
    for c in cands:
        for root in PROTECTED_REAL:
            if c == root or c.startswith(root + os.sep):
                return True
    return False

def seg_delete_kind(seg):
    # recursive rm (rm -rf / -fr / -Rf / split flags), find -delete / -exec rm,
    # or xargs ... rm ... -r
    if re.search(r'\brm\b[^\n]*?(?:\s|=)-{1,2}\S*[rR]', seg):
        return True
    if re.search(r'\bfind\b[^\n]*?(?:-delete\b|-execdir\s+rm\b|-exec\s+rm\b)', seg):
        return True
    if re.search(r'\bxargs\b[^\n]*?\brm\b[^\n]*?-{1,2}\S*[rR]', seg):
        return True
    return False

# Split the command into segments on shell control operators so a `cd` (or any
# non-delete command) elsewhere in the line cannot contribute target paths.
segments = re.split(r'&&|\|\||[;\n|]', cmd)

SKIP_WORDS = {"rm", "find", "xargs", "sudo", "cd", "-exec", "-execdir", "-delete", "-name", "-type", "-o", "-a"}

blocked = False
for seg in segments:
    if not seg_delete_kind(seg):
        continue

    # (a) normalized literal net: strip escaping backslashes, look for a
    #     protected root path spelled out in THIS delete segment.
    norm = seg.replace("\\", "")
    if any(lit in norm for lit in LITERALS):
        blocked = True
        break

    # (b) absolute / realpath-resolved token check on this segment's args.
    try:
        toks = shlex.split(seg, comments=False, posix=True)
    except Exception:
        toks = seg.split()
    for t in toks:
        if t.startswith("-") or t in SKIP_WORDS:
            continue
        p = os.path.expanduser(os.path.expandvars(t))
        if not os.path.isabs(p):
            continue  # relative targets are intentionally not caught
        if is_protected_abs(p):
            blocked = True
            break
    if blocked:
        break

if not blocked:
    allow()

roots_display = ", ".join(vault_roots) if vault_roots else "your vault"
sys.stderr.write(
    "BLOCKED by My Second Brain safety lock: this command runs a recursive delete "
    "against your vault (%s), ~/.claude/skills, or ~/.codex/skills.\n\n"
    "Those roots are protected because both skills folders hold symlinks INTO your "
    "vault, and 'rm -r' passes through the symlink and destroys real vault content.\n\n"
    "If you meant to remove a SYMLINK, use plain 'rm' WITHOUT -r (that deletes the link, "
    "not its target). To remove specific files, delete them by name or use your file "
    "manager. This guard is an accident net, not a security boundary.\n" % roots_display
)
sys.exit(2)
PYEOF
rc=$?
exit $rc
