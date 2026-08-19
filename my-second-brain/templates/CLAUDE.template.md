# {{BUSINESS_NAME}} · My Second Brain

This vault is {{YOUR_NAME}}'s second brain: one home, two wings. Personal life lives in `03_Personal-Wing/`. The business lives in `04_{{BUSINESS}}-Business-Wing/`, a four-layer map: `01_Assets` what it is made of · `02_Work` what is moving right now, in four lanes (Deliver · Grow · Run · Build) · `03_SOP` how things get done · `04_Methodology` why decisions go the way they go, filled only from the owner's reviewed judgment. Above both wings sits `02_Command-Base/`, the operator's desk. Built and run with the `my-second-brain` skill.

## Rules of the house

- **Filing, naming, and tag rules live in the constitution: `99_Meta/structure-doctrine.md`.** Read it before filing or creating anything. It opens with a decision tree (§0) that answers most filings without judgment; two-way calls are settled by the precedent table (§2), and settled ones do not get relitigated. Every AI filing appends one line to `99_Meta/filing-log.md`.
- **Every folder's `_*-Guide.md` is its manual: read it before working there. `_*-Brief.md` is a project's status card.** Neither is a directory: `02_Command-Base/Home.md` is the only directory this vault has.
- **Link once, derive the rest.** A journal line links the brief or guide of what it belongs to, and nothing else is written twice. Briefs are linked bare; **guides are always linked with their path**, because the same room name repeats across wings.
- **A task must have a project.** Tasks live in `<Project>/Tasks/` and carry no project, lane or domain key: the path already says all three. If no project fits, propose one before the task exists (unsure which lane or wing it belongs to, ask). There is no parking lot.
- **When in doubt, park it in `00_Inbox/`**; weekly maintenance drains it. `01_Daily/` is compiled at end of day and never written mid-day: a mid-day capture goes through the command-base skill or the Inbox.
- **Same pit twice, say so out loud in the moment.** ⛔ There is no flag to plant and no tag to add: a pit becomes a Lesson at the CLOSEOUT of the session it happened in, with your yes, while you still remember what it cost. ⛔ Do not write the lesson mid-session either; naming it is the whole job.
- **When a Lesson, Method or Playbook is confirmed, drop a one-line pointer to it in Claude's own memory** (the auto-memory that persists across sessions), so the next session knows it exists without being told. ⭐ Methods are the ones this matters most for: they are written at closeout, one at a time, and a method nobody knows about gets rewritten from scratch the next time the same job comes round.
- **Interaction language: {{LANGUAGE}}.** Folder and file names stay English.
- High-frequency transaction rows (invoices, POs, attendance) never enter this vault; pointers, exceptions, and monthly snapshots only, on the `IT-Systems/` note of the system that produces them. Passwords never, anywhere.
- **Brand foundation is the positioning source of truth**: `04_{{BUSINESS}}-Business-Wing/01_Assets/<Brand>-Brand-Assets/`, eight pillars across `Brand-Strategy/` and `Target-Audience/`. Any outward-facing work reads it first. Stubs marked `status: empty` are not yet defined; treat them as gaps to fill, not answers.
- **`04_Methodology` is earned, never captured.** Nothing lands there without the owner's yes.
- No em dashes, no double dashes (--), no spaced hyphens as separators; use standard punctuation only (comma, colon, period, parentheses); restructure the sentence if needed. Applies to anything written for the owner to read, including vault note bodies.

## Reading and finding

- Front door: `02_Command-Base/Home.md` (the full directory) · Business one-pager: `04_{{BUSINESS}}-Business-Wing/_{{BUSINESS}}-Guide.md`, whose `## Current state` is what a session reads to know where things stand · the law: `99_Meta/structure-doctrine.md`
- Dashboard: `02_Command-Base/Command-Deck.html` (generated, opens in a browser; ⛔ never hand-edit state into it, every rebuild rewrites it whole. Say "rebuild my deck" to refresh it, "fix my deck" when a panel is dark)

Three questions have a place to be read before they are answered:

- **An operational "how do we do X" question**: find the SOP in `03_SOP/`, answer FROM it, and update it in the same move if answering revealed it is stale. No SOP yet? Say so and offer to write one. ⛔ Do not improvise a finished-looking SOP from one answer.
- **About to re-decide something, or wondering why it is set up this way**: read `02_Command-Base/Decisions/` first. The reasoning is usually already there, and a decision that gets silently reversed is worse than one that gets argued with.
- **About to work in an area that has burned this business before**: scan `04_Methodology/Lessons/` for that lane first. A confirmed Lesson nobody read is a pit fallen into twice.

## Skills that run this vault

- **`{{SLUG}}-command-base`**: the daily operating system. Say "morning", "what's on my plate", "log a decision", "waiting for", or "compile" and it takes over.
- **`my-second-brain`**: built this vault. Say "move in a room" or "capture my business" (capture), "distill" or "tidy my vault" (weekly maintenance), "create my jarvis" (give the AI a persona).
- **`project-consultant`**: think a project through before building it. Say "help me plan this project" or "I'm stuck on this project". It came with `my-second-brain` and updates with it. Never required: a project is born legally as a bare brief plus `Tasks/`.
- **`session-report`**: closes out a working session. Say "wrap up" or "收工". It writes the Lesson the session earned, catches decisions that got made but never written, and offers what is reusable. ⭐ This is how `04_Methodology/` gets fed at all; nothing else writes there.
- **`method-builder`**: writes one Method when a piece of WORK closes. Say "case closed" or "结案了". A Method is how you do one kind of thing, in your words, named for the work and never for the case. Same name, same file: found a better way, rewrite it.
- **`playbook-lab`**: opens and closes the rare feedback loop around a playbook that has earned one (§9). Say "open a lab". Came with `my-second-brain` too. Most playbooks never need one. ⛔ Never hand-build a lab.
- **Not installed here, and nothing breaks without it:** `sop-builder` writes an SOP properly, in its own sitting. It is published separately and installed by the owner; hand-writing an SOP into `03_SOP/` is legal (§1), which is why this one can be optional and `playbook-lab` cannot.
- **Session memory** (only when `99_Meta/bootstrap-progress.md` says `session_memory_installed: installed`): every Claude Code conversation on this machine is searchable. When the owner asks "how did we fix that last time", "why did we choose A over B", or anything about a past session, search history before re-deriving: the tool ships in the `my-second-brain` skill payload at `scripts/session-history/`, run `python3 "<tool>/sh" search "<query>"` (index refreshes itself). ⛔ It answers when asked and never speaks first; there is no weekly pass over these sessions any more.

---

**Owner:** {{YOUR_NAME}} · **Business:** {{BUSINESS_NAME}} · **Created:** {{DATE}}

Written once at setup. Later sessions never rewrite it silently; amendments are proposed during weekly maintenance and approved by the owner, same discipline as doctrine amendments.
