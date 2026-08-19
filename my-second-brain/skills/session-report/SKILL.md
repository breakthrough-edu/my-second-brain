---
name: session-report
description: >
  Close out a working session in the owner's second-brain vault: land what this
  session actually produced, while whoever was in it still remembers. Writes any
  Lesson the session earned, catches decisions that were made but never written,
  proposes anything reusable, and stops. MUST trigger when the user says "wrap up",
  "close out", "收工", "done for today", "we're done here", "end of session",
  "session report", "写个收工报告", "记一下这次", or ends a working session that
  produced something worth keeping. NOT the daily journal compile (that is the
  owner's own command-base skill), NOT the weekly maintenance ritual (that is
  my-second-brain's distill mode), and NOT the place to write a Method (that is
  method-builder, which runs when a piece of WORK closes, not when a session does).
---

# Session Report

**The one job: nothing this session learned leaves with the session.**

This runs at the end of a working session, and it is the product's whole answer to a question it used to answer badly. A weekly pass that re-read old transcripts and guessed at what mattered was tried and measured: it was adopted at 0 of 649 and 0 of 26 on the passes that reached the owner raw. What replaced it is this: **decide at the closeout, with the person who was there.**

⭐ **Two minutes, and it is over.** A closeout that turns into a second meeting stops happening within a month, and a ritual that stops happening captures nothing at all.

## Read first

1. `99_Meta/structure-doctrine.md` **§8** for the real shape of every record you might write, read at the time. ⛔ Never a key list quoted here.
2. `99_Meta/structure-doctrine.md` §7 for what each kind of record is, and for the decision guardrail.
3. `02_Command-Base/Decisions/` filtered to `status: active`, for the guardrail below.

## Three questions, asked out loud, in this order

⛔ **Ask them; do not answer them for the owner.** You may say what you think the answer is, and they correct it. That is faster and it is still their call.

### 1 · "Did anything bite us?"

A pit: something that actually hurt. On a yes, write **one Lesson** into `04_Methodology/Lessons/` (subfoldered when a string of pits shares a subject), from the Lesson template, `confirmed_by_owner: true` once they have seen the text.

⚠️ **Two sections, two different kinds of sentence.** `## What happened` is history and is never edited again. `## What we now do differently` is the living half. Write both; ⛔ do not collapse them into a narrative.

⛔ **A near miss with no cost is not a Lesson.** "That could have gone badly" is a feeling. What hurt, and what it cost, is a Lesson.

### 2 · "What kept coming up that you had to judge?"

⭐ **This question belongs to `method-builder`, and this skill's job is to notice and hand over, not to answer it.** If the session closed a piece of WORK (a case, a project, a job), say so in one line and offer: "that is a method, and `method-builder` writes it properly. Want to do that now or next time you open this?" ⛔ Do not write a Method from here. ⛔ Do not press if they say later; the offer is the whole contribution.

### 3 · "Did we produce anything you will reach for again?"

⭐ **Three destinations and they are genuinely different things**, so name which one and let the owner pick:

- **A way of doing something** → a Method (see question 2, `method-builder` writes it).
- **A thing you now own** (a template, a script, a calculator, an asset) → it belongs in a real room in the vault, filed by doctrine §0, not described in a note about it.
- **Material worth keeping to read again** (a reference, a source, someone else's document) → `02_Command-Base/Resources/`. ⭐ That is the owner's library, kept by the owner; ⛔ nothing reads it on a schedule.

⛔ **"None of the above" is the usual answer** and it is a correct one. Say it and move on.

## The backstop: decisions that were made but never written

⭐ **This is the part that runs whether or not the three questions found anything**, because it is the one thing nobody ever remembers to do in the moment.

Scan the session for calls that will still stand tomorrow ("we're not doing X any more", "from now on Y", a price, a rule, a standing no). For each one, name it and ask. On a yes, write a `cb: decision` into `02_Command-Base/Decisions/` with every key §8 requires, read from §8 at the time.

⛔ **Run the guardrail before the note lands, even here.** Check the active set in the same lane: if this contradicts a decision that still stands, ask the one question, **change the rule, or break it once?** On "change the rule" the new note carries `supersedes:` and the old one flips to `status: superseded`. On "break it once" nothing is filed as a rule at all.

⭐ **The guardrail is not skipped for being late.** This path is the fallback for a decision the main path missed; a fallback that lands unchecked writes exactly the contradictions the guardrail exists to catch, and it does it on the notes nobody was watching.

## Memory, and the one line that is not optional

Append the session's own log line to `99_Meta/memory.md`, as the vault's memory template says.

⛔ **Anything else headed for `99_Meta/memory.md` or `99_Meta/profile.md` needs the owner to see the exact words first.** Those two files enter every future session's context: a wrong line there never errors, it only steers, quietly, for as long as it sits there.

⚠️ **A claim about the owner themselves that you have only seen once is not memory.** It is a hypothesis, it goes in `04_Methodology/Hypotheses/`, and it earns its way into `profile.md` through the weekly distillation by being seen again. ⛔ Do not shortcut that: "he prefers X" written after one sitting is how a profile fills up with things that happened to be true on a Tuesday.

## Close

One paragraph, plain: what landed, where, and what was deliberately not written. ⛔ Do not summarise the session; they were there.

⭐ **An empty closeout is a real outcome and says so plainly:** "Nothing to land, this one was execution." A session that produces a keeper roughly one time in three is a healthy ratio; anything higher usually means the bar has slipped.
