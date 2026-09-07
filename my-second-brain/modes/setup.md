# Setup Mode: from bare machine to wired second brain

Setup runs as **three stations, in order**: the foundation, the dashboard, the rest. Each station ends with a close that puts something on the machine in front of the owner, and asks one question: continue now? Keep momentum; no lectures between steps. Record every step's state in `99_Meta/bootstrap-progress.md` as you go (create it first inside the vault once the vault location exists), so an interrupted setup resumes cleanly: on entry, if `bootstrap-progress.md` exists with `setup_complete: false`, resume from the first unchecked step instead of restarting. ⛔ **Only a `- [ ]` line in that file's body is a step.** Its body also carries the wiring check's results, one line per check, and those are findings rather than work left to do. Between stations that first unchecked line is simply the next station's first step, so "continue setup" needs no special handling: it is a resume. ⚠️ **Whether this mode is entered at all is the router's call and not this file's** (`SKILL.md` rule 2): between stations, setup opens only when the owner asks for it.

**A note for whoever edits this file, not for the owner.** A whole room of owners installs at once, and the failure mode is not total time (the stations save almost none of it) but a straight line with no visible end, where any one stuck machine stops the whole room. Three stations turn the line into three legs, each ending with something on the machine the owner can look at. ⭐ **The stations are mandatory and sequential**: Station 1, then 2, then 3, with no option to stop and start using the vault in between. The end of a station is a breather, not a parking spot. ⛔ **Do not renumber any step.** Stations are a grouping layer above the steps and the step labels ride along unchanged, because files all over this product point at them by label. ⛔ **Nothing in this product ever says "run the rest at home"**, or "later", or any equivalent. ⚠️ **Total time is not shorter.** What is shorter is each leg, and the one real saving is the Obsidian download overlapping the scaffold. ⭐ The one thing that would make setup materially faster is the scaffold burst itself, and behaviour rule 8 forbids handing it to a subagent, so that is a separate piece of work rather than something to try here.

## Station 1: The foundation

Ends with the vault on disk, the owner's own command base installed on this machine, and their first project inside it.

### Step 1: Confirm

One opening question (keep it to a line): confirm they want to set up their second brain here and now.

### Step 3: Vault location

Ask: existing Obsidian vault, or new one?

- **New:** propose `~/Documents/<Name>-Second-Brain/` (their name or business name, English, hyphenated; if the business name has not come up yet, ask it here and reuse the answer in step 4). They can pick any path. `mkdir -p` it.
- **Existing vault:** get the path. The scaffold is idempotent (`mkdir -p`, never overwrite an existing file), so a vault with PARA folders already in place is fine; we add what is missing.
- **Existing vault with a structure of its own** (signature: a PARA layout, `06_MOCs/`, an existing command base, anything the owner clearly built and uses): do NOT migrate, rename, or rebuild what they have. What works keeps working. Add only what is missing and clearly ours: the business wing (`04_<Business>-Business-Wing/`), `99_Meta` doctrine plus state files, and `02_Command-Base/` if nothing plays that role yet. Tell them plainly what you are adding and what you are leaving untouched, and be honest about the one real consequence: the doctrine describes a personal wing at `03_Personal-Wing/` that their vault does not have, so on their side the doctrine governs the business wing and the shared layers, and their own personal structure stands. ⛔ Never quietly restructure someone's existing personal folders to match the law; propose it as its own piece of work, another day, or leave it alone. ⭐ **That piece of work now has a tool**, `breakthrough-vault-migrator`, which ships beside this skill and installs in step 6.6: it carries an existing structure into the law's structure in batches, over as many short sittings as it takes, rewriting the links as it goes. ⛔ It is still not a thing that happens tonight and it is still not a thing that happens without the owner asking: name it here as what they can say when they want it, then finish setup.

### Step 4: Name and business (the only interview in setup)

Two quick things, one message each or one compact message, their call:

1. **What to call them.** One line: "And what should I call you?" ⛔ **Ask it, never infer it.** This answer becomes `{{YOUR_NAME}}`, which the generated command-base skill uses throughout and the vault's `CLAUDE.md` puts at the top, so an install that skips the question either invents a name for the owner or addresses them by their business name forever. The vault folder from step 3 is not this answer: it may well be the business's name, and it is a folder name either way.
2. Business name (and its folder-safe English form, e.g. `Aroma Coffee & Co.` -> `Aroma-Coffee`; propose, they confirm). Derive the domain tag from it (`{{BUSINESS_TAG}}`, kebab-case) and confirm that too, in the same breath.

⛔ **Do not ask about the personal wing.** It and its six life rooms are always created; the doctrine states its contents flatly, so a vault missing them does not match its own law.

⛔ **Two questions, and there is no third.** The preset toggles this step used to carry (physical outlets, machines or equipment) are gone, and `Outlets/` and `Equipment/` are not scaffolded at setup at all. They are born the day capture meets them, through the missing-room ladder capture mode already carries (its level ②, where a room that exists only when the business makes it real is proposed and opened rather than invented). ⭐ The reason, briefly, because putting them back will be tempting: two yes/no questions asked before anything has been moved in were two questions setup did not need, and a room costs nothing to open later. ⛔ **Do not add a toggle back.**

### Step 2: Obsidian (viewing deck)

⭐ **Kick the install off and carry on; do not wait for it.** This step starts a download and then leaves, so the download runs while the scaffold does.

Check if Obsidian is installed. If the user simply says it is already installed, take their word and skip the checks:

- macOS: `[ -d "/Applications/Obsidian.app" ]` (also try `~/Applications`)
- Windows: `winget list Obsidian.Obsidian` or check `%LOCALAPPDATA%\Programs\Obsidian`
- Linux: `which obsidian`, flatpak list, or ask

If missing, offer to install it now (recommended; every step of setup works without it, but reading and browsing the vault live there). On a yes, start it in the background and move straight on:

- macOS with Homebrew: start `brew install --cask obsidian` in the background.
- macOS without Homebrew: start the official DMG download from `https://obsidian.md/download` with curl in the background, and when it lands mount it with `hdiutil attach`, copy the .app to `/Applications`, detach. If any step fails, give the download link and move on; do not stall setup.
- Windows: start `winget install Obsidian.Obsidian` in the background.
- Linux: point to the AppImage / flatpak on `https://obsidian.md/download`
- Any failure: link `https://obsidian.md/download` once and continue setup. Nothing downstream hard-depends on it; the come-back before Step 7.9 A looks once more, and Step 8 A carries the link if the app is still not there.

**Then go straight to Step 5.** The download overlaps the scaffold, and that overlap is the one real time saving the stations have. ⛔ **Come back exactly once, before Step 7.9 A**, and confirm the app is present with the detection commands above. If it is not there, give the download link once and carry on: Step 8 A then names the vault path and the link in the slot where it would have said "open Obsidian", in one sentence, without apology.

Nothing about the dashboard depends on Obsidian: it is a generated HTML file that opens in a browser (step 6.95). Obsidian is the reading and graph surface, nothing more.

⛔ **This is the only step that touches Obsidian, and it touches it once.** Setup does not register the vault with Obsidian, does not launch the app, does not bring it to the front, does not open a graph view, and does not teach a keystroke. ⛔ **And it installs no plugin, community or otherwise:** the official URI scheme has no action for the graph, and no third-party plugin gets installed for one keystroke on one night. The close says where the vault is, once (step 8 A); opening it is the owner's. ⚠️ **This paragraph exists because all of that used to be here and was cut on purpose** (2026-08-23), so a session reading these steps does not helpfully put it back. ⚠️ **Amended 2026-09-07, and the amendment is written into this paragraph and dated rather than made silently, precisely because the ⚠️ above tells a later session to cut anything that looks like Obsidian handling.** From that date the Station 1 close asks the owner to open the vault in Obsidian now, as that station's breather, because a station needs something visible at its end, and a folder in Finder is a list while a vault in Obsidian is a picture. Everything the 2026-08-23 cut removed stays removed: the product still does not register the vault, does not launch the app, does not front it, does not open a graph view, does not install a plugin, and does not teach a keystroke. The one sentence that changed is the close's, from "whenever they like" to "open it and look now". ⛔ Do not cut that sentence back, and ⛔ do not grow it into the product driving the app.

### Step 5: The scaffold burst

⛔ **This session builds it. Do not hand this step to a subagent** (behaviour rule 8). The burst copies three long files whole, and a copy made under context pressure comes back as a summary; a session that made that copy itself can at least see what it did, while a session reading a report cannot. ⛔ The same holds for every other step here, and step 6.8 says why it matters most there.

Execute [../references/scaffold-spec.md](../references/scaffold-spec.md) in one go: all folders, every door file (`_<Name>-Guide.md` per room, lane, brand subfolder and wing, plus `_SOP-Menu.md`; ⛔ no playbook folders and therefore no playbook doors, which are born at runtime), `Home.md` as the vault's full directory, `Business-Profile` at the wing root (empty schema), doctrine (from [../templates/structure-doctrine.template.md](../templates/structure-doctrine.template.md)), tagging vocabulary (from [../templates/tagging-vocabulary.template.md](../templates/tagging-vocabulary.template.md)), note templates (from [../templates/note-templates.md](../templates/note-templates.md)), the pre-seeded brand rooms (`Brand-Strategy/` with seven pillar stubs + `Target-Audience/` with the Journey stub, per the spec), and the state files, including working memory `99_Meta/memory.md` (from [../templates/memory.template.md](../templates/memory.template.md); this is what the command-base skill reads and appends every session, so it exists from day one).

Two layers ship deliberately bare and it is worth not "fixing" them mid-burst: `03_SOP/` holds nothing but its menu, and `04_Methodology/` holds two empty folders and zero `.md` files, doors included.

Report one line: "Scaffolded N folders, M files. Home lists all of it." ⚠️ **The wiring check does not run here.** It is step 7.9 A, at the end of this station, because several of its checks test things that do not exist yet at this point (the vault `CLAUDE.md`, the starter project). ⛔ **Never write a count of those checks, here or anywhere**, for the reason step 6.8 gives about the guard set; and ⛔ never report a partial run of them as a score, because a "most of them pass so far" carried forward is how a real install arrived at a total nobody had measured.

### Step 5.5: Vault CLAUDE.md (the always-on context layer)

Skills wake on trigger words; `CLAUDE.md` at the vault root loads into EVERY Claude Code session started there, unconditionally. Without it, a session opened tomorrow with a casual first message has no idea this is a structured vault, and the constitution is just a file lying in `99_Meta`. This step is what makes the rules self-announcing.

- **No `CLAUDE.md` at the vault root** (the normal case): write one from [../templates/CLAUDE.template.md](../templates/CLAUDE.template.md), replacing `{{YOUR_NAME}}`, `{{BUSINESS}}`, `{{BUSINESS_NAME}}`, `{{SLUG}}`, `{{DATE}}`. Write once; later sessions never rewrite it silently (it evolves only through propose-and-approve during maintenance).
- **`CLAUDE.md` already exists** (existing-vault users): **never overwrite and never edit what is there.** Show the user a ready-to-append `## My Second Brain` section (the template's content demoted one heading level, minus the top title) and ask one question: append it for them, or leave it for them to place manually? Append only on an explicit yes.

Record the outcome in `bootstrap-progress.md` (`claude_md: written | appended | left-to-user`).

### Step 6: Generate their command-base skill

From [../templates/command-base-SKILL.template.md](../templates/command-base-SKILL.template.md), replace `{{YOUR_NAME}}`, `{{SLUG}}` (their name or business, kebab-case), `{{VAULT_PATH}}`, `{{BUSINESS}}` (folder name), `{{BUSINESS_NAME}}`, `{{BUSINESS_TAG}}`, `{{COMPANION_SOUL_NAME}}` (`<slug>-companion-soul`; the skill handles its absence until Create-My-Jarvis runs). Zero interview; every value already exists from steps 1 to 4.

Write it to `<vault>/99_Meta/Skills/<slug>-command-base/SKILL.md`, then install:

- macOS / Linux: `ln -s "<vault>/99_Meta/Skills/<slug>-command-base" ~/.claude/skills/<slug>-command-base` (create `~/.claude/skills/` if missing; if a same-named entry exists, ask before touching it). Symlink means editing the vault copy edits the live skill.
- **Windows, default: copy the folder**, and tell them the canonical copy is the vault one. ⛔ A copy means **every later edit to the vault copy leaves the live skill untouched until it is copied over again**, which is why the flag below exists and why the retrofit path in `SKILL.md` reads the installed file back instead of trusting that its edit landed. Staleness on this path is handled; do not reach for a link to solve it.
- **A junction is available if the owner asks for live editing, but say the trade out loud first.** Step 6.8 installs a delete guard, and **that guard is macOS only**. The single accident it exists to stop is a `rm -r` aimed at `~/.claude/skills/` that **follows the link into the vault and destroys the real content behind it**. A copy cannot be followed, so a Windows copy install is the one shape that is safe from this by construction. A junction gives up that safety on the one platform where nothing is watching. ⛔ Do not present the junction as the recommended path, and do not install one without saying this in plain words.
  - Mechanically: `mklink /D` (a directory symlink) needs elevation or Developer Mode; `mklink /J` makes a **junction**, which does not, and on a local disk one folder ends up with two paths. From `cmd.exe`, link first then target: `mklink /J "%USERPROFILE%\.claude\skills\<slug>-command-base" "<vault>\99_Meta\Skills\<slug>-command-base"` (create `%USERPROFILE%\.claude\skills\` first; if a same-named entry exists, ask before touching it). From PowerShell, either `cmd /c mklink /J ...` or `New-Item -ItemType Junction -Path <link> -Target <vault-path>`. **Verify before believing it:** write a marker line into the vault copy, read it back through the `~/.claude/skills/...` path, then remove the marker. If the read-back does not show it, the junction did not take; stay on the copy.
  - **Two known ways a junction will not work.** Junctions are **local volumes only**, so a vault on a mapped network drive or a UNC path (`\\server\share\...`) cannot be junctioned. And a vault living inside a **OneDrive / Dropbox / Google Drive sync folder** can put the sync client and the junction at odds: some clients refuse to traverse it, some follow it and upload a second copy of everything behind it.
- ⚠️ **Everything in the junction branch is untested on Windows.** This skill is developed on macOS and we have no Windows machine to verify against: the commands above, the shell they run in, and whether a Windows `rm -rf` actually follows a junction are all unverified. Treat the whole branch as best-effort, run the verify step rather than assuming, and stay on the copy without drama when anything is unclear.

**Record which one happened.** Set `command_base_install: symlink | junction | copy` in `bootstrap-progress.md`. This is not bookkeeping: it tells a later session whether editing the vault copy is enough or whether a re-copy has to follow. It is a hint, not proof (the owner may have re-installed by hand since), which is why `SKILL.md`'s retrofit path reads the installed file back instead of trusting the flag. Leaving the flag out costs that session its starting guess.

One line on what they just got: "From now on, in any session, say 'morning' or 'log a decision' and this skill runs your day on top of the vault" (from the next session on).

⚠️ **That parenthetical is a measurement, not a hedge.** A skill linked into `~/.claude/skills/` while a session is running is not loaded by that session: measured on 2026-09-07, the Skill tool answered "Unknown skill" to a skill created mid-session, and the harness listed it only a few turns later, on no schedule anyone can rely on. ⛔ **This session must not act out the skill it just wrote.** A "morning" typed now would get an improvisation that reads exactly like the real thing, which is how an owner learns a behaviour their installed skill may not have. It is also why no station's breather asks the owner to type "morning".

### Step 6.6: Install the companion skills that ride in this payload

⛔ **Read the set off the payload, never off this list:** `ls <payload>/skills/` is the registry, and the descriptions below are here so the owner can be told what each one is, not so the count can be quoted. They are **not** generated and **not** personalised: there is nothing to interview, nothing to fill in, and no `bootstrap-progress` question to ask first.

- **`breakthrough-project-consultant`** thinks a project through with the owner before they build it, and proposes the smallest set of working files that project earns (usually a bare brief and nothing else). It is never on the critical path: a project is born legally without it.
- **`breakthrough-session-report`** closes out a working session: it lands the Lesson the session earned, catches decisions that were made but never written, and offers what is reusable. ⛔ It matters that this one ships: the vault's whole capture of judgment now happens at closeout, so shipping the law without this skill would leave `04_Methodology/` with a family, a template, an address and no writer.
- **`breakthrough-method-builder`** writes one Method when a piece of WORK closes: how the owner did that kind of thing, in their words, and writes a playbook whenever the owner asks, which needs no methods first: the owner can dictate one on day one. ⛔ It matters that this one ships for two reasons. It is the other half of the closeout pair, and the two never fire at the same moment (one closes a session, one closes a job). And it is the **only writer of a playbook folder's door**, which doctrine §9.1 makes mandatory from the day such a folder exists: ship the law without this skill and the first method written creates a folder that is out of shape the moment it is made.
- **`breakthrough-vault-guardian`** carries one change to the owner's own law through every file that change touches: section 8, the template it teaches from, the tag vocabulary, `Home.md`, the doors, `CLAUDE.md`. ⛔ It matters that this one ships for a different reason than the three above, and the reason is on paper in the vault it just built: §8 names this skill as the recommended route for an amendment. Ship the law without it and the owner's own constitution points at something that is not on their machine. ⚠️ **The by-hand test below does not decide this one**, because amending by hand is explicitly legal (§8 says so in the same sentence); what decides it is that the law names the tool.
- **`breakthrough-vault-migrator`** moves an existing body of files into the vault without breaking the relationships between the documents: it freezes what is being moved so the boundary stops shifting, has the owner rule on a mapping before anything moves, then moves it in batches and rewrites the links as it goes, resuming from its own tracker across as many sittings as it takes. It is what step 3's "another day" now points at, for the owner who arrives with an old vault, an export, or years of files. ⚠️ **This one is here for a mechanical reason rather than a doctrinal one, and the note at the end of this step spells it out:** migrating by hand is perfectly legal and no rule names this skill, so the by-hand test alone would leave it out. It ships by ruling, it therefore lives in `skills/`, and everything in `skills/` is installed by this step.

**Install every folder under `<payload>/skills/` as its own entry, and link rather than copy wherever the platform allows.** Resolve the running skill's folder (via a global `npx skills add -g` install it is `~/.claude/skills/my-second-brain/`, resolved at runtime). ⭐ **Linking is what makes `npx skills update my-second-brain` carry them along**: update the payload and every companion skill is updated in the same breath, with nothing to re-run here.

1. **Check first.** If `~/.claude/skills/<name>` already exists for any of the folders found, ⛔ do not touch it. Say what is there and move on; an owner may have installed one by hand, and clobbering it loses their copy.
2. **macOS / Linux:** `ln -s "<payload>/skills/<name>" ~/.claude/skills/<name>` for each folder found (create `~/.claude/skills/` if missing).
3. **Windows, default: copy the folder** `<payload>/skills/<name>` to `%USERPROFILE%\.claude\skills\<name>`. ⚠️ **Say the cost out loud:** a copy does not follow payload updates, so `npx skills update` will refresh `my-second-brain` and leave them at the version copied tonight. Re-running this step is how they catch up. The junction trade-off and its whole warning block are in step 6 above and apply here unchanged; ⛔ do not present a junction as the recommended path.
4. **Verify by reading, not by assuming.** For each one, confirm `~/.claude/skills/<name>/SKILL.md` is readable through the installed path and that its first line is `---`. ⛔ A link that was created but does not resolve reads as success to every check except this one.

Record `companion_skills_installed:` in `bootstrap-progress.md` (`linked` / `copied` / `partial` / `failed`, and name any that were left alone because something was already there).

⛔ **Install them, and say nothing about them here.** The one line that introduces this set to the owner is said at Station 3, beside Step 6.7, where the tools this vault names get named; tonight's close (Step 8 A) covers them with "a few tools that came in with it" and no more.

⚠️ **The test that decides whether a skill installs here or only gets named in 6.7, for whoever edits this list next.** It is not preference and not popularity: **ask what the doctrine permits the owner to do by hand.** §1 explicitly permits hand-writing an SOP, so an owner without that skill can still do the work and it is honest to leave it out. §9.1 makes a playbook folder's door mandatory from the day the folder exists and `breakthrough-method-builder` is the only thing in the box that writes one, so an owner without that skill gets a folder that breaks its own constitution the first time a method is written, and nothing else would ever tell them. ⛔ **Never move a skill between the two steps without running that test first.**

⚠️ **One worked example, because the test's answer was overridden once and the next editor to run it honestly would otherwise move the skill.** `breakthrough-vault-migrator` fails the test: the doctrine permits an owner to move their own files by hand, no rule names the skill, and nothing it writes is mandatory from the day something exists. On the test alone it belongs in 6.7 beside `breakthrough-sop-builder`. **It is installed here anyway, and the reason is mechanical rather than doctrinal:** it was ruled to ship with the payload, which puts it under `skills/`, and `ls <payload>/skills/` is this step's registry. Keeping it out of 6.6 while it sits in `skills/` would take an exclusion list, and an exclusion list is a second registry that drifts from the first. ⭐ **So the test decides the line for a tool that could be published separately; it does not decide it for a tool already riding the payload.** ⛔ Do not "correct" this by moving the skill to 6.7: that would leave it installed by 6.6 and described in 6.7 at the same time.

### Step 6.95 A: The starter project

Two halves of one step, in this order. The order is the whole point: the deck is built to read the vault, so the vault has to have something in it first. This half is Station 1's, and `Step 6.95 B` is what Station 2 opens with.

**A. Create the starter project, then name it in Home.** Full shape in [../references/scaffold-spec.md](../references/scaffold-spec.md) (the starter-project section): one project folder in `03_Personal-Wing/Personal-Projects/`, its Brief with **all four deck keys filled** (`started`, `due`, `stage`, `priority`), and three tasks in its `Tasks/` under the three file names that section gives literally. ⭐ Say what it is in one line and no more: "The three things you still have to do after tonight are already in there as tasks. That is your first project, and it is real." ⛔ Do not create a business project, do not invent work the owner has not mentioned, and ⛔ do not fill the four keys with placeholders: they are what the deck's Next Action, Countdown and swimlane bar are derived from, and a Brief the product wrote itself with them blank teaches that frontmatter is decoration.

⛔ **Then add one line to `02_Command-Base/Home.md`, before moving on**, under the `## 03_Personal-Wing` heading:

```markdown
- `Personal-Projects/Second-Brain-Rollout/`: the starter project ([[_Second-Brain-Rollout-Brief|brief]])
```

⚠️ **This is not bookkeeping and it is not optional.** `Home.md` was written back at step 5, from the tree that existed then, and this folder did not. Home calls itself the only directory this vault has, so the moment the owner's first real project is missing from it, that sentence is false, in the first hour, on a correct install. The wiring check `home-is-true` fails on exactly this and has done so on a real end-to-end run. ⭐ Its `Tasks/` folder is deliberately **not** listed: what is inside a project is the project's business and its Brief is the address (doctrine §3). Every folder made after tonight carries the same duty, which is why the frontmatter guard injects it on every `mkdir`; the difference here is that this one is made by the product itself, so the product does it rather than reminding anyone.

### Step 7.9 A: Wiring check, Station 1

⚠️ **First, the one Obsidian come-back Step 2 sends here**, and only if an install was started there: confirm the app is present with Step 2's detection commands. If it is not, give `https://obsidian.md/download` once and carry on. Nothing below depends on it.

⭐ **A check runs at the close of the station that built what it tests, and never again.** By Station 3 the vault may already be in use, and some of these checks fail on a vault that is being used correctly, so they are named here rather than left to be re-derived: `sop-ships-empty` (a lived-in vault with a written SOP fails it correctly), `methodology-ships-empty` (same: a Lesson written at a closeout is the vault working), `brand-stubs-in-place` (a filled pillar flips `status:` off `empty` and this check would report it), and `frontmatter-is-legal` (it reads "every generated `.md`", which is a sentence about the scaffold rather than about the owner's notes; the frontmatter guard and the weekly inspector own legality after that). ⛔ **So no station re-runs an earlier station's checks.** The `## Wiring check` heading in `bootstrap-progress.md` collects the lines from all three stations as they run.

Run the checks the spec's list labels **Station 1**, by name, at the end of [../references/scaffold-spec.md](../references/scaffold-spec.md). ⛔ **Refer to each by its name, never by its number, and never by a count of them**, for the reason written at the top of that list. `progress-keys-match-spec` runs at every station's close, this one included, and its pending logic already handles a key whose step is still unticked. `report-then-hand-over` stays last: it counts the folders and files created inside the vault and writes both numbers into its own line, and those two numbers are what Step 8 A speaks.

⛔⛔ **Every check writes its own line into `99_Meta/bootstrap-progress.md` as it finishes**, under a `## Wiring check` heading: its name, its verdict, and **the value it judged on**. The shape and the reason are in that section of the spec. ⛔ **A verdict with no value beside it is not a finished check**, and ⛔ **nothing anywhere reports a total**, in the file or out loud. ⭐ The reason is the failure this whole step exists to catch: a score is a claim, and the file is the only thing anyone can check it against tomorrow.

Report failures plainly and fix what is mechanically fixable (a missing `Home.md` line, a leftover `{{` placeholder). ⛔ Do not hide a failure to keep the ending clean: the close below is where the owner starts trusting this thing, and a clean-sounding ending on top of broken wiring is how a vault gets abandoned in month three.

**The three disciplines every close obeys, Step 8 A, Step 8 B and Step 8 C alike.** They are written out here because these are the paragraphs a later editor will most easily break.

1. ⛔ **A close never says "later", "at home", "when you have time", "next time", or any phrase that points past now.** The only question is "Continue now?". This is also the product's defence of behaviour rule 3: a hook nearly always grows on the far side of the word "later", so a close that never says it has nowhere for one to grow.
2. **Every sentence in a close names one of three things:** a file that is on the disk, an action this machine can do right now, or the next station's name and what it builds. The next station is named once, as a noun, and never recommended. ⛔ No "you will want", no "the good part is coming", no "most people".
3. ⛔ **Every number in a close is one a wiring check counted a moment ago** (setup's own iron rule, restated here because the close is where it gets broken).

⛔ **Step 8 A and Step 8 B never offer the first capture and never mention capture mode.** That offer belongs to Step 8 C alone, and it is the last thing setup says.

**When the owner answers no at Step 8 A or Step 8 B:** say exactly one line, "Noted. You are at Station N.", and stop. `setup_station: N` is already on disk, and the next station opens when the owner says "continue setup" and at no other moment. ⛔ **Nothing else is said**: the product does not manage the room, whoever is running the room does.

### Step 8 A: Station 1 close

Write `setup_station: 1` into `bootstrap-progress.md`, then speak the close, then ask the one question.

The shape is the same at all three closes: the station is done and what it was · what the owner now holds · go and look · what the next station builds, named once as a noun · "Continue now?". The skill speaks the owner's language and the shape does not change; the station names are written `Station 1` / `Station 2` / `Station 3` literally. The English below is the reference text: keep the shape, substitute the values.

> **Station 1 is done: the foundation.**
> You now have: a second brain at `<vault path>`, `<N>` folders and `<M>` files, every one of them listed in Home. A set of rules that is yours, at `99_Meta/structure-doctrine.md`. A command base of your own, already installed on this machine. A few tools that came in with it. And your first project, with `<T>` tasks already inside it.
> Open Obsidian and look at this vault. That is what you just built.
> Station 2 builds your dashboard. Continue now?

`<N>` and `<M>` are the two numbers `report-then-hand-over` wrote a moment ago at Step 7.9 A. ⛔ Report the numbers that check actually counted, not a fresh estimate; a count improvised at the close has already been measured going wrong on a real install. `<T>` is a count of the files in the starter project's `Tasks/` folder, taken now.

**Where the vault is gets said once**, as the absolute path in that first line, and the owner is asked to open it there and look. ⛔ **Do not open it for them, do not register it, do not name a keystroke.** Setup touched Obsidian once, at step 2, and that was the whole of it. A setup that ends by driving another application is a setup that can get stuck on its own last step.

**If Obsidian is not on the machine** (Step 2's come-back found nothing), the third line becomes: "The vault is at `<vault path>`. Obsidian is at `https://obsidian.md/download`; open the vault there and look." One sentence, and ⛔ no apology.

## Station 2: The dashboard

One job, and it ends on the only picture this product has. ⛔ **Station 2 is not merged into Station 1** even though it holds that one job: the dashboard has to be a station's end rather than a step in the middle of one.

**At the station's entry, probe `python3`**, which is the probe Step 6.95 B carries as its first item, run here so a missing interpreter is known before the station starts rather than halfway through it. It is present on macOS and most Linux; on Windows it is often absent. If it is missing, the second item of Step 6.95 B is what happens next.

### Step 6.95 B: The first dashboard build

**B. Build the dashboard once.** The engine and its display template ship in this skill's payload at `scripts/deck.py` and `scripts/deck-template.html`; resolve the running skill's folder the same way step 6.6 does. ⛔ Neither is ever copied into the vault: the generator is the part that grows patches, and a copy in the vault is a snapshot of tonight that no update can reach.

1. **Probe `python3`.** Present on macOS and most Linux; on Windows it is often absent.
2. **If it is missing, explain before you touch anything.** Say what is missing, what it is for (the dashboard, and the same interpreter the weekly checker and session search already need), and where to get it. ⛔ **Never install it, or change the owner's PATH or system settings, without their explicit yes.** If they decline or cannot right now: record `deck: skipped-no-python` in `bootstrap-progress.md`, say in one line that the dashboard is pending and that "fix my deck" builds it the moment Python is there, and move on. Nothing else in setup depends on it. The fallback for those days is `Home.md` and the starter project's Brief, both plain markdown.
3. **Run it once:** `python3 "<payload>/scripts/deck.py" build "<vault-path>"`. Record `deck: built`, and record what the run actually produced in `deck_build_result:`, an inline mapping carrying the process exit code and the counts the run printed (`{exit: 0, briefs: 1, tasks: 3}`). ⭐ **That key is the whole evidence for the first item of `deck-is-alive`**, which is why it is written here, by the step that ran the build, rather than recalled later: the spec forbids a second rebuild to prove it, and setup can resume in a new session where the run is not in living memory. A build that fails records its real exit code, not an absent key.
4. **Report one line, the one it printed**, e.g. "Command Deck rebuilt: 1 projects, 3 tasks, N notes scanned." ⛔ Do not paste the path and do not open it yet; the deck is handed over at this station's close (Step 8 B).

⚠️ If the build exits non-zero, say so plainly, record `deck: skipped-no-python` only when Python was the actual reason, and carry on. A failed dashboard must never end a setup that otherwise worked.

### Step 7.9 B: Wiring check, Station 2

Run the checks the spec's list labels **Station 2**, by name: `deck-is-alive`, which reads what step 6.95 B recorded in `deck_build_result:`, including the skipped-as-passed case when there is no `python3`, and `progress-keys-match-spec`, which runs at every station's close. ⛔ **Refer to each by its name, never by its number, and never by a count of them.** ⛔ **Do not re-run Station 1's checks**, for the reason written at Step 7.9 A, and ⛔ do not re-count folders and files: this station's close speaks the value its own check wrote.

Every check writes its own line into `99_Meta/bootstrap-progress.md` as it finishes, under the same `## Wiring check` heading Station 1 opened, in the shape Step 7.9 A gives: its name, its verdict, and the value it judged on. Report failures plainly, on the same terms.

### Step 8 B: Station 2 close

Write `setup_station: 2` into `bootstrap-progress.md`, then the close. Same shape, same three disciplines, reference text below.

> **Station 2 is done: the dashboard.**
> `02_Command-Base/Command-Deck.html` is built, and on it are your project and its `<T>` tasks.
> Open it and bookmark it. It is rebuilt every time you start work, so it is always as fresh as the last time you worked, and "rebuild my deck" refreshes it on the spot.
> Station 3 installs the guards that watch this vault and connects the rest of the tools. Continue now?

Open `02_Command-Base/Command-Deck.html` in their browser as that line is said. `<T>` is the task count `deck_build_result:` recorded at Step 6.95 B; ⛔ not a fresh count taken here.

**If step 6.95 B recorded `deck: skipped-no-python`**, the second and third lines become one line instead: "The dashboard is waiting on Python; 'fix my deck' builds it the moment Python is there." Nothing else about the close changes, and ⛔ nothing is apologised for.

## Station 3: The rest

⭐ **The guards install here because the stations are mandatory and sequential, so every vault arrives here.** ⛔ Not because anything earlier catches what the guards catch, and ⛔ do not write a rationale that leans on a gate in capture mode.

### Step 6.8: The standard guards (one explanation, one install, one uninstall)

⭐ **The guards are a set, and this step installs the set.** **Which guards are in the set is read off this payload, never off a number written here:** every `scripts/*-hook.sh` file is one guard, each has its own subsection below, and adding a guard means adding a script and a subsection, not editing a count. ⛔ **Never write "all four" or any other number into this step, into the wiring check, or into what you say to the owner.** The set has already changed size once, and every sentence that carried a count became a lie the day it did.

⭐ **And what each guard NEEDS is read off the guard too, not out of this prose.** Every `scripts/*-hook.sh` carries one `# MSB-GUARD:` line in its header declaring four facts about itself: its `bootstrap-progress` key, the file name it installs as, the `PreToolUse` matchers it must be registered under, and a plain-words `does=`. **Read that line for each guard before doing anything below** (`grep -h "^# MSB-GUARD:" <payload>/scripts/*-hook.sh` returns the whole registry, one line per guard). ⛔ Do not take the key, the file name or the matchers from any sentence in this step or from what the subsections below happen to say: those are descriptions, and a description is a copy. The declaration is the source, and it lives beside the code it describes so the two cannot drift apart. The weekly checker reads the same lines, so all three readers of this registry read the same physical characters.

⭐ **And HOW EACH GUARD PROVES IT IS ALIVE is read off the guard as well.** Beside the registry line, every guard carries at least one `# MSB-PROBE:` line: a call it must refuse (or must allow), written as the exact `PreToolUse` payload Claude Code would hand it, with `{{VAULT}}` where the vault path goes. `grep -h "^# MSB-PROBE:" <payload>/scripts/*-hook.sh` returns them all. Step 4 below pipes each one into the guard as it was actually installed and compares the exit code to what the line demands. ⛔ **Do not compose a payload of your own.** A composed payload invents a case the guard was right to allow, then reads the pass-through as a hole, and files a healthy guard as broken. The guard knows what it refuses; this step does not.

**What they have in common.** Each is a Claude Code `PreToolUse` hook: it sees a tool call before it runs and either lets it through, attaches a note to it, or refuses it. All of them are **read-only** (none writes to the vault, none phones anywhere), all of them **fail open** (anything they cannot parse is allowed), and all of them live in one folder, `~/.claude/hooks/`, registered in one file, `~/.claude/settings.json`.

**This changes the owner's `~/.claude/settings.json`, which is machine-level configuration outside the vault. Explain before you install, and install only on an explicit yes.** One explanation covering the whole set, in plain words, then one yes. Do not walk them through the guards one at a time asking separately; that is the shape this step exists to replace. What the explanation has to contain, per guard: **what it stops · what that costs when it fires · that it is off with one edit.** Then the uninstall, once, for the set.

**The guards that ship in this payload today:**

- **The delete guard** (`scripts/rm-guard-hook.sh`, matcher `Bash`). Stops a recursive delete (`rm -rf` and its variants) aimed at the vault or at `~/.claude/skills`. It exists for one specific, hard-to-reverse accident: the command-base skill installs as a **symlink** under `~/.claude/skills/` pointing INTO the vault, so a plain `rm -r` on that link follows it and destroys the real vault content behind it. It never touches a non-delete command. Placeholder: `__MSB_VAULT_PATHS__`, on exactly one line.
- **The frontmatter guard** (`scripts/fm-guard-hook.sh`, matchers `Write` **and** `Bash`). Judges a note at the moment it is about to be born: it refuses a filename that breaks doctrine §5 and frontmatter that breaks §8, and on a pass it hands the session the filing protocol so notes get filed by the law rather than from memory. It reads the law live out of the vault's own `99_Meta/structure-doctrine.md`, so it can never disagree with the weekly checker. ⚠️ **Tell the owner the one thing about it that will surprise them:** it blocks writing a note through the shell (`cat > x.md`) and points at the Write tool instead, because it can read a Write's content and cannot read a heredoc's. Placeholders: `__MSB_VAULT_PATHS__` and `__MSB_SKILL_DIR__`, one line each.

**Platform.** Both guards are bash plus `python3` and are validated on **macOS**, which is the machine this product is built on. On Windows or Linux, say that plainly, and then **try anyway rather than refusing**: you are here, in a session, and the verify step below is a real test on this actual machine rather than a promise about the platform. If it passes, it passes. If it does not, debug it with the owner on the spot (a missing `python3`, a shell that is not bash, a settings file in a different place), and if it still does not work, say what broke in one line, record the guard as `skipped-platform`, and carry on. ⛔ Do not record a guard as `installed` on a failed or unrun verify, whatever the platform.

**Before installing anything, probe the reader the law travels through.** The frontmatter guard does not carry section 8; it reads it live through `scripts/doctrine_schema.py`, and that reader needs **PyYAML**, which is not in the standard library. Run the reader against the vault once, on the interpreter the guards will actually run on:

```
/usr/bin/env python3 "<payload>/scripts/doctrine_schema.py" "<vault-path>"
```

⚠️ **`/usr/bin/env python3`, not whichever python you have been using.** Every guard invokes its Python that way, so that resolution is the one that decides whether the law is readable. Probing one interpreter and installing into another is a way to be confidently wrong here, and on a Mac with three pythons on PATH it is the likely mistake rather than an exotic one.

- **Exit 0**: it printed the families it read. The law is readable; carry on.
- **Exit 3**: PyYAML is missing for that interpreter, so section 8 cannot be read and **nothing it declares can be enforced**. The reader has already worked out what is true on THIS machine and printed it: the exact install command (it runs PEP 668's own externally-managed test, so a Homebrew python gets `--break-system-packages --user` and a python.org or Command Line Tools python gets plain `--user`) and the directory it will land in. ⭐ **Show the owner those two lines, ask, and on a yes run it yourself** (this is a one-line per-user install into their own site directory, not a system change, and handing them a command to go and run is how a setup ends with a dead gate nobody came back to). ⛔ **Ask first anyway** (it installs software on their machine), and **if the install fails, say so out loud in one line and keep going to the behaviour check below, which will then fail honestly.** ⛔ Never take a failed install quietly: this is the whole reason the check exists.
- **Exit 1 or 2**: something else: the vault has no doctrine yet, or section 8 will not parse. That is a different fault; read what it says before touching the guards.

⛔ **Do not skip the probe because the guard "fails open anyway".** It does fail open, deliberately (a guard that cannot read the law but blocks anyway would wedge every session), and it says so **in the context it injects**, which nobody is reading tonight. Failing open plus nobody reading is exactly a house whose constitution has no enforcer while every check says installed.

On yes, per guard in the set, then once for the settings file:

1. **Build the concrete copy.** Read the payload script and replace every `__MSB_*__` placeholder token it carries: `__MSB_VAULT_PATHS__` with the vault's absolute path from Step 3, and `__MSB_SKILL_DIR__` (frontmatter guard only) with the resolved path of this running skill's folder, the same resolution step 6.6 does. Write the result to `~/.claude/hooks/<the guard's own installs-as value>` (create `~/.claude/hooks/` if missing) and `chmod +x` it. ⛔ Never edit the payload template in place; the path-injected copy lives in `~/.claude/hooks/` and the payload stays clean for the next update.
2. **Register all of them in one edit** to `~/.claude/settings.json` under `hooks.PreToolUse`, each as a `{"type": "command", "command": "<absolute path to the hook>", "timeout": 10}` entry under **every matcher its `MSB-GUARD:` line declares** (`matchers=` is comma-separated; a guard declaring two goes under both). Expand `~` to the absolute path. **Use the official `update-config` skill for this edit if it is available; only hand-edit the JSON as a fallback, and preserve any existing entries under those matchers by appending, never overwriting.**
3. **Verify by reading, per guard**: every placeholder token that guard declares is gone from the installed file (`grep -c __MSB_VAULT_PATHS__` returns 0, and for the frontmatter guard `grep -c __MSB_SKILL_DIR__` too), `bash -n` on it is clean, and the file's path appears in `~/.claude/settings.json` under every matcher it was meant to go into. ⛔ A guard written but not registered, or registered but still carrying a placeholder, is a guard that does nothing while reading as installed to everything except this check.

   ⚠️ **Grep for the whole token, never for the `__MSB_` prefix.** Each guard deliberately keeps a copy of its own placeholder name, built by string concatenation so the full token never appears, and uses it at runtime to notice a botched install. A prefix search hits those sentinels and reports a correct install as broken; that is a real trap.

4. ⭐ **Then verify by RUNNING, per guard, and this is the check that decides what gets recorded.** Everything in step 3 is a reading: the file is there, it parses, it is registered. **A guard can pass all of it and refuse nothing.** So take each `# MSB-PROBE:` line off the payload script, substitute the vault's absolute path for `{{VAULT}}`, **write that JSON to a file**, pipe the file into the guard **as installed in `~/.claude/hooks/`**, and compare its exit code: `expect=block` means exit 2, `expect=allow` means exit 0.

   ⚠️ **Write the payload to a file, or use `printf '%s'`. ⛔ Not `echo`.** In zsh the builtin `echo` expands the `\n` inside the JSON into real newlines, the hook cannot parse its own input, and every guard fails OPEN on unparseable input by design, so the probe reports a dead guard on a perfectly healthy one. Measured on this product, on zsh.

   ⛔ **The probe is piped to the hook. It is never run as a command.** The delete guard's probe names a recursive delete, because that is the thing it exists to refuse.

   **What a failure means, concretely.** A `block` probe that comes back exit 0 is a guard that is installed, registered, clean and **not enforcing anything**. The frontmatter guard's probe is the one that catches a missing PyYAML: its payload is a note with a legal name and a `type:` section 8 has never heard of, so the only thing that can refuse it is the law, read live, just now.

**Uninstall** (tell the owner this once, for the set): delete the scripts from `~/.claude/hooks/` and remove their entries from `~/.claude/settings.json`. Nothing else in the system references them, and nothing breaks without them.

⛔⛔ **This session installs the guards and watches the probes itself. Do not hand this step to a subagent** (behaviour rule 8). ⭐ **This is the step where that matters most:** `installed` is a claim about behaviour, and the only thing that can honestly make it is whoever saw the exit code. A session that says "verified live" on a report it was handed has verified nothing, and the sentence reads identically either way.

**Record one key per guard** in `bootstrap-progress.md`, using **the key that guard's own `MSB-GUARD:` line declares** (`key=`), each set to `installed` / `installed-not-enforcing` / `declined` / `skipped-platform`. ⭐ **Write the probe result beside the keys, in the body, as it happens**, one line per guard in the guard's own words: which probe, what it demanded, what it exited (`rm-guard expect=block actual_exit=2`). ⛔ **That line is written here, by the step that ran the probe, and never reconstructed at step 7.9 C**, which reads files and settings and has no exit code of its own to report; setup can also resume in a new session, and an exit code that only ever lived in a sentence is gone by then. ⭐ **One key per guard rather than one key for the set**, because that is what lets the wiring check count what this step actually did without a number written anywhere, and what lets a later guard join by adding a key instead of by changing a schema.

⛔ **`installed` means step 4 passed.** A guard whose file is in place and registered but whose probe did not behave gets **`installed-not-enforcing`**, plus one line to the owner in plain words saying which guard, what it is not doing, and what would fix it (for the frontmatter guard that is almost always the PyYAML install above). ⛔ Never write `installed` on an unrun or failed probe, and ⛔ never quietly downgrade the probe to "the file looks right". **A guard recorded as installed while enforcing nothing is worse than no guard**, because the owner stops watching for the thing it was supposed to catch. The wiring check `guards-registered` reads these keys, so this value is what makes the failure visible at the end of setup instead of six weeks later.

### Step 6.7: Name the tools this vault points at but does not contain (one line each, no install)

**First, the one line about the skills Station 1 installed silently, no more than this line, and ⛔ without a count:** "A few more skills came with this one. Say 'help me plan this project' when a piece of work is big enough to need thinking through, 'wrap up' when a working session ends and what it taught should be written down, `breakthrough-method-builder` by name when a whole job closes and how you did it is worth keeping, or the moment you want a way of working written down as a playbook, which you can ask for on day one, 'change the doctrine' the day your vault's own rules need to change, and 'move my old notes in' whenever you are ready to bring years of existing files across."

⭐ **This is where that line lives, and Step 6.6 installs those skills without saying anything about them.** This step is its natural home: 6.7 names tools, and this names the ones already on the machine.

Some pieces of work have their own tool, published separately and installed by the owner when they want it. Say each one once, in one line, and only so nothing later reads as if it were already on the machine:

- **Writing an SOP** runs on the `breakthrough-sop-builder` skill. `03_SOP/` ships empty by design and hand-writing an SOP is perfectly legal (doctrine §1); the skill is the comfortable path, not the only legal writer.
- **Filling the brand pillars** runs on the `breakthrough-brand-strategy` skill. The pillar stubs the scaffold just wrote each close with "run the brand intake", and this is what answers to that line, so an owner who is not told the name reads an instruction with nothing behind it. Hand-writing a pillar is legal too, and the skill reads this vault's own law live rather than carrying a copy of it.

⛔ Do not install them here, and do not present them as missing pieces. Nothing in this vault breaks while they are absent. **The test for whether a skill belongs in this step rather than the one that installs them is written at the end of 6.6; apply it before moving anything here.**

⚠️ **What this step is scoped to, because widening it will be tempting and nobody would notice it had happened.** A tool earns a line here only when something this setup wrote into the vault sends the owner to it: `03_SOP/` shipping empty under a doctrine clause that names the skill, and the stubs' own closing line for the other. ⛔ **The authors publish other skills, and none of them belong in this step**: they do work this vault does not do, no file setup wrote points at them, and appending them would quietly turn "the door signs you are obliged to answer" into a catalogue of everything for sale. They are on the repo front page, where anyone looking for them is already standing.

### Step 6.9: Session memory (optional, recommended, validated on macOS)

This step turns on **session memory**: every Claude Code conversation on this machine becomes searchable, so future sessions can answer "how did we fix that last time?" and "why did we choose A over B?" instead of re-solving solved problems.

**Explain before you install.** Three facts, in plain terms, before asking for the yes:

- **What it reads:** only Claude Code's own session transcripts (`~/.claude/projects/`), strictly read-only. It never touches the vault, notes, or any other file, and it never modifies a transcript.
- **Where it writes:** one search database in `~/.my-second-brain/`. That folder sits outside the vault and outside this skill, so a skill update never wipes the index.
- **Purely local:** there is no network code in the tool at all. Nothing is uploaded anywhere. It is also not a background process; it only runs when a session invokes it.

**Platform.** The tool is standard-library Python and needs `python3` plus SQLite with FTS5, which macOS ships. It is validated on **macOS**; on Windows or Linux, say that plainly and then **try it rather than refusing**. The tool carries its own FTS5 probe, so this machine can answer the question that no claim about the platform can: run the probe, and if it passes, keep going. If something breaks, debug it here with the owner (the usual causes are no `python3` on PATH, or a Python built without FTS5) and tell them the one concrete thing that would fix it, for example installing python.org Python rather than relying on what shipped. If it still will not run, say so in one line and record `skipped-platform`. The repo front page's **"Windows self-serve path"** section is the written-down version of the same route for an owner who would rather do it themselves later; point them at it when they defer, not instead of trying.

On yes:

1. The tool ships in this skill's payload at `scripts/session-history/` (self-contained, nothing to download). Resolve the running skill's folder (via npx install it is `~/.claude/skills/my-second-brain/`, resolved at runtime); call the tool's path `<tool>` below.
2. Build the first index: `python3 "<tool>/sh" ingest`. On a machine with a long Claude Code history this can take a little while on first run; incremental runs afterwards take seconds. Report the one-line stats it prints. ⛔ Do not skip this: the query verbs read what `ingest` builds, and until it has run they will say so and stop.
3. Show the owner one search they can try, e.g. `python3 "<tool>/sh" search "the thing we fixed"`, and say plainly: from now on, asking "how did we solve that before" in any session can actually be answered from history.

**Uninstall** (tell the owner once): delete `~/.my-second-brain/session-history.db`. The tool has no hooks, no daemon, and no other footprint.

Record `session_memory_installed:` in `bootstrap-progress.md` (`installed` / `declined` / `skipped-platform`).

⛔ **This step asks one question and only one, and a second must not be added.** ⛔ Do not ask whether the owner wants a weekly pass over their new sessions, and ⛔ do not write a `harvest_auto:` key.

⭐ **What the tool is now, said plainly to the owner in one line, because the difference is the whole point:** it is a filing cabinet, not a colleague who reads it over the weekend. It answers "how did we solve that before" **when somebody asks**, and it never speaks first. What is worth keeping out of a session is decided at that session's own closeout, while whoever was in it still remembers.

### Step 7: Official Obsidian skills (optional, recommended)

Offer once: the Obsidian team publishes official skills (Bases syntax, Obsidian-flavored markdown, web clipping) that make the AI sharper inside Obsidian. Install with `npx skills add -g kepano/obsidian-skills`. Recommended yes; a no costs nothing tonight. Record the answer in `bootstrap-progress.md` (`obsidian_skills_offered:`).

### Step 7.5: Connect a calendar (optional, recommended)

Offer once: connect a calendar so the morning brief can see today's actual schedule, not just the task list. Read-only, folded into the brief, never stored in the vault. Recommend-leaning, because a morning brief that ignores the day's meetings is half-blind, but a skip costs nothing and is reversible any time.

Three choices. Do the lightweight part inline, do not stall setup on OAuth or an install:

- **Google Calendar (recommended):** point them to the one-click connector. Directory panel, Connectors tab, Anthropic and Partners, Google Calendar, click `+`, authorize. Tell them to leave the read-only tools on "Always allow" so the morning read never prompts. Full steps in [../references/calendar-connect.md](../references/calendar-connect.md). Record `calendar_provider: google`.
- **Lark / Feishu:** offer to install the official CLI now (`npm install -g @larksuite/cli`, then `lark-cli config init` and `lark-cli auth login --recommend`) or to do it later. Steps in the reference. Record `calendar_provider: lark` on success (plus `calendar_lark_bin:` if not on PATH); if they defer, record `none` and note where to come back.
- **Skip / later:** record `calendar_provider: none`.

Always record the outcome in `bootstrap-progress.md` (`calendar_offered: true` + `calendar_provider:`). Offer once, never nag; the command-base skill reads the flag every morning and stays silent when it is `none`.

### Step 7.9 C: Wiring check, Station 3

Run the checks the spec's list labels **Station 3**, by name: `guards-registered`, which reads what step 6.8 recorded, one key per guard, and confirms each one it says it installed is actually registered (a declined or platform-skipped guard passes; session memory is not a guard and is not counted), and `progress-keys-match-spec`, which runs at every station's close. ⛔ **Refer to each by its name, never by its number, and never by a count of them**, for the reason written at the top of that list. ⛔ **Do not re-run the checks of Station 1 or Station 2**, for the reason written at Step 7.9 A: the vault may be in use by now. ⛔ And do not re-count folders and files, because this station's close speaks the keys its own steps wrote.

Every check writes its own line into `99_Meta/bootstrap-progress.md` as it finishes, under the same `## Wiring check` heading, in the shape Step 7.9 A gives: its name, its verdict, and the value it judged on. Report failures plainly and fix what is mechanically fixable. ⛔ Do not hide a failure to keep the ending clean.

### Step 8 C: The handover (Station 3 close)

Write `setup_station: 3` and set `setup_complete: true` in `bootstrap-progress.md`, then hand over. Same shape, same three disciplines, reference text below.

> **Station 3 is done. Setup ends here.**
> Installed just now: `<the items whose keys say installed, in plain words: the guards that watch this vault · session memory · the Obsidian skills · your calendar>`.
> What comes next is not setup. It is use: the first ten minutes of capture mode is your Business Profile. Move the first thing in now?

The second line names only what the keys in `bootstrap-progress.md` record as installed or connected. ⛔ An item that was declined, or skipped on this platform, is not named and not apologised for.

If they say yes, load capture mode and go.

⛔ **Nothing else gets offered at the close.** Setup ends on the first capture. Anything that adds structure to a vault with nothing in it yet is stacking empty rooms, and every capability in this system is earned by activity rather than granted at install.
