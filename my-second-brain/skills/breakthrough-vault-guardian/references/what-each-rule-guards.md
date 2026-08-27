# What Each Rule Guards: the real mistake behind every required key and closed list

Section 8 of the doctrine declares the families, the required keys and the closed lists. It does not say what any of them are **for**, and a rule whose purpose nobody can state is a rule that gets dropped for the wrong reason or defended for the wrong reason. This file is the other half: per family, what real mistake each rule stops, which downstream reader depends on it, and the smallest route that keeps the owner's goal when they want the rule gone.

⭐ **Look up the one rule being touched.** This is a lookup table, not a document to read through. The mechanics section is the exception: read it once before quoting any entry, because two of those notes (A2, A3) change what an entry means and one of them (A7) answers most requests outright.

⛔ **The owner's own section 8 is the live law.** This file describes the shapes the product ships; that vault may already have been amended. Run the reader on the vault first, and where the two disagree, their file wins and this one is background.

---

## Mechanics: read once before quoting any entry

### A1 · The floor every required key already has, and why it is never an answer

A missing required key is caught twice without anyone writing a line of code for that particular key. The guard blocks the write and prints the required keys, the optional keys and the closed lists it just read out of section 8 (`scripts/fm-guard-hook.sh` → `def schema_gate`). The weekly checker raises the same problems as errors (`scripts/checkup.py` → `def _check_against_schema`). The judgment itself is one function (`scripts/doctrine_schema.py` → `def validate`).

⛔ **So "the guard would block it" is never an answer to "who reads this key".** That answer is circular: it says the key is required because it is required. Every "who reads it" column below names readers **other** than this floor.

### A2 · A global closed list fires only where the family declares the field

`scripts/doctrine_schema.py` → `def validate`, verbatim:

```
for field, allowed in spec.enums.items():
    if field not in fm or not spec.declares(field):
        continue
```

`lane` and `domain` sit at the bottom of section 8 and are pushed into **every** family's enum table, but a family is only compared against the list when that family names the field in its own `required` or `optional`. A `domain:` written on a family that does not declare it is checked by nothing, and the checker does not report undeclared keys at all (A5).

### A3 · The mounting key is derived, and two edits abort the reader

`type` is not hard-coded anywhere. It is worked out as the one required key that every marker-less family declares (`scripts/doctrine_schema.py` → `def _derive_type_key`). Both of these edits stop the reader dead:

| Edit | What the reader says |
|---|---|
| Drop `type` from any single family's `required` | `ABORT: no single required key is shared by every non-record shape in section 8, so there is no derivable way for a note to declare which family it belongs to` |
| Add one more key to every family's `required` | `ABORT: more than one required key is shared by every non-record shape in section 8 (...), so which one a note mounts on is ambiguous` |

After an abort, A4 applies: both enforcers switch themselves off. ⛔ **Run the reader before editing, never after, whenever the change touches `type:` or adds a key that every family would carry.**

### A4 · A section 8 that will not parse switches both enforcers off, quietly

The guard fails open on purpose, because an unreadable law must not become an unopenable door: it checks the filename only and says it "checked this note's NAME only and let its frontmatter through unchecked" (`scripts/fm-guard-hook.sh` → `checked this note's NAME only`). The checker reports one `schema-unreadable` finding and enforces nothing else (`scripts/checkup.py` → `def _get_schema`); that finding is in `INVALIDATING_CHECKS` (`scripts/checkup.py` → `INVALIDATING_CHECKS = {"schema-unreadable"}`), so the report banner marks every number under it untrustworthy.

⛔ **Exit codes prove nothing here.** `checkup.py` exits non-zero only when the vault path itself cannot be read.

### A5 · Undeclared keys are named by the guard, never by the checker, and only at birth

The guard builds its `known` set from required, optional, the enum fields, the marker key and the type key, and flags anything left over as a judgment call rather than blocking it (`scripts/fm-guard-hook.sh` → `known = set(spec.required)`). The checker's schema walk reports three things only: an empty mounting key, a mounting value section 8 does not declare, and the results of `validate` (`scripts/checkup.py` → `def _check_against_schema`). It has no equivalent section. And the guard watches births, not edits (`scripts/fm-guard-hook.sh` → `an edit, not a birth; this guard watches births`).

⇒ **A stray key already sitting in an existing note is reported by nothing.** ⇒ And the reverse, which is the load-bearing half: **being declared is what keeps the guard quiet about a key the product itself wrote.** That is why many optional keys below have no reader and still earn their place. Section 8 says so in its own words: declaring them "lets this block tell a key the PRODUCT wrote from a key somebody invented on the spot".

### A6 · A required key present but empty counts as missing

`scripts/doctrine_schema.py` → `def validate` treats `""`, `None` and `[]` as absent. Several templates ship required keys blank on purpose (the SOP template's `lane:`, `owner:` and `last_verified:`; the Lesson template's `source:` and `lane:`). Copying one out unchanged and writing it is blocked, correctly: the template teaches the shape, the session fills it. ⛔ Do not "fix" a template by pre-filling a value the session is supposed to supply.

### A7 · ⭐⭐ Moving a key from `required` to `optional` keeps its closed list

**This is the answer to "I don't want to fill this in every time" almost every time it is asked.** `Spec.declares` (`scripts/doctrine_schema.py` → `def declares`) counts required and optional alike, and the closed-list gate keys on `declares()`, not on `required` (`scripts/doctrine_schema.py` → `def validate`). Downgrading `entity.client`'s `status` behaves like this:

| Note written | Result |
|---|---|
| `{type: client}`, no `status` at all | passes |
| `{type: client, status: retired}` | refused: `'status: retired' is not in the closed list section 8 declares for entity.client (active, prospective)` |
| `{type: client, status: prospective}` | passes |

⇒ The key becomes legal to leave out **and stays governed on every note that carries it.** Offer this route before any route that removes a key or opens a list. ⛔ The one thing it does give up: after the downgrade, nothing says the key is absent.

### A8 · Structure changes have a second cost on the product side only

The product's own acceptance script pins the shape of section 8: the family and shape totals, the count of in-family and global closed lists, the personal and decision lane counts, and which fields are multi-value. Removing a family, a shape or a closed list turns it red. ⛔ **It does not ship with the payload and never runs against an owner's vault**, so no amendment made in a vault can reach it. ⭐ **Adding a required key does reach one thing, and it is THIS file.** Check 8 of that script walks every shape in section 8 and demands a row here for each of its required keys, so a key added to the block turns the script red until an entry beside it says what the key stops. The script never counts required keys and does not care how many there are; it cares that each one can be looked up. The two mounting keys are exempt (`cb` and `type`, taken from the parsed schema rather than typed into the script), which is why the six shapes whose tables carry no `type` row are correct as they stand. Removing a required key still turns nothing red: the row it leaves behind here is stale and nothing reports it.

---

## How to read an entry

Each family below is a table with four columns.

- **What it stops** is the real mistake, stated as a consequence. Never the A1 floor.
- **Who reads it** lists readers other than that floor. ⚠️ **"Nothing reads it" is a finding, not a verdict.** `doctrine_version` is written on every house and acted on by nothing, on purpose, because a house that goes unstamped can never be dated afterwards (`references/scaffold-spec.md` → `once a house goes unstamped it can never be dated afterwards`). Writing and reading are two jobs. Weigh the fourth column, not the reader count.
- **If the owner wants it gone** names the smallest route that keeps what they actually want. A7 is the most common one. Where the column says ⛔, say so plainly and let the owner rule anyway.
- **A citation is a file, an arrow, and an anchor** (`scripts/checkup.py` → `def check_freshness` is one), where the anchor is a string that appears **verbatim** in the file named just before it: a `def`, a heading, or a line of the file's own prose. Several anchors into the same file follow one after the other, each behind its own arrow. ⛔ **Never cite a line number here.** Line numbers slide the moment anything above them is edited, and a citation that has quietly slid onto the wrong line reads exactly like one that is still right.

---

## `tags`, the open key on every family

Declared once at the bottom of section 8, in the `open_keys` table rather than on any family. The reader appends the name to every family's `optional` (`scripts/doctrine_schema.py` → `schema.open_keys = open_keys`), which is what makes it legal on every note without being written on every row.

| | |
|---|---|
| **What it stops** | An enforcer having no way to tell a key this vault ships from a key somebody invented while writing a note. ⭐ An open key is the opposite of a closed list, not a loose one: a closed list names the only legal values and refuses every other one, an open key names the **key** and refuses no value. Both are declared in section 8 for the same reason. |
| **Who reads it** | The checker compares the words against `99_Meta/tagging-vocabulary.md` (`scripts/checkup.py` → `def check_tags`), which makes this one of the few keys with a check of its own. The words themselves are governed by doctrine §6 and that file, never by section 8. |
| **If the owner wants it constrained** | ⛔ Not with a closed list here. Giving `tags` a closed list anywhere in section 8 stops the reader outright rather than letting it pick which half of the block to believe (`scripts/doctrine_schema.py` → `section 8 declares %r an open key`). A narrower tag set is an edit to the vocabulary file, which is where §6 already puts it. |

---

## `guide`

`required: [type, guide_family, updated]` · `guide_family: [wing, room, lane, brand, playbook]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `type` | See A3. | A3. | ⛔ No route. This is the one key with no alternative anywhere in the block. |
| `guide_family` | A door that calls itself a `layer`. The layer folders (`01_Assets/`, `02_Work/`, `03_SOP/`, `04_Methodology/`) get no door, and this list is the reason: it holds no `layer` value, so a layer door cannot be written legally (`references/scaffold-spec.md` → `The four layer folders get no door`). Without the list every layer folder grows a door, and the weekly "exactly one door per folder" check carries permanent noise. | `references/scaffold-spec.md` → `for the two wing doors` maps each kind of door to its value, and → `The four layer folders get no door` says why a layer has none · `references/rooms-assets.md` → `because the two sources read differently and the doctrine wins` · `references/work-lanes.md` → `## The four doors`. ⚠️ No script reads it. | A sixth kind of door is a value added to the list, not the list opened to free text. ⛔ Keep it required: the door-to-value table only works if every door carries one. |
| `updated` | Nobody can tell which year the door was written in. Maintenance judges door **content**, not just its existence (`modes/maintenance.md` → `Doors and the directory, four things at once`, item (c), and → `(c) is the one with teeth`), and "is this still true" needs a date to start from. | `modes/maintenance.md` → `Purely mechanical items` lists a stale `updated:` among the items a pass may pre-mark. ⚠️ No script: the checker's freshness check reads `maintenance-state.md` only (`scripts/checkup.py` → `def check_freshness`, fields at → `"freshness_fields"`). | A7. Downgraded, maintenance still reads it where present, and door content is still judged by comparison. |

## `brief`

`required: [type, status, updated]` · `optional: [started, due, owner, brand, stage, depends_on, hide_on_deck, milestone, priority]` · `status: [active, done, killed]` · `stage: [pending, planning, pursuing, executing, closed]`

⭐ This family has the densest downstream in the block: the whole dashboard is generated from briefs.

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `type` | A3. | A3. | ⛔ |
| `status` | A dead project holding a swimlane and a board column forever. The closed list refuses `paused`, `on-hold` and `pending`, words that look like an ending and are not: the deck tests `status == "done"`, so an invented value keeps the project on stage silently. | `scripts/deck.py` → `"status": str(fm.get("status", "")).strip() or "active"` reads it, and the test is → `p["status"] == "done" or p["hide_on_deck"]`, once in `_read_pulse` and again in `_dark_cells` · `scripts/deck-template.html` renders it · `scripts/fm-guard-hook.sh` → `in ("done", "killed") and "status" in spec.enums`, where `done` or `killed` triggers the distillation offer. | ⭐ Ask first whether they mean `hide_on_deck: true`, which already exists and needs no amendment. That is the zero-cost answer to "I want to park this". Otherwise a fourth value is a value added here **plus** the deck's three tests, in one breath. |
| `updated` | As `guide.updated`. | `modes/maintenance.md` → `Purely mechanical items`. | A7. |
| `started` `due` | The project cannot be drawn on the timeline. With neither, the swimlane leaves it off entirely; with `due` alone it becomes a milestone diamond; with both it is a runway bar (unless `milestone: true` overrides, see below). | `scripts/deck.py` → `"started": str(fm.get("started", "")).strip() or None` reads them, and `cmd_doctor` reports the gap → `if not p["due"] and not p["started"]` · the timeline and countdown in `scripts/deck-template.html`. | Already optional. |
| `owner` | ⚠️ Nothing states what this stops, and nothing explains it. | ⚠️ None. | Already optional, so it costs nothing to carry. Declared, it stays out of the guard's judgment-call list (A5). |
| `brand` | A project landing in the wrong brand band in a multi-brand vault. | `scripts/deck.py` → `"brand": str(fm.get("brand", "")).strip() or None` · the brand bands in `scripts/deck-template.html`. | Already optional. |
| `stage` | Every project piling into the board's unstaged column. | `scripts/deck.py` → `"stage": str(fm.get("stage", "")).strip() or None`, and `cmd_doctor` → `if not p["stage"]` · the board in `scripts/deck-template.html` → `STAGE_ORDER`. | A narrower or wider set of stages is a value added or removed from the list, plus the board. |
| `depends_on` | A timeline with no arrows. Unresolvable pointers are reported rather than dropped. | `scripts/deck.py` → `"depends_on": [_link_target(x) for x in _listify(fm.get("depends_on"))]`, resolved just below at → `for dep in p["depends_on"]` (`dep-unresolved`), and `cmd_doctor` → `if projects and not any(p["depends_on"] for p in projects)` · the timeline arrows in `scripts/deck-template.html`. | Already optional; leaving it out costs one arrow. |
| `hide_on_deck` | Having no way to park a project without lying that it is done. | `scripts/deck.py` → `"hide_on_deck": _truthy(fm.get("hide_on_deck"))` and → `p["status"] == "done" or p["hide_on_deck"]` · `scripts/deck-template.html` → `laneEmptyNote`. | Already optional. ⭐ It is itself the alternative route for `status` above. |
| `milestone` | A fixed-date event that spans several days being forced to choose between counting down (drop `started`, become a point) and showing its span (keep `started`, become a bar and fall out of Countdown). `milestone: true` is the declared override: diamond on `started` (falling back to `due`), into Countdown, span shown in the pill. The second declared deck-override after `hide_on_deck`. | `scripts/deck.py` → `"milestone": _truthy(fm.get("milestone"))`, and `cmd_doctor` names a flag with no date to sit on · `scripts/deck-template.html` → `isMilestone`, `milestoneDate`, `inCountdown`, the swimlane diamond and the pill range. | Already optional. ⭐ The zero-amendment alternative for "count me down but keep my span" would not exist without it: the derived rule can express a point or a span, never both. |
| `priority` | The priority list staying empty forever. | `scripts/deck.py` → `"priority": _int_or_none(fm.get("priority"))`, and `cmd_doctor` → `if p["priority"] is None` · the priority list in `scripts/deck-template.html`. | Already optional. |

## `menu`

`required: [type, updated]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `type` | `type: menu` is the SOP menu's only family. Without it the shipped menu is reported as a shape section 8 does not declare. | `references/scaffold-spec.md` → `The menu's shape is owned by the` ships the block · → `sop-ships-empty`, the wiring check. | ⛔ |
| `updated` | No way to tell which run of the SOP builder the menu reflects. | ⚠️ No reader inside this payload. The reader is the separate `breakthrough-sop-builder` skill, and `references/scaffold-spec.md` → `the skill's own copy wins wherever the owner has it` rules which copy wins. | A7 works mechanically. ⚠️ Confirm against that skill first: its reader is outside this payload and outside what this file can see. |

## `entity` (all subtypes)

Every subtype declares `required: [type, status]` and carries `renew_by` and `status_since` in its own `optional`. The `status` closed list is written at the family level and reaches all of them; a `required` written there would not (section 8 states this trap in its own comment).

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `type` | A3. | A3. | ⛔ |
| `status` · `[active, prospective]` | Two mistakes, and the doctrine names both. (a) A person or company the owner is **only talking to** recorded as won. `templates/structure-doctrine.template.md` → `a prospect, a landlord, a candidate` already rules that a prospect, a landlord or a candidate IS an entity note, so the note exists and the only thing separating it from a closed deal is this value, and `active` is a legal word nobody will ever warn about. (b) The absence of `retired` is itself the rule: leaving is a MOVE to `98_Archive/`, and an in-place value for it would be a legal way around the move. | `templates/structure-doctrine.template.md` → `a prospect, a landlord, a candidate` · the entity templates teach `prospective` in their bodies (`templates/note-templates.md` → `status is active or prospective`, once in each entity template). ⚠️ No script reads entity status. | ⛔ An owner asking for `churned` or `former` is asking for exactly what (b) refuses. Ask what they actually want: if it is "I still want to find them later", that is the archive move plus a link, not a status value. |
| `status_since` | Nobody can answer "how long has this said `prospective`". | `modes/maintenance.md` → `File timestamps are not durable` lists it among the dates more trustworthy than a file timestamp, used to judge a cold room. ⚠️ Section 8's own note beside the key says no check counts the days. That is true: no check counts them. Maintenance still reads the date. Both are the case today. | Already optional. |
| `renew_by` | Every expiry date living in one person's memory (`references/rooms-assets.md` → `The renewal single-thread`). | `scripts/deck.py` → `# ---- renewals (any family that carries renew_by)` scans **every** family for it, not just entities · `cmd_doctor` → `its Brief carries renew_by, which is the expiry key and belongs` moves a brief's `renew_by` back onto the entity that owns the expiring thing, and → `nothing in the vault carries renew_by` when none exists · the renewals card in `scripts/deck-template.html` · the generated command-base skill's morning renewals window (`templates/command-base-SKILL.template.md` → `Boot windows: This Week`) · the capture question sets in `references/rooms-assets.md`. | Already optional. ⛔ It is the one deadline key in the vault; a second one anywhere splits the renewals view in half. |

**The subtype-specific optional keys.**

| Spec | Its own optional keys | Reader |
|---|---|---|
| `entity.client` | `source` `since` `current_terms` | ⚠️ Template only. |
| `entity.vendor` | `supplies` `terms` `contact` | ⚠️ `terms` appears in the capture question set; the rest are template only. |
| `entity.employee` | `role` `started` | ⚠️ Template only. |
| `entity.product-service` | `price` `cost` | ⚠️ Template only. The obligation to keep a price current is written as a human one (`templates/command-base-SKILL.template.md` → `If it changes a stored value like a price, update that note in the same breath`, and `templates/note-templates.md` → `This note is the SINGLE source of price truth for the whole vault`), not as a reader of the key. |
| `entity.company-doc` | `doc_kind` `issuer` `location_of_original` | ⚠️ Template only. |
| `entity.equipment` | `model` `purchased` `last_serviced` | ⚠️ Template only. |
| `entity.outlet` | `address` `licenses` | ⭐ `address` has a real reader: doctrine §3 finds entity notes by **type plus address**, not by links (`templates/structure-doctrine.template.md` → `**Type queries**`), and the orphan check exempts them on exactly that basis (`modes/maintenance.md` → `**Orphans.**`). |
| `entity.it-system` | `holder` | ⚠️ No reader. It is the one question this product asks about an IT system, and the template is how that question gets asked. |
| `entity.marketing-asset` | `asset_kind` `where_it_lives` | ⚠️ Template only. |
| `entity.property` | `address` | ⭐ As `entity.outlet.address`. |
| `entity.vehicle` | `plate` | ⚠️ Template only. |

⛔ **Do not drop these for having no reader.** They are the landing points of the capture question sets in `references/rooms-assets.md`, and declaring them is the whole of A5: undeclared, the guard reports the product's own keys back to the session as judgment calls on every new entity note.

## `record.decision`

`marker: "cb: decision"` · `required: [cb, date, status, domain, lane]` · `optional: [supersedes, project]` · `status: [active, superseded, closed]` · `extends` the lane list with the personal wing's lanes

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `cb` | The note mounts on nothing and is reported as a shape section 8 does not declare. | `scripts/doctrine_schema.py` → `def _derive_marker_key` derives the marker key · `scripts/deck.py` → `if str(fm.get("cb", "")).strip() != "decision"` · the command-base skill's boot recipe greps `^cb: task` and its decision equivalent (`templates/command-base-SKILL.template.md` → `rg -l '^cb: task'`). | ⛔ |
| `date` | Two decisions and no way to tell which one is current. | `scripts/deck.py` → `scan.decisions.append(` · `scripts/deck-template.html` → `.sort((a,b) => a.date < b.date ? -1 : 1)`. | ⛔ |
| `status` | Two superseded laws standing at once until somebody trips over one. | `scripts/deck.py` → `scan.decisions.append(` · `scripts/deck-template.html` splits active, superseded and closed into three piles · `templates/command-base-SKILL.template.md` → `Before the note lands, check the active set` · `skills/breakthrough-session-report/SKILL.md` → `for the guardrail below` and → `The backstop: decisions that were made but never written`. | ⛔ |
| `domain` | A decision belonging to no wing. | `scripts/deck.py` → `"domain": str(fm.get("domain", "")).strip() or ""` scans it into the dashboard payload; no view renders it. ⭐ **Its real weight is A2: this is the only family that declares `domain`, so the global `domain` closed list is compared against nothing else.** | ⭐ A7. Downgraded, the key stays legal to omit **and** the global list keeps firing, because `declares()` counts optional. ⛔ Removing the key from this family altogether leaves that global list with nothing to fire on anywhere in the vault. |
| `lane` | A decision belonging to no line of the business, which turns off the same-lane conflict check the command-base skill runs before writing a new one (`templates/command-base-SKILL.template.md` → `Before the note lands, check the active set`, filtered to `status: active` and the same `lane:`). | A2 fires here · `scripts/deck.py` → `"lane": str(fm.get("lane", "")).strip() or ""` · `scripts/deck-template.html` · `skills/breakthrough-session-report/SKILL.md` → `The backstop: decisions that were made but never written` · `modes/maintenance.md` → `in particular: required on SOPs`. | ⛔ |
| `supersedes` | The succession chain breaks and "what did this replace" has no answer. | `scripts/deck.py` → `"supersedes": str(fm.get("supersedes", "")).strip() or None` · `scripts/deck-template.html` · `templates/command-base-SKILL.template.md` → `Before the note lands, check the active set` · `skills/breakthrough-session-report/SKILL.md` → `The backstop: decisions that were made but never written`. | Already optional. |
| `project` | ⚠️ Nothing. Doctrine §3 already rules that a pointer is written on the note being written, and the Decision template does not teach this key. | ⚠️ None. | Already optional. An owner who wants "this decision belongs to that project" writes one wikilink in the body, which is what §3's pointer rule says anyway. Zero amendment. |

## `record.task`

`marker: "cb: task"` · `required: [cb, status, created]` · `optional: [start, due, waiting_on, depends_on, priority]` · `status: [not-started, in-progress, waiting, blocked, done]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `cb` | As `record.decision.cb`. | `scripts/deck.py` → `if str(fm.get("cb", "")).strip() != "task"` · `templates/command-base-SKILL.template.md` → `rg -l '^cb: task'`. | ⛔ |
| `status` | A finished task sitting in This Week forever. And `waiting` is the only entry into the morning brief's Waiting For window, so an invented value empties that window without saying so. | `scripts/deck.py` → `"status": str(fm.get("status", "")).strip() or "not-started"` · `cmd_doctor` → `if t["status"] == "waiting" and not t["waiting_on"]`, which catches `waiting` with no `waiting_on` · `scripts/deck-template.html` · `templates/command-base-SKILL.template.md` → `"follow up with X" / "waiting for Y"` and → `Boot windows: This Week`. | ⛔ |
| `created` | A task that has been sitting for months reading exactly like one opened this morning. ⭐ A task is deliberately **not** a dated record and its filename carries no date (`references/scaffold-spec.md` → `Why they are spelled out rather than left to be derived from a title`), so frontmatter is the only place this date can live. | `modes/maintenance.md` → `File timestamps are not durable` counts it among the durable dates. ⚠️ The deck does not read it. | ⭐ The request is usually "stop making me type it". The generated command-base skill writes tasks from the template already (`templates/command-base-SKILL.template.md` → `Boot windows: This Week` and the boot recipe at → `rg -l '^cb: task'`), so it can fill this from context. Zero amendment. |
| `start` `due` `waiting_on` `depends_on` `priority` | The same board and timeline gaps as on a brief. | `scripts/deck.py` → `"waiting_on": str(fm.get("waiting_on", "")).strip() or None` and the `cmd_doctor` checks below it · the board and timeline in `scripts/deck-template.html` · `templates/command-base-SKILL.template.md` → `Boot windows: This Week`. | Already optional. |

## `process.sop`

`required: [type, lane, owner, last_verified]` · `optional: [playbook]` · `multi: [lane]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `type` | A3. | A3. | ⛔ |
| `lane` | An SOP that belongs to no line of the business is invisible to every lane-filtered view; `modes/maintenance.md` → `in particular: required on SOPs` says to watch `lane:` for exactly this. ⭐ The `multi` half guards something separate: `multi` is a reserved word in the block, and without it `lane: [deliver, run]` is reported as several values in a single-valued field (`scripts/doctrine_schema.py` → `def validate`). | A2 fires here · `modes/maintenance.md` → `in particular: required on SOPs`. | ⛔ And ⛔ separately: do not drop `multi` while keeping the key. |
| `owner` | A process nobody answers for. The template defines the key as the A of every RACI row, which is why the step table does not repeat it (`templates/note-templates.md` → `This is the A of every row`). | ⚠️ No machine reader. | A7 works mechanically. ⚠️ Weigh it first: this family's required set is small and each member answers a different question (which line, who answers for it, when it was last walked). Dropping one leaves the note unable to answer that question at all. |
| `last_verified` | A process nobody has walked in three years reading exactly like one walked yesterday. | `templates/command-base-SKILL.template.md` → `only if the process was actually re-walked`, which is the whole rule: never bump it because the note was touched. | A7. |
| `playbook` | The judgment layer above the steps cannot be reached from the steps. | The distillation chain (`modes/distill.md`) and §7's one-way pointer rule. | Already optional. |

## `process.method`

`required: [type, lane, status, confirmed_by_owner]` · `optional: [distilled_into]` · `status: [active, superseded]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `lane` | As `process.sop.lane`. | A2 fires here · `modes/maintenance.md` → `in particular: required on SOPs`. | ⛔ |
| `status` | A method already absorbed into a playbook still being read as live. The distillation flips each contributing method to `superseded` (`modes/distill.md` → `Compose a playbook, when several methods have earned one`); an invented third value makes that filter miss without a sound. | `modes/distill.md` → `Compose a playbook, when several methods have earned one` · `skills/breakthrough-method-builder/SKILL.md` → `Flip each contributing method`. | ⛔ |
| `confirmed_by_owner` | ⭐⭐ The hardest rule in the block, and section 8 defines it in its own words: the owner who was in the room said yes, out loud, at the moment the note was written. It does **not** mean a process approved it, a queue cleared it, or a weekly pass proposed it and nobody objected. Silence is not a yes. What it stops is an assistant writing a method, approving its own work, and that method being read three months later as the owner's own. | `skills/breakthrough-method-builder/SKILL.md` → `only after they have seen the actual note and said yes` · `modes/distill.md` → `Compose a playbook, when several methods have earned one` · `skills/breakthrough-session-report/SKILL.md` → `A pit: something that actually hurt`. | ⛔⛔ Never downgrade. It is the one key in the block whose value is a human act rather than a fact about the note, and an optional record of a human act is no record. |
| `distilled_into` | Which playbook absorbed this method cannot be answered from the method. | `modes/distill.md` → `Compose a playbook, when several methods have earned one` · `skills/breakthrough-method-builder/SKILL.md` → `Flip each contributing method`. | Already optional. |

## `process.playbook`

`required: [type, lane, status, confirmed_by_owner]` · `optional: [references]` · `multi: [references]` · `status: [forming]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `lane` `confirmed_by_owner` | As `process.method`. | As `process.method`. | ⛔ |
| `status` · one value | A closed list of one refuses **every** other word. Section 8 states why: the value describes the methodology's maturity, not this note's fill state, and no second value is sourced anywhere. | `templates/note-templates.md` → `status: forming` is the only source. | ⭐ Wanting `mature` or `retired` is a legitimate amendment, not a rule to talk them out of. Ask the second question with it: who reads the new value, and what changes when it is set. Nothing reads this key today, so a new value that changes no action is a wish rather than a rule. |
| `references` | The playbook and the lessons and decisions behind it lose their one link. §7 makes this the single pointer, written once when the playbook is born, on the note being written anyway. ⛔ There is deliberately no matching key on the lesson or decision side: a back-list would need revisiting forever. | `modes/distill.md` → `Compose a playbook, when several methods have earned one`. | Already optional. |

## `process.lesson`

`required: [type, date, source, lane, confirmed_by_owner]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `date` | When the lesson happened is lost. ⚠️ Unlike a decision's `date`, nothing sorts on this one. | ⚠️ None. | A7. |
| `source` | ⭐ Which piece of work taught it. The whole distillation chain runs on traceability: evidence is quoted verbatim **with its session pointer** (`modes/distill.md` → `quoted verbatim with its session pointer in the body`), and a lesson that cannot name where it came from is an opinion. | ⚠️ No machine reader; that line and → `Graduation needs all four` are the rules that depend on the concept. | ⛔ Do not downgrade. This is the key that makes a lesson a lesson. |
| `lane` `confirmed_by_owner` | As `process.method`. | A2 fires on `lane` · `skills/breakthrough-session-report/SKILL.md` → `A pit: something that actually hurt`. | ⛔ |

## `hypothesis`

`required: [type, status, destination, weeks_supported, weeks_silent]` · `status: [open, expired, graduated, rejected]` · `destination: [profile]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `status` | A rejected claim walking back in next month wearing different words. `modes/distill.md` → `**Contradiction.**`, verbatim: it dies immediately, `status:` flips to `rejected`, and the body stays with the reason. | That line and → `Graduation needs all four` · the Pool vitals section of the weekly review template (`templates/note-templates.md`), which counts open, graduated and expired. | ⛔ |
| `destination` · one value | The pool growing a second landing point without the judgment that would have to move with it. Section 8 states the principle: a closed list earns its keep only by refusing what is not on it. `modes/distill.md` → `The pool has exactly one landing point now` says so, and the first-pass test (does this claim need time to become true) only makes sense for that one destination. | ⚠️ Nothing reads the key by name. The reader is that pass, which assumes one destination throughout. | A second value is a real amendment, and ⛔ it is not done by adding the value alone: the distillation test moves with it. |
| `weeks_supported` `weeks_silent` | A hypothesis that never expires. `modes/distill.md` → `**Corroboration.**` ages one, and → `**Silence.**` ages the other and expires the hypothesis after about four cadence periods of nothing. Without the counters there is no line to cross. | Those two lines. | ⛔ |

## `ritual.daily`

`required: [type]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `type` | A3, and it is the only thing that makes a daily note a daily note to the schema. | A3. Everything else about a daily note is read from its address: the dashboard's pulse parses the filename (`scripts/deck.py` → `def _read_pulse`, verbatim `parse_date(name[:-3])`), maintenance reads the folder (`modes/maintenance.md` → `Weekly rollup, and the two things that close it`), and the command-base skill reads the path (`templates/command-base-SKILL.template.md` → `Read yesterday's`). | ⛔ |

## `ritual.weekly-review`

`required: [type, week_of, reviewed_on]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `type` | A3, and here it has real readers: both halves of the weekly ritual find this file by `type: weekly-review`, one after the other, and write into the same note. | `modes/maintenance.md` → `Weekly rollup, and the two things that close it` · `modes/distill.md` → `Open the `type: weekly-review` note the anti-drift half filed`. | ⛔ |
| `week_of` `reviewed_on` | A review written three weeks late reading as though it were written that week. The template gives the reason in its own words: `week_of` is the Monday of the week reviewed, `reviewed_on` is when the review actually happened, and they differ often enough that one key cannot answer both (`templates/note-templates.md` → `week_of is the Monday of the week reviewed`). | ⚠️ Neither has a reader. | A7 on both, ⭐ **never one alone**: they are a pair, and downgrading half of it leaves the distinction unanswerable while looking maintained. ⚠️ Weigh it against this: a weekly review is never backfilled once written, so what is left out is left out permanently, and the filename is the only fallback (§5 does not fix a filename shape for reviews the way `references/scaffold-spec.md` → `Why they are spelled out rather than left to be derived from a title` does for tasks). |

## `ritual.monthly-theme`

`required: [type, month, status, status_since]` · `status: [active, closed]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `month` | A theme from two months ago still standing as the current one. | `modes/maintenance.md` → `**Theme check (the doorbell).**`: a theme whose `month:` is more than a month behind gets a proposal to replace it. | ⛔ |
| `status` | Two themes active at once, so "what month am I in" has no single answer. | `modes/maintenance.md` → `**Theme check (the doorbell).**` reads the reviews folder for a `type: monthly-theme` with `status: active`. That is the only place reading it by name. The command-base skill walks the theme **chain** (the `Follows` and `Followed by` links), and that chain only gets written at the moment this key is flipped. | ⛔ |
| `status_since` | ⭐ Required here while it is optional on every entity subtype, and that is deliberate: the flip date is the one fact `month:` cannot carry, because the trigger is a new theme opening and not the calendar turning. Without it, `month:` and the real changeover drift apart. | `modes/maintenance.md` → `**Theme check (the doorbell).**` writes today's `status_since` onto the old theme as it closes · → `File timestamps are not durable` counts it among the durable dates. | ⛔ |

## `resources`

`required: [type]` · `type: [clipping, course, book, prompt, tool-note]` · `optional: [source]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `type` | ⭐ This is the one family whose own closed list **is** its mounting value (`scripts/doctrine_schema.py` → `schema.by_type[v] = spec` takes the family-list branch rather than the spec-name branch). Each value is a folder that exists under the resources room, so a sixth value is a note with nowhere to land. | `references/scaffold-spec.md` → `Clippings/  Courses/  Books/  Prompts/  Tools/` · `scripts/doctrine_schema.py` → `schema.by_type[v] = spec`. | A new kind of resource is a value **plus** a folder, added in one breath. ⛔ Neither half alone. |
| `source` | Where the clipping came from is lost. | ⚠️ No machine reader; the Resource template in `templates/note-templates.md` teaches it. | Already optional. |

## `brand-strategy`

`required: [type, pillar, status]` · `pillar: [DNA, Personality, Proposition, Relationship, Sensory-Cues, Positioning, Style, Journey]` · `status: [empty, filled]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `pillar` | A pillar missing or duplicated with nobody noticing. The wiring check requires one stub per value with no repeats, so the list is what makes "all of them are there" a checkable statement. | `references/scaffold-spec.md` → `Brand-Positioning.md` gives each pillar its door sign and its empty cost, and → `brand-stubs-in-place` is the wiring check · `templates/note-templates.md` → `pillar: DNA`. | ⛔ |
| `status` · `[empty, filled]` | ⭐⭐ **The most expensive rule in the block to lose.** This is the only `status` in section 8 that describes the note's own fill state instead of a real-world lifecycle, and the vault's `CLAUDE.md` reads it in **every** session: stubs marked `status: empty` are to be treated as gaps to fill, "not answers" (`templates/CLAUDE.template.md` → `Brand foundation is the positioning source of truth`). Without it, an unanswered brand pillar gets quoted into outward-facing work as though it were the answer. | `templates/CLAUDE.template.md` → `Brand foundation is the positioning source of truth`, every session · `references/scaffold-spec.md` → `pre-populated at scaffold with **empty stub files**`, the machine signal that any outward-facing work reads to know it is running generic, and → `brand-stubs-in-place` · `modes/capture.md` → `Map what they give onto the eight pillar stubs`, which flips the stubs it fills · `references/rooms-assets.md` → `which stubs are still`, which asks which empty stub is the most expensive one · `templates/note-templates.md` → `status: empty`. | ⛔⛔ Do not downgrade and do not open the list. |

## `brand-research`

`required: [type, updated]` · `optional: [source, brand]`

⭐ **Read this next to `brand-strategy` above, because the pair is the point.** The pillars are the answers; this family is the evidence they were built on, the owner's own convictions included. Section 8 names it "the evidence behind the pillars" and refuses "market research" for one stated reason: a family named after looking outward would push the owner's own beliefs somewhere else. ⚠️ Unlike the brand rooms, `Brand-Research/` is not scaffolded. It is made the first time evidence is written, so the wiring checks never see it and the folder's own door is a runtime door, like the door on a playbook folder.

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `type` | A3. | A3. | ⛔ |
| `updated` | A pillar being rebuilt on a customer read or a competitor scan from two years ago. This is the one family in the block whose **age** decides whether the content can be trusted, and a stale finding reads exactly as certain as a fresh one. | ⚠️ Nothing. ⛔ **And do not reach for the freshness check to fill this column:** `scripts/checkup.py` → `def check_freshness` reads only the vault's `maintenance-state.md`, on the fields `scripts/checkup.py` → `"freshness_fields"` names (`last_tidy`, `last_distill`). Section 8 says so itself so that nobody offers the owner a guarantee that does not exist. The reader is the person who opens the note. | A7 works mechanically, and weigh it against the paragraph above before offering it: dropped, the note keeps its authority and loses its expiry. ⭐ If what they want is to stop typing it, that is the session's job to fill, not a key to remove. |
| `source` | Something the owner recalled over coffee and something that was actually looked up ending up indistinguishable, which is the difference between a finding and a hunch. ⭐ Blank is a legal, meaningful value here: it means the owner's own knowledge. | ⚠️ No machine reader; the template teaches it, and it follows `resources.source` above. | Already optional. |
| `brand` | A5, and only that: in a multi-brand vault a session writes the brand out of habit, and undeclared it comes back as a judgment call on a note the product's own template shaped. The folder path already carries the answer. | ⚠️ None. `brief.brand` is the key it copies. | Already optional. |

⛔ **The request to expect, and the answer.** An owner running a named research method will ask for the topics as a closed list (`type: [consumer-research, competitor-research, ...]` or a `research_kind` key). Section 8 refuses it in its own words, and the reason is worth stating plainly: the topic set belongs to a school of practice, not to this vault, so putting it in the law means every change to somebody else's vocabulary arrives as an amendment to their constitution. The subject already has a home the law does not have to police, which is the filename and the title. ⭐ If they want the set visible rather than enforced, that is a line in their own `Brand-Research/` door, and the door needs no amendment.

## `control.doctrine` · `control.vocabulary` · `control.profile`

Each: `required: [type]`, plus, on the ones whose shipped file carries them, the keys that file carries: `vocabulary` takes `maintained_by` `last_updated` `version`; `profile` takes `subject` `last_updated` `maintained_by`.

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `type` on all four | A brand-new, entirely correct install being warned every week about its own control plane. `scripts/checkup.py` → `There is no exemption for the control plane here` records the ruling in the code it replaced: an earlier version skipped every file sitting directly in the meta directory, and, verbatim, "That was a rule living in code instead of in the law". Declared here, they mount and pass like anything else, and a control file that arrives **without** an amendment is correctly surfaced instead of waved through by a path test. | `scripts/checkup.py` → `def _check_against_schema` · → `"required_meta_files"`, which separately checks the control files exist. | ⛔ |
| The optional keys | A5: undeclared, the product's own frontmatter is reported back as judgment calls on every install. | `templates/tagging-vocabulary.template.md` → `maintained_by: AI (with owner approval)` · `templates/profile.template.md` → `subject: {{YOUR_NAME}}`. | Already optional. |

⭐ Section 8 explains why `required` is thin across this family and it is worth repeating to an owner who wants to tighten it: a constitution, a tag table, a threshold config and a person's dossier have almost nothing in common to demand, and a schema invented to cover all of them would fit none. Tighten one when its own shape settles.

⛔ Section 8 also rules the other direction, and it is the mistake to watch for: the state files in the meta directory (`bootstrap-progress`, `capture-progress`, `maintenance-state`, `filing-log`, `capture-buffer`, `memory`) carry no `type:` at all, nothing mounts them, and a correct install is already silent about them. **Adding `type:` to a notepad is what creates the warning, not what silences it.**

## `singletons.home`

`required: [type]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `type` | A correct `Home.md` reported as a shape section 8 does not declare. | ⚠️ Its real readers work by **path**, not by this key: the wiring check `home-is-true` (`references/scaffold-spec.md` → `Every folder created is listed in`) and the directory audit in maintenance (`modes/maintenance.md` → `Doors and the directory, four things at once`, item (d)). | ⛔ |

## `singletons.business-profile`

`required: [type, business]` · `optional: [founder_name, brand_name, industry, category, location, one_line_description, created, last_updated]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `type` | The wing's profile cannot be found by shape. | `modes/capture.md` → `(the wing root, not inside a layer)` finds it by its frontmatter (`type: business-profile`, `business:`). | ⛔ |
| `business` | Which business this profile is about. ⭐ In a single-wing vault this is nearly free information; in a multi-wing vault it is the thing that separates two files of the same fixed name sitting at two wing roots. | ⚠️ No machine reader. Watch a false one: the dashboard's business name comes from `99_Meta/bootstrap-progress.md` (`scripts/deck.py` → `shape.business_name = str(fm.get("business_name", "")).strip()`), not from this note. The real readers are prose that finds the file by address (`skills/breakthrough-project-consultant/SKILL.md` → `What business is this, what does it sell, who to` · `references/rooms-assets.md` → `The light gate (one question, at Business-Profile close)`). | A7 is safe while the vault has one wing. ⛔ Reconsider before a second wing opens: at that point the key is what tells two identically named files apart from the inside. |
| The optional keys | A5, and they are the landing points of the business-profile capture. | `templates/business-profile.template.md`. | Already optional. |
