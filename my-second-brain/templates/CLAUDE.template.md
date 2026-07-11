# This vault is a My Second Brain

One home, two wings: personal life in PARA (`02_Projects` to `05_Archive`), the business in a three-layer map under `07_{{BUSINESS}}/` (01_Assets: what it is made of · 02_SOP: how things get done · 03_Methodology: why decisions go the way they go, filled only from the owner's reviewed judgment). A function room can later graduate into a wing-level **pod** (its own learning loop); the rules for that live in section 9 of the constitution. Built and run with the `my-second-brain` skill.

## Rules of the house

- **Filing, naming, and tag rules live in the constitution: `99_Meta/structure-doctrine.md`.** Read it before filing or creating anything. Two-way calls are settled by its canonical rulings table; do not relitigate them. Every AI filing appends one line to `99_Meta/filing-log.md`.
- **Interaction language: {{LANGUAGE}}.** Folder and file names stay English.
- High-frequency transaction rows (invoices, POs, attendance) never enter this vault; pointers, exceptions, and monthly snapshots only.
- **Brand foundation is the positioning source of truth**: `07_{{BUSINESS}}/01_Assets/Brand-Strategy/` (the five identity pillars) + `01_Assets/Target-Audience/`, with pillar 1 (Positioning) in `03_Methodology/Positioning/`. Any outward-facing work reads it first. Stubs marked `status: empty` are not yet defined; treat them as gaps to fill, not answers.
- No em dashes, no double dashes (--), no spaced hyphens as separators; use standard punctuation only (comma, colon, period, parentheses); restructure the sentence if needed. Applies to anything written for the owner to read, including vault note bodies.

## Navigation

- Front door: `06_Command-Base/Home.md` · Business one-pager: `07_{{BUSINESS}}/_Map.md`
- Dashboard: `06_Command-Base/Command-Base.base` (renders inside Obsidian; never hand-edit state into it)

## Skills that run this vault

- **`{{SLUG}}-command-base`**: the daily operating system. Say "morning", "what's on my plate", "log a decision", "compile", or "file this" and it takes over.
- **`my-second-brain`**: built this vault. Say "move in a room" or "capture my business" (capture), "distill" or "tidy my vault" (weekly maintenance), "create my jarvis" (give the AI a persona).
- **Session memory** (only when `99_Meta/bootstrap-progress.md` says `session_memory_installed: installed`): every Claude Code conversation on this machine is searchable. When the owner asks "how did we fix that last time", "why did we choose A over B", or anything about a past session, search history before re-deriving: the tool ships in the `my-second-brain` skill payload at `scripts/session-history/`, run `python3 "<tool>/sh" search "<query>"` (index refreshes itself). The weekly harvest of these sessions belongs to Distill, not to this line.

---

**Owner:** {{YOUR_NAME}} · **Business:** {{BUSINESS_NAME}} · **Created:** {{DATE}}

Written once at setup. Later sessions never rewrite it silently; amendments are proposed during weekly maintenance and approved by the owner, same discipline as doctrine amendments.
