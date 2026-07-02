# Scaffold Spec -- the fully wired vault (tree v5)

This is the exact structure Setup mode creates. The principle is **full wiring**: not bare folders but every front-desk MOC pre-built, every navigation link live on day zero, every template in place. The AI always has a firm anchor to file against; the user never faces a blank page. Keep every generated file light: a door sign, a filing test, an empty inventory, nav links. No tutorials inside MOCs.

All `mkdir` operations use `mkdir -p` (idempotent; a vault that already has PARA folders is fine, nothing gets overwritten). **Never overwrite an existing file** during scaffold; skip and report instead.

Replace `{{BUSINESS}}` with the business folder name (English, hyphenated, e.g. `Aroma-Coffee`), `{{BUSINESS_NAME}}` with the display name, `{{DATE}}` with today.

## Full tree

```
<vault>/
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
│   └── 05_R&D/
│       ├── _R-and-D-MOC.md
│       ├── Product/  System/
└── 99_Meta/
    ├── structure-doctrine.md        (from templates/structure-doctrine.template.md)
    ├── tagging-vocabulary.md        (from templates/tagging-vocabulary.template.md)
    ├── filing-log.md
    ├── bootstrap-progress.md
    ├── capture-progress.md
    ├── maintenance-state.md
    └── Templates/
        ├── Client.md  Vendor.md  Employee.md  Product-Service.md
        ├── Company-Doc.md  Equipment.md  Outlet.md
        ├── SOP.md  Decision.md  Task.md  Session.md
        ├── Business-Daily-Log.md  Engagement.md  Lesson.md  Playbook.md
```

Empty SOP starter rooms get **no per-room MOC** at scaffold time (they hold nothing yet; `_SOP-MOC.md` lists them). A SOP room's own MOC appears once it holds 2+ notes. Same rule for empty entity subfolders. The exceptions pre-built at scaffold: every Layer-1 room MOC listed above (they anchor capture from night one).

## Preset toggles

Three yes/no questions at setup, recorded in `bootstrap-progress.md`:

1. **Physical outlets?** (shopfront, branches) -> `01_Assets/Outlets/` + SOP `Store-Open-Close/`
2. **Machines or equipment?** -> `01_Assets/Equipment/` + SOP `Maintenance/`
3. **Import goods?** -> SOP `Importing/` + `Stock-Count/`

Untoggled rooms are simply not created. Any of them can be proposed later during capture when the business turns out to need one (propose, owner approves, create).

## Personal wing pre-open question

Ask once during setup: "Personal wing rooms (Family, Health, Personal Finance, Property, Vehicles, People): pre-open them now, or start with just the business wing and add these when you first need them?" Record the answer. If skipped, create only `_Areas-MOC.md` and `_Resources-MOC.md` plus the `04_Resources` subfolders (they serve the business wing's learning inlet too).

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
- [[_Map]] -- {{BUSINESS_NAME}} full map
- [[_Daily-Log-MOC]] -- business cockpit (decisions, actions, deadlines)

## Personal wing
- [[_Projects-MOC]] · [[_Areas-MOC]] · [[_Resources-MOC]]

## Command center
- [[Command-Base.base|Dashboard]] -- open inside Obsidian
- Decisions live in `06_Command-Base/Decisions/` (one decision, one note)

## System
- [[structure-doctrine]] -- the constitution. Every filing follows it.
- [[tagging-vocabulary]] -- the controlled tag list.
```

### `07_{{BUSINESS}}/_Map.md` (AI-first, one page, refreshed at maintenance)

```markdown
---
type: business-map
business: {{BUSINESS_NAME}}
last-refreshed: {{DATE}}
---

# {{BUSINESS_NAME}} -- Map

One-page overview for any AI session working on this business. Refreshed during maintenance; treat as a build artifact.

## What this business is
(filled from Business-Profile after first capture)

## The three layers
- [[_Assets-MOC|01 Assets]] -- what the business is made of. (empty)
- [[_SOP-MOC|02 SOP]] -- how things get done. (empty)
- 03 Methodology -- why decisions go the way they go. (empty, and that is deliberate: this layer fills from reviewed judgment, not from capture)

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
(empty -- nothing moved in yet)

## Observations
(insights about this room land here after capture sessions)

## Navigation
Up: [[<parent MOC>]]{{CHILD_LINE}}
```

Door-sign lines and filing tests per room are in the room guide files ([rooms-assets.md](rooms-assets.md), [rooms-functions.md](rooms-functions.md), [rooms-sop.md](rooms-sop.md)); copy each room's door sign from its guide header so menu, MOC, and guide always say the same thing.

`_SOP-MOC.md` additionally carries the two-cut view: a list by intent (the folders) and a note that by-function views come from the `function:` field, plus the SOP frontmatter contract (`function:` + `owner:` + `last-verified:` required).

`_Daily-Log-MOC.md` is the business cockpit: sections for This business's recent Decisions (filter: domain), Action log highlights, Renewal deadlines (from `renew-by:` fields in Company-Docs / Outlets / Equipment). Until Bases views are added, keep these as maintained lists refreshed during maintenance.

### `01_Assets/Business-Profile.md`

Copy from [templates/business-profile.template.md](../templates/business-profile.template.md). Frontmatter fields stay empty at scaffold; capture mode fills them.

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

`bootstrap-progress.md` (frontmatter: `language:`, `vault_path:`, `business_name:`, `toggles:` [outlets/equipment/importing booleans], `personal_wing_preopened:`, `obsidian_installed:`, `command_base_generated:`, `companion_skills_offered:`, `setup_complete:`) plus a body checklist of setup steps done.

`capture-progress.md` (frontmatter: `profile_captured: false`, `rooms_captured: []`; body: a table of room · date · items moved · insight given, plus `next_suggestion:`).

`maintenance-state.md` (frontmatter: `last_tidy:`, `last_distill:`, both empty at scaffold; body: one-line history log appended per maintenance run).

### `99_Meta/Templates/` note templates

Copy each block from [templates/note-templates.md](../templates/note-templates.md) into its own file. These are the starter shapes capture mode writes from. Templater-free on purpose; the AI fills values.

## Wiring check (run after scaffold, before the graph moment)

1. Every created folder with content has its `_<Name>-MOC.md` and the MOC's Up link resolves.
2. `Home.md` reaches both wings in 2 hops or fewer.
3. `03_Methodology/` contains its four subfolders and zero `.md` files.
4. `Command-Base.base` parses (open it in Obsidian later; at minimum the YAML loads).
5. `99_Meta` state files all exist.
6. Report the file count created. Then the graph moment (setup mode step 8).
