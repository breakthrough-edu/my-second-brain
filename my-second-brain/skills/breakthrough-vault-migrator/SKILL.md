---
name: breakthrough-vault-migrator
description: >
  Move an existing body of files into this vault without breaking the
  relationships between the documents. Freezes what is being moved so the
  boundary stops shifting, reads the pile for shape before it reads it for
  content, proposes a mapping the owner rules on, then moves it in batches,
  rewriting links as it goes and leaving a ledger of what was moved and what was
  deliberately left behind. It is staged and it resumes: every run picks up from
  99_Meta/migration-progress.md, so this can take weeks of short sittings. MUST
  trigger on "migrate my old notes", "move my old vault in", "I have years of
  files to bring over", "import my Notion export", "import my Evernote export",
  "bring my Google Drive folder in", "my old second brain", "continue the
  migration", "where were we with the migration", or an owner arriving with a
  hard drive, an export, or a folder tree they want to live in this vault. NOT
  for material that carries no links and no structure worth keeping and can be
  mapped and moved in one sitting (that is Capture's bulk move-in). NOT for
  building the vault (setup runs first and this skill will not scaffold). NOT
  for transactional rows exports, which never enter a vault at all (doctrine
  section 4, law 1). NOT for changing the law to fit the incoming material
  (breakthrough-vault-guardian).
---

# Breakthrough Vault Migrator

You are moving a house. Somebody has years of material somewhere else, a folder tree they built themselves, an export from another tool, or just a pile, and they want to live in this vault instead. ⛔ **This is not a copy job.** Putting a file in the right folder is the easy half; the half that decides whether the move worked is whether the documents still know about each other afterwards. A vault of correctly filed notes that have lost their links is a worse home than the mess it came from, because the mess at least had folders that meant something.

**The one sentence that governs everything below: the vault is legal and link-whole at the end of every batch, and the tracker is what lets any session pick this work up cold.** Nothing here has to finish today. What must be true is that whenever you stop, the vault is in a state the owner could live in, and a session that has never seen this material can read one file and know exactly where the work stands.

⭐ **This skill fixes a process, not a method.** The stages, the gates, the tracker, the freeze, the ledger and the link check are rails and they do not bend. What a given folder means, which family a given file is, how big a batch should be, whether two notes are related: those are yours to judge, in front of the actual material, and no table in this file will judge them better than you can. The section "What is rail and what is yours" says exactly where that line sits and why. ⛔ Do not add rails of your own invention, and ⛔ do not treat a judgment as a rail by looking for a rule that decides it for you.

## Where you are in the product

This skill ships inside the `my-second-brain` payload and is installed alongside it (setup step 6.6), so it updates when that skill updates.

**⛔ You carry no copy of this vault's structure.** Not the family table, not the folder shapes, not the naming regimes, not the iron laws. Every structural fact you use is read live, in the session, out of the owner's own `99_Meta/structure-doctrine.md`. This is the same discipline the frontmatter guard runs on (it reads the law live so it can never disagree with the weekly checker) and the same discipline the scaffold spec applies to the doctrine's version number, which is allowed to live on three lines and nowhere else. The reason is specific to this skill and it is worse here than anywhere: a migrator that remembers the shape of the house will, the day the law changes version, start moving somebody's life into rooms that no longer exist, and it will not error while it does it. If you find yourself about to write a structural fact into a proposal from memory, stop and go read the section it came from.

**Runs after setup, never before, and reads one book.** The destination has to exist before there is anything to talk about. On entry, find the vault and confirm `99_Meta/structure-doctrine.md` is there. If either is missing, say in one line that setup comes first, offer to run it, and stop. ⛔ **Never scaffold anything yourself**, and ⛔ never read the product's own `templates/structure-doctrine.template.md`: that copy still has its placeholders in it and it does not know about any amendment this owner has made to their own law. The installed book is the only book you read, which is also why the question of which book to read does not arise.

**Where this skill's boundary with Capture sits**, written the same way in both places: **"If the material carries links or a structure the owner wants kept, or it cannot be mapped and moved in one sitting, it is a migration and `breakthrough-vault-migrator` runs it; otherwise it is a bulk move-in and capture handles it tonight."** ⛔ That sentence is quoted in `modes/capture.md` Stage 3B word for word; an edit to one is an edit to both.

**What you never do.** You do not amend the law to fit the incoming material (that is `breakthrough-vault-guardian`, and a migration that turns out to need a new family has hit something to report rather than something to do). You do not delete anything, ever, including at the very end. You do not touch the owner's original files. You do not import transactional rows.

## Two topologies, and you name which one you are in before anything else

- **Staged copy.** The material lives outside the vault: another folder tree, an export, a drive, an old system's dump. This is the common case.
- **In place.** The material IS a working vault, the owner's own structure, and setup has already added what was missing beside it without disturbing it. Migration is the piece of work setup deferred: carrying their old structure into the law's structure, gradually. ⛔ Do not copy the vault to stage it. Copying it splits the wikilink ecosystem in two and every link you then rewrite is rewritten in the wrong half.

The two differ only in Stage 0. Everything after that is the same work.

## Stage 0: The handshake, then the freeze

**The handshake runs on every entry to this skill, including the first.** In order:

1. Locate the vault. If it is not obvious from where the session is standing, ask once.
2. Read `99_Meta/migration-progress.md`. **If it is there**, report where the work stands in the tracker's own words (which stage, what the last batch did, what is next), and resume at the first unticked `- [ ]`. ⛔ Only a `- [ ]` line is a step; everything else in that file is findings, not a checklist.
3. **If it is not there**, ask the one question that decides the next move: is this the first run, or has this work been going on somewhere else and the tracker is elsewhere? If there is a tracker elsewhere, read it and propose adopting it into `99_Meta/`, keeping what it says.
4. If the vault or the law is missing, setup first, and stop.

**Then the freeze, and say plainly why it exists.** The material is going to keep growing while this work runs, and a boundary that moves is a migration that never finishes: the survey goes stale, the batches stop adding up, and nobody can say what "done" would mean. So the boundary gets fixed today, once.

- **Staged copy:** the owner **copies** what they want migrated into one staging folder and stops adding to it from that moment. Anything new from today goes into the vault the normal way (`00_Inbox/` or a capture sitting), ⛔ never into staging. Staging lives **outside the vault**: put it beside the vault (`<vault-name>-migration-staging/` as a sibling is a good default, their path if they prefer). ⛔ Not inside the vault, where Obsidian would index a half-built pile, the checker and the dashboard would see a room full of illegal notes, and sync would carry the weight twice.
- **In place:** the boundary is a list rather than a copy. On the cut date, record the top level folders of their old structure as `legacy_roots:`. Those folders are a read-only waiting area from today; new material goes to the law's structure, which setup already wired the vault to do on its own.

**Take a census when you freeze**, and record it: how many files, and a hash of the sorted list of their names. ⛔ **Not modification times.** Timestamps in a pile that has been copied, synced and restored are not evidence of anything.

**When the freeze gets broken, and it will.** On every later entry, compare staging (or `legacy_roots`) against the census. If it grew, name it in one sentence, without reproach, propose moving the new arrivals into `00_Inbox/` to be filed the normal way, retake the census, and write one line under `## Freeze incidents`. ⛔ Do not re-plan the migration over it and do not lecture. A broken freeze is ordinary human behaviour and the handling has to be cheap enough that nobody hides it from you next time.

## Stage 1: Survey, in three layers, and you pay for the third one by the batch

⭐ **Read the whole corpus for shape. Read content only for the batch you are actually moving.** This is a rail, and it has three separate bills behind it: tokens, session length, and the owner's privacy.

1. **Shape.** The folder tree, file counts, extension distribution, obvious clusters. This buys the map, the first batch proposal, and the shortlist of things that look like database material.
2. **Names, plus a sample.** Filenames across the whole corpus, a few files opened per cluster, and a **link census**: how often `[[...]]`, `](...)`, `file://` and any foreign URI scheme (`evernote:///` and its kind) actually appear, and where. This buys a real destination judgment per cluster instead of a guess, and it tells you what kind of link problem you are about to have.
3. **Full content.** Only for the current batch, only after the owner has ruled on it.

**Say the privacy line out loud, once, at the start:** across the whole pile you look at shape and filenames; the contents of a file get read when it is in a batch they approved.

Report the survey as a map, not as an inventory. The owner does not need a list of their own files; they need to know how many distinct kinds of thing are in there, which ones the vault has an obvious home for, and which ones are going to need a decision from them.

## Stage 2: Mapping, ruled by the owner

Produce **one mapping table** covering the corpus at the grain of groups rather than files: item or group, destination, the rule that sent it there (which step of the law's filing decision tree, or which row of its precedent table), and the link type involved. An item no rule covers gets an honest "needs a precedent" row and a question, ⛔ never a silent guess.

**Then the owner rules, with the same grammar Capture and the tidy report already use: file all, file by group, or walk item by item.** ⛔ **Nothing moves before the ruling.** Write the ruled mapping into the tracker; it is the input to every batch that follows and the reason the next session does not have to re-derive it.

**Two things come out of Stage 2 besides the mapping.**

- **The referrals** (see below): the groups that are not going into the vault at all.
- **The batch plan**: how the approved material is cut into sittings. Propose it, do not compute it. A batch is usually one source folder or one subject cluster, sized to what a sitting can finish.

## Stage 3: The batch loop

Each batch: propose, get the ruling, move, rewrite links, verify, record. Then stop cleanly, whether or not there is time for another.

**The link work is the batch, not a step at the end of it.** Handle each kind for what it is:

| What you find | What you do |
|---|---|
| `[[wikilinks]]` | Moving or renaming a linked file means rewriting its inbound links in the same breath. That is not a rule this skill invented; it is the law's anchoring section, and you are executing it. A name that collides under the unique-name regime gets renamed per the naming section, and the rename rewrites the inbound links too. |
| Relative markdown links (`](./x.md)`) | They break on the move. Convert them to wikilinks as the file lands: wikilinks are this house's native tongue and the backlink mechanism the law depends on runs on them. Record the conversion. |
| Absolute paths and `file://` | Pointing outside the corpus: leave it, it still resolves. Pointing at something already migrated: rewrite it. |
| Foreign syntax (export UUID filenames, `%20` escapes, `evernote:///` and friends) | Cleaning the filename rewrites the links that pointed at it. A URI nothing can resolve is ⛔ never silently dropped: it goes in the ledger as unresolvable and the whole set gets shown to the owner once. |
| No links at all | The relationships exist, they were just never written down. Infer them and express them in this house's own vocabulary: same room or same project (the path is the relationship), a wikilink in the body, a key the law already declares. ⛔ **Never invent a frontmatter key the law has not declared.** Material that genuinely needs one is a finding for `breakthrough-vault-guardian`, not something you add on the way past. |

**Five things must be true before a batch is over. All five, every time.**

1. Every note that landed has frontmatter its family accepts.
2. Every folder that was created is written into `Home.md` in the same breath.
3. One line per filing in `99_Meta/filing-log.md`.
4. **Zero dead links inside everything migrated so far**, or every remaining one named in the ledger with its reason.
5. The tracker's batch line is updated.

⛔ **There is no legal half-moved state.** A group either lands completely or stays in staging completely. A batch that runs out of time stops at a group boundary.

**On the link check, do it yourself.** ⚠️ The weekly checker has no dead-link check, and the weekly maintenance pass looks for notes nothing links TO, which is a different question from links that point at nothing. The law says a move rewrites its inbound links and that weekly maintenance re-checks as a backstop; that backstop is a human pass, so **the mechanical check at the end of each batch is this skill's own work and it is not delegated.** Extract every `[[...]]` and `](...)` target from what landed, resolve them against the vault, and fix or ledger every miss. At close, run it once over everything migrated. Pointing the owner at Obsidian's own unresolved-links panel afterwards is a courtesy, not the check.

**Write notes with the Write tool, never through the shell.** The frontmatter guard can read a Write and cannot read a heredoc, and the guard is what tells you on the spot whether a note is landing legally.

**In place migrations: the weekly report will name the old folders, and that is correct.** Until a legacy root is emptied it is genuinely outside the law, and the checker saying so every week is true. ⛔ Do not ask for an exemption and ⛔ do not teach the checker about this migration. Tell the owner once that the list shrinking week by week is their progress bar.

## The referral: material that should not be in a second brain at all

Some of what the owner hands over is not notes. High frequency rows of the same shape (invoices, purchase orders, POS dumps, attendance, transaction exports), append-only streams (chat exports, activity logs), a folder of four hundred files with the same structure: **this material never enters a vault**, and that is an iron law that predates this skill, not a preference of yours.

Recognising it is your judgment; what happens next is not:

1. **Say it plainly.** This belongs in a system built for rows, not in a second brain. Then read that iron law in the owner's own copy of the doctrine before you describe what the vault keeps instead, and describe what it actually says there. ⛔ Do not paraphrase it from here: the substitute the law prescribes is exactly the kind of specific this skill is forbidden to remember.
2. ⛔ **Consolidating that data into a database is out of scope for this skill.** Say so in one sentence and do not start it, do not design it, and do not propose a schema. The owner may well want that work; it is a different job.
3. **Record it** as a ledger row with the disposition `referred-out` and the law's section cited. ⭐ That row is what stops a session six months from now from cheerfully offering to import it.

## Stage 4: Close

1. **Walk the ledger with the owner**, and give the same weight to what was deliberately not moved as to what was. The `referred-out` and `left-behind` rows are the ones they will otherwise wonder about in a year.
2. **Declare which copy is canonical**, in writing, in the tracker: from the cut date, the vault's copy is the only working original; staging and the originals are archives.
3. **Full link sweep** across everything migrated.
4. **Staging is the owner's to dispose of.** Ask what they want to do with it and do what they say. ⛔ You never delete it, and you carry no recommendation on how long to keep it.
5. Set `migration_complete: true`. The tracker stays where it is, permanently readable, exactly like the setup progress file it is modelled on.
6. **Hand over to the ordinary rhythm**: new material now goes in through Capture and the weekly ritual, and the migration is over.

## The tracker

One file, `99_Meta/migration-progress.md`. You are its only writer.

⛔ **It carries no `type:` key, and that is the rule rather than an omission.** A file with `type:` is a document a person reads and the record schema governs; a file without one is state, a machine's notepad. The vault's other progress and state files work exactly this way and the checker skips them on purpose. The frontmatter guard may note the shape as it lands: that nudge is expected, and this paragraph is the answer to it. ⛔ Do not silence it by inventing a `type:`, which turns an expected nudge into a hard block, and ⛔ do not ask the guardian to amend the law for it.

```markdown
---
started: <date>
topology: staged-copy | in-place
source_paths: [<where the originals live, one per line>]
staging_path: <absolute path; empty when in-place>
cut_date: <date>
staging_census: {files: N, names_hash: <hash of the sorted filename list>, taken: <date>}
legacy_roots: []            # in-place only: the old structure's top level folders
batches_done: 0
migration_complete: false
---

# Migration Progress

- [ ] Stage 0 · freeze (staging + census + cut line)
- [ ] Stage 1 · survey (shape read, link census)
- [ ] Stage 2 · mapping ruled by the owner
- [ ] Stage 3 · batches (one `- [ ]` line appended per ruled batch)
- [ ] Stage 4 · close (ledger review, canonical declared, staging disposal ruled)

## Ledger
| Item / group | Disposition | Destination | Rule cited | Links | Date |
|---|---|---|---|---|---|

## Freeze incidents

## Notes
```

**Disposition is one of four values**: `migrated`, `referred-out`, `left-behind`, `pending`. ⭐ `referred-out` and `left-behind` must carry a reason. Those two columns are the whole reason this ledger exists: they are what a later session reads instead of re-arguing a call the owner already made.

## What is rail and what is yours

**Rails. These hold whatever the material turns out to look like.** The stage order. The tracker: that it exists, where it lives, its shape, and the resume handshake. The freeze and its census. The mapping table's grammar and the owner's three-way ruling, with nothing moving before it. The five batch-end invariants. The link check at every batch end and at close. The four ledger dispositions with reasons on two of them. Reading the law live and carrying no copy of it. Referring rows material out. Shape for the whole corpus, content only for the current batch. Write tool for notes, never the shell.

**Yours to judge. These cannot be answered without looking at the actual material.** What a folder means and which family a file is. How to cut the batches and how big one should be. What relationship two files have when nothing says so explicitly. Whether a given pile is database material. How much to sample and how to word a proposal.

⭐ **The test, when something is not obviously on one side:** would this still be true of a completely different pile? If yes it is a rail. If it only makes sense while looking at this particular material, it is judgment, and writing it down as a rule makes the skill brittle without making it smarter.

## Settled, and not to be reopened

- ⛔ **Setup first, always.** This skill never scaffolds and never reads the product's doctrine template. One book: the installed one.
- ⛔ **Originals are never touched.** Staged items move within staging into a `_migrated/` mirror as they land, so staging visibly empties without anything being destroyed.
- ⛔ **Nothing is deleted by this skill, at any stage, including close.**
- ⛔ **Link verification is this skill's own work.** The weekly checker does not check links; do not delegate to it and do not extend it.
- ⛔ **Database consolidation is out of scope.** Recognise, refer, record, stop.
- ⛔ **The law is never amended to fit incoming material.** That is the guardian's work, and needing it is a finding to report, not a step to take.
- ⛔ **The weekly report naming legacy folders is correct behaviour.** No exemptions, no teaching the checker about migrations.
- ⭐ **One skill, staged, resumable.** Diagnosis is a stage of this work and not a separate tool: the mapping is an input to the move, and splitting them would put the tracker's writer and its reader on opposite sides of a handover.
