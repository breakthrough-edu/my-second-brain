---
name: method-builder
description: >
  MANUAL TRIGGER ONLY: runs when the owner calls this skill by name, or when the
  session was told at the outset to write a Method when the work closed. ⛔ Do not
  fire on work-closing phrasing.
  Write down how the owner actually did a piece of work, at the moment that work
  closes, as one Method note in their second-brain vault. Reads the vault first
  (doctrine section 8, existing methods, the lane), asks about what it could not
  read, and lands one note with the owner's yes given out loud in that moment.
  NOT for a pit that hurt (that is a Lesson, written at session closeout), NOT for
  a call that still stands (that is a decision), NOT for dead repeatable steps
  (that is sop-builder), and NOT for composing several methods into a playbook
  (that is the weekly distillation, and it is not this skill's call to make).
disable-model-invocation: true
---

# Method Builder

You write ONE thing: a **Method**, which is one move of the owner's, written down at the moment the work that taught it closes.

**Why now and not later.** How somebody did something is at its sharpest the hour they finish. A week later it has become a summary of itself. ⛔ Do not defer this to any later pass that re-reads the week and guesses.

## What a Method is, and the three things it is not

A Method answers: **how do I do this kind of work?** It is the owner's own way of doing one thing, in their words.

- ⛔ **Not a Lesson.** A Lesson is a pit: something that hurt. If the sentence starts "never again", it is a Lesson and it belongs to the session closeout, not here.
- ⛔ **Not a Decision.** A Decision is a call that still stands ("we never discount below 20%"). It lands in `02_Command-Base/Decisions/` the moment it is made.
- ⛔ **Not an SOP.** An SOP is dead steps anyone can follow. A Method is judgment: what you weigh, what you reach for first, where you slow down. If a new hire could execute it without thinking, it is an SOP and `sop-builder` writes it.

⛔ **You do not decide what kind of work this method belongs to, and there is no field for it.** That judgment happens later, when several methods are read together in the weekly distillation. Asking for it here would put the classification burden on the one moment the owner least wants it, which is the moment they just finished the job.

## Read before you ask

1. `99_Meta/structure-doctrine.md` **§8** for the method family's real shape, read at the time. ⛔ Never a key list quoted from this file.
2. `99_Meta/structure-doctrine.md` §5 and §7 for the naming rule and the edges.
3. `04_Methodology/Playbooks/*-method.md`, all of them, names and headings. ⭐ **This is the step that pays for itself:** if a method for this work already exists, ⛔ you are not writing a new one.
4. The work itself: the project brief, its `Tasks/`, whatever the session just did.

## The interview: three questions, and no more

Ask them one at a time. If the session that just closed already answered one, ⛔ do not ask it again; say what you have and ask them to correct it.

1. **"When do you reach for this?"** The trigger. What kind of job, what circumstances.
2. **"How do you actually do it?"** The moves, in their order. ⛔ Do not tidy this into a numbered procedure if it did not happen as one.
3. **"What did you have to judge along the way?"** ⭐ **This is the question that makes it a Method rather than an SOP**, and it is the one worth pushing on. "What would have gone wrong if you had done the obvious thing instead?" usually gets it.

⛔ **Their words, not yours.** You are transcribing a practitioner, not writing documentation. If a sentence sounds like a manual, it is wrong.

## Then write exactly one note

From the **Method template** in `99_Meta/Templates/`, into `04_Methodology/Playbooks/`, flat, beside the playbooks.

⚠️ **`04_Methodology/` is the layer inside the business wing, not a folder at the vault root**; read the full path off section 1 of the vault's `99_Meta/structure-doctrine.md` rather than guessing it.

- **Name it for the work**, `<the-work>-method.md`, ⛔ never for the case that taught it (§5). Show the owner the filename before you write it; a wrong name here is the one thing that has to be fixed by hand later.
- ⛔ **Same work, same file.** If step 3 above found a method for this work, **rewrite that one** and say what changed. ⛔ Do not create a second file with a version or a date in its name.
- **`confirmed_by_owner: true` only after they have seen the actual note and said yes**, out loud, in this session. ⛔ Silence is not a yes and ⛔ "sounds good" to a summary is not a yes to the text.
- Append one line to `99_Meta/filing-log.md`.
- ⭐ **Then drop a one-line pointer into the vault's working memory, `99_Meta/memory.md`**, so the next session knows this method exists without being told. A method nobody knows about gets rewritten from scratch the next time the same job comes round, and that is the failure this whole skill exists to prevent.

## Two things to say once, at the end, and then stop

- **What happens to it next**: several related methods can compose into a playbook in the weekly distillation, and when that happens this note keeps its name, flips to `status: superseded` and gains `distilled_into:` pointing at the playbook. ⛔ It is never deleted; which fights a playbook came out of has to stay answerable.
- **⛔ Never propose the playbook yourself.** One method is not a pattern, and a playbook proposed off a single job is the exact thing that makes the layer stop being trustworthy.

## If there is nothing here

Plenty of finished work teaches nothing new: it was routine, or it followed an existing method exactly. **Say so and write nothing.** ⛔ A method written to be productive is worse than no method, because it is one more thing the weekly pass has to read and rule on. "You already do this the way `<existing>-method.md` says. Nothing to add." is a complete and correct outcome.
