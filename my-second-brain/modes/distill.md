# Distill Mode: the weekly maintenance ritual (tidy + distill)

About 10 minutes of the owner's attention: the AI does the hygiene, then brings distillation proposals; the owner only rules. This mode is the engine; the reminder doorbell lives in the generated command-base skill (morning check against `99_Meta/maintenance-state.md`), and any mode entry backstops it. Cadence: weekly is healthy; the doorbell rings past 7 days.

Two halves, always in this order (clean room first, then think):

## Half 1: Tidy (structure hygiene)

Scan the vault and build ONE report. Do not fix anything yet. The seven checks:

1. **Orphans:** notes reachable from no MOC and carrying no inbound links (skip `99_Meta`, `05_Archive`, daily notes). For each: proposed home MOC.
2. **Misfiled:** notes whose content contradicts their room (a procedure sitting in a function room; a client note in Inbox; a filled record where a template should be). Judge by the doctrine's filing tests and rulings table; cite the rule per item.
3. **Inbox backlog:** everything in `00_Inbox/` older than 3 days, each with a proposed destination (doctrine-cited).
4. **Stale MOCs:** rooms whose contents changed after the MOC's `last-refreshed:`; MOC inventories listing dead links; MOCs missing files that exist. Cross-reference `capture-progress.md`: rooms captured once and untouched for 4+ weeks are listed as cold rooms, proposal only (revisit the room, or mark it stable).
5. **Schema violations:** off-vocabulary tags, missing required frontmatter (`domain:` on decisions/tasks, `renew_by:` on company docs, `owner:`/`last_verified:` on SOPs), mis-cased enum values.
6. **Memory weight:** keep `99_Meta/memory.md` lean. Session-log entries older than 30 days rotate to `99_Meta/memory-archive/YYYY-MM.md` (create the folder on first rotation; append under a dated heading, never delete). Recent decisions trimmed to the newest 10 (the full notes live in `06_Command-Base/Decisions/`). Active-initiatives rows matching no live work get flagged. Watch-for entries sighted 3+ times get proposed for promotion into `profile.md` (only if that file exists). Rotation and trimming are mechanical; promotions and flags need the owner.
7. **Filing patterns:** read `filing-log.md` since the last tidy. Three or more filings to the same destination that has no room yet -> propose the room. Repeated filings decided by judgment with no rule to cite -> propose a canonical rulings-table row for doctrine section 8 (on approval: append the row, add a revision-log line). Report only; nothing structural gets created without the owner.

Present the report compactly, grouped by check, each item one line: what, where, proposed action, rule cited. Then ask for one ruling: fix all, fix by group, or walk through item by item. Purely mechanical items (MOC refreshes, dead-link cleanup) can be pre-marked "will do unless you object". Moving or renaming anything the owner wrote needs explicit approval, always.

Execute what was approved. Append every move to `filing-log.md`. Update every touched MOC. Set `last_tidy:` in `maintenance-state.md` and append a one-line history entry (date, items found, items fixed).

## Half 2: Distill (three pipes into Layer 3)

Now the thinking half. Read the week's material and bring PROPOSALS. The discipline, stated to the owner once per run: **distillation proposes, judgment rules.** Nothing enters Layer 3 unless the owner says yes; that is what keeps the third layer honest (it holds judgment, not sediment).

**Pipe 1, Decisions -> Decision-Rules.** Read `06_Command-Base/Decisions/` for this business (domain filter), recent 10 to 20. Look for repeated shape: the same trade-off resolved the same way three or more times. Propose it as a candidate rule, evidence attached: "Five of your last eight supplier decisions chose delivery reliability over unit price. Is that a rule you hold? Want it written as one?" On yes: one note in `03_Methodology/Decision-Rules/`, listing the evidencing decisions as links, `confirmed_by_owner: true`.

**Pipe 2, Logs -> rollup + refreshed maps.** Compress the week's `00_Daily-Log/` entries and function-room `Action-Log.md` lines into a short weekly rollup section appended to the newest daily log (or a `Weekly-Rollup` note if the owner prefers). Refresh `_Map.md` ("Current state", key numbers) and any room MOC whose key numbers moved. This pipe needs no ruling beyond a glance; it is memory maintenance, and it is what keeps `_Map.md` a truthful one-pager for every future session.

**Pipe 3, Learning + potholes -> Lessons.** Read new `04_Resources/Clippings/` (and Courses/Books notes) plus anything tagged `#lesson-candidate` this week. Where something was actually APPLIED or actually hurt, propose a Lesson: "You clipped that pricing article Tuesday, and Thursday you repriced the bundle. Worth a Lesson note that fuses the two?" Study lands in Resources, realization lands in Methodology, and the difference is the owner saying "yes, that is now how I operate." On yes: `03_Methodology/Lessons/` from the Lesson template, `confirmed_by_owner: true`.

Also under pipe 3: a Playbook whose every step has stabilized gets flagged for demotion into an SOP; an SOP whose pothole keeps recurring gets its pothole proposed as a Lesson. Say it when seen; the layers are a loop, not drawers.

## Close

- Set `last_distill:` in `maintenance-state.md`, append the history line (proposals made / accepted).
- Check the vault root `CLAUDE.md` against reality (a skill renamed, a second wing added, language changed, a rule amended). If it has drifted, propose the specific edit; the owner approves; never rewrite it silently.
- If this was the first time Layer 3 received ANY content, mark the moment; one line, no ceremony: "Your third layer is no longer empty. That is the layer capture could never fill."
- Surface next week's hook once, reading `next_suggestion:` from `capture-progress.md` so the hook is concrete: "Doorbell rings in 7 days. <Next room> is the suggested next move-in. Anything you want me to watch for between now and then?"

## First-run honesty

If maintenance runs before there is anything to distill (thin logs, no decisions yet), say so and run tidy only. Never manufacture insight from insufficient material; a short honest run builds more trust than a padded one.
