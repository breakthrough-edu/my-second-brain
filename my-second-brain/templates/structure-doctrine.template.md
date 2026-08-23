---
type: doctrine
doctrine_version: 4
created: {{DATE}}
last_updated: {{DATE}}
maintained_by: the owner (AI proposes amendments, owner approves)
---

# Structure Doctrine

Read this before creating or filing anything in this vault. This file is the single source of law for where things live. Changing it is an amendment: propose, get the owner's yes, then edit.

⚠️ **`doctrine_version` in the frontmatter above is a machine marker, not decoration.** It is a bare integer, and it records **which generation of the product built this house**. Nothing reads it today, and it is still written on every new house on purpose: a house that goes unstamped can never be dated afterwards, because the folders do not say which generation shaped them, and guessing a generation from folder shapes has already been measured misreading a stranger's own Obsidian vault. ⛔ **So do not delete this key as an orphan.** Keep amending this file freely; the number moves only when the product's structure itself moves, and only through the same propose-and-approve. ⛔ Do not edit the number by hand: editing it makes it lie, and the whole point of it is that it cannot.

## 0 · Filing decision tree (run top to bottom, stop at first hit)

1. **Path gates first.** Some things have a reserved lane, no judgment needed:
   - Daily journal entry → `01_Daily/` (end-of-day compile only)
   - A decision → `02_Command-Base/Decisions/` (one decision, one note; if it changes a price or any other stored state, update that state's note in the same breath: the decision records the change, the entity note holds the current truth)
   - A task → `<its project>/Tasks/`. **A task must have a project.** If none fits, propose opening one (small is fine) before the task exists; if you cannot tell which lane or wing it belongs under, ask the owner. There is no parking lot for homeless tasks.
   - Weekly review / monthly theme → `02_Command-Base/Reviews/`
   - A template → `99_Meta/Templates/`
   - Retired material → `98_Archive/`
   - A hypothesis → `99_Meta/Hypotheses/`. **The machine writes it: the weekly ritual's distillation half, and the `breakthrough-session-report` skill when a session throws off a claim.** Nothing you file by hand ever lands here: the pool is where maintenance parks a claim that is not yet earned, and it graduates out on evidence. Do not create one to hold an idea. ⚠️ **What sits on a playbook door is not this.** That folder's own door (§9) carries an index of what the playbook produced, plus the owner's own bets on the rows that carried one: the pool is the machine observing the owner, a door's bottom half is the owner testing their own way of working. The pool never enters a session's context; a door is read every time its folder is opened, which is why they cannot be one family.
2. **Everything else: identify the type family** (§8 has the closed list).
   **2b. Map the family to its home:** entity → its room in `01_Assets/` (or the matching Personal-Wing room) · process (sop) → `03_SOP/` · playbook / lesson → `04_Methodology/` · brand-strategy → that brand's `<Brand>-Brand-Assets/` · brand-research → that brand's `<Brand>-Brand-Assets/Brand-Research/` · resources → `02_Command-Base/Resources/` · guide / brief / menu → with the folder or project they describe · control → `99_Meta/`, and setup is what puts them there (the control plane is declared in §8 so a correct install is not flagged for its own machinery, not so that new ones get filed by hand).
3. **If no family fits: STOP.** Do not force it in. Do not invent frontmatter. Propose a new family: a new template plus a new row in §8, get a yes, then file. (The frontmatter guard blocks a hard schema violation: a bad filename, a missing required key, a value outside a closed list. A key §8 has not declared is a judgment call, not a violation, so the guard **flags it to this session** instead of blocking: register it in §8 if this kind of note always carries it, drop it if it was invented on the spot.)
4. **Two plausible homes?** Check the precedent table (§2). If the case is genuinely new, ask the owner once, then record the answer as a new precedent line. Never ask the same question twice.
5. **Every filing appends one line to `99_Meta/filing-log.md`** (date · what · where · which rule decided it). The weekly ritual's distillation half reads the log for patterns: three filings to the same missing home become a proposal. ⛔ **The distillation half, not the anti-drift half**: the anti-drift half writes this log and never reads it back, and naming the wrong half here has already sent one reader hunting for a check that was sitting in the other file all along.

## 1 · Structure

Top level (numbers are anchors, gaps in the middle are allowed):

```
00_Inbox/            unfiled holding area, whole vault shares it (maintenance drains it; anything still sitting there when maintenance runs gets named)
01_Daily/            the only journal, also the only activity log
02_Command-Base/     the operator's desk, above both wings
03_Personal-Wing/    personal life
04_{{BUSINESS}}-Business-Wing/   first business (a second business takes 05_, a third 06_...)
98_Archive/          retired things, always second-to-last
99_Meta/             law, state, memory, templates, skills, the hypothesis pool
```

- **Archive and Meta are the fixed tail (98/99).** Business wings grow downward from 04. Never renumber Archive to make room.
- **02_Command-Base** holds: `Home.md` (the vault's full directory, see §3), `Decisions/`, `Reviews/`, `Resources/` (the owner's library: Clippings, Courses, Books, Prompts, Tools), `Command-Deck.html` (generated dashboard).
- **03_Personal-Wing** holds: `Personal-Projects/` plus six life rooms (`Family/ Health/ Finance-Personal/ Property/ Vehicles/ People/`). Nothing else.
- **Business wing, four layers** (numbers tell the story: what it's made of, what's moving, how things get done, why decisions go the way they go):
  - `01_Assets/`: what the business is made of. Entity rooms: `Clients/ Vendors/ Employees/ Company-Docs/ Marketing-Assets/ IT-Systems/` (plus `Equipment/ Outlets/` when relevant) and one `<Brand>-Brand-Assets/` folder per brand (holding `Brand-Strategy/`, `Target-Audience/`, `Products-Services/`; a fourth room, `Brand-Research/`, is legal beside them and holds the evidence those brand answers rest on, and it is made the first time evidence is written rather than at setup).
    ⚠️ **The eight brand pillars are one family (`type: brand-strategy`) living across two of those subfolders**: seven in `Brand-Strategy/`, and the Journey pillar in `Target-Audience/` (it is the customer journey, so it files with the audience it maps). Type comes from the family, never from the folder (§0 step 2), and this is the case where the two do not line up in the obvious way. All eight carry a `pillar` value from the closed list in §8.
  - `02_Work/`: the activity layer, four lanes. Every project lives in exactly ONE lane, chosen by the filing ladder (ask in order, first yes wins):
    - `Deliver/`: is this work for a specific NAMED customer or hot prospect? A client job (an engagement) is one project here from pursuit to handover; its `stage:` field tracks the lifecycle (pursuing → executing → closed), the project never moves. Recurring service for a named customer (a standing weekly order) stays ONE Deliver project indefinitely at `stage: executing`; Run is internal-only, and Deliver is deliberately excluded from the re-homing rule below.
    - `Grow/`: else, is it aimed at people who haven't bought yet, addressed as an audience? (content, ads, channels, offer design)
    - `Run/`: else, would this work still exist if the business never grew? (recurring upkeep, maintenance, routine)
    - `Build/`: else, by elimination: finite internal work that leaves the business different when done (new capability, tooling, training, expansion, R&D).
    The ladder classifies by facts the work observably has (a name, an audience, recurrence), never by which department would own it in a big company; this vault has no departments. When a `Grow/` or `Build/` project turns into routine, the finite project archives and the recurring residue re-homes to `Run/`.
    Lanes hold projects, never loose materials; the files inside a project (transcripts, drafts, exports) are project materials, live with it, and need no frontmatter family. **When a project closes, its reusable outputs graduate to the entity room that owns them** (campaign output → `Marketing-Assets/`); the rest archives with the project. Standing materials go to `01_Assets`: first try the entity room that naturally owns them; only when nothing absorbs them and they keep accumulating does a new materials room get proposed (IT-Systems and Marketing-Assets are the two standing precedents).
    **Naming a room: name it after what it holds, and add a suffix only when the bare noun would be ambiguous.** `Clients` needs nothing. `Marketing` is both an activity and a pile of material, so it is `Marketing-Assets`. `IT` alone says too little, so it is `IT-Systems`. ⛔ Never name a room by which lane produced its contents: lanes move (a `Grow` project that turns routine re-homes to `Run`), and a name that records a moving fact becomes a lie the day it moves (§5). ⛔ And never a name any file could belong to: no `Materials/`, no `Assets/`.
  - `03_SOP/`: ships empty. One process, one note, flat. **Flat means no category subfolders**; a note's own same-named folder is not a subfolder, and a finished SOP normally has one (its swimlane diagram and every other non-markdown file live beside their note, per §2). The `breakthrough-sop-builder` skill is the recommended way to write one, **not the only legal writer**: it ships separately, so a vault can be running without it, and **hand-writing an SOP here is legal**. Either way the shape is governed by the template and the frontmatter guard. Steps dictated before the shape settles park in a working folder, `00_Inbox/<process-name>-sop-draft/`. Cross-lane by nature, so it lives centrally and links out via frontmatter.
  - `04_Methodology/`: `Lessons/ Playbooks/`. Ships empty on purpose. **Capture never writes here**, and nothing lands without the owner's yes. Weekly maintenance is the usual proposer, and the owner asking for it out loud is the other; `breakthrough-method-builder` is the skill that carries out either.
- **Business-Profile.md** sits at the wing root: the one-page anchor of what this business is.
- **A second business** = a new wing (05_), same internal shape, its own value in the domain vocabulary. The wing shape is pre-approved here; adding its domain value to §8 rides along without a separate amendment.

## 2 · Filing tests and precedents

The test sentence for any item: **"when something goes wrong, where would the owner look for this?"**

Precedent table (settled, do not re-argue):

| Case | Home |
|---|---|
| Facts about a specific client | `01_Assets/Clients/` |
| How we win or serve clients | `03_SOP/` |
| A client job / engagement (named customer, pursuit through delivery) | ONE project under `02_Work/Deliver/`, lifecycle tracked by `stage:`, never split or moved |
| Someone we are only talking to (a prospect, a landlord, a candidate) | an entity note in the room they would join if it works out (a landlord or lessor files under `Vendors/`; the premises itself, once leased, becomes an `Outlets/` entity); pursuing a named CUSTOMER prospect, if worth tracking, is a `Deliver/` project at `stage: pursuing`; Deliver is only for people who pay us, so pursuing a landlord, supplier or hire is `Build/` (or `Run/`) work with the person filed as an entity. **That entity note carries `status: prospective`** while it is still only a conversation, and flips to `active` the day it becomes real (they sign, they start, they buy). Writing `active` because the template ships that way is the failure this line exists to prevent: it is a legal value, so nothing will ever warn you |
| Employee policy / handbook material | `01_Assets/Employees/` (the room absorbs it) |
| Systems, logins, who holds which account | `01_Assets/IT-Systems/` |
| Pointers to external row systems, and their monthly snapshots | on the entity note of the system that produces them (POS → its IT-Systems note) |
| Price of an offer | its note in `<Brand>-Brand-Assets/Products-Services/` (single source of price truth; a price change is a decision note PLUS an update here, same breath) |
| Reusable marketing output (posts, photos, testimonials) | `01_Assets/Marketing-Assets/` |
| Positioning, brand identity answers | `<Brand>-Brand-Assets/Brand-Strategy/` |
| The method for doing brand strategy | `04_Methodology/` (methods live here, a brand's answers live with the brand) |
| Saved articles, courses, book notes | `02_Command-Base/Resources/` (the artifact; ATTENDING a course, as an undertaking, is a `Build/` project, two homes on purpose) |
| Owner's car / house / policy papers | the matching room in `03_Personal-Wing/` (a paper with a deadline gets `renew_by` on that room's entity note) |
| Non-markdown files (PDFs, photos) | a subfolder next to the note that owns them; the note is the address, the folder is its closet |

## 3 · Anchoring and finding

Three ways anything is found, and only three:

1. **Home.md**: the full directory of the vault (folders plus guide files). The only **vault-wide** directory that exists; §4 names the two deliberate exceptions, and both are scoped indexes of one folder's own business rather than second directories of the vault. Maintained by machine: whoever makes a folder writes its name in, in the same breath, and the frontmatter guard injects that duty on every `mkdir`; weekly maintenance audits it against the filesystem.
2. **Type queries**: frontmatter (`type:`, `cb:`, `renew_by:` and friends) is how dashboards, radars and checkers find things. Entity notes are found by type plus address, not by links.
3. **Backlinks**: activity lives in `01_Daily/` as journal lines that **link to the guide or brief of what they belong to**. One mention, everything else derives. Briefs are linked bare; guides are linked path-qualified (§5).

The anchoring law: **link once, derive the rest.** Written out:

- Work on a project → the journal line links `[[_<Project>-Brief]]`. The project's address already says which lane, which wing, which dashboard swimlane; nothing is written twice.
- A task lives in `<Project>/Tasks/`, so its location already says which project, lane and wing it belongs to. That is why task frontmatter has no project, lane or domain keys: the folder path carries that information.
- Activity with no project → business side links the lane's guide (fixed the display fridge → `[[04_{{BUSINESS}}-Business-Wing/02_Work/Run/_Run-Guide]]`), personal side links the life room's guide (car repair → `[[03_Personal-Wing/Vehicles/_Vehicles-Guide]]`). Guides are always linked with their path (§5); the same room name repeats across wings, so the short form stops being unique the day a second business arrives.
- Things that naturally span several places (decisions, SOPs) live centrally, once, and carry fields (`domain:`, `lane:`) so each wing or lane can filter its own view. Things that naturally belong to one place (tasks, project files) live in that place and carry no redundant fields.
- Moving or renaming a linked file: the move itself must rewrite inbound links (scan, rewrite or leave a `_MOVED` stub, verify zero dead links). Weekly maintenance re-checks as backstop.

**Every folder's `_*-Guide.md` is its manual: read it before working there. `_*-Brief.md` is a project's status card.** That sentence is written in three places on purpose, word for word: here, in `CLAUDE.md`, and in the command-base skill. It is the one wiring instruction that has to reach a session no matter which of the three it happens to load, so it is quoted rather than paraphrased; ⛔ an edit to any one of the three is an edit to all three.

Guide files: every folder that needs explaining has one file `_<Name>-Guide.md`. It says what the room is for, what belongs here, and collects observations. **It is not a directory** (Home is). Guide names repeat across wings by design, so they are **fixed names addressed by path** (§5, regime B); an agent reaching one globs `_*-Guide.md` inside the folder it is already standing in, never by name across the vault. Projects have `_<Project>-Brief.md` instead: a status card (status, dates, owner, brand, goal, deliverables), linked bare because project names are unique. **Two deliberate exceptions map content, and they are named here so nobody has to judge**: `_SOP-Menu.md`, which lists the processes this business should have including the ones not written yet; and the bottom half of a playbook folder's door (§9.2), which indexes the outputs made with that playbook and ⛔ nothing else. Both are scoped to one folder's own business, which is what keeps Home the only place that answers "what is in this vault".

## 4 · Iron laws

1. **High-frequency business rows never enter the vault** (invoices, POs, attendance, POS data, ad-spend rows). The vault keeps: a pointer to where they live, exception narratives, and monthly snapshots, all on the entity note of the system or party that produces them. Nothing else. (A personal habit tick in the daily journal is a journal line, not a business row; it is fine. Any aggregate view of habits is a dashboard query over `01_Daily/`, never a new note type.)
2. **Passwords never enter the vault.** `01_Assets/IT-Systems/` records which systems exist and who holds each login; credentials live in a password manager; the vault stores pointers only.
3. **The expiry key is `renew_by`**: one key across the whole vault (company docs, outlets, equipment, personal property and vehicles). If a date means "act before this day", it goes in `renew_by`, details in the body.
4. **`04_Methodology` is earned, never captured.** Capture never writes here, and **only the owner's yes lands anything**. (A rule the owner declares on the spot is not blocked by this: standing rules are decisions, they land in `Decisions/` immediately; see §7.)
5. **CLAUDE.md and this file are never silently rewritten.** They evolve only through propose-and-approve.
6. **Folder and file names are English**, hyphenated, no spaces.

## 5 · File naming

A name is an address. Two regimes, and the test is one question: **is this file a standard artifact that exists once per folder or per wing?**

- **Regime A, unique names.** Everything else. The name is unique across the whole vault, so `[[wikilinks]]` resolve without ambiguity: notes, decisions, lessons, SOPs, entity notes, project materials.
- **Regime B, fixed names.** One per folder or per wing, always reached **by path**, never by a bare wikilink: **every `_<Name>-Guide.md`**, plus `Business-Profile.md` at each wing root and `_SOP-Menu.md` in each `03_SOP/`. A vault with two business wings holds two files of each of these names (both wings have a `Run/` lane, so both have a `_Run-Guide.md`), which makes a bare `[[_Run-Guide]]` ambiguous by construction.
  **Path-qualified means the link carries enough of the path to be unique**: `[[04_{{BUSINESS}}-Business-Wing/02_Work/Run/_Run-Guide]]`. It is still a wikilink, so it still registers as a backlink, which §3 depends on. A markdown link to the same path works too.
  This applies to **every** guide, including the personal wing's, where nothing collides today. One uniform rule survives the day a second wing appears; a rule conditional on how many wings exist does not.
  `_<Project>-Brief.md` is the deliberate exception: project names are Regime A and therefore unique vault-wide, so a brief is linked bare.

**Dated records are `YYYY-MM-DD-keyword-slug.md`.** The date is **when the thing happened, not when the note was typed**. A decision made on Monday and written up on Friday carries Monday.

**No bare generic nouns in Regime A.** `findings.md`, `notes.md`, `decisions.md` and their kind are banned. A name that could belong to any note belongs to no note: the next search returns five of them and picks the wrong one.

**A name carries only facts that do not change.** Date and kind are safe. Which project, lane or wing something belongs to is not: those move, and a filename that records them becomes a lie the day they do. Belonging lives in the path and the frontmatter, which is where §3 reads it from anyway.

⭐ **Methods and playbooks are where that rule bites hardest, so they name it in the filename itself:** `<the-work>-method.md` and `<the-kind-of-work>-playbook.md`, named for **the work**, ⛔ never for the case that taught it. `quoting-a-renovation-method.md`, ⛔ not `the-tan-house-method.md`. A method written during one job is about the job, not the client, and the client is exactly the fact that changes.

⭐ **The folder they live in carries that same work name with no suffix** (`04_Methodology/Playbooks/quoting-a-renovation/`), ⛔ never `<the-work>-playbook/`. What a folder holds changes over its life: methods, a playbook, both, and in either order (§9.1). A folder named for one of those states is false on some day of its life and would have to be renamed on the day it stops being false. That is the rule directly above: a name carries only facts that do not change.

**The `_` prefix means front door.** `_<Name>-Guide.md`, `_<Project>-Brief.md`, `_SOP-Menu.md`. **At most one `_`-prefixed file per folder**, so an agent that globs `_*.md` in a folder gets exactly one hit. A file without the prefix is content, never a door.

Names are English, hyphenated, no spaces (§4, law 6).

Three enforcement layers: **templates teach** (each template's bottom comment block carries the naming convention for its own type, which is where per-type specifics live), **the frontmatter guard blocks** (unknown shapes don't land), **the checker sweeps** (weekly lint catches what slipped). This section owns the system; the templates own the per-type detail.

## 6 · Tags

Controlled vocabulary in `99_Meta/tagging-vocabulary.md`. New tags and new enum values are proposals first: approved, then used.

## 7 · Judgment and process: decisions, lessons, methods, playbooks, SOPs

Five kinds, five questions:

- **Decision = a call that still stands.** One decision, one note, in `02_Command-Base/Decisions/`, landed the moment it is made. A decision's `lane:` is the lane of the work it governs (pricing and offer rules: `grow`; delivery-of-work rules: `deliver`; routine and upkeep rules: `run`; capability bets: `build`). The set of ACTIVE decisions, filtered by lane, IS the rulebook: "never discount below 20%" is simply a decision that never expires. When a new decision replaces an old one, the NEW note names what it replaces via `supersedes:` (written once, at birth) and the old note just flips to `status: superseded`; history comes free. Event decisions (hire this person, buy that oven) flip to `closed` once executed, so the active set stays a rulebook and not a junk drawer. **Guardrail duty: before landing a new decision, check the active set; on conflict, ask the owner "change the rule, or break it once?"** ⛔ The guardrail runs **before the note lands, in the same breath as the decision**, never on a queue that clears later. Its entire value is in the word "before": deferred to the end of the day, a ten o'clock decision and a three o'clock decision that contradicts it both land, and the conflict waits for a human to trip over it. A decision the owner made and nobody wrote down gets caught at closeout as a backstop, and ⛔ **the backstop runs the same guardrail** rather than skipping it for being late.
- **Lesson = a pit.** Something that actually hurt, recorded so it never surprises twice. `04_Methodology/Lessons/`, grouped in subfolders when a string of them shares a subject. It lands at the closeout of the session the pit happened in, with the owner's yes. Two sections and they are not the same kind of sentence: **what happened is history and never changes**; **what we now do differently is alive and gets edited** when the world moves. If the reason for a change is that you got better rather than that the world changed, that is a Method, not an edit to a Lesson.
- **Method = one move of yours, written down.** How you personally do one kind of thing, landed at the closeout of the work that taught it. `04_Methodology/Playbooks/<the-work>/`, the folder for that kind of work, named `<the-work>-method.md`. Named for the work, ⛔ never for the case it came from (§5). Rewritten whole when you find a better way; the same name is updated rather than a second file created, so the note carries how many times you have done this without counting anything.
- **Playbook = judgment composed.** The methodology of a kind of work: what to weigh, how to decide. In the same folder, beside the methods it came from. It is **earned**, and there are exactly two ways to earn it, ⭐ **with deliberately different bars**. **The weekly distillation may propose one only off several related methods** that turn out to be one way of working: that bar is what stops a machine generalising off a single job. **The owner asking for one out loud needs nothing at all**: a playbook may be the first note in its folder, written on day one, dictated from how they already work. ⭐ **"Earned" means the owner's confirmed judgment put it there**, never captured and ⛔ never the machine's own idea; it has never meant a count of methods. ⛔ Neither route is a skill deciding on its own (§9, and `breakthrough-method-builder` is the skill that writes it either way).
- **SOP = steps.** A dead process anyone can follow. Lives flat in `03_SOP/`; usually written through the `breakthrough-sop-builder` skill, legally hand-written when that skill is not installed (§1).

**Only two kinds of edge exist between them: BECOMING and REFERENCING.** They are not interchangeable and the difference decides whether a note moves:

- **Becoming happens once, in one place: several Methods become a Playbook.** The methods flip to `status: superseded` and carry `distilled_into:` naming the playbook they fed, so the question "which fights did this come out of" always has an answer. ⛔ Nothing else in this vault becomes anything. A Lesson never becomes a Playbook, a Decision never becomes a Playbook, a Playbook never becomes an SOP.
- **Referencing is the other edge, and it is one-directional by design.** A Playbook may reference the Lessons and Decisions behind it (`references:`, written **once, when the playbook is born**). An SOP may reference the Playbook it leans on (`playbook:`). ⛔ **A Lesson and a Decision never register who cited them.** The pointer always lives on the note that is being written anyway at the moment the relationship is created; a list on the other end would have to be revisited every time, and a list nobody updates is worse than no list.

Runtime reading order: doing an SOP → need a judgment call, open the linked playbook and the lane's active decisions → hit (or suspect) a pit, check lessons first.

Content flows, types don't transmute. "The same trade-off decided the same way five times" does not grow into a playbook on its own, because a decision is a ruling and a method is a way of working, and only the second one composes.

## 8 · Record schema (machine-readable; the single source, no copies anywhere)

The frontmatter guard and the checker read this section live and keep no copies: a family, a required key, a closed list, or a key whose values this section leaves open is declared here once and nowhere else. Both go through one reader (`scripts/doctrine_schema.py`), which parses this block on every run, so there is no generated config and nothing to keep in sync; "generated" would still be a second artifact, and the sync is what rots. The checker reports what breaks the law here, and the guard stops a hard violation before it lands: a bad filename, a missing required key, a value outside a closed list. The families below ship with this vault, so they are enforced from day one. Amend this section and both enforcers change with it in the same breath.

```yaml
# Reading rule, so a reader hard-codes nothing: at the top level a key is read by its VALUE.
# A mapping of mappings holds the families. A mapping of one-line strings declares the OPEN
# keys (see the bottom). A list is a field name plus its closed list, global to all families.
# Inside a family, `required` `optional` `marker` `multi` `extends` `cardinality` are reserved
# keys; every other key is a field name whose value is either that field's closed list (a
# list) or that family's subtypes (a mapping). `multi` = a field that may carry several
# values at once. `extends` = values this family adds to a top-level closed list.
# ⛔ The consequence of that rule, and it bites silently: once a family has subtypes, the
# family contributes its subtypes and NOT itself, so `required` `optional` `multi` written
# at the family level are dropped and enforce nothing. A closed LIST written at the family
# level still reaches every subtype, which is why `entity`'s `status: [active, prospective]`
# is live while a `required` next to it would not be. A key every subtype shares is
# therefore written on every subtype's own line, one at a time, and the repetition is the
# price of the rule rather than an oversight.
families:
  guide:      {required: [type, guide_family, updated],
               guide_family: [wing, room, lane, brand, playbook]}   # brand = a subfolder
                                          # of <Brand>-Brand-Assets/ ; playbook = one playbook
                                          # folder under 04_Methodology/Playbooks/, holding one
                                          # kind of work. Every playbook folder has one.
  brief:      {required: [type, status, updated],
               optional: [started, due, owner, brand, stage, depends_on, hide_on_deck, priority],
               status: [active, done, killed],
               stage: [pending, planning, pursuing, executing, closed]}
  menu:       {required: [type, updated]}
  entity:                                 # eleven subtypes, one kind of real-world thing each,
                                          # and each one declares the keys its own template
                                          # ships. That is what lets this block tell a key the
                                          # PRODUCT wrote from a key somebody invented on the
                                          # spot: the first kind is declared here, so only the
                                          # second kind is ever reported as a judgment call. A
                                          # field added to a template is a name added to that
                                          # subtype's line, in the same breath. `renew_by` and
                                          # `status_since` are on all eleven: the expiry key is
                                          # the one deadline key in this vault and belongs to
                                          # whichever entity has a deadline, and the status date
                                          # belongs to every status.
    status: [active, prospective]         # the real-world state of the THING itself, not
                                        # this note's fill state: none of the eleven subtypes
                                        # ships an empty-shell template, so this follows the
                                        # majority pattern, not brand-strategy's. `prospective`
                                        # is the one value in this whole block sourced from a
                                        # PRECEDENT instead of a template: §2 already rules that
                                        # "someone we are only talking to (a prospect, a
                                        # landlord, a candidate)" IS an entity note. ⛔ No
                                        # `retired`: leaving is a MOVE to `98_Archive/` (§0 path
                                        # gate, §1), and an in-place value for it would be a
                                        # legal way around the move.
                                        # `status_since:` is OPTIONAL and stays optional: the day
                                        # the status above was last set. `prospective` is the one
                                        # value here that is supposed to stop being true, and
                                        # `active` is a legal word for a note nobody has looked at
                                        # since the deal closed, so the date is what makes "how
                                        # long has this said prospective" a question anyone can
                                        # answer. ⭐ One reader exists: the weekly anti-drift
                                        # pass takes it as a date written INSIDE the note, which
                                        # beats the file's timestamp when it judges what has gone
                                        # cold, because copying a vault rewrites every timestamp
                                        # and moves nothing a person typed. ⛔ And no check counts
                                        # the days: writing the ruler comes before reading it, and
                                        # a threshold for "too long" is the owner's business rhythm
                                        # to set, not this product's to guess. Same key, same
                                        # meaning, as `ritual.monthly-theme` below.
    client:          {required: [type, status],
                      optional: [renew_by, status_since, source, since, current_terms]}
    vendor:          {required: [type, status],
                      optional: [renew_by, status_since, supplies, terms, contact]}
    employee:        {required: [type, status],
                      optional: [renew_by, status_since, role, started]}
    product-service: {required: [type, status],
                      optional: [renew_by, status_since, price, cost]}
    company-doc:     {required: [type, status],
                      optional: [renew_by, status_since, doc_kind, issuer,
                                 location_of_original]}
    equipment:       {required: [type, status],
                      optional: [renew_by, status_since, model, purchased, last_serviced]}
    outlet:          {required: [type, status],
                      optional: [renew_by, status_since, address, licenses]}
    it-system:       {required: [type, status],
                      optional: [renew_by, status_since, holder]}
    marketing-asset: {required: [type, status],
                      optional: [renew_by, status_since, asset_kind, where_it_lives]}
    property:        {required: [type, status],
                      optional: [renew_by, status_since, address]}
    vehicle:         {required: [type, status],
                      optional: [renew_by, status_since, plate]}
  record:
    decision: {marker: "cb: decision", required: [cb, date, status, domain, lane],
               optional: [supersedes, project], status: [active, superseded, closed],
               extends: {lane: [personal, family, health, finance-personal,
                                property, vehicles, people]}}  # the personal wing's lanes,
                                          # decisions only, on top of the lane list at the bottom
    task:     {marker: "cb: task", required: [cb, status, created],
               optional: [start, due, waiting_on, depends_on, priority],
               status: [not-started, in-progress, waiting, blocked, done]}
  process:                                  # `confirmed_by_owner` appears on three of these
                                            # four and means one thing: the owner who was in
                                            # the room said yes, out loud, at the moment this
                                            # note was written. ⛔ It does NOT mean a process
                                            # approved it, a queue cleared it, or a weekly
                                            # pass proposed it and nobody objected. Silence
                                            # is not a yes, and a yes that arrived a week
                                            # later belongs to whoever was in the room then.
    sop:      {required: [type, lane, owner, last_verified], optional: [playbook],
               multi: [lane]}                                  # lane is multi-value
    method:   {required: [type, lane, status, confirmed_by_owner],
               optional: [distilled_into],
               status: [active, superseded]}   # one move of the owner's, written at the
                                    # closeout of the work that taught it (§7). `superseded`
                                    # is set by the weekly distillation when several methods
                                    # compose into a playbook, and `distilled_into` names
                                    # that playbook. ⛔ No `kind:` key and there never will
                                    # be one. The FOLDER records which kind of work this is
                                    # (§9.1), chosen by one binary question at writing time,
                                    # "this folder or a new one", ⛔ never by asking what
                                    # category the work falls under. The burden this rule
                                    # guards against is being asked to classify at the moment
                                    # the job just closed; picking off the shelf is not that.
    playbook: {required: [type, lane, status, confirmed_by_owner],
               optional: [references], multi: [references],
               status: [forming]}   # only sourced value (Playbook.md template); describes
                                    # the methodology's maturity, not this note's fill state.
                                    # No second value is sourced anywhere. `references` is
                                    # the ONE pointer added for the lesson and decision edge
                                    # (§7): written once, when the playbook is born, on the
                                    # note being written anyway.
                                    # ⛔ There is deliberately no matching key on lesson or
                                    # decision: a back-list would need revisiting forever.
    lesson:   {required: [type, date, source, lane, confirmed_by_owner]}
  hypothesis: {required: [type, status, destination,
                          weeks_supported, weeks_silent],
               status: [open, expired, graduated, rejected],
               destination: [profile]}   # the pool has exactly one landing point:
                                        # patterns about the owner that only observation can
                                        # establish, destined for `99_Meta/profile.md`. The key
                                        # stays required and stays a closed list of one, because
                                        # a closed list earns its keep only by refusing what is
                                        # not on it, and a list of values nobody writes refuses
                                        # nothing while looking like it does.
  ritual:
    daily:          {required: [type]}
    weekly-review:  {required: [type, week_of, reviewed_on]}
    monthly-theme:  {required: [type, month, status, status_since],
                     status: [active, closed]}   # `active` from the Monthly-Theme.md
                                        # template; `closed` is the word the template's own
                                        # comment now names ("flips status to closed"), which
                                        # is what `status_since` was always for. ⛔ One closing
                                        # value, not two: nothing anywhere reads a theme's
                                        # status (a decision splits `superseded` from `closed`
                                        # only because `supersedes:` has readers), so "expired"
                                        # versus "replaced" would change no action and would be
                                        # a wish, not a rule.
  resources:  {type: [clipping, course, book, prompt, tool-note], required: [type],
               optional: [source]}
  brand-strategy:   {required: [type, pillar, status],
                     pillar: [DNA, Personality, Proposition, Relationship, Sensory-Cues,
                              Positioning, Style, Journey],
                     status: [empty, filled]}   # unlike every other status family below,
                                                # this describes THIS NOTE's own fill state,
                                                # not a real-world lifecycle.
  brand-research:   {required: [type, updated],
                     optional: [source, brand]}
                                        # the evidence behind the pillars: what was found, and
                                        # what the owner already believed, both of which the
                                        # answers in Brand-Strategy/ get built on. ⛔ Not
                                        # "market research". An owner's own conviction is
                                        # evidence here too, and a family named after looking
                                        # outward would push it somewhere else.
                                        # `updated` is required the way it is on guide, brief
                                        # and menu; what differs is the REASON. This is the one
                                        # family whose age changes whether you can still trust
                                        # what it says: a competitor read or a customer read
                                        # goes stale while the note goes on sounding just as
                                        # certain, and a pillar built on it inherits that
                                        # without saying so. ⛔ Nothing checks this date. The
                                        # freshness check reads maintenance-state.md's
                                        # `last_tidy` and `last_distill` and nothing else, so
                                        # the key is a date for a person to weigh, not a rule
                                        # with teeth.
                                        # `source` follows resources: it separates what was
                                        # actually looked up from what was recalled. The two
                                        # read identically on the page and are not worth the
                                        # same.
                                        # `brand` is for a vault holding more than one, the
                                        # same key brief carries. The note's folder already
                                        # names the brand, so declaring the key is what keeps
                                        # the guard quiet when a session writes it anyway.
                                        # ⛔ No closed list of research topics, now or later.
                                        # Which question a note answers is carried by its
                                        # filename and its title. A list here would freeze one
                                        # school's vocabulary into this vault's law, and every
                                        # change to that vocabulary would arrive as an
                                        # amendment.
  control:                                  # this vault's own machinery: one file each,
                                            # directly in 99_Meta/, written by setup rather
                                            # than filed by hand. Declared here so a correct
                                            # install is never warned about its own control
                                            # plane. ⛔ The 99_Meta STATE files (bootstrap-
                                            # progress, capture-progress, maintenance-state,
                                            # filing-log, capture-buffer) are deliberately
                                            # NOT here and never will be: they carry no
                                            # `type:` at all, so nothing mounts them and a
                                            # correct install is silent about them already.
                                            # `memory.md` is the sixth of those: not a
                                            # progress file but the session's own working
                                            # notepad, and it carries no `type:` for exactly
                                            # the same reason.
                                            # The line: a file with `type:` is a document a
                                            # person reads; a file without one is a machine's
                                            # notepad. Adding the key to a notepad is what
                                            # CREATES the warning, not what silences it.
                                            # `required` is deliberately thin: a
                                            # constitution, a tag table, a threshold config
                                            # and a person's dossier have almost nothing in
                                            # common to demand, and a schema invented to
                                            # cover all four would fit none. Tighten each
                                            # one when its shape settles.
    doctrine:        {required: [type],
                      optional: [doctrine_version, created, last_updated,
                                 maintained_by]}
                                        # the four keys this file's own template ships,
                                        # declared for the reason the other three
                                        # control files declare theirs: a house must
                                        # not be reported for the machinery it was
                                        # born carrying. Undeclared until 2026-08-22,
                                        # which made the frontmatter guard read a
                                        # freshly written constitution as a note
                                        # carrying four keys nobody had registered.
                                        # ⛔ `doctrine_version` being a LEGAL key here
                                        # is not permission to touch it. This file's
                                        # own header rules on it in one line, `Do not
                                        # edit the number by hand`, and that rule
                                        # is untouched by this line: declaring a key
                                        # tells an enforcer the product wrote it, and
                                        # says nothing about who may change it after.
                                        # The number moves when the product's
                                        # generation moves, through the product, and
                                        # no other way.
    vocabulary:      {required: [type],
                      optional: [maintained_by, last_updated, version]}
    profile:         {required: [type],
                      optional: [subject, last_updated, maintained_by]}
  singletons:
    home:              {required: [type],
                        optional: [updated]}
                                        # `updated:` ships on the scaffolded Home.md
                                        # itself, and the directory is re-audited
                                        # against the filesystem at every maintenance
                                        # run (§3), so the date is part of the file
                                        # rather than something a session invented.
                                        # Same omission as `control.doctrine` above,
                                        # closed on the same day and for one reason.
    business-profile:  {required: [type, business],
                        optional: [founder_name, brand_name, industry, category,
                                   location, one_line_description, created,
                                   last_updated]}
lane: [deliver, grow, run, build]           # the four-lane ladder, see §1; decisions may also use
                                            # the personal lanes in families.record.decision.extends
domain: ["#personal", "#{{BUSINESS_TAG}}"]  # one value per wing; a new wing's value rides along at wing birth
open_keys: {tags: "legal on every note, and the words themselves are governed by §6 and by
                   99_Meta/tagging-vocabulary.md rather than by section 8"}
                                            # An open key is the opposite of a closed list,
                                            # not a loose one: a closed list above names the
                                            # only legal values and refuses every other one,
                                            # while an open key names the KEY and refuses no
                                            # value. Both are declared here for the same
                                            # reason, which is that an enforcer must be able
                                            # to tell a key this vault ships from a key
                                            # somebody invented while writing a note, and
                                            # the answer to that lives in this block alone.
                                            # ⛔ Giving one of these names a closed list
                                            # anywhere in this section contradicts the line
                                            # above, and the reader stops instead of picking
                                            # which half of the block to believe.
```

Example frontmatter, a decision: `cb: decision · date: {{DATE}} · status: active · domain: "#{{BUSINESS_TAG}}" · lane: grow`. A client: `type: client · status: active`.

Adding a family or a required key = amending this file (propose-and-approve). There is no other copy to keep in sync. The `breakthrough-vault-guardian` skill is the recommended way to carry an amendment through every file it touches (this file, the note templates, the tag vocabulary, `Home.md`, the folder doors, `CLAUDE.md`); amending by hand is legal, and the guard and the checker read the result the same way either way.

## 9 · Playbook folders: one folder per kind of work, and its door

9.1 What a playbook folder is. `04_Methodology/Playbooks/` holds folders, not loose
files: **one folder per kind of work**, named for the work with no suffix (§5). A folder
holds its playbook, the methods that kind of work throws off, and **one door,
`_<Name>-Guide.md`, which is mandatory from the day the folder exists**. ⭐ **A folder
is born either way round**: from the first method written when a job closes, or from the
owner dictating the playbook itself on day one (§7). Whoever writes the first note,
method or playbook, makes the folder and writes the door in the same breath; ⛔ a folder
without its door is the one shape this layer does not have.

⭐ **Why a folder rather than a flat file.** "Which fights did this come out of" is the
question a **composed** playbook has to be able to answer (§7), and a folder answers it
by opening rather than by searching. ⭐ **The test for whether a folder belongs here is
not how full it is**: it is whether the owner does that kind of work and wants their way
of doing it kept. A folder holding one playbook and its door, with no methods at all, is
a legal and ordinary day-one shape.

⚠️ **What this costs, said plainly rather than discovered later.** The older form kept
every degree of maturity at one flat address, so a single listing showed the whole
ladder at a glance. A listing of folders shows the **kinds of work** instead, and how
far any one of them has got takes one more opening to see. That is the trade that was
made: the ladder is a little less visible, the provenance is a lot more.

9.2 The door has two halves, and they do not age at the same rate.

**Top half: how to use this playbook.** Three states, and the folder can start in
either of the first two: the playbook's own summary from day one when the owner dictated
one; one line pointing at the method while the folder holds only methods; the playbook's
summary once one is composed.
It goes stale, so it gets revised, and ⛔ revising it takes the owner's yes like
everything else in this layer (§4 law 4).

**Bottom half: everything made with this playbook, where it is, and what came back.**
⭐ **One row per output, and the first column is an address**: a wikilink or path when
the thing lives in the vault, a URL or a plain-words location when it does not. That
column is the point of the table. Three months later, "what have I actually made with
this" and "where is it" are one glance, and ⛔ neither is answerable from anywhere else.

| What came out | What I expect | When it counts | What happened | So |
|---|---|---|---|---|

The address goes in when the output ships, and the owner is asked exactly one question,
which is what they expect from it. ⭐ **"Nothing in particular" is a real answer and the
row still lands**, address only, the bet columns blank. The last two columns are for the
rows that carried a bet, filled when the result is back.

⛔ **A row with no bet is never chased.** Nothing comes back later to ask how it went,
because there was no question. It is an index entry, and being findable is the whole of
its job. ⚠️ **This is a deliberate floor on how much the door can nag**, and it is why
the one question at ship time is allowed to be answered with a shrug. ⛔ **Every row lands the way everything else in this layer lands: the machine
drafts it, the owner says yes.** §4 law 4 is not carved out here and does not need to
be; a table the machine could write into by itself would be the first thing in
`04_Methodology/` that the owner did not put there.

⭐ **"When it counts" is the owner's own number, not the calendar's.** A post is
answered in about a week, a proposal in about a month, a course in about a quarter.
Whoever writes the row asks, because the maturing time belongs to that line of work and
nothing else knows it. ⛔ **It is left blank on a row with no bet**, and a blank there is
what tells beat 1 there is nothing to settle.

⭐ **The same sentence appearing in the "So" column for the third time is the signal to
revise the top half.** That is the whole trigger mechanism. It is deliberately a person
noticing a repeat rather than a number crossing a configured line, because the number
would need somebody to tune it and the repeat needs nobody.

⚠️ **This table used to forbid exactly what it now requires, so here is where each of
the old protections went.** Home's monopoly survives, narrowed to what it always really
was: Home is the only **vault-wide** directory, and this table indexes one playbook's own
outputs and ⛔ nothing else (§3, which names it as one of the two scoped exceptions). The
door's length is held by the two-layer rule below, unchanged. The bets-only purity is
gone on purpose: it bought a tidy table at the price of the owner not being able to find
his own work, and the iteration trigger is unharmed because it reads only rows whose
"So" is filled, so index rows cost it nothing.

⛔ **One carve-out, and it comes from iron law 1 (§4).** A line of work that ships at
high frequency (daily content is the case that exists) ⛔ does not get a row per output:
that is a high-frequency row, and those never enter the vault. Its door carries **one
pointer line naming where those rows actually live**, and keeps individual rows only for
the outputs that carried a bet. ⭐ The test is the same one §4 already uses everywhere
else: if you would not want it as a note, you do not want it as a row.

⚠️ **The bottom half grows, and it is read every single time the folder is opened**, so
it is kept in two layers: **what has been learned** (a few permanent lines, which are
the "So" sentences that came up a third time) and **the recent rows**. Older rows sink
below them. ⛔ Skipping this is how the door dies: not by being wrong, by being long.

9.3 The order of a session that uses a playbook, and ⭐ the order is the design.

1. **Settle what is open.** Read the bottom half first. Any row whose date has passed
   with nothing in "What happened" gets looked up wherever the answer actually lives
   (the messages, the orders, the sign-ups), drafted, and put to the owner as one
   question. ⛔ **A row with a blank date is not open and is never chased** (§9.2): it
   carried no bet, so there is no question to bring back.
2. **Revise, if a sentence just came up for the third time.** The owner's yes first,
   then the top half changes.
3. **Do the work**, with a top half that was brought up to date a minute ago.
4. **Register what came out**, in the same session, one row, ⭐ **its address first**,
   then the bet columns when the owner has an expectation and blank when they do not.

⭐ **Settling comes before the work and not after it.** Put it after and it becomes a
chore attached to a finished job, which is where rituals of this kind die.

⛔ **The door carries these four beats in its own words**, at its own top. That is what
makes a playbook folder something the owner can hand to an assistant, a contractor or
another AI and have it still work: ⭐ **nothing in this section depends on which skills
happen to be installed.**

9.4 One kind of work, one folder (the split test). Segments of methodology that get used
on the same outputs live as chapters of one playbook, sharing one door. A stream with
its own outputs and its own feedback is a different kind of work, so it is its own
folder. Split before the door's bottom half starts holding two conversations.

9.5 A line that goes cold needs no closing ceremony. ⭐ **Rows sitting unsettled past
their date are themselves the evidence that the line went quiet**, visible to anyone who
opens the door, which is why nothing here scans for silence and no folder is ever
closed. ⛔ Nothing in this layer is deleted either: a kind of work that comes back finds
its own history waiting, which is the point of having written it down.

9.6 Discipline. Every change here runs propose → approve → log, like every structural
change in this vault.

## Revision log

- **{{DATE}}**: v4, written at vault setup. Four-layer business wing (`01_Assets` / `02_Work` / `03_SOP` / `04_Methodology`), guide files as folder doors, `02_Command-Base` as its own top-level layer, §8 as the machine-readable record schema, §9 as playbook folders: one folder per kind of work, born from either end (the owner dictates the playbook on day one, or the first method written when a job closes), each with a mandatory door whose top half says how to use the playbook and whose bottom half indexes every output made with it, by address, with a bet on the rows that carried one. The prose here is the human record; `doctrine_version: 4` in the frontmatter is the same fact in the form a machine can read, and the two say v4 together or one of them is wrong.
