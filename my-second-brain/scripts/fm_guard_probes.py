#!/usr/bin/env python3
"""Behaviour table for the frontmatter guard's Bash branch.

Usage: python3 fm_guard_probes.py <hook-path> <vault-path>

Pipes each case into <hook-path> as the PreToolUse payload Claude Code would
hand it, and compares the exit code (2 = block, 0 = allow) with what the case
demands. Run it against a path-injected COPY of scripts/fm-guard-hook.sh (the
two __MSB_*__ placeholders replaced), never against the payload template.

Nothing here is executed as a shell command: every case is analysed by the
hook and nothing else, so no file in the vault is created or modified. The one
file the block cases name, 00_Inbox/Guard-Probe-Bash.md, must NOT exist, or
the run refuses to start (an existing file turns a birth into an edit and every
block case would read as a hole).

Cases whose fixture is missing in this vault are SKIPPED with a message, never
counted as passed. Exit 1 on any mismatch.
"""
import json
import os
import subprocess
import sys
import tempfile


def main():
    if len(sys.argv) != 3:
        sys.stderr.write(__doc__)
        return 2
    hook = os.path.abspath(sys.argv[1])
    V = os.path.realpath(sys.argv[2])
    if not os.access(hook, os.X_OK):
        sys.stderr.write("hook is not executable: %s\n" % hook)
        return 2

    NEW = V + "/00_Inbox/Guard-Probe-Bash.md"
    if os.path.exists(NEW):
        sys.stderr.write("refusing to run: %s exists, so every block case would "
                         "be an edit rather than a birth\n" % NEW)
        return 2

    # Outside-vault paths. They need not exist; none is written.
    T = os.path.realpath(tempfile.gettempdir())
    if T == V or T.startswith(V + os.sep):
        sys.stderr.write("the temp dir sits inside the vault; set TMPDIR elsewhere\n")
        return 2
    OUT = T + "/fm-guard-probes"          # an outside folder that does not exist

    LOG = V + "/99_Meta/filing-log.md"
    BUF = V + "/99_Meta/capture-buffer.md"
    INBOX = V + "/00_Inbox"
    TEMPLATES = V + "/99_Meta/Templates"

    # (label, command, fixtures that must exist for the case to mean anything)
    must_allow = [
        ("read with 2>/dev/null | head",
         "cat %s 2>/dev/null | head" % BUF, [BUF]),
        ("heredoc writes a script OUTSIDE the vault whose body names a vault .md",
         "cat > %s/x.py <<'EOF'\nimport os\np = \"%s/00_Inbox/foo.md\"\nEOF\npython3 %s/x.py"
         % (OUT, V, OUT), []),
        ("diff two existing notes; echo rc",
         "diff %s %s; echo \"rc=$?\"" % (LOG, BUF), []),
        ("diff two existing notes 2>&1 | head",
         "diff %s %s 2>&1 | head" % (LOG, BUF), []),
        ("echo hdr >&2; diff two existing notes",
         "echo '== diff ==' >&2; diff %s %s" % (LOG, BUF), []),
        ("rsync ~/.claude/CLAUDE.md to a remote host",
         "rsync -av ~/.claude/CLAUDE.md remote-host:~/.claude/CLAUDE.md", []),
        ("cat file | ssh host 'cat > remote.md'",
         "cat ~/.claude/CLAUDE.md | ssh remote-host 'cat > ~/.claude/CLAUDE.md'", []),
        ("cd elsewhere && cat PROGRESS.md 2>/dev/null (relative)",
         "cd %s && cat PROGRESS.md 2>/dev/null" % T, []),
        ("cat PROGRESS.md 2>&1 | head (relative, cwd=vault)",
         "cat PROGRESS.md 2>&1 | head", []),
        ("grep --include=*.md with 'cat >' in the pattern",
         "grep -rn \"heredoc\\|cat > \\|cat >\" --include=*.md README.md . | head", []),
        ("grep 'cat >' on a vault dir | tee outside",
         "grep -rn 'cat >' %s/99_Meta 2>/dev/null | tee %s/out.txt" % (V, OUT), []),
        ("append heredoc to EXISTING filing-log, body contains '> '",
         "cat >> %s <<'EOF'\n- 2026-09-16 x > y\nEOF" % LOG, [LOG]),
        ("tee -a to existing filing-log",
         "printf '%%s\\n' '- line' | tee -a %s" % LOG, [LOG]),
        ("cp vault note OUT to temp",
         "cp %s %s/copy.md" % (BUF, OUT), []),
        ("write .md outside the vault",
         "cat > %s/notes-outside.md <<'EOF'\nhello\nEOF" % OUT, []),
        ("write non-.md inside the vault (not this guard's business)",
         "ls > %s/listing.txt" % INBOX, []),
        ("mv within the vault (surface 3 note, not a birth)",
         "mv %s/a.md %s/b.md" % (INBOX, INBOX), []),
        ("write into an exempt dir",
         "cat > %s/Guard-Probe-Bash.md <<'EOF'\nx\nEOF" % TEMPLATES, []),
        ("overwrite an existing note with > (edit, not birth)",
         "printf '' > %s" % BUF, [BUF]),
        ("stderr redirect to /dev/null on a vault read",
         "wc -l %s 2>/dev/null" % LOG, []),
        ("stdout to fd 2",
         "echo %s/whatever.md >&2" % INBOX, []),
        ("append heredoc with apostrophe to EXISTING note",
         "cat >> %s <<'EOF'\nit's fine\nEOF" % LOG, [LOG]),
        ("bash -c that only reads",
         "bash -c 'cat %s 2>/dev/null | head'" % LOG, []),
        ("target uses an undefined $VAR (unresolved: allow with a note)",
         "printf x > \"$UNDEFINED_FM_GUARD_DIR/00_Inbox/x.md\"", []),
        ("cd into vault then write .md OUTSIDE via absolute path",
         "cd %s && cat > %s/out.md <<'EOF'\nx\nEOF" % (V, OUT), []),
        ("cp several notes out of the vault",
         "cp %s %s %s/" % (LOG, BUF, T), []),
        ("python -c that writes a vault md (known residual hole)",
         "python3 -c \"open('%s','w').write('x')\"" % NEW, []),
        ("comment with an apostrophe, then a read",
         "# it's only a read\ncat %s | head" % LOG, []),
    ]
    must_block = [
        ("heredoc birth in Inbox",
         "cat > %s <<'EOF'\n---\ntype: x\n---\nEOF" % NEW, [INBOX]),
        ("ls > new note", "ls > %s" % NEW, [INBOX]),
        (">> to a NON-existing note (append creates)",
         "printf 'x' >> %s" % NEW, [INBOX]),
        ("tee new note", "echo hi | tee %s" % NEW, [INBOX]),
        ("cp into vault as new note", "cp %s/x.md %s" % (T, NEW), [INBOX]),
        ("cp into vault DIR (dest is a folder)",
         "cp %s/Guard-Probe-Bash.md %s/" % (T, INBOX), [INBOX]),
        ("mv from outside into vault as new note",
         "mv %s/x.md %s" % (T, NEW), [INBOX]),
        ("cd Inbox && > relative new",
         "cd %s && > Guard-Probe-Bash.md" % INBOX, [INBOX]),
        ("cd Inbox; printf > relative new",
         "cd %s; printf 'x' > Guard-Probe-Bash.md" % INBOX, [INBOX]),
        ("VAR=vault; > $VAR/new",
         "V=%s; printf 'x' > \"$V/00_Inbox/Guard-Probe-Bash.md\"" % V, [INBOX]),
        ("bash -c heredoc birth",
         "bash -c 'cat > %s <<EOF\nhi\nEOF'" % NEW, [INBOX]),
        ("zsh -lc with cd inside",
         "zsh -lc 'cd %s && echo x > Guard-Probe-Bash.md'" % INBOX, [INBOX]),
        ("&> new note", "some-cmd &> %s" % NEW, [INBOX]),
        (">| new note", "ls >| %s" % NEW, [INBOX]),
        ("line continuation before target",
         "cp %s/x.md \\\n  %s" % (T, NEW), [INBOX]),
        ("multi-line: read then birth on line 2",
         "cat %s\ncat > %s <<'EOF'\nx\nEOF" % (LOG, NEW), [INBOX]),
        ("heredoc body with an apostrophe",
         "cat > %s <<'EOF'\nit's here\nEOF" % NEW, [INBOX]),
        ("export VAR then > $VAR/new",
         "export V=%s\nprintf 'x' > $V/00_Inbox/Guard-Probe-Bash.md" % V, [INBOX]),
        ("sudo tee new note", "echo x | sudo tee %s" % NEW, [INBOX]),
        ("two heredocs on one line, second is the birth",
         "cat <<A > %s/a.txt; cat <<B > %s\na\nA\nb\nB" % (OUT, NEW), [INBOX]),
        ("glued separator: 'cd Inbox &&' newline, relative birth",
         "cd %s &&\nprintf x > Guard-Probe-Bash.md" % INBOX, [INBOX]),
        ("comment line, then tee a new note on the next line",
         "echo x # a comment\ntee %s < /dev/null" % NEW, [INBOX]),
        ("bash --norc -c birth",
         "bash --norc -c 'ls > %s'" % NEW, [INBOX]),
    ]

    UNRESOLVED_LABEL = "target uses an undefined $VAR (unresolved: allow with a note)"
    UNRESOLVED_NOTE = "could not resolve"

    fails = skipped = passed = 0
    print("%-4s  %-6s  %-6s  %s" % ("", "expect", "actual", "label"))
    for want, cases in (("allow", must_allow), ("block", must_block)):
        for label, command, fixtures in cases:
            missing = [f for f in fixtures if not os.path.exists(f)]
            if missing:
                skipped += 1
                print("SKIP  %-6s  %-6s  %s  (fixture missing: %s)"
                      % (want, "-", label, ", ".join(missing)))
                continue
            payload = json.dumps({"tool_name": "Bash",
                                  "tool_input": {"command": command},
                                  "cwd": V})
            r = subprocess.run([hook], input=payload, capture_output=True,
                               text=True, cwd=V)
            actual = {0: "allow", 2: "block"}.get(r.returncode, "exit%d" % r.returncode)
            ok = actual == want
            extra = ""
            if actual == "block":
                extra = (r.stderr.strip().splitlines() or [""])[0]
            if ok and label == UNRESOLVED_LABEL and UNRESOLVED_NOTE not in r.stdout:
                ok = False
                extra = "no unresolved-target note in stdout: %r" % r.stdout[:200]
            if ok:
                passed += 1
            else:
                fails += 1
            print("%-4s  %-6s  %-6s  %s" % ("ok" if ok else "FAIL", want, actual, label))
            if extra:
                print("                      %s" % extra[:160])
    # The run must have left the vault untouched where it matters.
    if os.path.exists(NEW):
        fails += 1
        print("FAIL  %s now exists: something executed a case" % NEW)
    print("\npassed %d  failed %d  skipped %d" % (passed, fails, skipped))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
