# This vault is a My Second Brain

One home, two wings. Personal life lives in `03_Personal-Wing/`. The business lives in `04_{{BUSINESS}}-Business-Wing/`, a four-layer map: `01_Assets` what it is made of · `02_Work` what is moving right now, in four lanes · `03_SOP` how things get done · `04_Methodology` why decisions go the way they go, filled only from the owner's reviewed judgment. Above both wings sits `02_Command-Base/`, the operator's desk. Built and run with the `my-second-brain` skill.

## Rules of the house

- **Filing, naming, and tag rules live in the constitution: `99_Meta/structure-doctrine.md`.** Read it before filing or creating anything. It opens with a decision tree (§0) that answers most filings without judgment; two-way calls are settled by the precedent table (§2), and settled ones do not get relitigated. Every AI filing appends one line to `99_Meta/filing-log.md`.
- **`_<Name>-Guide.md` is the doorway of the folder it sits in: read it before working in that folder.** It says what belongs there and collects what sessions have noticed. `_<Project>-Brief.md` is a project's status card. Neither is a directory: `02_Command-Base/Home.md` is the only directory this vault has.
- **Link once, derive the rest.** A journal line links the brief or guide of what it belongs to, and nothing else is written twice. Briefs are linked bare; **guides are always linked with their path**, because the same room name repeats across wings.
- **A task must have a project.** Tasks live in `<Project>/Tasks/` and carry no project, lane or domain key: the path already says all three. If no project fits, propose one before the task exists. There is no parking lot.
- **Interaction language: {{LANGUAGE}}.** Folder and file names stay English.
- High-frequency transaction rows (invoices, POs, attendance) never enter this vault; pointers, exceptions, and monthly snapshots only, on the `IT-Systems/` note of the system that produces them.
- **Brand foundation is the positioning source of truth**: `04_{{BUSINESS}}-Business-Wing/01_Assets/<Brand>-Brand-Assets/`, eight pillars across `Brand-Strategy/` and `Target-Audience/`. Any outward-facing work reads it first. Stubs marked `status: empty` are not yet defined; treat them as gaps to fill, not answers.
- **`04_Methodology` is earned, never captured.** Nothing lands there without the owner's yes.
- No em dashes, no double dashes (--), no spaced hyphens as separators; use standard punctuation only (comma, colon, period, parentheses); restructure the sentence if needed. Applies to anything written for the owner to read, including vault note bodies.

## Navigation

- Front door: `02_Command-Base/Home.md` (the full directory) · Business one-pager: `04_{{BUSINESS}}-Business-Wing/_{{BUSINESS}}-Guide.md`, whose `## Current state` is what a session reads to know where things stand
- Dashboard: `02_Command-Base/Command-Base.base` (renders inside Obsidian; never hand-edit state into it)

## Skills that run this vault

- **`{{SLUG}}-command-base`**: the daily operating system. Say "morning", "what's on my plate", "log a decision", "compile", or "file this" and it takes over.
- **`my-second-brain`**: built this vault. Say "move in a room" or "capture my business" (capture), "distill" or "tidy my vault" (weekly maintenance), "create my jarvis" (give the AI a persona).
- **Not installed here, and nothing breaks without them:** `sop-builder` writes an SOP properly, in its own sitting (hand-writing one into `03_SOP/` is legal too); `playbook-lab` opens the rare feedback loop around a playbook that has earned one. Both are published separately and installed by the owner.
- **Session memory** (only when `99_Meta/bootstrap-progress.md` says `session_memory_installed: installed`): every Claude Code conversation on this machine is searchable. When the owner asks "how did we fix that last time", "why did we choose A over B", or anything about a past session, search history before re-deriving: the tool ships in the `my-second-brain` skill payload at `scripts/session-history/`, run `python3 "<tool>/sh" search "<query>"` (index refreshes itself). The weekly harvest of these sessions belongs to maintenance, not to this line.

---

**Owner:** {{YOUR_NAME}} · **Business:** {{BUSINESS_NAME}} · **Created:** {{DATE}}

Written once at setup. Later sessions never rewrite it silently; amendments are proposed during weekly maintenance and approved by the owner, same discipline as doctrine amendments.
