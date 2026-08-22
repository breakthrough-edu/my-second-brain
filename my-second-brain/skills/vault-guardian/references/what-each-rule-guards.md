# What Each Rule Guards: the real mistake behind every required key and closed list

Section 8 of the doctrine declares the families, the required keys and the closed lists. It does not say what any of them are **for**, and a rule whose purpose nobody can state is a rule that gets dropped for the wrong reason or defended for the wrong reason. This file is the other half: per family, what real mistake each rule stops, which downstream reader depends on it, and the smallest route that keeps the owner's goal when they want the rule gone.

⭐ **Look up the one rule being touched.** This is a lookup table, not a document to read through. The mechanics section is the exception: read it once before quoting any entry, because two of those notes (A2, A3) change what an entry means and one of them (A7) answers most requests outright.

⛔ **The owner's own section 8 is the live law.** This file describes the shapes the product ships; that vault may already have been amended. Run the reader on the vault first, and where the two disagree, their file wins and this one is background.

---

## Mechanics: read once before quoting any entry

### A1 · The floor every required key already has, and why it is never an answer

A missing required key is caught twice without anyone writing a line of code for that particular key. The guard blocks the write and prints the required keys, the optional keys and the closed lists it just read out of section 8 (`scripts/fm-guard-hook.sh:278-301`). The weekly checker raises the same problems as errors (`scripts/checkup.py:557-558`). The judgment itself is one function (`scripts/doctrine_schema.py:552-555`).

⛔ **So "the guard would block it" is never an answer to "who reads this key".** That answer is circular: it says the key is required because it is required. Every "who reads it" column below names readers **other** than this floor.

### A2 · A global closed list fires only where the family declares the field

`scripts/doctrine_schema.py:556-557`, verbatim:

```
for field, allowed in spec.enums.items():
    if field not in fm or not spec.declares(field):
        continue
```

`lane` and `domain` sit at the bottom of section 8 and are pushed into **every** family's enum table, but a family is only compared against the list when that family names the field in its own `required` or `optional`. A `domain:` written on a family that does not declare it is checked by nothing, and the checker does not report undeclared keys at all (A5).

### A3 · The mounting key is derived, and two edits abort the reader

`type` is not hard-coded anywhere. It is worked out as the one required key that every marker-less family declares (`scripts/doctrine_schema.py:322-349`). Both of these edits stop the reader dead:

| Edit | What the reader says |
|---|---|
| Drop `type` from any single family's `required` | `ABORT: no single required key is shared by every non-record shape in section 8, so there is no derivable way for a note to declare which family it belongs to` |
| Add one more key to every family's `required` | `ABORT: more than one required key is shared by every non-record shape in section 8 (...), so which one a note mounts on is ambiguous` |

After an abort, A4 applies: both enforcers switch themselves off. ⛔ **Run the reader before editing, never after, whenever the change touches `type:` or adds a key that every family would carry.**

### A4 · A section 8 that will not parse switches both enforcers off, quietly

The guard fails open on purpose, because an unreadable law must not become an unopenable door: it checks the filename only and says it "checked this note's NAME only and let its frontmatter through unchecked" (`scripts/fm-guard-hook.sh:252-260`). The checker reports one `schema-unreadable` finding and enforces nothing else (`scripts/checkup.py:459-480`); that finding is in `INVALIDATING_CHECKS` (`scripts/checkup.py:802`), so the report banner marks every number under it untrustworthy.

⛔ **Exit codes prove nothing here.** `checkup.py` exits non-zero only when the vault path itself cannot be read.

### A5 · Undeclared keys are named by the guard, never by the checker, and only at birth

The guard builds its `known` set from required, optional, the enum fields, the marker key and the type key, and flags anything left over as a judgment call rather than blocking it (`scripts/fm-guard-hook.sh:303-316`). The checker's schema walk reports three things only: an empty mounting key, a mounting value section 8 does not declare, and the results of `validate` (`scripts/checkup.py:489-562`). It has no equivalent section. And the guard watches births, not edits (`scripts/fm-guard-hook.sh:342-343`, verbatim `an edit, not a birth; this guard watches births`).

⇒ **A stray key already sitting in an existing note is reported by nothing.** ⇒ And the reverse, which is the load-bearing half: **being declared is what keeps the guard quiet about a key the product itself wrote.** That is why many optional keys below have no reader and still earn their place. Section 8 says so in its own words: declaring them "lets this block tell a key the PRODUCT wrote from a key somebody invented on the spot".

### A6 · A required key present but empty counts as missing

`scripts/doctrine_schema.py:552-553` treats `""`, `None` and `[]` as absent. Several templates ship required keys blank on purpose (the SOP template's `lane:`, `owner:` and `last_verified:`; the Lesson template's `source:` and `lane:`). Copying one out unchanged and writing it is blocked, correctly: the template teaches the shape, the session fills it. ⛔ Do not "fix" a template by pre-filling a value the session is supposed to supply.

### A7 · ⭐⭐ Moving a key from `required` to `optional` keeps its closed list

**This is the answer to "I don't want to fill this in every time" almost every time it is asked.** `Spec.declares` (`scripts/doctrine_schema.py:249`) counts required and optional alike, and the closed-list gate keys on `declares()`, not on `required` (`scripts/doctrine_schema.py:556-557`). Downgrading `entity.client`'s `status` behaves like this:

| Note written | Result |
|---|---|
| `{type: client}`, no `status` at all | passes |
| `{type: client, status: retired}` | refused: `'status: retired' is not in the closed list section 8 declares for entity.client (active, prospective)` |
| `{type: client, status: prospective}` | passes |

⇒ The key becomes legal to leave out **and stays governed on every note that carries it.** Offer this route before any route that removes a key or opens a list. ⛔ The one thing it does give up: after the downgrade, nothing says the key is absent.

### A8 · Structure changes have a second cost on the product side only

The product's own acceptance script pins the shape of section 8: the family and shape totals, the count of in-family and global closed lists, the personal and decision lane counts, which fields are multi-value, and the lab cardinality. Removing a family, a shape or a closed list turns it red. ⛔ **It does not ship with the payload and never runs against an owner's vault**, so no amendment made in a vault can reach it. Adding or removing a required key does not touch it either; it does not count required keys.

---

## How to read an entry

Each family below is a table with four columns.

- **What it stops** is the real mistake, stated as a consequence. Never the A1 floor.
- **Who reads it** lists readers other than that floor. ⚠️ **"Nothing reads it" is a finding, not a verdict.** `doctrine_version` is written on every house and acted on by nothing, on purpose, because a house that goes unstamped can never be dated afterwards (`references/scaffold-spec.md:303`). Writing and reading are two jobs. Weigh the fourth column, not the reader count.
- **If the owner wants it gone** names the smallest route that keeps what they actually want. A7 is the most common one. Where the column says ⛔, say so plainly and let the owner rule anyway.
- Line numbers move when a file is edited. If a citation does not land, the filename still does.

---

## `tags`, the open key on every family

Declared once at the bottom of section 8, in the `open_keys` table rather than on any family. The reader appends the name to every family's `optional` (`scripts/doctrine_schema.py:518-529`), which is what makes it legal on every note without being written on every row.

| | |
|---|---|
| **What it stops** | An enforcer having no way to tell a key this vault ships from a key somebody invented while writing a note. ⭐ An open key is the opposite of a closed list, not a loose one: a closed list names the only legal values and refuses every other one, an open key names the **key** and refuses no value. Both are declared in section 8 for the same reason. |
| **Who reads it** | The checker compares the words against `99_Meta/tagging-vocabulary.md` (`scripts/checkup.py:597`), which makes this one of the few keys with a check of its own. The words themselves are governed by doctrine §6 and that file, never by section 8. |
| **If the owner wants it constrained** | ⛔ Not with a closed list here. Giving `tags` a closed list anywhere in section 8 stops the reader outright rather than letting it pick which half of the block to believe (`scripts/doctrine_schema.py:519-527`). A narrower tag set is an edit to the vocabulary file, which is where §6 already puts it. |

---

## `guide`

`required: [type, guide_family, updated]` · `guide_family: [wing, room, lane, brand, lab]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `type` | See A3. | A3. | ⛔ No route. This is the one key with no alternative anywhere in the block. |
| `guide_family` | A door that calls itself a `layer`. The layer folders (`01_Assets/`, `02_Work/`, `03_SOP/`, `04_Methodology/`) get no door, and this list is the reason: it holds no `layer` value, so a layer door cannot be written legally (`references/scaffold-spec.md:83`). Without the list every layer folder grows a door, and the weekly "exactly one door per folder" check carries permanent noise. | `references/scaffold-spec.md:110` maps each kind of door to its value · `:83` · `references/rooms-assets.md:18` · `references/work-lanes.md:28`. ⚠️ No script reads it. | A sixth kind of door is a value added to the list, not the list opened to free text. ⛔ Keep it required: the door-to-value table only works if every door carries one. |
| `updated` | Nobody can tell which year the door was written in. Maintenance judges door **content**, not just its existence (`modes/maintenance.md:29` item (c), and `:31` on why (c) is the one with teeth), and "is this still true" needs a date to start from. | `modes/maintenance.md:96` lists a stale `updated:` among the mechanical items a pass may pre-mark. ⚠️ No script: the checker's freshness check reads `maintenance-state.md` only (`scripts/checkup.py:640`, fields at `:138`). | A7. Downgraded, maintenance still reads it where present, and door content is still judged by comparison. |

## `brief`

`required: [type, status, updated]` · `optional: [started, due, owner, brand, stage, depends_on, hide_on_deck, priority]` · `status: [active, done, killed]` · `stage: [pending, planning, pursuing, executing, closed]`

⭐ This family has the densest downstream in the block: the whole dashboard is generated from briefs.

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `type` | A3. | A3. | ⛔ |
| `status` | A dead project holding a swimlane and a board column forever. The closed list refuses `paused`, `on-hold` and `pending`, words that look like an ending and are not: the deck tests `status == "done"`, so an invented value keeps the project on stage silently. | `scripts/deck.py:408` · `:547` and `:701`, verbatim `p["status"] == "done" or p["hide_on_deck"]` · `scripts/deck-template.html:763` `:1058` · `scripts/fm-guard-hook.sh:318-327`, where `done` or `killed` triggers the distillation offer. | ⭐ Ask first whether they mean `hide_on_deck: true`, which already exists and needs no amendment. That is the zero-cost answer to "I want to park this". Otherwise a fourth value is a value added here **plus** the deck's three tests, in one breath. |
| `updated` | As `guide.updated`. | `modes/maintenance.md:96`. | A7. |
| `started` `due` | The project cannot be drawn on the timeline. With neither, the swimlane leaves it off entirely; with `due` alone it becomes a milestone diamond. | `scripts/deck.py:410-411` · `:720-732` doctor · `:743-749` · the timeline and countdown in `scripts/deck-template.html`. | Already optional. |
| `owner` | ⚠️ Nothing states what this stops, and nothing explains it. | ⚠️ None. | Already optional, so it costs nothing to carry. Declared, it stays out of the guard's judgment-call list (A5). |
| `brand` | A project landing in the wrong brand band in a multi-brand vault. | `scripts/deck.py:407` · `scripts/deck-template.html:694` `:699` `:773`. | Already optional. |
| `stage` | Every project piling into the board's unstaged column. | `scripts/deck.py:409` · `:750-753` doctor · the board in `scripts/deck-template.html`. | A narrower or wider set of stages is a value added or removed from the list, plus the board. |
| `depends_on` | A timeline with no arrows. Unresolvable pointers are reported rather than dropped. | `scripts/deck.py:416` · `:425-441` (`dep-unresolved`) · `:816-819` · `scripts/deck-template.html:1066-1067` `:1188`. | Already optional; leaving it out costs one arrow. |
| `hide_on_deck` | Having no way to park a project without lying that it is done. | `scripts/deck.py:417` `:547` `:701` · `scripts/deck-template.html:596` `:763` `:766` `:771`. | Already optional. ⭐ It is itself the alternative route for `status` above. |
| `priority` | The priority list staying empty forever. | `scripts/deck.py:412` · `:729-732` doctor · `scripts/deck-template.html:586`. | Already optional. |

## `menu`

`required: [type, updated]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `type` | `type: menu` is the SOP menu's only family. Without it the shipped menu is reported as a shape section 8 does not declare. | `references/scaffold-spec.md:189` ships the block · `:420` wiring check `sop-ships-empty`. | ⛔ |
| `updated` | No way to tell which run of the SOP builder the menu reflects. | ⚠️ No reader inside this payload. The reader is the separate `sop-builder` skill, and `references/scaffold-spec.md:185` rules that the skill's own copy wins wherever the owner has it. | A7 works mechanically. ⚠️ Confirm against that skill first: its reader is outside this payload and outside what this file can see. |

## `entity` (all subtypes)

Every subtype declares `required: [type, status]` and carries `renew_by` and `status_since` in its own `optional`. The `status` closed list is written at the family level and reaches all of them; a `required` written there would not (section 8 states this trap in its own comment).

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `type` | A3. | A3. | ⛔ |
| `status` · `[active, prospective]` | Two mistakes, and the doctrine names both. (a) A person or company the owner is **only talking to** recorded as won. `templates/structure-doctrine.template.md:75` already rules that a prospect, a landlord or a candidate IS an entity note, so the note exists and the only thing separating it from a closed deal is this value, and `active` is a legal word nobody will ever warn about. (b) The absence of `retired` is itself the rule: leaving is a MOVE to `98_Archive/`, and an in-place value for it would be a legal way around the move. | `templates/structure-doctrine.template.md:75` · the entity templates teach `prospective` in their bodies (`templates/note-templates.md:106` `:138` `:171`). ⚠️ No script reads entity status. | ⛔ An owner asking for `churned` or `former` is asking for exactly what (b) refuses. Ask what they actually want: if it is "I still want to find them later", that is the archive move plus a link, not a status value. |
| `status_since` | Nobody can answer "how long has this said `prospective`". | `modes/maintenance.md:37` lists it among the dates more trustworthy than a file timestamp, used to judge a cold room. ⚠️ Section 8's own note beside the key says no check counts the days. That is true: no check counts them. Maintenance still reads the date. Both are the case today. | Already optional. |
| `renew_by` | Every expiry date living in one person's memory (`references/rooms-assets.md:164`). | `scripts/deck.py:469-492` scans **every** family for it, not just entities · `:733-742` doctor moves a brief's `renew_by` back onto the entity that owns the expiring thing · `:824-827` · `scripts/deck-template.html:607` · the generated command-base skill's morning renewals window (`templates/command-base-SKILL.template.md:87`) · the capture question sets in `references/rooms-assets.md`. | Already optional. ⛔ It is the one deadline key in the vault; a second one anywhere splits the renewals view in half. |

**The subtype-specific optional keys.**

| Spec | Its own optional keys | Reader |
|---|---|---|
| `entity.client` | `source` `since` `current_terms` | ⚠️ Template only. |
| `entity.vendor` | `supplies` `terms` `contact` | ⚠️ `terms` appears in the capture question set; the rest are template only. |
| `entity.employee` | `role` `started` | ⚠️ Template only. |
| `entity.product-service` | `price` `cost` | ⚠️ Template only. The obligation to keep a price current is written as a human one (`templates/command-base-SKILL.template.md:63`), not as a reader of the key. |
| `entity.company-doc` | `doc_kind` `issuer` `location_of_original` | ⚠️ Template only. |
| `entity.equipment` | `model` `purchased` `last_serviced` | ⚠️ Template only. |
| `entity.outlet` | `address` `licenses` | ⭐ `address` has a real reader: doctrine §3 finds entity notes by **type plus address**, not by links (`templates/structure-doctrine.template.md:92`), and the orphan check exempts them on exactly that basis (`modes/maintenance.md:55`). |
| `entity.it-system` | `holder` | ⚠️ No reader. It is the one question this product asks about an IT system, and the template is how that question gets asked. |
| `entity.marketing-asset` | `asset_kind` `where_it_lives` | ⚠️ Template only. |
| `entity.property` | `address` | ⭐ As `entity.outlet.address`. |
| `entity.vehicle` | `plate` | ⚠️ Template only. |

⛔ **Do not drop these for having no reader.** They are the landing points of the capture question sets in `references/rooms-assets.md`, and declaring them is the whole of A5: undeclared, the guard reports the product's own keys back to the session as judgment calls on every new entity note.

## `record.decision`

`marker: "cb: decision"` · `required: [cb, date, status, domain, lane]` · `optional: [supersedes, project]` · `status: [active, superseded, closed]` · `extends` the lane list with the personal wing's lanes

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `cb` | The note mounts on nothing and is reported as a shape section 8 does not declare. | `scripts/doctrine_schema.py:300` derives the marker key · `scripts/deck.py:457` · the command-base skill's boot recipe greps `^cb: task` and its decision equivalent (`templates/command-base-SKILL.template.md:84`). | ⛔ |
| `date` | Two decisions and no way to tell which one is current. | `scripts/deck.py:460` · `scripts/deck-template.html:1457`, verbatim `.sort((a,b) => a.date < b.date ? -1 : 1)` · `:1469`. | ⛔ |
| `status` | Two superseded laws standing at once until somebody trips over one. | `scripts/deck.py:464` · `scripts/deck-template.html:1458-1460` splits active, superseded and closed into three piles · `templates/command-base-SKILL.template.md:63` · `skills/session-report/SKILL.md:32` `:68`. | ⛔ |
| `domain` | A decision belonging to no wing. | `scripts/deck.py:463` scans it into the dashboard payload; no view renders it. ⭐ **Its real weight is A2: this is the only family that declares `domain`, so the global `domain` closed list is compared against nothing else.** | ⭐ A7. Downgraded, the key stays legal to omit **and** the global list keeps firing, because `declares()` counts optional. ⛔ Removing the key from this family altogether leaves that global list with nothing to fire on anywhere in the vault. |
| `lane` | A decision belonging to no line of the business, which turns off the same-lane conflict check the command-base skill runs before writing a new one (`templates/command-base-SKILL.template.md:63`, filtered to `status: active` and the same `lane:`). | A2 fires here · `scripts/deck.py:462` · `scripts/deck-template.html:1472` · `skills/session-report/SKILL.md:68` · `modes/maintenance.md:50`. | ⛔ |
| `supersedes` | The succession chain breaks and "what did this replace" has no answer. | `scripts/deck.py:465` · `scripts/deck-template.html:1471` · `templates/command-base-SKILL.template.md:63` · `skills/session-report/SKILL.md:68`. | Already optional. |
| `project` | ⚠️ Nothing. Doctrine §3 already rules that a pointer is written on the note being written, and the Decision template does not teach this key. | ⚠️ None. | Already optional. An owner who wants "this decision belongs to that project" writes one wikilink in the body, which is what §3's pointer rule says anyway. Zero amendment. |

## `record.task`

`marker: "cb: task"` · `required: [cb, status, created]` · `optional: [start, due, waiting_on, depends_on, priority]` · `status: [not-started, in-progress, waiting, blocked, done]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `cb` | As `record.decision.cb`. | `scripts/deck.py:356` · `templates/command-base-SKILL.template.md:84`. | ⛔ |
| `status` | A finished task sitting in This Week forever. And `waiting` is the only entry into the morning brief's Waiting For window, so an invented value empties that window without saying so. | `scripts/deck.py:361` · `:766-770` doctor, which catches `waiting` with no `waiting_on` · `scripts/deck-template.html:1058` · `templates/command-base-SKILL.template.md:64` `:87`. | ⛔ |
| `created` | A task that has been sitting for months reading exactly like one opened this morning. ⭐ A task is deliberately **not** a dated record and its filename carries no date (`references/scaffold-spec.md:283`), so frontmatter is the only place this date can live. | `modes/maintenance.md:37` counts it among the durable dates. ⚠️ The deck does not read it. | ⭐ The request is usually "stop making me type it". The generated command-base skill writes tasks from the template already (`templates/command-base-SKILL.template.md:87` and the boot recipe at `:84`), so it can fill this from context. Zero amendment. |
| `start` `due` `waiting_on` `depends_on` `priority` | The same board and timeline gaps as on a brief. | `scripts/deck.py:362-365` · `:761-770` · `scripts/deck-template.html:586` `:827` `:1085` `:1327` · `templates/command-base-SKILL.template.md:87`. | Already optional. |

## `process.sop`

`required: [type, lane, owner, last_verified]` · `optional: [playbook]` · `multi: [lane]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `type` | A3. | A3. | ⛔ |
| `lane` | An SOP that belongs to no line of the business is invisible to every lane-filtered view; `modes/maintenance.md:50` says to watch `lane:` in particular for exactly this. ⭐ The `multi` half guards something separate: `multi` is a reserved word in the block, and without it `lane: [deliver, run]` is reported as several values in a single-valued field (`scripts/doctrine_schema.py:563`). | A2 fires here · `modes/maintenance.md:50`. | ⛔ And ⛔ separately: do not drop `multi` while keeping the key. |
| `owner` | A process nobody answers for. The template defines the key as the A of every RACI row, which is why the step table does not repeat it (`templates/note-templates.md:490`). | ⚠️ No machine reader. | A7 works mechanically. ⚠️ Weigh it first: this family's required set is small and each member answers a different question (which line, who answers for it, when it was last walked). Dropping one leaves the note unable to answer that question at all. |
| `last_verified` | A process nobody has walked in three years reading exactly like one walked yesterday. | `templates/command-base-SKILL.template.md:75`, verbatim: bump it "only if the process was actually re-walked, never because the note was touched". | A7. |
| `playbook` | The judgment layer above the steps cannot be reached from the steps. | The distillation chain (`modes/distill.md`) and §7's one-way pointer rule. | Already optional. |

## `process.method`

`required: [type, lane, status, confirmed_by_owner]` · `optional: [distilled_into]` · `status: [active, superseded]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `lane` | As `process.sop.lane`. | A2 fires here · `modes/maintenance.md:50`. | ⛔ |
| `status` | A method already absorbed into a playbook still being read as live. The distillation flips each contributing method to `superseded` (`modes/distill.md:40`); an invented third value makes that filter miss without a sound. | `modes/distill.md:40` · `skills/method-builder/SKILL.md:65`. | ⛔ |
| `confirmed_by_owner` | ⭐⭐ The hardest rule in the block, and section 8 defines it in its own words: the owner who was in the room said yes, out loud, at the moment the note was written. It does **not** mean a process approved it, a queue cleared it, or a weekly pass proposed it and nobody objected. Silence is not a yes. What it stops is an assistant writing a method, approving its own work, and that method being read three months later as the owner's own. | `skills/method-builder/SKILL.md:59`, which requires the owner to have seen the actual note and said yes · `modes/distill.md:40` · `skills/session-report/SKILL.md:40`. | ⛔⛔ Never downgrade. It is the one key in the block whose value is a human act rather than a fact about the note, and an optional record of a human act is no record. |
| `distilled_into` | Which playbook absorbed this method cannot be answered from the method. | `modes/distill.md:40` · `skills/method-builder/SKILL.md:65`. | Already optional. |

## `process.playbook`

`required: [type, lane, status, confirmed_by_owner]` · `optional: [references]` · `multi: [references]` · `status: [forming]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `lane` `confirmed_by_owner` | As `process.method`. | As `process.method`. | ⛔ |
| `status` · one value | A closed list of one refuses **every** other word. Section 8 states why: the value describes the methodology's maturity, not this note's fill state, and no second value is sourced anywhere. | `templates/note-templates.md:781` is the only source. | ⭐ Wanting `mature` or `retired` is a legitimate amendment, not a rule to talk them out of. Ask the second question with it: who reads the new value, and what changes when it is set. Nothing reads this key today, so a new value that changes no action is a wish rather than a rule. |
| `references` | The playbook and the lessons and decisions behind it lose their one link. §7 makes this the single pointer, written once when the playbook is born, on the note being written anyway. ⛔ There is deliberately no matching key on the lesson or decision side: a back-list would need revisiting forever. | `modes/distill.md:40`. | Already optional. |

## `process.lesson`

`required: [type, date, source, lane, confirmed_by_owner]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `date` | When the lesson happened is lost. ⚠️ Unlike a decision's `date`, nothing sorts on this one. | ⚠️ None. | A7. |
| `source` | ⭐ Which piece of work taught it. The whole distillation chain runs on traceability: evidence is quoted verbatim **with its session pointer** (`modes/distill.md:21`), and a lesson that cannot name where it came from is an opinion. | ⚠️ No machine reader; `modes/distill.md:21` `:25` is the rule that depends on the concept. | ⛔ Do not downgrade. This is the key that makes a lesson a lesson. |
| `lane` `confirmed_by_owner` | As `process.method`. | A2 fires on `lane` · `skills/session-report/SKILL.md:40`. | ⛔ |

## `hypothesis`

`required: [type, status, destination, weeks_supported, weeks_silent]` · `status: [open, expired, graduated, rejected]` · `destination: [profile]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `status` | A rejected claim walking back in next month wearing different words. `modes/distill.md:22`, verbatim: it dies immediately, `status:` flips to `rejected`, and the body stays with the reason. | `modes/distill.md:22` `:25` · the Pool vitals section of the weekly review template (`templates/note-templates.md`), which counts open, graduated and expired. | ⛔ |
| `destination` · one value | The pool growing a second landing point without the judgment that would have to move with it. Section 8 states the principle: a closed list earns its keep only by refusing what is not on it. `modes/distill.md:17` says the pool has exactly one landing point, and the first-pass test (does this claim need time to become true) only makes sense for that one destination. | ⚠️ Nothing reads the key by name. The reader is that pass, which assumes one destination throughout. | A second value is a real amendment, and ⛔ it is not done by adding the value alone: the distillation test moves with it. |
| `weeks_supported` `weeks_silent` | A hypothesis that never expires. `modes/distill.md:21` ages one on corroboration, `:23` ages the other on silence and expires the hypothesis after about four cadence periods of nothing. Without the counters there is no line to cross. | `modes/distill.md:21` `:23`. | ⛔ |

## `lab.rubric` · `lab.thresholds` · `lab.lab-register`

Each: `required: [type, updated]`. The family also declares `cardinality: {count: 1, per: lab-folder}`.

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `type` | Three organs, one family each. Without them a correctly opened lab is reported three times over as shapes section 8 does not declare. | A3 · `skills/playbook-lab/SKILL.md:63-65`. | ⛔ |
| `updated` | As `guide.updated`, applied to a lab's own machinery. | ⚠️ No reader. | A7. |
| `cardinality` | Not a key: it is the family's declared shape, one file each per lab. Section 8 says outright that no check anywhere counts these files against it. | ⚠️ Nothing enforces it. | ⛔ Keep it. A written shape is the entire value here, and a person noticing a lab with two rubrics is the intended enforcement. |

## `ritual.daily`

`required: [type]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `type` | A3, and it is the only thing that makes a daily note a daily note to the schema. | A3. Everything else about a daily note is read from its address: the dashboard's pulse parses the filename (`scripts/deck.py:509`, `parse_date(name[:-3])`), maintenance reads the folder (`modes/maintenance.md:70`), and the command-base skill reads the path (`templates/command-base-SKILL.template.md:23`). | ⛔ |

## `ritual.weekly-review`

`required: [type, week_of, reviewed_on]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `type` | A3, and here it has real readers: both halves of the weekly ritual find this file by `type: weekly-review`, one after the other, and write into the same note. | `modes/maintenance.md:70` · `modes/distill.md:59`. | ⛔ |
| `week_of` `reviewed_on` | A review written three weeks late reading as though it were written that week. The template gives the reason in its own words: `week_of` is the Monday of the week reviewed, `reviewed_on` is when the review actually happened, and they differ often enough that one key cannot answer both (`templates/note-templates.md:642-643`). | ⚠️ Neither has a reader. | A7 on both, ⭐ **never one alone**: they are a pair, and downgrading half of it leaves the distinction unanswerable while looking maintained. ⚠️ Weigh it against this: a weekly review is never backfilled once written, so what is left out is left out permanently, and the filename is the only fallback (§5 does not fix a filename shape for reviews the way `references/scaffold-spec.md:283` does for tasks). |

## `ritual.monthly-theme`

`required: [type, month, status, status_since]` · `status: [active, closed]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `month` | A theme from two months ago still standing as the current one. | `modes/maintenance.md:80`, the theme doorbell: a theme whose `month:` is more than a month behind gets a proposal to replace it. | ⛔ |
| `status` | Two themes active at once, so "what month am I in" has no single answer. | `modes/maintenance.md:80` reads the reviews folder for a `type: monthly-theme` with `status: active`. That is the only place reading it by name. The command-base skill walks the theme **chain** (the `Follows` and `Followed by` links), and that chain only gets written at the moment this key is flipped. | ⛔ |
| `status_since` | ⭐ Required here while it is optional on every entity subtype, and that is deliberate: the flip date is the one fact `month:` cannot carry, because the trigger is a new theme opening and not the calendar turning. Without it, `month:` and the real changeover drift apart. | `modes/maintenance.md:80` writes today's `status_since` onto the old theme as it closes · `:37` counts it among the durable dates. | ⛔ |

## `resources`

`required: [type]` · `type: [clipping, course, book, prompt, tool-note]` · `optional: [source]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `type` | ⭐ This is the one family whose own closed list **is** its mounting value (`scripts/doctrine_schema.py:497-505` takes the family-list branch rather than the spec-name branch). Each value is a folder that exists under the resources room, so a sixth value is a note with nowhere to land. | `references/scaffold-spec.md:24` `:146` · `scripts/doctrine_schema.py:497-505`. | A new kind of resource is a value **plus** a folder, added in one breath. ⛔ Neither half alone. |
| `source` | Where the clipping came from is lost. | ⚠️ No machine reader; the template teaches it (`templates/note-templates.md:942`). | Already optional. |

## `brand-strategy`

`required: [type, pillar, status]` · `pillar: [DNA, Personality, Proposition, Relationship, Sensory-Cues, Positioning, Style, Journey]` · `status: [empty, filled]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `pillar` | A pillar missing or duplicated with nobody noticing. The wiring check requires one stub per value with no repeats, so the list is what makes "all of them are there" a checkable statement. | `references/scaffold-spec.md:212-225` gives each pillar its door sign and its empty cost · `:422` wiring check `brand-stubs-in-place` · `templates/note-templates.md:416` `:432`. | ⛔ |
| `status` · `[empty, filled]` | ⭐⭐ **The most expensive rule in the block to lose.** This is the only `status` in section 8 that describes the note's own fill state instead of a real-world lifecycle, and the vault's `CLAUDE.md` reads it in **every** session: stubs marked `status: empty` are to be treated as gaps to fill, "not answers" (`templates/CLAUDE.template.md:15`). Without it, an unanswered brand pillar gets quoted into outward-facing work as though it were the answer. | `templates/CLAUDE.template.md:15`, every session · `references/scaffold-spec.md:228`, the machine signal that any outward-facing work reads to know it is running generic · `:422` · `modes/capture.md:48`, which flips the stubs it fills · `references/rooms-assets.md:34`, which asks which empty stub is the most expensive one · `templates/note-templates.md:434`. | ⛔⛔ Do not downgrade and do not open the list. |

## `control.doctrine` · `control.vocabulary` · `control.lab-gate-config` · `control.profile`

Each: `required: [type]`, plus, on the ones whose shipped file carries them, the keys that file carries: `vocabulary` takes `maintained_by` `last_updated` `version`; `lab-gate-config` takes `created` `last_updated` `maintained_by`; `profile` takes `subject` `last_updated` `maintained_by`.

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `type` on all four | A brand-new, entirely correct install being warned every week about its own control plane. `scripts/checkup.py:517-526` records the ruling in the code it replaced: an earlier version skipped every file sitting directly in the meta directory, and, verbatim, "That was a rule living in code instead of in the law". Declared here, they mount and pass like anything else, and a control file that arrives **without** an amendment is correctly surfaced instead of waved through by a path test. | `scripts/checkup.py:517-555` · `:99-110`, which separately checks the control files exist. | ⛔ |
| The optional keys | A5: undeclared, the product's own frontmatter is reported back as judgment calls on every install. | `templates/tagging-vocabulary.template.md:3` · `templates/lab-gate-config.template.md:5` · `templates/profile.template.md:5`. | Already optional. |

⭐ Section 8 explains why `required` is thin across this family and it is worth repeating to an owner who wants to tighten it: a constitution, a tag table, a threshold config and a person's dossier have almost nothing in common to demand, and a schema invented to cover all of them would fit none. Tighten one when its own shape settles.

⛔ Section 8 also rules the other direction, and it is the mistake to watch for: the state files in the meta directory (`bootstrap-progress`, `capture-progress`, `maintenance-state`, `filing-log`, `capture-buffer`, `memory`) carry no `type:` at all, nothing mounts them, and a correct install is already silent about them. **Adding `type:` to a notepad is what creates the warning, not what silences it.**

## `singletons.home`

`required: [type]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `type` | A correct `Home.md` reported as a shape section 8 does not declare. | ⚠️ Its real readers work by **path**, not by this key: the wiring check `home-is-true` (`references/scaffold-spec.md:409`) and the directory audit in maintenance (`modes/maintenance.md:29` item (d)). | ⛔ |

## `singletons.business-profile`

`required: [type, business]` · `optional: [founder_name, brand_name, industry, category, location, one_line_description, created, last_updated]`

| Key | What it stops | Who reads it | If the owner wants it gone |
|---|---|---|---|
| `type` | The wing's profile cannot be found by shape. | `modes/capture.md:36` finds it by its frontmatter (`type: business-profile`, `business:`). | ⛔ |
| `business` | Which business this profile is about. ⭐ In a single-wing vault this is nearly free information; in a multi-wing vault it is the thing that separates two files of the same fixed name sitting at two wing roots. | ⚠️ No machine reader. Watch a false one: the dashboard's business name comes from `99_Meta/bootstrap-progress.md` (`scripts/deck.py:278-282`), not from this note. The real readers are prose that finds the file by address (`skills/project-consultant/SKILL.md:53` · `references/rooms-assets.md:30` `:34`). | A7 is safe while the vault has one wing. ⛔ Reconsider before a second wing opens: at that point the key is what tells two identically named files apart from the inside. |
| The optional keys | A5, and they are the landing points of the business-profile capture. | `templates/business-profile.template.md`. | Already optional. |
