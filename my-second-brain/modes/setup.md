# Setup Mode: from bare machine to wired second brain

Fast by design: a handful of decisions from the user, then one scaffold burst. Target: under 10 minutes on a normal connection, most of it Obsidian downloading. Keep momentum; no lectures between steps. Record every step's state in `99_Meta/bootstrap-progress.md` as you go (create it first inside the vault once the vault location exists), so an interrupted setup resumes cleanly: on entry, if `bootstrap-progress.md` exists with `setup_complete: false`, resume from the first unchecked step instead of restarting.

## Step 1: Confirm and choose language

One combined opening question (keep it to a few lines): confirm they want to set up their second brain here and now, and ask which language to work in, English or 中文. Default English if they shrug. Everything after this speaks the chosen language. Folder and file names stay English regardless (tell them once: "folders stay English so tools and future AIs read them cleanly; we talk in whatever language you like").

## Step 2: Obsidian (viewing deck)

Check if Obsidian is installed. If the user simply says it is already installed, take their word and skip the checks:

- macOS: `[ -d "/Applications/Obsidian.app" ]` (also try `~/Applications`)
- Windows: `winget list Obsidian.Obsidian` or check `%LOCALAPPDATA%\Programs\Obsidian`
- Linux: `which obsidian`, flatpak list, or ask

If missing, offer to install it now (recommended; capture works without it, but the payoff screen and daily browsing live there):

- macOS with Homebrew: `brew install --cask obsidian`
- macOS without Homebrew: download the official DMG with curl from `https://obsidian.md/download`, mount with `hdiutil attach`, copy the .app to `/Applications`, detach. If any step fails, give the download link and move on; do not stall setup.
- Windows: `winget install Obsidian.Obsidian`
- Linux: point to the AppImage / flatpak on `https://obsidian.md/download`
- Any failure: link `https://obsidian.md/download`, tell them to install it later, continue setup. Nothing downstream hard-depends on it.

Note for later (step 8 and the dashboard): the dashboard uses Obsidian **Bases**, a core plugin. If it is not enabled: Settings -> Core plugins -> enable Bases. Mention this once at the graph moment, not now.

## Step 3: Vault location

Ask: existing Obsidian vault, or new one?

- **New:** propose `~/Documents/<Name>-Second-Brain/` (their name or business name, English, hyphenated; if the business name has not come up yet, ask it here and reuse the answer in step 4). They can pick any path. `mkdir -p` it.
- **Existing vault:** get the path. The scaffold is idempotent (`mkdir -p`, never overwrite an existing file), so a vault with PARA folders already in place is fine; we add what is missing.
- ⛔ **Before the branch below fires, separate "their own structure" from "our older structure", because the two look alike.** An older house this product itself built also shows a PARA layout, MOC files and a command base, and adopting one of those would put a second business wing beside the one already there and leave the owner with both shapes at once. `SKILL.md`'s house-vintage gate (mode routing, step 1) is the test, and it has already run this session; if it said the house is an older generation of ours, ⛔ do not scaffold into it, whatever `setup_complete:` says. Only a vault that gate cleared as **not ours** is a candidate for the branch below.
- **Existing vault with a structure of its own** (signature: a PARA layout, `06_MOCs/`, an existing command base, anything the owner clearly built and uses): do NOT migrate, rename, or rebuild what they have. What works keeps working. Add only what is missing and clearly ours: the business wing (`04_<Business>-Business-Wing/`), `99_Meta` doctrine plus state files, and `02_Command-Base/` if nothing plays that role yet. Tell them plainly what you are adding and what you are leaving untouched, and be honest about the one real consequence: the doctrine describes a personal wing at `03_Personal-Wing/` that their vault does not have, so on their side the doctrine governs the business wing and the shared layers, and their own personal structure stands. ⛔ Never quietly restructure someone's existing personal folders to match the law; propose it as its own piece of work, another day, or leave it alone.

## Step 4: Business + toggles (the only interview in setup)

Three quick things, one message each or one compact message, their call:

1. Business name (and its folder-safe English form, e.g. 咖啡老王 -> `Laowang-Coffee`; propose, they confirm). Derive the domain tag from it (`{{BUSINESS_TAG}}`, kebab-case) and confirm that too, in the same breath.
2. Toggle: physical outlets? (yes -> `Outlets/` room)
3. Toggle: machines or equipment? (yes -> `Equipment/` room)

⛔ **Do not ask about the personal wing.** It and its six life rooms are always created; the doctrine states its contents flatly, so a vault missing them does not match its own law. There is no third toggle either: the old importing toggle only ever created SOP subfolders, and `03_SOP/` now ships empty and flat.

## Step 5: The scaffold burst

Execute [../references/scaffold-spec.md](../references/scaffold-spec.md) in one go: all folders, every door file (`_<Name>-Guide.md` per room, lane, brand subfolder and wing, plus `_SOP-Menu.md`), `Home.md` as the vault's full directory, `Business-Profile` at the wing root (empty schema), doctrine (from [../templates/structure-doctrine.template.md](../templates/structure-doctrine.template.md)), tagging vocabulary (from [../templates/tagging-vocabulary.template.md](../templates/tagging-vocabulary.template.md)), note templates (from [../templates/note-templates.md](../templates/note-templates.md)), dashboard `.base` (verbatim from [../templates/command-base.base.template](../templates/command-base.base.template)), the pre-seeded brand rooms (`Brand-Strategy/` with seven pillar stubs + `Target-Audience/` with the Journey stub, per the spec), and the state files, including `99_Meta/lab-gate-config.md` (from [../templates/lab-gate-config.template.md](../templates/lab-gate-config.template.md)) and working memory `99_Meta/memory.md` (from [../templates/memory.template.md](../templates/memory.template.md); this is what the command-base skill reads and appends every session, so it exists from day one).

Two layers ship deliberately bare and it is worth not "fixing" them mid-burst: `03_SOP/` holds nothing but its menu, and `04_Methodology/` holds two empty folders and zero `.md` files, doors included.

Run the wiring check at the end of the spec. Report one line: "Scaffolded N folders, M files. Home lists all of it."

## Step 5.5: Vault CLAUDE.md (the always-on context layer)

Skills wake on trigger words; `CLAUDE.md` at the vault root loads into EVERY Claude Code session started there, unconditionally. Without it, a session opened tomorrow with a casual first message has no idea this is a structured vault, and the constitution is just a file lying in `99_Meta`. This step is what makes the rules self-announcing.

- **No `CLAUDE.md` at the vault root** (the normal case): write one from [../templates/CLAUDE.template.md](../templates/CLAUDE.template.md), replacing `{{YOUR_NAME}}`, `{{BUSINESS}}`, `{{BUSINESS_NAME}}`, `{{SLUG}}`, `{{LANGUAGE}}` (the step 1 choice, written as `English` or `中文`), `{{DATE}}`. Write once; later sessions never rewrite it silently (it evolves only through propose-and-approve during maintenance).
- **`CLAUDE.md` already exists** (existing-vault users): **never overwrite and never edit what is there.** Show the user a ready-to-append `## My Second Brain` section (the template's content demoted one heading level, minus the top title) and ask one question: append it for them, or leave it for them to place manually? Append only on an explicit yes.

Record the outcome in `bootstrap-progress.md` (`claude_md: written | appended | left-to-user`).

## Step 6: Generate their command-base skill

From [../templates/command-base-SKILL.template.md](../templates/command-base-SKILL.template.md), replace `{{YOUR_NAME}}`, `{{SLUG}}` (their name or business, kebab-case), `{{VAULT_PATH}}`, `{{BUSINESS}}` (folder name), `{{BUSINESS_NAME}}`, `{{BUSINESS_TAG}}`, `{{COMPANION_SOUL_NAME}}` (`<slug>-companion-soul`; the skill handles its absence until Create-My-Jarvis runs). Zero interview; every value already exists from steps 1 to 4.

Write it to `<vault>/99_Meta/Skills/<slug>-command-base/SKILL.md`, then install:

- macOS / Linux: `ln -s "<vault>/99_Meta/Skills/<slug>-command-base" ~/.claude/skills/<slug>-command-base` (create `~/.claude/skills/` if missing; if a same-named entry exists, ask before touching it). Symlink means editing the vault copy edits the live skill.
- **Windows, default: copy the folder**, and tell them the canonical copy is the vault one. ⛔ A copy means **every later edit to the vault copy leaves the live skill untouched until it is copied over again**, which is why the flag below exists and why the retrofit path in `SKILL.md` reads the installed file back instead of trusting that its edit landed. Staleness on this path is handled; do not reach for a link to solve it.
- **A junction is available if the owner asks for live editing, but say the trade out loud first.** Step 6.8 installs a delete guard, and **that guard is macOS only**. The single accident it exists to stop is a `rm -r` aimed at `~/.claude/skills/` that **follows the link into the vault and destroys the real content behind it**. A copy cannot be followed, so a Windows copy install is the one shape that is safe from this by construction. A junction gives up that safety on the one platform where nothing is watching. ⛔ Do not present the junction as the recommended path, and do not install one without saying this in plain words.
  - Mechanically: `mklink /D` (a directory symlink) needs elevation or Developer Mode; `mklink /J` makes a **junction**, which does not, and on a local disk one folder ends up with two paths. From `cmd.exe`, link first then target: `mklink /J "%USERPROFILE%\.claude\skills\<slug>-command-base" "<vault>\99_Meta\Skills\<slug>-command-base"` (create `%USERPROFILE%\.claude\skills\` first; if a same-named entry exists, ask before touching it). From PowerShell, either `cmd /c mklink /J ...` or `New-Item -ItemType Junction -Path <link> -Target <vault-path>`. **Verify before believing it:** write a marker line into the vault copy, read it back through the `~/.claude/skills/...` path, then remove the marker. If the read-back does not show it, the junction did not take; stay on the copy.
  - **Two known ways a junction will not work.** Junctions are **local volumes only**, so a vault on a mapped network drive or a UNC path (`\\server\share\...`) cannot be junctioned. And a vault living inside a **OneDrive / Dropbox / Google Drive sync folder** can put the sync client and the junction at odds: some clients refuse to traverse it, some follow it and upload a second copy of everything behind it.
- ⚠️ **Everything in the junction branch is untested on Windows.** This skill is developed on macOS and we have no Windows machine to verify against: the commands above, the shell they run in, and whether a Windows `rm -rf` actually follows a junction are all unverified. Treat the whole branch as best-effort, run the verify step rather than assuming, and stay on the copy without drama when anything is unclear.

**Record which one happened.** Set `command_base_install: symlink | junction | copy` in `bootstrap-progress.md`. This is not bookkeeping: it tells a later session whether editing the vault copy is enough or whether a re-copy has to follow. It is a hint, not proof (the owner may have re-installed by hand since), which is why `SKILL.md`'s retrofit path reads the installed file back instead of trusting the flag. Leaving the flag out costs that session its starting guess.

One line on what they just got: "From now on, in any session, say 'morning' or 'log a decision' and this skill runs your day on top of the vault."

## Step 6.7: Name the two skills that do not ship here (one line, no install)

Two pieces of work have their own tools, and both are published separately and installed by the owner when they want them. Say this once, in one line each, and only so nothing later reads as if it were already on the machine:

- **Writing an SOP** runs on the `sop-builder` skill. `03_SOP/` ships empty by design and hand-writing an SOP is perfectly legal (doctrine §1); the skill is the comfortable path, not the only legal writer.
- **Opening a playbook lab** runs on the `playbook-lab` skill, and that is a rare, later thing: most playbooks never need one, and the weekly maintenance scan proposes candidacy long before the owner has to think about it.

⛔ Do not install either here, and do not present them as missing pieces. Nothing in this vault breaks without them.

## Step 6.8: Safety lock (optional, recommended, macOS only)

This step installs a **read-only accident net**: a Claude Code hook that blocks a recursive delete (`rm -rf` and its variants) aimed at the vault or `~/.claude/skills`. It exists because of one specific, hard-to-reverse mistake. The command-base skill installs as a **symlink** under `~/.claude/skills/` that points INTO the vault; a plain `rm -r` on that link follows it and destroys the real vault content behind it. The hook stops exactly that. It is an accident net, not a security boundary: it fails open (allows) on anything it cannot parse, and it never blocks non-delete commands.

**This changes the owner's `~/.claude/settings.json`, which is machine-level configuration outside the vault. Explain before you install, and install only on an explicit yes.** Say, in plain terms: what it blocks (recursive deletes hitting the vault or the skills folder), how it blocks (the command is refused with a note before it runs), and how to remove it (below). If the owner declines, record that and move on; nothing else in the system depends on it.

**Platform honesty.** The install flow and the hook are validated on **macOS only** at this stage. On Windows or Linux, tell the owner it is not yet supported here, skip the install, and record the skip. Do not improvise a port.

On yes (macOS):

1. The hook template ships in this skill's payload at `scripts/rm-guard-hook.sh`. Read it, and replace the single placeholder token `__MSB_VAULT_PATHS__` (it appears on exactly one line, the `MSB_VAULT_PATHS=` env assignment) with the vault's absolute path from Step 3. Write the result to `~/.claude/hooks/my-second-brain-rm-guard.sh` (create `~/.claude/hooks/` if missing) and `chmod +x` it. Do not edit the payload template in place; the concrete, path-injected copy lives in `~/.claude/hooks/`.
2. Register it in `~/.claude/settings.json` under `hooks.PreToolUse`, matcher `"Bash"`, as a `{"type": "command", "command": "~/.claude/hooks/my-second-brain-rm-guard.sh", "timeout": 10}` entry (expand `~` to the absolute path). **Use the official `update-config` skill to make this edit if it is available; only hand-edit the JSON as a fallback, and preserve any existing `PreToolUse` / `Bash` entries by appending, never overwriting.**
3. Sanity-check: the token no longer appears in the installed file (`grep -c __MSB_VAULT_PATHS__` returns 0) and `bash -n ~/.claude/hooks/my-second-brain-rm-guard.sh` is clean.

**Uninstall** (tell the owner this, once): remove that one entry from the `PreToolUse` `Bash` matcher in `~/.claude/settings.json` and delete `~/.claude/hooks/my-second-brain-rm-guard.sh`. Nothing else references it.

Record `rm_guard_installed:` in `bootstrap-progress.md` (`installed` / `declined` / `skipped-platform`).

## Step 6.9: Session memory (optional, recommended, macOS first)

This step turns on **session memory**: every Claude Code conversation on this machine becomes searchable, so future sessions can answer "how did we fix that last time?" and "why did we choose A over B?" instead of re-solving solved problems. It is also the raw material for the weekly **Harvest** in Distill mode, where the AI reads unreviewed past sessions and proposes memories for the owner to approve or reject.

**Explain before you install.** Three facts, in plain terms, before asking for the yes:

- **What it reads:** only Claude Code's own session transcripts (`~/.claude/projects/`), strictly read-only. It never touches the vault, notes, or any other file, and it never modifies a transcript.
- **Where it writes:** one search database plus one small config file in `~/.my-second-brain/`. That folder sits outside the vault and outside this skill, so a skill update never wipes the index or the owner's review bookmarks.
- **Purely local:** there is no network code in the tool at all. Nothing is uploaded anywhere. It is also not a background process; it only runs when a session invokes it.

**Platform honesty.** The tool itself is standard-library Python and needs `python3` plus SQLite with FTS5, which macOS ships. It is validated on **macOS only** at this stage; on Windows or Linux, say so, skip, and record the skip. Do not improvise a port here. Windows owners who want it anyway have a documented, self-driven route: point them at the **"Windows self-serve path"** section of the README (native-first, they install python.org Python and run the tool by hand, and the tool's own FTS5 probe gives them a clear pass/fail). That path is best-effort and self-validated, which is exactly why it stays out of this gated Setup step.

On yes (macOS):

1. The tool ships in this skill's payload at `scripts/session-history/` (self-contained, nothing to download). Resolve the running skill's folder (via npx install it is `~/.claude/skills/my-second-brain/`, resolved at runtime); call the tool's path `<tool>` below.
2. Write the config so harvest reports know where the vault Inbox is: create `~/.my-second-brain/session-history.json` containing `{"vault": "<vault-path-from-step-3>"}` (create the folder if missing; if the file exists, update only the `vault` key).
3. Build the first index: `python3 "<tool>/sh" ingest`. On a machine with a long Claude Code history this can take a little while on first run; incremental runs afterwards take seconds. Report the one-line stats it prints.
4. Show the owner one search they can try, in their language, e.g. `python3 "<tool>/sh" search "the thing we fixed"`, and say plainly: from now on, asking "上次怎么解的 / how did we solve that before" in any session can actually be answered from history.

**Uninstall** (tell the owner once): delete `~/.my-second-brain/session-history.db` and `session-history.json`. The tool has no hooks, no daemon, and no other footprint.

Record `session_memory_installed:` in `bootstrap-progress.md` (`installed` / `declined` / `skipped-platform`).

Say one sentence about the weekly rhythm so it is never a surprise: once a week the morning brief quietly runs this pass in the background, reads whatever is new, and only speaks up if something is actually worth keeping, so most weeks the owner sees nothing. Nothing is ever written into the files their AI loads at session start without them reading the exact words first. If they would rather be asked each time, set `harvest_auto: false` in `bootstrap-progress.md` and it goes back to offering; leaving the key out means automatic.

## Step 7: Official Obsidian skills (optional, recommended)

Offer once: the Obsidian team publishes official skills (Bases syntax, Obsidian-flavored markdown, web clipping) that make the AI sharper inside Obsidian. Install with `npx skills add kepano/obsidian-skills`. Recommended yes; a no costs nothing tonight. Record the answer in `bootstrap-progress.md` (`obsidian_skills_offered:`).

## Step 7.5: Connect a calendar (optional, recommended)

Offer once: connect a calendar so the morning brief can see today's actual schedule, not just the task list. Read-only, folded into the brief, never stored in the vault. Recommend-leaning, because a morning brief that ignores the day's meetings is half-blind, but a skip costs nothing and is reversible any time.

Three choices. Do the lightweight part inline, do not stall setup on OAuth or an install:

- **Google Calendar (recommended):** point them to the one-click connector. Directory panel, Connectors tab, Anthropic and Partners, Google Calendar, click `+`, authorize. Tell them to leave the read-only tools on "Always allow" so the morning read never prompts. Full steps in [../references/calendar-connect.md](../references/calendar-connect.md). Record `calendar_provider: google`.
- **Lark / Feishu:** offer to install the official CLI now (`npm install -g @larksuite/cli`, then `lark-cli config init` and `lark-cli auth login --recommend`) or to do it later. Steps in the reference. Record `calendar_provider: lark` on success (plus `calendar_lark_bin:` if not on PATH); if they defer, record `none` and note where to come back.
- **Skip / later:** record `calendar_provider: none`.

Always record the outcome in `bootstrap-progress.md` (`calendar_offered: true` + `calendar_provider:`). Offer once, never nag; the command-base skill reads the flag every morning and stays silent when it is `none`.

## Step 8: The graph moment

Close setup with the payoff:

1. Tell them to open Obsidian -> Open folder as vault -> pick the vault path (skip if already open).
2. One-time check: Settings -> Core plugins -> **Bases** enabled (the dashboard needs it).
3. Open graph view (the network icon, or Ctrl/Cmd+G).

What they see is their second brain as a constellation: every door wired to Home, business wing on one side, personal wing on the other, all of it empty and waiting. Say it straight, in their language, something like: "That is your second brain, half built. The structure is done; the memories are not moved in yet. That is what capture mode is for, and the first ten minutes of it is your Business Profile. Want to move the first thing in now?"

Set `setup_complete: true` in `bootstrap-progress.md`. If they say yes, load capture mode and go.

⛔ **Nothing else gets offered at the close.** Setup ends on the graph and the first capture. Anything that adds structure to a vault with nothing in it yet is stacking empty rooms, and every capability in this system is earned by activity rather than granted at install.
