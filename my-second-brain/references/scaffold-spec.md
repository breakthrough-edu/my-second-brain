# Scaffold Spec: the fully wired vault (tree v5)

This is the exact structure Setup mode creates. The principle is **full wiring**: not bare folders but every front-desk MOC pre-built, every navigation link live on day zero, every template in place. The AI always has a firm anchor to file against; the user never faces a blank page. Keep every generated file light: a door sign, a filing test, an empty inventory, nav links. No tutorials inside MOCs.

All `mkdir` operations use `mkdir -p` (idempotent; a vault that already has PARA folders is fine, nothing gets overwritten). **Never overwrite an existing file** during scaffold; skip and report instead.

Replace `{{BUSINESS}}` with the business folder name (English, hyphenated, e.g. `Aroma-Coffee`), `{{BUSINESS_NAME}}` with the display name, `{{DATE}}` with today. **Scope exception:** inside the files written to `99_Meta/Templates/`, keep `{{DATE}}` literal; those are starter shapes for future notes and the date is filled when each note is created. `{{CHILD_LINE}}` in the MOC pattern = for a room with child MOCs THAT EXIST at write time, a newline plus `Down: [[child MOC]] · [[child MOC]]`; omit entirely for leaf rooms and for empty subfolders that have no MOC yet (e.g. R-and-D's `Product/`/`System/`). Never link a MOC that does not exist. Direct children of the business root (`_Assets-MOC`, `_SOP-MOC`, `_Daily-Log-MOC`, `_Business-Projects-MOC`, `_R-and-D-MOC`) all point Up to `[[_Map]]`.

## Full tree

```
<vault>/
├── CLAUDE.md                       (always-on session context; setup step 5.5, written once at setup, evolves only by propose-and-approve, NEVER silently overwritten)
├── 00_Inbox/
├── 01_Daily/
├── 02_Projects/
│   └── _Projects-MOC.md
├── 03_Areas/                       (rooms optional; ask once whether to pre-open)
│   ├── _Areas-MOC.md
│   ├── Family/  Health/  Finance-Personal/  Property/  Vehicles/  People/
├── 04_Resources/
│   ├── _Resources-MOC.md
│   ├── Skills/  Courses/  Books/  Clippings/  Prompts/  Tools/
├── 05_Archive/
├── 06_Command-Base/
│   ├── Home.md
│   ├── Decisions/
│   ├── Tasks/
│   ├── Sessions/
│   └── Command-Base.base
├── 07_{{BUSINESS}}/
│   ├── _Map.md
│   ├── 00_Daily-Log/
│   │   └── _Daily-Log-MOC.md
│   ├── 01_Assets/
│   │   ├── _Assets-MOC.md
│   │   ├── Business-Profile.md
│   │   ├── Brand-Strategy/    + _Brand-Strategy-MOC.md  (+ 6 empty stubs)
│   │   ├── Target-Audience/   + _Target-Audience-MOC.md (+ Customer-Journey-Mapping.md, empty)
│   │   ├── Clients/         + _Clients-MOC.md
│   │   ├── Vendors/         + _Vendors-MOC.md
│   │   ├── Employees/       + _Employees-MOC.md
│   │   ├── Products-Services/ + _Products-Services-MOC.md
│   │   ├── Content-Assets/  + _Content-Assets-MOC.md
│   │   ├── Company-Docs/    + _Company-Docs-MOC.md
│   │   ├── Equipment/       + _Equipment-MOC.md          (toggle: equipment)
│   │   ├── Outlets/         + _Outlets-MOC.md            (toggle: outlets)
│   │   ├── Marketing/       + _Marketing-MOC.md  + Action-Log.md
│   │   ├── Sales/           + _Sales-MOC.md      + Action-Log.md
│   │   ├── Customer-Service/ + _Customer-Service-MOC.md + Action-Log.md
│   │   ├── HR/              + _HR-MOC.md         + Action-Log.md
│   │   ├── Finance/         + _Finance-MOC.md    + Action-Log.md
│   │   └── Operations/      + _Operations-MOC.md + Action-Log.md
│   │       └── IT-Systems/  + _IT-Systems-MOC.md
│   ├── 02_SOP/
│   │   ├── _SOP-MOC.md
│   │   ├── Staff-Onboarding/  Client-Onboarding/  Sales-Followup/
│   │   ├── Delivery/  Collection/  Complaint-Handling/  Content-Production/
│   │   ├── Purchasing/  Payroll-Monthly-Closing/
│   │   ├── Store-Open-Close/                              (toggle: outlets)
│   │   ├── Maintenance/                                   (toggle: equipment)
│   │   └── Importing/  Stock-Count/                       (toggle: importing)
│   ├── 03_Methodology/
│   │   ├── Positioning/  Decision-Rules/  Lessons/  Playbooks/
│   │   └── (NO MOC files anywhere in 03_Methodology -- the empty layer is the point)
│   ├── 04_Projects/
│   │   └── _Business-Projects-MOC.md
│   └── 05_R-and-D/
│       ├── _R-and-D-MOC.md
│       ├── Product/  System/
└── 99_Meta/
    ├── structure-doctrine.md        (from templates/structure-doctrine.template.md)
    ├── tagging-vocabulary.md        (from templates/tagging-vocabulary.template.md)
    ├── filing-log.md
    ├── bootstrap-progress.md
    ├── capture-progress.md
    ├── maintenance-state.md
    ├── graduation-config.md         (from templates/graduation-config.template.md)
    ├── memory.md                    (from templates/memory.template.md)
    ├── capture-buffer.md            (durable staging for in-the-moment captures)
    └── Templates/
        ├── Client.md  Vendor.md  Employee.md  Product-Service.md
        ├── Company-Doc.md  Equipment.md  Outlet.md
        ├── SOP.md  Decision.md  Task.md  Session.md
        ├── Business-Daily-Log.md  Engagement.md  Lesson.md  Playbook.md
```

Empty SOP starter rooms get **no per-room MOC** at scaffold time (they hold nothing yet; `_SOP-MOC.md` lists them). A SOP room's own MOC appears once it holds 2+ notes. Same rule for empty entity subfolders. The exceptions pre-built at scaffold: every Layer-1 room MOC listed above (they anchor capture from night one), plus the two brand-foundation rooms, which scaffold with their MOC **and** their empty stub files already in place (they are seeds, not blank rooms; see the brand-foundation skeleton below).

## Preset toggles

Three yes/no questions at setup, recorded in `bootstrap-progress.md`:

1. **Physical outlets?** (shopfront, branches) -> `01_Assets/Outlets/` + SOP `Store-Open-Close/`
2. **Machines or equipment?** -> `01_Assets/Equipment/` + SOP `Maintenance/`
3. **Import goods?** -> SOP `Importing/` + `Stock-Count/`

Untoggled rooms are simply not created. Any of them can be proposed later during capture when the business turns out to need one (propose, owner approves, create).

## Personal wing pre-open question

Ask once during setup (including existing-vault runs, unless those rooms already exist there): "Personal wing rooms (Family, Health, Personal Finance, Property, Vehicles, People): pre-open them now, or start with just the business wing and add these when you first need them?" Record the answer. If skipped, create only `_Areas-MOC.md` and `_Resources-MOC.md` plus the `04_Resources` subfolders (they serve the business wing's learning inlet too). `02_Projects/` and `_Projects-MOC.md` are always created regardless of this answer.

## File skeletons

### `06_Command-Base/Home.md`

```markdown
---
type: home
last-refreshed: {{DATE}}
---

# Home

The front door of this vault. Both wings at a glance.

## Business wing
- [[_Map]]: {{BUSINESS_NAME}} full map
- [[_Daily-Log-MOC]]: business cockpit (decisions, actions, deadlines)

## Personal wing
- [[_Projects-MOC]] · [[_Areas-MOC]] · [[_Resources-MOC]]

## Command center
- [[Command-Base.base|Dashboard]]: open inside Obsidian
- Decisions live in `06_Command-Base/Decisions/` (one decision, one note)

## System
- [[structure-doctrine]]: the constitution. Every filing follows it.
- [[tagging-vocabulary]]: the controlled tag list.
```

### `07_{{BUSINESS}}/_Map.md` (AI-first, one page, refreshed at maintenance)

```markdown
---
type: business-map
business: {{BUSINESS_NAME}}
last-refreshed: {{DATE}}
---

# {{BUSINESS_NAME}}: Map

One-page overview for any AI session working on this business. Refreshed during maintenance; treat as a build artifact.

## What this business is
(filled from Business-Profile after first capture)

## The three layers
- [[_Assets-MOC|01 Assets]]: what the business is made of. (empty)
- [[_SOP-MOC|02 SOP]]: how things get done. (empty)
- 03 Methodology: why decisions go the way they go. (empty, and that is deliberate: this layer fills from reviewed judgment, not from capture)

## Current state
- Rooms moved in: none yet
- Open items: none

## Navigation
[[Home]] · [[_Daily-Log-MOC|Daily Log]] · [[_Business-Projects-MOC|Projects]] · [[_R-and-D-MOC|R&D]]
```

### Room MOC pattern (`_<Name>-MOC.md`, every content folder)

```markdown
---
type: moc
room: <Name>
last-refreshed: {{DATE}}
---

# <Name>

<One door-sign line: what lives in this room.>

**Files here when:** <the room's filing test, one sentence from the doctrine.>

## Inventory
(empty: nothing moved in yet)

## Observations
(insights about this room land here after capture sessions)

## Navigation
Up: [[<parent MOC>]]{{CHILD_LINE}}
```

Door-sign lines and filing tests per room are in the room guide files ([rooms-assets.md](rooms-assets.md), [rooms-functions.md](rooms-functions.md), [rooms-sop.md](rooms-sop.md)); copy each room's door sign from its guide header so menu, MOC, and guide always say the same thing.

`_SOP-MOC.md` additionally carries the two-cut view: a list by intent (the folders) and a note that by-function views come from the `function:` field, plus the SOP frontmatter contract (`function:` + `owner:` + `last-verified:` required). It also carries an `## Observations` section: insights from SOP-room captures land here whenever the specific SOP room has no MOC of its own yet.

`_Daily-Log-MOC.md` is the business cockpit: sections for This business's recent Decisions (filter: domain), Action log highlights, Renewal deadlines (from `renew-by:` fields in Company-Docs / Outlets / Equipment). Until Bases views are added, keep these as maintained lists refreshed during maintenance. Mention only rooms that exist: drop Equipment/Outlets from the renewals line when their toggle is off.

### `01_Assets/Business-Profile.md`

Copy from [templates/business-profile.template.md](../templates/business-profile.template.md). Frontmatter fields stay empty at scaffold; capture mode fills them.

### `01_Assets/Brand-Strategy/` and `01_Assets/Target-Audience/` (the brand-foundation rooms)

Unlike other rooms (which scaffold empty and fill from capture), these two rooms are pre-populated at scaffold with **empty stub files**. The brand foundation is cross-functional (marketing, sales, and every outward-facing pod read it), so the schema exists from day zero; it just starts empty. Each stub is a **seed, not a blank**: its door sign names what it holds AND what stays broken while it is empty, so the gap is visible and worth filling. In Obsidian's graph these read as dim stars waiting to light up.

The eight door signs below are canonical **English**. On a `中文` install, translate the door-sign prose at write time (file names stay English always, same rule as room MOCs and CLAUDE.md).

**`_Brand-Strategy-MOC.md`** (front door). Door sign: "Your brand foundation: the six-part code that decides how everything downstream sounds, looks, and feels. Pillar 1 (Positioning) lives in `03_Methodology/Positioning`; the five identity pillars live here. Right now it's empty, so marketing and sales will run generic until it's filled. Fill it through a brand intake, or bring in a brand strategy you already have." Its Inventory lists the six stubs. Its Navigation Up is `[[_Assets-MOC]]`. **The reference to pillar 1 uses the plain path `03_Methodology/Positioning` as literal text, NEVER a `[[wikilink]]`** (Positioning carries no MOC by law; a wikilink there is a wiring failure and spawns a ghost file).

**The six identity stubs in `Brand-Strategy/`** (What + Empty cost per door sign):
- **Brand-DNA.md** (pillar DNA): What = "What this business actually believes: the convictions behind its choices, not what it sells." Empty cost = "your marketing has no throughline. It reads like the category, never like you."
- **Brand-Personality.md** (pillar Personality): What = "The character the brand shows up as: how it talks, what it jokes about, what it would never say." Empty cost = "every post sounds written by a different stranger. Recognition needs one consistent voice."
- **Brand-Proposition.md** (pillar Proposition): What = "What you promise, and who the customer becomes by choosing you." Empty cost = "marketing can only list features. Features compete on price; promises get chosen."
- **Brand-Relationship.md** (pillar Relationship): What = "The role the brand plays in the customer's life, and how each touchpoint should feel." Empty cost = "service and follow-up get improvised. The feeling people remember is left to luck."
- **Brand-Sensory-Cues.md** (pillar Sensory Cues, strategy): What = "The senses the brand chooses to own, so it's recognizable before anyone reads the name." Empty cost = "you default to the category's look and sound. Distinctiveness is chosen, not stumbled into."
- **Brand-Style-Guide.md** (pillar Sensory Cues, execution): What = "The concrete spec that renders those cues: color, type, logo use, spacing." Empty cost = "every designer and AI guesses. Consistency comes from one shared spec, not memory."

**`_Target-Audience-MOC.md`** (front door). Door sign: "Who this brand is for, drawn sharply enough to repel who it isn't." Empty cost = "marketing aims at everyone and moves no one. Sharp beats broad." Its Navigation Up is `[[_Assets-MOC]]`.
**`Target-Audience/Customer-Journey-Mapping.md`**. Door sign: "The path one real person takes from never-heard-of-you to loyal, and how each stage should feel." Empty cost = "you market to a blur instead of a moment. The right message at the wrong stage still misses." The MOC notes this file also feeds the Brand-Relationship pillar.

**Stub file shape** (every one of the six identity stubs and Customer-Journey-Mapping; `pillar:` omitted on the journey file):

```markdown
---
type: brand-foundation
pillar: <DNA | Personality | Proposition | Relationship | Sensory-Cues | Style-Guide>
status: empty
---

# <Brand DNA>

<the What line>

**Empty cost:** <the empty-cost line>

> Status: not defined yet. To fill: run the brand intake, or drop in a brand strategy you already have.
```

`status: empty` in frontmatter is the machine signal: the marketing skill reads it to know whether to run in "generic" degraded mode, and a future brand patch reads it to know where it may land. The stub file bodies name what is missing and its cost; they do **not** teach how to fill it (no frameworks, no course pitch): the vault stays clean, and the how-to lives outside it.

### Function room `Action-Log.md`

```markdown
---
type: action-log
function: <Function>
business: {{BUSINESS_NAME}}
---

# <Function> Action Log

Append-only running log of actions in this function. One dated line each. Decisions do NOT go here (they get a note in `06_Command-Base/Decisions/`).

- {{DATE}} Log opened.
```

### `06_Command-Base/Command-Base.base`

Copy verbatim from [templates/command-base.base.template](../templates/command-base.base.template).

### `99_Meta` state files

`filing-log.md`:

```markdown
# Filing Log

Append-only. One line per AI filing action: date · what · where · rule applied.

- {{DATE}} · vault scaffolded · (setup) · structure-doctrine v1
```

`bootstrap-progress.md` (frontmatter: `language:`, `vault_path:`, `business_name:`, `toggles:` [outlets/equipment/importing booleans], `personal_wing_preopened:`, `obsidian_installed:`, `claude_md:` [written | appended | left-to-user], `command_base_generated:`, `obsidian_skills_offered:` (the setup step 7 offer of the official kepano/obsidian-skills bundle), `jarvis_offered: false` (flipped by the command-base skill after its one-time Create-My-Jarvis offer), `pod_maker_installed:` (the setup step 6.6 symlink of the pod-maker skill from the payload into `~/.claude/skills/`; `copied` on the Windows fallback), `rm_guard_installed:` (the setup step 6.8 safety lock: `installed` / `declined` / `skipped-platform`), `session_memory_installed:` (the setup step 6.9 session-memory tool, same three values; the distill harvest pipe and the command-base doorbell read this), `marketing_pod_offered:` / `marketing_pod_installed:` (the setup step 8.5 Marketing-pod offer and its outcome), `setup_complete:`) plus a body checklist of setup steps done.

`capture-progress.md` (frontmatter: `profile_captured: false`, `rooms_captured: []`; body: a table of room · date · items moved · insight given, plus `next_suggestion:`).

`maintenance-state.md` (frontmatter: `last_tidy: {{DATE}}`, `last_distill: {{DATE}}`, `last_harvest: {{DATE}}`, all seeded with the setup date so staleness math needs no empty-value case; body: one-line history log, first line noting the dates were seeded at setup, then appended per maintenance run). `last_harvest` is only read when session memory is installed (setup step 6.9); seeding it regardless costs nothing and spares a missing-key case later.

`graduation-config.md` (from [templates/graduation-config.template.md](../templates/graduation-config.template.md), `{{DATE}}` filled). The thresholds the distill pod-altitude scan reads to surface graduation / demotion candidates. Owner-adjustable; scaffolded so the doorbell has something to read from day one even before any function is close to graduating.

`memory.md` (from [templates/memory.template.md](../templates/memory.template.md), `{{DATE}}` filled; the seeded session-log line "Vault set up." stays). This is the working memory the generated command-base skill reads at session start and appends to at closeout; scaffolding it here is what makes that loop live from day one. Old session-log entries rotate out during weekly maintenance (distill mode), not here.

`capture-buffer.md` (header line only at scaffold: "Append-only staging. The command-base skill lands every in-the-moment capture here as one dated raw line the moment it arrives; compile drains the day's lines into the daily note."). This is the safety net for the day the owner never says "compile": the captures survive the session, and the next morning's backfill doorbell writes that day's note from these lines. A system file, not user content.

### `99_Meta/Templates/` note templates

Copy each block from [templates/note-templates.md](../templates/note-templates.md) into its own file. These are the starter shapes capture mode writes from. Templater-free on purpose; the AI fills values.

### `<vault>/CLAUDE.md`

From [templates/CLAUDE.template.md](../templates/CLAUDE.template.md), all placeholders replaced (`{{LANGUAGE}}` = the setup language choice, `English` or `中文`). **Written once at setup, never silently rewritten**: later amendments go through propose-and-approve at the distill-mode close, same discipline as doctrine amendments. If a `CLAUDE.md` already exists at setup time, never overwrite or edit it; the append-proposal flow in setup step 5.5 applies instead. This file is the always-on layer that tells every future session what this vault is and where the constitution lives; without it the doctrine is invisible until a skill happens to fire.

## Wiring check (run after scaffold, before the graph moment)

1. Every created folder with content has its `_<Name>-MOC.md` and the MOC's Up link resolves. Any Down links written at scaffold time must resolve too; a link to a not-yet-born MOC is a wiring failure.
2. `Home.md` reaches both wings in 2 hops or fewer.
3. `03_Methodology/` contains its four subfolders (Positioning, Decision-Rules, Lessons, Playbooks) and zero `.md` files. The brand-foundation stubs live in `01_Assets/`, not here.
3b. `Brand-Strategy/` holds its MOC + six stubs, `Target-Audience/` holds its MOC + Customer-Journey-Mapping, every stub carries `status: empty`, and `_Brand-Strategy-MOC` references `03_Methodology/Positioning` as literal text (no `[[wikilink]]` to it).
4. `Command-Base.base` parses (open it in Obsidian later; at minimum the YAML loads).
5. `99_Meta` state files all exist.
6. `CLAUDE.md` exists at the vault root with zero `{{` placeholders left (or, for an existing-vault user, the append/leave choice is recorded in `bootstrap-progress.md`).
7. Report the file count created. Then the graph moment (setup mode step 8).
