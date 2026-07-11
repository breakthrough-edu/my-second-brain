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
- **Existing vault built by an earlier personal-AI-OS bootstrap** (signature: `06_MOCs/` exists, or `03_Areas/Command-Base/` exists): do NOT migrate, rename, or rebuild what they have. Their `06_MOCs` and command-base keep working. Add the business wing (`07_...`), `99_Meta` doctrine + state files, and the business-wing pieces only. Tell them plainly what you are adding and what you are leaving untouched, and offer a short routing note they can paste into their existing command-base skill: business decisions and business daily logs live in the business wing; the doctrine file now governs filing.

## Step 4: Business + toggles (the only interview in setup)

Four quick things, one message each or one compact message, their call:

1. Business name (and its folder-safe English form, e.g. 咖啡老王 -> `Laowang-Coffee`; propose, they confirm).
2. Toggle: physical outlets? (yes -> Outlets room + Store-Open-Close SOP room)
3. Toggle: machines or equipment? (yes -> Equipment room + Maintenance SOP room)
4. Toggle: import goods? (yes -> Importing + Stock-Count SOP rooms)

Plus one: pre-open the personal wing rooms (Family, Health, Personal Finance, Property, Vehicles, People), or start business-only and add them when first needed? Either is fine; record the choice.

## Step 5: The scaffold burst

Execute [../references/scaffold-spec.md](../references/scaffold-spec.md) in one go: all folders, all MOCs, Home, `_Map`, `Business-Profile` (empty schema), doctrine (from [../templates/structure-doctrine.template.md](../templates/structure-doctrine.template.md)), tagging vocabulary (from [../templates/tagging-vocabulary.template.md](../templates/tagging-vocabulary.template.md)), note templates (from [../templates/note-templates.md](../templates/note-templates.md)), dashboard `.base` (verbatim from [../templates/command-base.base.template](../templates/command-base.base.template)), the two pre-seeded brand-foundation rooms (`Brand-Strategy/` + `Target-Audience/` with their stubs, per the spec), and the state files, including `99_Meta/graduation-config.md` (from [../templates/graduation-config.template.md](../templates/graduation-config.template.md)) and working memory `99_Meta/memory.md` (from [../templates/memory.template.md](../templates/memory.template.md); this is what the command-base skill reads and appends every session, so it exists from day one). Methodology stays a folder of empty folders; no MOC there, on purpose.

Run the wiring check at the end of the spec. Report one line: "Scaffolded N folders, M files. Navigation is live from Home."

## Step 5.5: Vault CLAUDE.md (the always-on context layer)

Skills wake on trigger words; `CLAUDE.md` at the vault root loads into EVERY Claude Code session started there, unconditionally. Without it, a session opened tomorrow with a casual first message has no idea this is a structured vault, and the constitution is just a file lying in `99_Meta`. This step is what makes the rules self-announcing.

- **No `CLAUDE.md` at the vault root** (the normal case): write one from [../templates/CLAUDE.template.md](../templates/CLAUDE.template.md), replacing `{{YOUR_NAME}}`, `{{BUSINESS}}`, `{{BUSINESS_NAME}}`, `{{SLUG}}`, `{{LANGUAGE}}` (the step 1 choice, written as `English` or `中文`), `{{DATE}}`. Write once; later sessions never rewrite it silently (it evolves only through propose-and-approve during maintenance).
- **`CLAUDE.md` already exists** (existing-vault users): **never overwrite and never edit what is there.** Show the user a ready-to-append `## My Second Brain` section (the template's content demoted one heading level, minus the top title) and ask one question: append it for them, or leave it for them to place manually? Append only on an explicit yes.

Record the outcome in `bootstrap-progress.md` (`claude_md: written | appended | left-to-user`).

## Step 6: Generate their command-base skill

From [../templates/command-base-SKILL.template.md](../templates/command-base-SKILL.template.md), replace `{{YOUR_NAME}}`, `{{SLUG}}` (their name or business, kebab-case), `{{VAULT_PATH}}`, `{{BUSINESS}}` (folder name), `{{BUSINESS_NAME}}`, `{{BUSINESS_TAG}}`, `{{COMPANION_SOUL_NAME}}` (`<slug>-companion-soul`; the skill handles its absence until Create-My-Jarvis runs). Zero interview; every value already exists from steps 1 to 4.

Write it to `<vault>/04_Resources/Skills/<slug>-command-base/SKILL.md`, then install:

- macOS / Linux: `ln -s "<vault>/04_Resources/Skills/<slug>-command-base" ~/.claude/skills/<slug>-command-base` (create `~/.claude/skills/` if missing; if a same-named entry exists, ask before touching it). Symlink means editing the vault copy edits the live skill.
- Windows: symlinks often need elevation; copy the folder instead and tell them the canonical copy is the vault one (re-copy after edits).

One line on what they just got: "From now on, in any session, say 'morning' or 'log a decision' and this skill runs your day on top of the vault."

## Step 6.6: Install the pod-maker skill (the pod surgery tool)

The `pod-maker` skill ships **inside this skill's payload** as a `pod-maker/` subfolder. It is **static and identical for every user** (a tool that reads the vault constitution and scaffold at runtime, not personalized content), which is why it is **symlinked from the payload** rather than generated into the vault the way the command-base skill is. A skill nested inside another skill's folder is not independently discoverable by Claude Code, so surface it by linking that subfolder up into the skills directory:

- Locate this running skill's folder (the `my-second-brain` skill dir; via npx install it is `~/.claude/skills/my-second-brain/`, resolved at runtime). Its `pod-maker/` subfolder is the payload.
- macOS / Linux: `ln -s "<my-second-brain-skill-dir>/pod-maker" ~/.claude/skills/pod-maker` (create `~/.claude/skills/` if missing; if a `pod-maker` entry already exists, ask before touching it). Symlinking means an `npx` update of `my-second-brain` refreshes pod-maker automatically, and it matches the same symlink discipline the command-base skill uses.
- Windows: symlinks often need elevation, so copy the folder instead (`pod-maker/` into `~/.claude/skills/pod-maker`) and tell them the canonical copy is the payload one, so re-copy after any skill update. Same fallback as the command-base Windows path.

Record `pod_maker_installed:` in `bootstrap-progress.md` (`symlinked` on macOS / Linux, `copied` on the Windows fallback). One line to the owner, only if they ask what it is: "pod-maker is the tool that grows a busy function (marketing, sales...) into its own self-learning pod when it earns one; say 'forge a pod' or 'graduate my marketing' when the time comes."

## Step 6.8: Safety lock (optional, recommended, macOS only)

This step installs a **read-only accident net**: a Claude Code hook that blocks a recursive delete (`rm -rf` and its variants) aimed at the vault or `~/.claude/skills`. It exists because of one specific, hard-to-reverse mistake. The command-base skill and pod-maker install as **symlinks** under `~/.claude/skills/` that point INTO the vault; a plain `rm -r` on one of those links follows it and destroys the real vault content behind it. The hook stops exactly that. It is an accident net, not a security boundary: it fails open (allows) on anything it cannot parse, and it never blocks non-delete commands.

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

**Platform honesty.** The tool itself is standard-library Python and needs `python3` plus SQLite with FTS5, which macOS ships. It is validated on **macOS only** at this stage; on Windows or Linux, say so, skip, and record the skip. Do not improvise a port.

On yes (macOS):

1. The tool ships in this skill's payload at `scripts/session-history/` (self-contained, nothing to download). Resolve the running skill's folder as in step 6.6; call the tool's path `<tool>` below.
2. Write the config so harvest reports know where the vault Inbox is: create `~/.my-second-brain/session-history.json` containing `{"vault": "<vault-path-from-step-3>"}` (create the folder if missing; if the file exists, update only the `vault` key).
3. Build the first index: `python3 "<tool>/sh" ingest`. On a machine with a long Claude Code history this can take a little while on first run; incremental runs afterwards take seconds. Report the one-line stats it prints.
4. Show the owner one search they can try, in their language, e.g. `python3 "<tool>/sh" search "the thing we fixed"`, and say plainly: from now on, asking "上次怎么解的 / how did we solve that before" in any session can actually be answered from history.

**Uninstall** (tell the owner once): delete `~/.my-second-brain/session-history.db` and `session-history.json`. The tool has no hooks, no daemon, and no other footprint.

Record `session_memory_installed:` in `bootstrap-progress.md` (`installed` / `declined` / `skipped-platform`).

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

What they see is their second brain as a constellation: every room wired to Home, business wing on one side, personal wing on the other, all of it empty and waiting. Say it straight, in their language, something like: "That is your second brain, half built. The structure is done; the memories are not moved in yet. That is what capture mode is for, and the first ten minutes of it is your Business Profile. Want to move the first thing in now?"

Set `setup_complete: true` in `bootstrap-progress.md`. If they say yes, load capture mode and go.

## Step 8.5: Offer the Marketing pod (recommend-leaning, never mid-burst)

After the graph moment (or at the first capture, whichever comes first), offer the core **Marketing pod** once. Placement matters: never embed this inside the scaffold burst, so the "under 10 minutes" promise holds; it comes at the close, as a clearly separate beat. Tone is **recommend-leaning**, not neutral: every business does marketing, and the pod is the one core capability that ships polished.

The offer must say two things plainly, because they resolve the tension between "day 0 value" and "don't stack empty structure":

1. **The seed is usable on day zero.** The Marketing pod ships with generic-but-real marketing doctrine and a loop-config, so it can do useful marketing immediately. It is not an empty shell.
2. **The learning part waits for real activity.** The loop (the part that grows this business's own marketing judgment) only starts once there is real activity and feedback to learn from. The early-maturity rule that would send a from-scratch pod back to a thin room governs *forging* a pod with no seed; it does not govern this *pre-seeded patch*, which is why offering it on day 0 is sound.

Frame it as recoverable, not a one-way door: if it turns out unused, the weekly maintenance demotion scan will notice and offer to shrink it back (learning preserved, per doctrine section 9). That safety net is what makes an early yes safe.

Installing the pod runs the shared pod-install flow owned by the **`pod-maker` skill**, which was installed in step 6.6. On the owner's yes, hand off to pod-maker to load its shipped Marketing patch (`pod-maker/patches/marketing/`): mechanically this is a graduation (it grows the always-present thin `Marketing/` room into a wing-level pod, carrying the room's `Action-Log` up intact), with the patch supplying the day-0 seed brain. Do not half-build a pod by hand: if for some reason `pod-maker` is absent (an interrupted step 6.6), record the owner's answer and note the install is pending pod-maker, rather than improvising the structure. Record the outcome in `bootstrap-progress.md` (`marketing_pod_offered:` + `marketing_pod_installed:`).
