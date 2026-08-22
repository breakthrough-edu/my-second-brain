# Maintenance Mode: the anti-drift half of the weekly ritual

**The question this half answers: is the house still what it says it is?** Everything here is about keeping the vault from rotting: doors that lost their folders, notes that broke their own schema, a memory file quietly growing into a pile, a wing guide that describes a business from four months ago. Most of it is mechanical, most of it is decidable without the owner, and that is exactly why it is separated from the other half.

**It runs FIRST, and the order is load-bearing.** The distillation half reads the state of the house to decide what is worth keeping; this half is what makes that state true. Distilling out of a drifted house distills the drift.

⛔ **One doorbell, two files.** The doorbell in the generated command-base skill rings once and names the half that is actually overdue rather than handing the owner a choice. This file runs, and then [distill.md](distill.md) runs. An owner who does name a half gets that half, and it runs alone.

Cadence comes from `cadence_days` in `99_Meta/maintenance-state.md` (weekly by default). ⛔ Every staleness comparison in this file reads that key; never assume 7.

## Run the machine pass first

`python3 <skill>/scripts/checkup.py "<vault-path>"`

It covers the mechanical share of the checks below in seconds, so the human pass spends its attention on judgment (orphans, misfiling, what a wing guide actually says now). The script is strictly report-only: it never moves, renames, or deletes anything, and its findings are proposals. Fold its output into the ONE report at the end; the owner still rules on every fix.

⛔ **Read the report, not the exit code.** `checkup.py` returns 0 even when it printed errors, on purpose (it is a linter, not a gate). A session that checks the exit code and reports "clean" has read nothing.

⛔ **Do not run `deck.py doctor` here and do not fold dark dashboard cells into this report.** Every key it reports is optional in §8, so nothing it finds is a violation, and a weekly list of legal-but-unfilled keys is a nag the owner learns to scroll past. `doctor` runs when the owner asks why a panel is dark, and no other time.

⛔ **The dashboard rebuild is NOT this pass's job.** It belongs to the command-base skill's session start, where it already happens. ⛔ Do not add a backstop for it here either: this pass is reached through a doorbell that lives in that very session start, so a backstop here shares a single point of failure with the thing it backs up.

## The checks

Scan, build ONE report, fix nothing yet.

**Doors, doorplates and the directory**

1. **Doors and the directory, four things at once.** (a) **Exists:** every room, lane, brand subfolder and wing has a door. (b) **Unique:** exactly one `_`-prefixed file per folder, never two (§5). (c) **Content:** the door's text still describes what is actually in the folder. (d) **Directory:** `Home.md` audited against the filesystem **in both directions**, every folder listed exists and every folder that exists is listed, minus the three documented exemptions (inside a project folder, inside `99_Meta/Skills/`, and `99_Meta/memory-archive/` itself). ⭐ **A folder that turns out to be a whole new wing is not a directory fix.** Home, the doors, `CLAUDE.md` and §8 all have to move together, which is `vault-guardian`'s job; name it here and propose opening it, ⛔ never paper over it with a Home line.

    ⭐ **(c) is the one with teeth.** A door that exists and is unique can still be a lie: it was written the week the room was moved into and the room has had a year since. Scan door **content** for **rooms and brand folders only**, around seventeen files. ⛔ **Do not scan `## Observations` sections**, ⛔ do not scan the SOP menu (`sop-builder` reconciles that itself every time it runs), and ⛔ do not judge a wing guide's `## Current state` here, which is prose and gets its own check below.

    Cross-reference `capture-progress.md`: rooms or lanes captured once and **untouched** for four cadence periods are listed as **cold**, proposal only (revisit, or mark stable).

    ⭐ **`untouched` means nothing in the folder has changed; ⛔ it does not mean capture has not run again.** Read the newest change inside the folder itself. The other reading makes this check say something that is true of every healthy vault by about the sixth week: rooms are moved in once, in the first week or two, and are never "captured" a second time, so almost every room would be named cold every week from then on, forever. ⚠️ **One alarm the owner knows is empty and they learn to skip the whole report**, which costs more than this check is worth.

    ⚠️ **File timestamps are not durable, and this check has to survive that.** A sync, a restore, or a copy to a second machine rewrites every modification time at once and nothing notices; this product says the same thing about `built_on:` for the same reason. Two rules follow. **A date written inside a note beats the file's timestamp whenever one exists** (`status_since:`, `created:`, the newest dated journal line linking that room): a person wrote it, and copying a vault does not move it. And ⛔ **if the newest timestamps across the whole vault land on or around one day, they were rewritten, not earned**: say so in one line and list nothing as cold this run.

**Machine-layer self-check**

2. **Required `99_Meta` files.** Every control file `required_meta_files` in `scripts/checkup.py` names is present. ⛔ **Do not copy those names here.** That list is the whole list and not a sample of it, the machine pass above is what reads it (`check_required_meta`), and a second copy on paper is a second thing to keep true: the day the product generates one more control file, the paper copy is the one that goes on saying the old number. A missing one is an error, not a note.
3. **Standard guards.** Every guard `bootstrap-progress.md` records as installed is still registered where it says it is. ⭐ **This one reports at INFO and never errors**, deliberately: a declined guard and a machine that could not run one are correct outcomes, and a weekly scolding for an answer the owner was asked to give is how a check gets switched off.
4. **Top-level rooms.** Nothing has appeared at the vault root that the doctrine does not name.

**One file, judged on its own**

5. **Record (`cb:`) schema.** Every `cb:` record against its family in §8.
6. **Type-mounted families.** Every note that mounts a family through `type:` against §8.
7. **Tag vocabulary.** Every tag used against `99_Meta/tagging-vocabulary.md`. A tag that is not on the list is a proposal to add it or a typo to fix, and the report says which it looks like.
8. **Schema violations, the judgment layer.** ⛔ A key §8 has NOT declared is **not** a violation: flag it as a judgment call ("register it in §8, or drop it"), never as an error. Watch `lane:` in particular: required on SOPs, methods, playbooks and lessons, and a blank one makes that note invisible to every lane-filtered view.

**Relationships between files, and the calendar**

9. **Freshness.** Read `maintenance-state.md` and say, in one line, how each half stands against `cadence_days`: `last_tidy` for this pass, `last_distill` for the other. ⭐ This is the check that makes stamping at the close non-optional: skip the stamp and Freshness reports maintenance as permanently overdue.
10. **Orphans.** Notes with no inbound links, reachable from no door (skip `99_Meta`, `98_Archive`, daily notes). Remember what reachable means: entity notes are found by type plus address, not by links (§3), so a client note with no backlinks is normal. The real orphan is a note whose type family has no home rule, or a file in a folder nothing explains.
11. **Misfiled.** Notes whose content contradicts their location (a procedure in an entity room; a client note in Inbox; a filled record where a template should be; a project in the wrong lane by the §1 ladder). Judge by the doctrine's filing tests and precedent table; cite the rule per item.
12. **Inbox drain.** Everything sitting in `00_Inbox/` gets named, each with a proposed destination and the rule behind it. ⛔ **There is no age threshold**: whoever runs the pass names what is there.
13. **Memory weight, the mechanical half only.** Session-log entries older than 30 days rotate to `99_Meta/memory-archive/YYYY-MM.md` (create the folder on first rotation; append under a dated heading, ⛔ never delete). Recent decisions trimmed to the newest 10 (the full notes live in `02_Command-Base/Decisions/`). Active-initiatives rows matching no live work get flagged.

    ⛔ **The `## This week's compass` slot is exempt from all of it.** It is replaced whole every week by check 14 and it has exactly one week in it at a time, so there is nothing in it old enough to rotate; archiving it would file a copy of something that already has its own note in `02_Command-Base/Reviews/`. The other half does not touch it either.

    **The line to hold, past which it is the other half's business:** rotation and trimming are mechanical and land here. ⛔ **"This memory line looks like a durable fact about the owner" is a judgment and does NOT land here**; hand it to the distillation half, which writes the pool that claims like that have to age in, and where the owner rules on it. ⛔ **This half never writes that pool**; it counts it (check 14's Pool vitals) and nothing more, and `session-report` writes it too, at a session's closeout.

    ⭐ **A retired fact line goes to `99_Meta/memory-archive/` like everything else, and this matters more than tidiness.** The failure this product has actually produced is a thing the owner said out loud being silently dropped. Retiring is the owner's "no"; keeping the body is how a no stays reviewable.

    ⚠️ The line count past which the file is too heavy is `memory_max_lines:` in `99_Meta/maintenance-state.md`, beside `cadence_days`. ⛔ Never hardcode it here: an owner running two businesses legitimately carries a longer memory than one running a stall, and a threshold nobody can move is one they learn to ignore.

**Truth of the written record**

14. **Weekly rollup, and the two things that close it.** Compress the week's `01_Daily/` entries into a weekly review filed in `02_Command-Base/Reviews/` (`type: weekly-review`), grouped by wikilink backlink, on the `Weekly-Review.md` shape in `99_Meta/Templates/`. Fill every section down to **Pool vitals**; ⛔ leave **What I noticed** alone, the other half writes it. The compression itself needs no ruling beyond a glance; it is memory maintenance.

    ⛔ **A week with nothing in `01_Daily/` gets no review.** A break is covered by the next one, never by a stub: a folder half full of empty reviews is a folder that stops being read, and this layer is read by machines every single week.

    ⚠️ **Ask for the headline; ⛔ never write it.** One line, the owner's own words, pasted back as said. It is the only sentence in the whole ritual that is not mechanical, and it is the seed for the theme check below, which is exactly why the AI's own reading of the week is kept out of it and given its own section in the other half.

    **Pool vitals** is three counts off `99_Meta/Hypotheses/` itself: open, graduated this week, expired this week. ⛔ Nothing else goes in that section.

    ⭐ **Two producers hang off this item's close, and they are here for one reason: they read what this check just wrote.** Splitting either into the other half would put a producer and its only input on opposite sides of a handover, which is the exact failure this product keeps finding (an address and a shape with nobody writing into them).

    - **Theme check (the doorbell).** Read `02_Command-Base/Reviews/` for a `type: monthly-theme` with `status: active`. **None** → propose opening one, seeded from this week's headline. **One that this week's headline contradicts, or whose `month:` is more than a month behind** → say so and propose replacing it. ⛔ **Proposal only, always:** a theme is the owner's word for their own month, and one the machine picked is a label, not a theme. ⛔ **Never open one silently and never close one silently.** On yes: write the new theme from the `Monthly-Theme.md` template with `Follows [[<the theme it replaces>]]`, and **in the same breath** flip the old one to `status: closed` with today's `status_since:` and write `Followed by [[<the new theme>]]` under its title. ⭐ **Both directions get written at the one moment somebody knows both names**; that mutual link is the whole reason the review layer reads as a line rather than a pile, and it is what the command-base skill's growth conversation walks. On no: nothing is written, and it is not raised again until the next run. **Why this check exists at all:** a monthly theme has a family, a template and an address, and until this line it had no producer, which is how a vault goes eight weeks without a theme while everything looks correctly set up.

    - **This week's compass.** Overwrite the `## This week's compass` slot at the top of `99_Meta/memory.md` with this week's **headline**, **Top 3** and **active theme**. ⛔ **This is that slot's only writer**, it is replaced whole (⛔ never appended to), and it holds one week at a time. The reason it exists is a reader, not tidiness: session start reads `memory.md` as its first act, so the morning after the ritual the AI opens already carrying the week the owner just described. ⛔ Do not copy anything else into it: the record of record is the review note itself.
15. **`## Current state` refresh.** The wing guide's `## Current state` section, in the owner's own words, refreshed if the week moved it. ⚠️ **This is the one state in the whole vault carried by prose, which no machine can judge.** So it is asked, never assumed: show what it says today and ask whether it is still true.

## Close

16. **Stamp `maintenance-state.md`.** Set `last_tidy:` and append a one-line history entry (date, items found, items fixed). ⭐ **`last_tidy` is this pass's own key: the key and the pass carry two names for one thing, and this is the one place that says so.** ⛔ **This half stamps `last_tidy` and nothing else.** The other half stamps `last_distill`; that is the whole reason the file keeps two dates, and it is what lets the doorbell name the half that is actually overdue.
17. **`CLAUDE.md` drift check.** Read the vault root `CLAUDE.md` against reality (a skill renamed, a second wing added, a rule amended). If it has drifted, propose the specific edit and let the owner approve. ⛔ Never rewrite it silently (§4, law 5). ⭐ **If it drifted because the law itself moved** (a wing opened, a family was added, a rule was loosened), patching this file alone leaves the rest of the amendment undone: that is `vault-guardian`'s job, and the honest move is to propose opening it rather than to fix the sentence here.

## Then hand over

18. ⛔ **Do not close the ritual here.** Load [distill.md](distill.md) and run it. The last word of the week (next week's hook) is spoken there, because that is where the ritual actually ends.

## How to present it

Grouped by check, each item one line: what, where, proposed action, rule cited. Then ask for ONE ruling: fix all, fix by group, or walk through item by item. Purely mechanical items (a stale `updated:`, a dead link, a Home entry that lost its folder) can be pre-marked "will do unless you object". Moving or renaming anything the owner wrote needs explicit approval, always, and a move rewrites its inbound links in the same breath (§3).

Execute what was approved. Append every move to `filing-log.md`.

## First-run honesty

On a young vault most of this finds nothing. Say so in one line and move on. ⛔ Never manufacture findings to look thorough; a short honest pass builds more trust than a padded one, and it is also what makes a real finding believable when one turns up.
