---
name: session-report
description: >
  Close out a working session in the owner's second-brain vault: land what this
  session actually produced, while whoever was in it still remembers. Writes any
  Lesson the session earned, catches decisions that were made but never written,
  proposes anything reusable, and leaves one session-report note in the vault's
  `00_Inbox/`: a one-paragraph summary plus the list of outputs, a baton the
  owner's next session reads and archives. MUST trigger when the
  user says "wrap up", "close out", "we're done here", "end of session", "session
  report", or ends a working session that produced something worth keeping. ⛔ NOT
  the end of the day, which is the owner's own command-base skill: a day ending
  is not a piece of work ending, and the two have separate words. NOT the weekly
  maintenance ritual (that is my-second-brain's distill mode), and NOT the place
  to write a Method (that is method-builder, which runs when a piece of WORK
  closes, not when a session does).
---

# Session Report

**The one job: nothing this session learned leaves with the session.**

This runs at the end of a working session, and the whole design is one rule: **decide at the closeout, with the person who was there.**

⭐ **Two minutes of the owner's attention, and it is over.** The report note below is your writing, not theirs: you draft it from what the closeout already surfaced, they glance at it. A closeout that turns into a second meeting stops happening within a month, and a ritual that stops happening captures nothing at all.

## Read first

1. `99_Meta/structure-doctrine.md` **§8** for the real shape of every record you might write, read at the time. ⛔ Never a key list quoted here.
2. `99_Meta/structure-doctrine.md` §7 for what each kind of record is, and for the decision guardrail.
3. `99_Meta/structure-doctrine.md` §1 (the `00_Inbox/` line) and §5 (dated-record names), which govern the report note this closeout leaves behind.
4. `02_Command-Base/Decisions/` filtered to `status: active`, for the guardrail below.

## Three questions, asked out loud, in this order

⛔ **Ask them; do not answer them for the owner.** You may say what you think the answer is, and they correct it. That is faster and it is still their call.

### 1 · "Did anything bite us?"

A pit: something that actually hurt. On a yes, write **one Lesson** into `04_Methodology/Lessons/` (subfoldered when a string of pits shares a subject), from the Lesson template, `confirmed_by_owner: true` once they have seen the text.

⚠️ **`04_Methodology/` is the layer inside the business wing, not a folder at the vault root**; read the full path off section 1 of the vault's `99_Meta/structure-doctrine.md` rather than guessing it.

⚠️ **Two sections, two different kinds of sentence.** `## What happened` is history and is never edited again. `## What we now do differently` is the living half. Write both; ⛔ do not collapse them into a narrative.

⛔ **A near miss with no cost is not a Lesson.** "That could have gone badly" is a feeling. What hurt, and what it cost, is a Lesson.

### 2 · "What kept coming up that you had to judge?"

⭐ **This question belongs to `method-builder`, and this skill's job is to notice and hand over, not to answer it.** If the session closed a piece of WORK (a case, a project, a job), say so in one line and hand the action back: "that is a method, and `method-builder` writes it properly. Say `method-builder` whenever you want it written, now or months from now." ⛔ Do not write a Method from here. ⛔ Do not press if they say later; the offer is the whole contribution.

### 3 · "Did we produce anything you will reach for again?"

⭐ **Four destinations and they are genuinely different things**, so name which one and let the owner pick:

- **A way of doing something** → a Method (see question 2, `method-builder` writes it).
- **A thing you now own** (a template, a script, a calculator, an asset) → it belongs in a real room in the vault, filed by doctrine §0, not described in a note about it.
- **Material worth keeping to read again** (a reference, a source, someone else's document) → `02_Command-Base/Resources/`. ⭐ That is the owner's library, kept by the owner; ⛔ nothing reads it on a schedule.
- **Something made by following a playbook** (a post, a proposal, a pitch, a quote) → **one row on that playbook folder's door**, in `04_Methodology/Playbooks/<the-work>/_<Name>-Guide.md`, under `## Recent runs`. Three columns: what came out, what the owner expects, and when it counts. ⭐ **The owner answers only "what do you expect", and the row lands with their yes** like anything else in that layer.

⛔ **"None of the above" is the usual answer** and it is a correct one. Say it and move on.

⚠️ **The fourth one is a backstop, not the main road, and the difference matters.** The session that used the playbook is supposed to write that row itself, because the door says so in its own words (doctrine §9.3, beat 4) and that runs with nothing installed. This skill catches the case where the work happened and nobody opened the door. ⛔ **Never let this become the normal way rows get written**: a door that only gets filled when somebody says "wrap up" is a door that depends on a skill, which is exactly what §9 refuses.

⛔ **No bet, no row.** If the owner has no expectation about the thing that was made, it does not go on the door at all. That table is a record of bets and what came back, ⛔ not a list of everything the playbook produced.

## The backstop: decisions that were made but never written

⭐ **This is the part that runs whether or not the three questions found anything**, because it is the one thing nobody ever remembers to do in the moment.

Scan the session for calls that will still stand tomorrow ("we're not doing X any more", "from now on Y", a price, a rule, a standing no). For each one, name it and ask. On a yes, write a `cb: decision` into `02_Command-Base/Decisions/` with every key §8 requires, read from §8 at the time.

⛔ **Run the guardrail before the note lands, even here.** Check the active set in the same lane: if this contradicts a decision that still stands, ask the one question, **change the rule, or break it once?** On "change the rule" the new note carries `supersedes:` and the old one flips to `status: superseded`. On "break it once" nothing is filed as a rule at all.

⭐ **The guardrail is not skipped for being late.** This path is the fallback for a decision the main path missed; a fallback that lands unchecked writes exactly the contradictions the guardrail exists to catch, and it does it on the notes nobody was watching.

## The baton: one report note, parked in the Inbox

⭐ **A closeout that had anything in it leaves ONE markdown note in `00_Inbox/`.** Every time, whatever the session served, whether it served one project or five. ⛔ Do not file it into a project folder, a room, or anywhere else, and ⛔ do not invent a folder for it. `00_Inbox/` is this vault's unfiled holding area, shared by the whole vault, and this note is unfiled on purpose (§1).

**Who it is for decides everything about it: the owner, opening their own session later, and whoever is in that session with them, neither of whom was in the room when this work happened.** The Lessons, decisions and hypotheses this closeout landed are the permanent record, and they live at their own central addresses. The report is the hand-off that carries "what happened here and what came out of it" across the gap between two sessions: read once, then archived, never a second record of anything. It has a second reader by default, which is why the Inbox is the right shelf: weekly maintenance drains everything sitting there and names it, so a report nobody opened is surfaced rather than lost.

**Name:** `YYYY-MM-DD-<slug>-session-report.md`. The date is the day the session happened (§5), and the slug names the project plus what the session did to it (`2026-03-14-acme-rebrand-homepage-copy-session-report.md`); a session that served no single project names the work instead. ⭐ **The name is carrying the whole address here:** the Inbox says nothing about where the work lives, and neither does `98_Archive/` afterwards, so a name that only says "session report" makes both piles unreadable. ⛔ Never `_`-prefixed: `_` means front door and a folder gets at most one (§5).

**Shape, four parts and nothing else:**

1. An H1 title: the project and the date.
2. Directly under it, the disposal line, blockquoted so it is the first thing any reader meets, and addressed to the session that opens it rather than to the owner:

   > To the session reading this: **archive this report after you are done reading it.** Move the file to `98_Archive/`, filename unchanged, in the same breath as reading it. This is a baton from the last working session on this work, ⛔ not a task list, and everything permanent it names already lives at its own address.

3. **One paragraph**: what the session set out to do, what it produced and decided, where it stopped (the loose end the next session picks up first), and anything weighed and deliberately not filed (the near miss judged not a Lesson, the call the owner chose not to make a rule). Plain sentences. ⛔ Not a play-by-play: the next session needs what came OUT of this one, not what it was like to be in it.
4. **The outputs, as a list**, one line per artifact, each by its address: notes this closeout landed (the Lesson, the decision) as wikilinks, files created or changed as paths, anything shipped outside the vault (a page live, a deck sent) named plainly. ⛔ List an output once, by address; do not restate its contents.

⛔ **No frontmatter. None. That is the design, not an omission to repair.** §8 declares no family for this note and §0 item 3 forbids forcing one, and §8's own control-family comment says why that is the right end of it: a `type:` marks a document a person reads and keeps, and a read-then-archive baton is the other kind. The Inbox is where the doctrine already parks material that carries no family (the SOP working folder lives there for the same reason, §1). The frontmatter guard will note the missing frontmatter as the note lands: that nudge is expected, and this paragraph is the answer to it. ⛔ Do not silence it by inventing a `type:`, which turns an expected nudge into a hard block.

Then append one line to `99_Meta/filing-log.md`: date, what, where, and the rule that decided it (§1, the Inbox holding area).

**Older reports still in the Inbox are not your business.** ⛔ Do not fold them into this one and ⛔ do not tidy them: the drain names everything sitting there, and a closeout that starts reorganising the Inbox is the second meeting this skill exists to avoid.

**Nothing to hand over is a real outcome.** A session that produced no outputs and landed no notes gets no file: an empty baton is clutter in the one folder the owner is asked to keep clear, and an Inbox that collects them teaches every future reader to skip the one that matters.

## Memory, and the one line that is not optional

Append the session's own log line to `99_Meta/memory.md`, as the vault's memory template says.

⛔ **Anything else headed for `99_Meta/memory.md` or `99_Meta/profile.md` needs the owner to see the exact words first.** Those two files enter every future session's context: a wrong line there never errors, it only steers, quietly, for as long as it sits there.

⚠️ **A claim about the owner themselves that you have only seen once is not memory.** It is a hypothesis, it goes in `99_Meta/Hypotheses/`, and it earns its way into `profile.md` through the weekly distillation by being seen again. ⛔ Do not shortcut that: "he prefers X" written after one sitting is how a profile fills up with things that happened to be true on a Tuesday.

## Close

One paragraph, spoken, plain: what landed, where (the report's path included), and what was deliberately not written. ⛔ Still no summary of the session for the person in the room; they were there. The summary exists, in the report, written for the one reader who was not: the next session. The spoken close hands over addresses, not a recap.

⭐ **An empty closeout is a real outcome and says so plainly:** "Nothing to land, this one was execution." An execution session still leaves the baton when it built something; what it never leaves is a Lesson written to feel productive. A session that produces a keeper for the judgment layer roughly one time in three is a healthy ratio; anything higher usually means the bar has slipped, ⛔ and the report never counts toward that ratio: it is the record OF the session, not something the session earned.
