# Distill Mode: the weekly maintenance ritual (tidy + distill)

About 10 minutes of the owner's attention: the AI does the hygiene, then brings distillation proposals; the owner only rules. This mode is the engine; the reminder doorbell lives in the generated command-base skill (morning check against `99_Meta/maintenance-state.md`), and any mode entry backstops it. Cadence: weekly is healthy; the doorbell rings past 7 days.

Two halves, always in this order (clean room first, then think):

## Half 1: Tidy (structure hygiene)

**Run the machine pass first.** Before the human scan, run the read-only linter: `python3 <skill>/scripts/checkup.py "<vault-path>"` (add `--config <path>` if the owner keeps a private `.checkup.json` with their record-schema). It covers the mechanical half of the seven checks below (top-level rooms, required `99_Meta/` files, `cb:` schema, off-vocabulary tags, freshness) in seconds, so the human scan spends its attention on judgment (orphans, misfiling, distillation). The script is strictly report-only: it never moves, renames, or deletes anything, and its findings are proposals, not actions. Fold its output into the ONE report below; the owner still rules on every fix.

Scan the vault and build ONE report. Do not fix anything yet. The seven checks:

1. **Orphans:** notes reachable from no MOC and carrying no inbound links (skip `99_Meta`, `05_Archive`, daily notes). For each: proposed home MOC.
2. **Misfiled:** notes whose content contradicts their room (a procedure sitting in a function room; a client note in Inbox; a filled record where a template should be). Judge by the doctrine's filing tests and rulings table; cite the rule per item.
3. **Inbox backlog:** everything in `00_Inbox/` older than 3 days, each with a proposed destination (doctrine-cited).
4. **Stale MOCs:** rooms whose contents changed after the MOC's `last-refreshed:`; MOC inventories listing dead links; MOCs missing files that exist. Cross-reference `capture-progress.md`: rooms captured once and untouched for 4+ weeks are listed as cold rooms, proposal only (revisit the room, or mark it stable).
5. **Schema violations:** off-vocabulary tags, missing required frontmatter (`domain:` AND `function:` on decisions/tasks, `renew_by:` on company docs, `owner:`/`last_verified:` on SOPs, `function:` on lessons), mis-cased enum values. The `function:` field is load-bearing beyond hygiene: the pod-graduation doorbell counts decisions and lessons per function, so a blank `function:` makes that function silently invisible to it. Flag blanks; propose the fill.
6. **Memory weight:** keep `99_Meta/memory.md` lean. Session-log entries older than 30 days rotate to `99_Meta/memory-archive/YYYY-MM.md` (create the folder on first rotation; append under a dated heading, never delete). Recent decisions trimmed to the newest 10 (the full notes live in `06_Command-Base/Decisions/`). Active-initiatives rows matching no live work get flagged. Watch-for entries sighted 3+ times get proposed for promotion into `profile.md` (only if that file exists). Rotation and trimming are mechanical; promotions and flags need the owner.
7. **Filing patterns:** read `filing-log.md` since the last tidy. Three or more filings to the same destination that has no room yet -> propose the room. Repeated filings decided by judgment with no rule to cite -> propose a canonical rulings-table row for doctrine section 8 (on approval: append the row, add a revision-log line). Report only; nothing structural gets created without the owner.

Present the report compactly, grouped by check, each item one line: what, where, proposed action, rule cited. Then ask for one ruling: fix all, fix by group, or walk through item by item. Purely mechanical items (MOC refreshes, dead-link cleanup) can be pre-marked "will do unless you object". Moving or renaming anything the owner wrote needs explicit approval, always.

Execute what was approved. Append every move to `filing-log.md`. Update every touched MOC. Set `last_tidy:` in `maintenance-state.md` and append a one-line history entry (date, items found, items fixed).

## Half 2: Distill (three pipes into Layer 3)

Now the thinking half. Read the week's material and bring PROPOSALS. The discipline, stated to the owner once per run: **distillation proposes, judgment rules.** Nothing enters Layer 3 unless the owner says yes; that is what keeps the third layer honest (it holds judgment, not sediment).

**Pipe 1, Decisions -> Decision-Rules (or a pod's rubric).** Read `06_Command-Base/Decisions/` for this business (domain filter), recent 10 to 20. Look for repeated shape: the same trade-off resolved the same way three or more times. Propose it as a candidate rule, evidence attached: "Five of your last eight supplier decisions chose delivery reliability over unit price. Is that a rule you hold? Want it written as one?"

**Pod-aware routing (both pipes):** before proposing where a rule or lesson lands, look at the evidence's `function:` tag. If that function has **graduated into a pod**, the candidate belongs in that pod's `03_Methodology/rubric/` (its own loop owns function-local learning), not the wing `03_Methodology`. Only patterns that span two or more functions, or bind the business as a whole, go to the wing `Decision-Rules/` / `Lessons/`. Without this split the same evidence would be distilled twice, once into the wing and once into the pod, and the two copies drift. On yes for a wing rule: one note in `03_Methodology/Decision-Rules/`, listing the evidencing decisions as links, `confirmed_by_owner: true`. On yes for a pod rule: a candidate card in that pod's `rubric/` instead (the pod's loop-config governs when it hardens into the pod's `doctrine.md`).

**Pipe 2, Logs -> rollup + refreshed maps.** Compress the week's `00_Daily-Log/` entries and function-room `Action-Log.md` lines into a short weekly rollup section appended to the newest daily log (or a `Weekly-Rollup` note if the owner prefers). Refresh `_Map.md` ("Current state", key numbers) and any room MOC whose key numbers moved. This pipe needs no ruling beyond a glance; it is memory maintenance, and it is what keeps `_Map.md` a truthful one-pager for every future session.

**Pipe 3, Learning + potholes -> Lessons (or a pod's rubric).** Read new `04_Resources/Clippings/` (and Courses/Books notes) plus anything tagged `#lesson-candidate` this week. Where something was actually APPLIED or actually hurt, propose a Lesson: "You clipped that pricing article Tuesday, and Thursday you repriced the bundle. Worth a Lesson note that fuses the two?" Study lands in Resources, realization lands in Methodology, and the difference is the owner saying "yes, that is now how I operate." Route by `function:` exactly as Pipe 1: a function-local lesson for a graduated pod becomes a candidate in that pod's `rubric/`; a cross-function lesson goes to `03_Methodology/Lessons/` from the Lesson template, `confirmed_by_owner: true`.

Also under pipe 3: a Playbook whose every step has stabilized gets flagged for demotion into an SOP; an SOP whose pothole keeps recurring gets its pothole proposed as a Lesson. Say it when seen; the layers are a loop, not drawers.

**Pipe 4, the pod loop pass (one pass, all pods).** There is a single global distill; pods do not run their own rituals or carry their own maintenance doorbells (a per-pod doorbell would make the weekly load grow with pod count and break the ten-minute promise). Instead, this one distill iterates every graduated pod, one short subsection each. Per pod: read its `03_Methodology/rubric/` against its `loop-config.md`; any candidate card that has reached its confirmation threshold is proposed for promotion into the pod's `doctrine.md`; any hardened rule its loop-config marks as no-longer-holding is proposed for `retired.md`. Promotion never happens automatically; the owner rules, same as every other pipe. If a pod carries a `_state.md`, treat it as a timestamp record this pass writes to, not as an independent reminder.

## Pod altitude scan (the graduation and demotion doorbell)

Once per distill, read `99_Meta/graduation-config.md` (thresholds, owner-adjustable) and run a cheap, high-recall tripwire over the function rooms and pods. This is not a classifier; it errs toward surfacing, because a false positive costs the owner one sentence to wave off while a false negative means a function never grows a brain. The pod-worthiness judgment itself is made later, by the owner and the `pod-maker` gate; this scan only decides what to put on the table.

- **Graduation candidates (thin room -> pod):** a thin function room passes when its activity gate is open (recent movement in its `Action-Log`) AND either the decision density (`function:`-tagged decisions in the window) or the orphan-lesson count crosses threshold. Busy-but-no-decisions is an SOP, not a pod, so activity alone never triggers it; the decision count is the discriminator. Propose: "Marketing has logged 6 decisions and 5 lessons in 90 days and is still active. That looks like judgment worth its own loop. Want to graduate it into a pod?"
- **Demotion candidates (pod -> thin room / archive):** a graduated pod whose `Action-Log`, decisions, and `rubric/` have all gone quiet past the silence threshold, OR whose loop is idling (rubric candidates present but nothing has promoted and `doctrine.md` has not grown in a long window). Propose shrinking it back, and state the guarantee: its learning is archived, not lost (doctrine section 9), and re-graduating later can re-feed it.

Everything here is propose only. On the owner's yes, hand off to the `pod-maker` skill (installed at setup step 6.6): a graduation runs its graduate-room path, a demotion runs its demotion branch. Both preserve learning and run the inbound-link sweep. If `pod-maker` is somehow absent, record the accepted proposal and note it is pending pod-maker. Never move a pod by hand.

## Close

- Set `last_distill:` in `maintenance-state.md`, append the history line (proposals made / accepted).
- Check the vault root `CLAUDE.md` against reality (a skill renamed, a second wing added, language changed, a rule amended). If it has drifted, propose the specific edit; the owner approves; never rewrite it silently.
- If this was the first time Layer 3 received ANY content, mark the moment; one line, no ceremony: "Your third layer is no longer empty. That is the layer capture could never fill."
- Surface next week's hook once, reading `next_suggestion:` from `capture-progress.md` so the hook is concrete: "Doorbell rings in 7 days. <Next room> is the suggested next move-in. Anything you want me to watch for between now and then?"

## First-run honesty

If maintenance runs before there is anything to distill (thin logs, no decisions yet), say so and run tidy only. Never manufacture insight from insufficient material; a short honest run builds more trust than a padded one.
