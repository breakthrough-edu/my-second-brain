# Scaffold Spec: the fully wired vault (tree v6)

This is the exact structure Setup mode creates. The principle is **full wiring**: not bare folders but every door file pre-built, every frontmatter shape already legal under the doctrine, every template in place. The AI always has a firm anchor to file against; the owner never faces a blank page. Keep every generated file light: a door sign, a filing test, an Observations section. No tutorials inside doors, and no inventories anywhere: **Home.md is the only directory this vault has** (doctrine §3), and a second list is a second thing to keep true.

All `mkdir` operations use `mkdir -p` (idempotent). **Never overwrite an existing file** during scaffold; skip and report instead.

Replace `{{BUSINESS}}` with the business folder name (English, hyphenated, e.g. `Aroma-Coffee`), `{{BUSINESS_NAME}}` with the display name, `{{BUSINESS_TAG}}` with the domain tag (kebab-case, e.g. `aroma-coffee`), `{{DATE}}` with today. **Scope exception:** inside the files written to `99_Meta/Templates/`, keep `{{DATE}}` literal; those are starter shapes for future notes and the date is filled when each note is created.

**The law this file builds.** Everything below is the physical form of `templates/structure-doctrine.template.md`. Where the two ever disagree, the doctrine wins and this file is the bug. Section references in this document point at that file.

## Full tree

```
<vault>/
├── CLAUDE.md                       (always-on session context; setup step 5.5, written once, never silently overwritten)
├── 00_Inbox/
├── 01_Daily/
├── 02_Command-Base/
│   ├── Home.md                     (the vault's full directory, the only directory that exists)
│   ├── Decisions/
│   ├── Reviews/
│   ├── Resources/
│   │   ├── _Resources-Guide.md
│   │   └── Clippings/  Courses/  Books/  Prompts/  Tools/
│   └── Command-Base.base           (verbatim from templates/command-base.base.template)
├── 03_Personal-Wing/
│   ├── _Personal-Wing-Guide.md                     (guide_family: wing)
│   ├── Personal-Projects/     + _Personal-Projects-Guide.md
│   ├── Family/                + _Family-Guide.md
│   ├── Health/                + _Health-Guide.md
│   ├── Finance-Personal/      + _Finance-Personal-Guide.md
│   ├── Property/              + _Property-Guide.md
│   ├── Vehicles/              + _Vehicles-Guide.md
│   └── People/                + _People-Guide.md
├── 04_{{BUSINESS}}-Business-Wing/
│   ├── _{{BUSINESS}}-Guide.md                      (guide_family: wing; carries Current state)
│   ├── Business-Profile.md                         (wing root, per §1)
│   ├── 01_Assets/
│   │   ├── Clients/           + _Clients-Guide.md
│   │   ├── Vendors/           + _Vendors-Guide.md
│   │   ├── Employees/         + _Employees-Guide.md
│   │   ├── Company-Docs/      + _Company-Docs-Guide.md
│   │   ├── Marketing-Assets/  + _Marketing-Assets-Guide.md
│   │   ├── IT-Systems/        + _IT-Systems-Guide.md
│   │   ├── Equipment/         + _Equipment-Guide.md          (toggle: equipment)
│   │   ├── Outlets/           + _Outlets-Guide.md            (toggle: outlets)
│   │   └── {{BUSINESS}}-Brand-Assets/  + _{{BUSINESS}}-Brand-Assets-Guide.md
│   │       ├── Brand-Strategy/    + _Brand-Strategy-Guide.md   (+ 7 pillar stubs)
│   │       ├── Target-Audience/   + _Target-Audience-Guide.md  (+ Customer-Journey-Mapping.md)
│   │       └── Products-Services/ + _Products-Services-Guide.md
│   ├── 02_Work/
│   │   ├── Deliver/           + _Deliver-Guide.md
│   │   ├── Grow/              + _Grow-Guide.md
│   │   ├── Run/               + _Run-Guide.md
│   │   └── Build/             + _Build-Guide.md
│   ├── 03_SOP/
│   │   └── _SOP-Menu.md                            (the only file; the folder itself ships empty)
│   └── 04_Methodology/
│       ├── Lessons/  Playbooks/
│       └── (NO .md files anywhere in 04_Methodology: the empty layer is the point)
├── 98_Archive/
└── 99_Meta/
    ├── structure-doctrine.md       (from templates/structure-doctrine.template.md)
    ├── tagging-vocabulary.md       (from templates/tagging-vocabulary.template.md)
    ├── filing-log.md
    ├── bootstrap-progress.md
    ├── capture-progress.md
    ├── maintenance-state.md
    ├── lab-gate-config.md          (from templates/lab-gate-config.template.md)
    ├── memory.md                   (from templates/memory.template.md)
    ├── capture-buffer.md           (durable staging for in-the-moment captures)
    ├── Hypotheses/                 (the pool; weekly maintenance is its only writer, §0)
    ├── Skills/                     (the generated command-base skill lives here, setup step 6)
    └── Templates/                  (see the note-template list below)
```

**Doors, and only one per folder.** Every folder that needs explaining carries exactly one `_`-prefixed file (§5): a `_<Name>-Guide.md` for rooms, lanes, brand subfolders and wings; `_SOP-Menu.md` for `03_SOP/`. Two rules follow, and the wiring check enforces both:

- **The four layer folders get no door.** `01_Assets/`, `02_Work/`, `03_SOP/` (beyond its menu) and `04_Methodology/` are containers of rooms, not rooms. `guide_family` is a closed list (`wing / room / lane / brand / lab`, §8) and a layer is none of them, so a layer guide could not carry a legal value. The wing guide explains the four layers in one place; Home lists them.
- **`04_Methodology/` ships with zero `.md` files**, guides included. Capture cannot write there and nothing lands without the owner's yes (§4, law 4); an empty layer with a welcome sign is not empty.

## Preset toggles

Two yes/no questions at setup, recorded in `bootstrap-progress.md`:

1. **Physical outlets?** (shopfront, branches) → `01_Assets/Outlets/`
2. **Machines or equipment?** → `01_Assets/Equipment/`

Untoggled rooms are simply not created. Either can be proposed later during capture when the business turns out to need one (propose, owner approves, create). There is no third toggle any more: the old importing toggle only ever created SOP subfolders, and `03_SOP/` now ships empty and flat (§1).

## The personal wing is not a question

`03_Personal-Wing/` and its six life rooms are always created, no question asked. The doctrine states the wing's contents flatly (`Personal-Projects/` plus exactly six rooms, "Nothing else"), so a vault missing them is a vault that does not match its own law. There is no `personal_wing_preopened:` flag any more.

## File skeletons

### The guide file (`_<Name>-Guide.md`, every room, lane, brand subfolder and wing)

```markdown
---
type: guide
guide_family: <wing | room | lane | brand>
updated: {{DATE}}
---

# <Name>

<One door-sign line: what lives here.>

**Files here when:** <the filing test for this folder, one sentence, traceable to the doctrine.>

## Observations
(what sessions notice about this folder lands here, one dated line each)
```

Door-sign lines and filing tests per room live in the room guide files ([rooms-assets.md](rooms-assets.md), [work-lanes.md](work-lanes.md)); copy each one from its guide header so the door and the reference always say the same thing.

⛔ **No Inventory section and no Navigation section.** A guide is not a directory (§3); Home is. ⛔ **No project list in a lane guide**: the lane's job is to be the anchor a journal line can link when work has no project, not a second copy of what the folder already shows.

### `04_{{BUSINESS}}-Business-Wing/_{{BUSINESS}}-Guide.md` (the wing door)

Same shape as any guide (`guide_family: wing`), plus one extra section, and it is the only guide that carries it:

```markdown
## Current state
(3 to 5 lines: what this business is, what is moving right now. Written at the first capture,
refreshed at maintenance. This is what a session reads to know where things stand.)
```

Its door-sign line names the four layers in one sentence each: `01_Assets` what the business is made of · `02_Work` what is moving, in four lanes · `03_SOP` how things get done · `04_Methodology` why decisions go the way they go, and that this last one fills from reviewed judgment, never from capture.

### `02_Command-Base/Home.md` (the full directory)

The one directory of the vault: every folder that exists, plus its door file where it has one. Written at scaffold from the tree that was actually created (skip untoggled rooms, never list a path that does not exist), and audited against the filesystem at every maintenance run.

```markdown
---
type: home
updated: {{DATE}}
---

# Home

The full directory of this vault. Every folder is listed here, and this is the only list.

## 02_Command-Base
- `Decisions/` · `Reviews/` · `Resources/` ([[02_Command-Base/Resources/_Resources-Guide|Resources]]: Clippings, Courses, Books, Prompts, Tools)
- `Command-Base.base`: the dashboard, opens inside Obsidian

## 03_Personal-Wing  [[03_Personal-Wing/_Personal-Wing-Guide|guide]]
- `Personal-Projects/` · `Family/` · `Health/` · `Finance-Personal/` · `Property/` · `Vehicles/` · `People/`
  (each with its own `_<Name>-Guide.md`)

## 04_{{BUSINESS}}-Business-Wing  [[04_{{BUSINESS}}-Business-Wing/_{{BUSINESS}}-Guide|guide]]
- `Business-Profile.md`: what this business is, one page
- `01_Assets/` what it is made of: `Clients/` `Vendors/` `Employees/` `Company-Docs/` `Marketing-Assets/` `IT-Systems/` `{{BUSINESS}}-Brand-Assets/` (Brand-Strategy, Target-Audience, Products-Services)
- `02_Work/` what is moving: `Deliver/` `Grow/` `Run/` `Build/`
- `03_SOP/` how things get done: starts empty, see `_SOP-Menu.md`
- `04_Methodology/` why decisions go the way they go: `Lessons/` `Playbooks/`, earned not captured

## The rest
- `00_Inbox/` unfiled · `01_Daily/` the journal · `98_Archive/` retired · `99_Meta/` law, state, memory, templates, skills

## System
- [[structure-doctrine]]: the constitution. Every filing follows it.
- [[tagging-vocabulary]]: the controlled tag list.
```

Guide links are written **path-qualified** (§5, regime B): guide names repeat across wings by design, so a bare `[[_Run-Guide]]` is ambiguous the day a second business arrives.

### `04_{{BUSINESS}}-Business-Wing/Business-Profile.md`

Copy from [templates/business-profile.template.md](../templates/business-profile.template.md), at the **wing root** (§1). Frontmatter fields stay empty at scaffold; capture mode fills them.

### `03_SOP/_SOP-Menu.md`

`03_SOP/` ships **empty and flat**: no starter processes, no category subfolders (§1). It ships with its door, and only its door.

The menu's shape is owned by the `sop-builder` skill, which reconciles this file against the folder every time it runs. ⛔ **Do not write a second version of it here.** Copy the template block verbatim from that skill's `references/sop-menu.md`, which at time of writing is:

```markdown
---
type: menu
updated: {{DATE}}
---

# SOP Menu

> Maintained by the SOP creation skill. Do not hand edit: the skill reconciles this file against the folder every time it runs, so hand edits get overwritten without warning.
>
> **What belongs in the second section**: processes that are **already happening but were never written down**. ⛔ Not processes that should exist one day. A wish list turns into a forty line guilt list in three months, and then nobody opens this file again.

## Written

## Happening but not written
```

Both sections ship **empty**. ⛔ Never pre-fill the second section with processes this kind of business usually has: the admission test is "is this already happening, and is it unwritten", and a list of things that ought to exist is a list of debts. That skill ships separately and the owner may not have it; a hand-written SOP is legal (§1, §7), and the menu is simply stale until either a skill run or the owner updates it.

### `01_Assets/{{BUSINESS}}-Brand-Assets/` (the brand rooms)

One `<Brand>-Brand-Assets/` folder per brand (§1). A single-brand business gets one, named after the business; capture asks which brand a thing belongs to only when a second brand exists.

Unlike other rooms (which scaffold empty and fill from capture), `Brand-Strategy/` and `Target-Audience/` are pre-populated at scaffold with **empty stub files**. The brand foundation is cross-cutting (every outward-facing piece of work reads it), so the schema exists from day zero; it just starts empty. Each stub is a **seed, not a blank**: its door sign names what it holds AND what stays broken while it is empty, so the gap is visible and worth filling. In Obsidian's graph these read as dim stars waiting to light up.

**The eight pillars are one family across two folders** (§1): seven in `Brand-Strategy/`, and the Journey pillar in `Target-Audience/`. All eight carry `type: brand-strategy` and a `pillar` value from the closed list in §8. The door signs below are canonical **English**; on a `中文` install, translate the door-sign prose at write time (file names stay English always).

**The seven stubs in `Brand-Strategy/`** (What + Empty cost per door sign):

- **Brand-Positioning.md** (pillar `Positioning`): What = "The place this business claims in the customer's mind, and who it is against." Empty cost = "every message starts from scratch and argues on the competitor's ground."
- **Brand-DNA.md** (pillar `DNA`): What = "What this business actually believes: the convictions behind its choices, not what it sells." Empty cost = "your marketing has no throughline. It reads like the category, never like you."
- **Brand-Personality.md** (pillar `Personality`): What = "The character the brand shows up as: how it talks, what it jokes about, what it would never say." Empty cost = "every post sounds written by a different stranger. Recognition needs one consistent voice."
- **Brand-Proposition.md** (pillar `Proposition`): What = "What you promise, and who the customer becomes by choosing you." Empty cost = "marketing can only list features. Features compete on price; promises get chosen."
- **Brand-Relationship.md** (pillar `Relationship`): What = "The role the brand plays in the customer's life, and how each touchpoint should feel." Empty cost = "service and follow-up get improvised. The feeling people remember is left to luck."
- **Brand-Sensory-Cues.md** (pillar `Sensory-Cues`): What = "The senses the brand chooses to own, so it's recognizable before anyone reads the name." Empty cost = "you default to the category's look and sound. Distinctiveness is chosen, not stumbled into."
- **Brand-Style.md** (pillar `Style`): What = "The concrete spec that renders those cues: color, type, logo use, spacing." Empty cost = "every designer and AI guesses. Consistency comes from one shared spec, not memory."

**`Target-Audience/Customer-Journey-Mapping.md`** (pillar `Journey`). Door sign: "The path one real person takes from never-heard-of-you to loyal, and how each stage should feel." Empty cost = "you market to a blur instead of a moment. The right message at the wrong stage still misses." ⚠️ It is the eighth pillar and carries the same `type: brand-strategy`, even though it files with the audience it maps; type comes from the family, never from the folder (§0 step 2).

**Stub file shape** (all eight):

```markdown
---
type: brand-strategy
pillar: <one value from the §8 closed list>
status: empty
---

# <Brand DNA>

<the What line>

**Empty cost:** <the empty-cost line>

> Status: not defined yet. To fill: run the brand intake, or drop in a brand strategy you already have.
```

`status: empty` is the machine signal that this pillar has not been answered yet: any outward-facing work reads it to know it is running generic. The stub bodies name what is missing and its cost; they do **not** teach how to fill it (no frameworks, no course pitch): the vault stays clean, and the how-to lives outside it.

### `02_Command-Base/Command-Base.base`

Copy verbatim from [templates/command-base.base.template](../templates/command-base.base.template). Its views read the §8 record schema (`cb: task` statuses, `type: brief` with `stage`, active decisions by `domain` and `lane`, and everything carrying `renew_by`), so a change to §8 is a change to this file in the same breath.

⚠️ **Known gap, stated rather than hidden.** Doctrine §1 lists `Command-Deck.html` (a generated dashboard) among the contents of `02_Command-Base/`, and setup does not create one, because its generator does not exist yet. Until it does, `Command-Base.base` is the dashboard and it renders inside Obsidian. ⛔ Do not write a placeholder `Command-Deck.html`: a dashboard file with nothing generating it is a file that will be stale on day two and trusted on day one.

### `99_Meta` state files

`filing-log.md`:

```markdown
# Filing Log

Append-only. One line per AI filing action: date · what · where · rule applied.

- {{DATE}} · vault scaffolded · (setup) · structure-doctrine v2
```

`bootstrap-progress.md` (frontmatter: `language:`, `vault_path:`, `business_name:`, `business_tag:`, `toggles:` [outlets/equipment booleans], `obsidian_installed:`, `claude_md:` [written | appended | left-to-user], `command_base_generated:`, `command_base_install:` (how the generated skill reached `~/.claude/skills/`: `symlink` / `junction` / `copy`; a `copy` install means edits to the vault copy do not reach the live skill until it is copied over again, which the `SKILL.md` retrofit path has to handle), `obsidian_skills_offered:` (the setup step 7 offer of the official kepano/obsidian-skills bundle), `jarvis_offered: false` (flipped by the command-base skill after its one-time Create-My-Jarvis offer), `rm_guard_installed:` (the setup step 6.8 safety lock: `installed` / `declined` / `skipped-platform`), `session_memory_installed:` (the setup step 6.9 session-memory tool, same three values; the distill harvest pipe and the command-base doorbell read this), `calendar_offered:` / `calendar_provider:`, `setup_complete:`) plus a body checklist of setup steps done.

`capture-progress.md` (frontmatter: `profile_captured: false`, `rooms_captured: []`, `lanes_captured: []`; body: two tables, one for entity rooms (the brand folder counts as a room) and one for `02_Work/` lanes, each row room-or-lane · date · items moved · insight given, plus `next_suggestion:` drawn from the same two vocabularies).

`maintenance-state.md` (frontmatter: `cadence_days: 7`, `last_tidy: {{DATE}}`, `last_distill: {{DATE}}`, `last_harvest: {{DATE}}`, the three dates seeded with the setup date so staleness math needs no empty-value case; body: one-line history log, first line noting the dates were seeded at setup, then appended per maintenance run). `cadence_days` is the single source for every staleness threshold in the product: doorbells and checkers read it rather than hardcoding 7, so an owner who changes the rhythm changes it once. `last_harvest` is only read when session memory is installed (setup step 6.9); seeding it regardless costs nothing.

`lab-gate-config.md` (from [templates/lab-gate-config.template.md](../templates/lab-gate-config.template.md), `{{DATE}}` filled). The thresholds the weekly lab scan reads when it decides whether a playbook is a candidate for a lab, and when an open lab looks like it should close (§9.5, §9.6). Owner-adjustable; scaffolded so the scan has something to read from day one, long before any playbook is close to earning a lab.

`memory.md` (from [templates/memory.template.md](../templates/memory.template.md), `{{DATE}}` filled; the seeded session-log line "Vault set up." stays). This is the working memory the generated command-base skill reads at session start and appends to at closeout. Old session-log entries rotate out during weekly maintenance, not here.

`capture-buffer.md` (header line only at scaffold: "Append-only staging. The command-base skill lands every in-the-moment capture here as one dated raw line the moment it arrives; compile drains the day's lines into the daily note."). This is the safety net for the day the owner never says "compile". A system file, not user content.

`Hypotheses/` ships as an **empty folder**. Weekly maintenance is its only writer (§0); nothing hand-filed ever lands there, so there is no starter file and no template offered to the owner.

### `99_Meta/Templates/` note templates

Copy each block from [templates/note-templates.md](../templates/note-templates.md) into its own file. These are the starter shapes capture and command-base sessions write from. Templater-free on purpose; the AI fills values. Every block's frontmatter is a legal instance of its family in §8, which is the whole reason they ship: a template is how the law gets taught without anyone reading it.

### `<vault>/CLAUDE.md`

From [templates/CLAUDE.template.md](../templates/CLAUDE.template.md), all placeholders replaced (`{{LANGUAGE}}` = the setup language choice, `English` or `中文`). **Written once at setup, never silently rewritten**: later amendments go through propose-and-approve at the maintenance close, same discipline as doctrine amendments. If a `CLAUDE.md` already exists at setup time, never overwrite or edit it; the append-proposal flow in setup step 5.5 applies instead. This file is the always-on layer that tells every future session what this vault is and where the constitution lives; without it the doctrine is invisible until a skill happens to fire.

## Wiring check (run after scaffold, before the graph moment)

1. **One door per folder.** Every room, lane, brand subfolder and wing holds exactly one `_`-prefixed file; no folder holds two (§5). The four layer folders and `04_Methodology/` hold none.
2. **Home is complete and true.** Every folder created is listed in `Home.md`, and every path `Home.md` names exists on disk. This replaces the old "two hops to both wings" check: with a full directory, reachability is not the question, accuracy is.
3. **`03_SOP/` holds exactly one file** (`_SOP-Menu.md`), zero subfolders, and both menu sections are empty.
4. **`04_Methodology/` contains its two subfolders** (Lessons, Playbooks) and **zero `.md` files**.
5. **Brand rooms.** `Brand-Strategy/` holds its guide plus seven stubs; `Target-Audience/` holds its guide plus `Customer-Journey-Mapping.md`; all eight stubs carry `type: brand-strategy`, `status: empty`, and a `pillar` value that appears in §8's closed list (eight distinct values, no repeats).
6. **Frontmatter is legal.** Every generated `.md` outside `99_Meta/Templates/` satisfies its family in §8: required keys present, closed-list values on-list. Zero `{{` placeholders remain anywhere outside `99_Meta/Templates/`.
7. `Command-Base.base` parses (at minimum the YAML loads).
8. `99_Meta` state files all exist, and `maintenance-state.md` carries `cadence_days`.
9. `CLAUDE.md` exists at the vault root with zero `{{` placeholders left (or, for an existing-vault owner, the append/leave choice is recorded in `bootstrap-progress.md`).
10. Report the file count created. Then the graph moment (setup mode step 8).
