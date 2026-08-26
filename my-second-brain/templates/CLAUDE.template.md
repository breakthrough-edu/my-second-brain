# {{BUSINESS_NAME}} · My Second Brain

This vault is {{YOUR_NAME}}'s second brain: one home, two wings. Personal life lives in `03_Personal-Wing/`. The business lives in `04_{{BUSINESS}}-Business-Wing/`, a four-layer map: `01_Assets` what it is made of · `02_Work` what is moving right now, in four lanes (Deliver · Grow · Run · Build) · `03_SOP` how things get done · `04_Methodology` why decisions go the way they go, filled only from the owner's reviewed judgment. Above both wings sits `02_Command-Base/`, the operator's desk. Built and run with the `my-second-brain` skill.

## Rules of the house

- **Filing, naming, and tag rules live in the constitution: `99_Meta/structure-doctrine.md`.** Read it before filing or creating anything. It opens with a decision tree (§0) that answers most filings without judgment; two-way calls are settled by the precedent table (§2), and settled ones do not get relitigated. Every AI filing appends one line to `99_Meta/filing-log.md`. Amending it goes through the `breakthrough-vault-guardian` skill: propose, get {{YOUR_NAME}}'s yes, then every file the change touches moves in one breath.
- **Every folder's `_*-Guide.md` is its manual: read it before working there. `_*-Brief.md` is a project's status card.** Neither is a directory: `02_Command-Base/Home.md` is the only directory this vault has.
- **Link once, derive the rest.** A journal line links the brief or guide of what it belongs to, and nothing else is written twice. Briefs are linked bare; **guides are always linked with their path**, because the same room name repeats across wings.
- **A task must have a project.** Tasks live in `<Project>/Tasks/` and carry no project, lane or domain key: the path already says all three. If no project fits, propose one before the task exists (unsure which lane or wing it belongs to, ask). There is no parking lot.
- **When in doubt, park it in `00_Inbox/`**; weekly maintenance drains it. `01_Daily/` is compiled at end of day and never written mid-day: a mid-day capture goes through the command-base skill or the Inbox.
- **Same pit twice, say so out loud in the moment.** ⛔ There is no flag to plant and no tag to add: a pit becomes a Lesson at the CLOSEOUT of the session it happened in, with your yes, while you still remember what it cost. ⛔ Do not write the lesson mid-session either; naming it is the whole job.
- **When a Lesson, Method or Playbook is confirmed, drop a one-line pointer to it in Claude's own memory** (the auto-memory that persists across sessions), so the next session knows it exists without being told. ⭐ Methods are the ones this matters most for: they are written at closeout, one at a time, and a method nobody knows about gets rewritten from scratch the next time the same job comes round. ⛔ **For anything in `04_Methodology/Playbooks/`, the pointer names the FOLDER, never the file inside it**: the folder's door is what has to be read first, and a pointer aimed at the playbook text walks straight past the record of what using it actually produced.
- High-frequency transaction rows (invoices, POs, attendance) never enter this vault; pointers, exceptions, and monthly snapshots only, on the `IT-Systems/` note of the system that produces them. Passwords never, anywhere.
- **Brand foundation is the positioning source of truth**: `04_{{BUSINESS}}-Business-Wing/01_Assets/{{BUSINESS}}-Brand-Assets/`, eight pillars across `Brand-Strategy/` and `Target-Audience/`. Any outward-facing work reads it first. Stubs marked `status: empty` are not yet defined; treat them as gaps to fill, not answers.
- **`04_Methodology` is earned, never captured.** Nothing lands there without the owner's yes.
- No em dashes, no double dashes (--), no spaced hyphens as separators; use standard punctuation only (comma, colon, period, parentheses); restructure the sentence if needed. Applies to anything written for the owner to read, including vault note bodies.

## Shared language

The words this business thinks in, so a session says "the {{BUSINESS_NAME}} way" in one term instead of a paragraph. A term listed here means exactly what its line says, in conversation and in every file this vault writes; name things (files, headings, projects) with these terms so the same word means the same thing everywhere. Starts empty on purpose.

- *(none yet)*

Growing it: when a session catches itself explaining the same concept in a sentence for the second time, or the owner uses a house word an outsider would misread, propose one line here (term, then meaning, ten words or fewer). Owner says yes, the line lands; this is a wording register, not law, so it needs no doctrine amendment.

## Reading and finding

- Front door: `02_Command-Base/Home.md` (the full directory) · Business one-pager: `04_{{BUSINESS}}-Business-Wing/_{{BUSINESS}}-Guide.md`, whose `## Current state` is what a session reads to know where things stand · the law: `99_Meta/structure-doctrine.md`
- Dashboard: `02_Command-Base/Command-Deck.html` (generated, opens in a browser; ⛔ never hand-edit state into it, every rebuild rewrites it whole. Say "rebuild my deck" to refresh it, "fix my deck" when a panel is dark)

These questions have a place to be read before they are answered:

- **An operational "how do we do X" question**: find the SOP in `03_SOP/`, answer FROM it, and update it in the same move if answering revealed it is stale. When the answer turns on a judgment rather than a step, open the playbook the SOP's `playbook:` key names, and the lane's active decisions with it. ⭐ **Enter a playbook through its folder's door, not through the playbook file alone**: the door carries what has come back from using it, and a row still waiting on its result is settled before the work starts, not after (§9.3). Then the lane's active decisions; an SOP without that key has no playbook behind it, which is legal. No SOP yet? Say so and offer to write one. ⛔ Do not improvise a finished-looking SOP from one answer.
- **About to re-decide something, or wondering why it is set up this way**: read `02_Command-Base/Decisions/` first. The reasoning is usually already there, and a decision that gets silently reversed is worse than one that gets argued with.
- **About to work in an area that has burned this business before**: scan `04_Methodology/Lessons/` for that lane first. A confirmed Lesson nobody read is a pit fallen into twice.
- **About to re-derive something that was already worked out in an earlier session** (only when `99_Meta/bootstrap-progress.md` says `session_memory_installed: installed`): every Claude Code conversation on this machine is searchable. When the owner asks "how did we fix that last time", "why did we choose A over B", or anything about a past session, search history before re-deriving: the tool ships in the `my-second-brain` skill payload at `scripts/session-history/`, run `python3 "<tool>/sh" search "<query>"`. Searching never indexes anything: `python3 "<tool>/sh" ingest` is what builds and refreshes the index, and the tool says so in plain words if it has not been run yet. ⛔ It answers when asked and never speaks first.

---

**Owner:** {{YOUR_NAME}} · **Business:** {{BUSINESS_NAME}} · **Created:** {{DATE}}

Written once at setup. Later sessions never rewrite it silently; amendments are proposed during weekly maintenance and approved by the owner, same discipline as doctrine amendments, or through `breakthrough-vault-guardian` when a change to the law is what brought the session here and this file is one of the files that change touches.
