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

Execute [../references/scaffold-spec.md](../references/scaffold-spec.md) in one go: all folders, all MOCs, Home, `_Map`, `Business-Profile` (empty schema), doctrine (from [../templates/structure-doctrine.template.md](../templates/structure-doctrine.template.md)), tagging vocabulary (from [../templates/tagging-vocabulary.template.md](../templates/tagging-vocabulary.template.md)), note templates (from [../templates/note-templates.md](../templates/note-templates.md)), dashboard `.base` (verbatim from [../templates/command-base.base.template](../templates/command-base.base.template)), and the state files, including working memory `99_Meta/memory.md` (from [../templates/memory.template.md](../templates/memory.template.md); this is what the command-base skill reads and appends every session, so it exists from day one). Methodology stays a folder of empty folders; no MOC there, on purpose.

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

## Step 7: Official Obsidian skills (optional, recommended)

Offer once: the Obsidian team publishes official skills (Bases syntax, Obsidian-flavored markdown, web clipping) that make the AI sharper inside Obsidian. Install with `npx skills add kepano/obsidian-skills`. Recommended yes; a no costs nothing tonight. Record the answer in `bootstrap-progress.md` (`obsidian_skills_offered:`).

## Step 8: The graph moment

Close setup with the payoff:

1. Tell them to open Obsidian -> Open folder as vault -> pick the vault path (skip if already open).
2. One-time check: Settings -> Core plugins -> **Bases** enabled (the dashboard needs it).
3. Open graph view (the network icon, or Ctrl/Cmd+G).

What they see is their second brain as a constellation: every room wired to Home, business wing on one side, personal wing on the other, all of it empty and waiting. Say it straight, in their language, something like: "That is your second brain, half built. The structure is done; the memories are not moved in yet. That is what capture mode is for, and the first ten minutes of it is your Business Profile. Want to move the first thing in now?"

Set `setup_complete: true` in `bootstrap-progress.md`. If they say yes, load capture mode and go.
