<p align="center">
  <img src="assets/hero.jpg" alt="My Second Brain: one vault, two wings, operated in plain conversation" width="100%">
</p>

# My Second Brain

**The one asset that stays yours no matter which AI model ships next quarter.**

A Claude Code skill that builds and runs a complete second brain for a business owner: one vault, two wings (your life in PARA, your business in a three-layer knowledge map), operated in plain conversation, with Obsidian as the viewing deck.

And it does the two things note systems never do: it **grows its own memory** (every AI conversation becomes searchable history, and a weekly harvest proposes what is worth keeping; nothing is saved until you approve it), and it **keeps machines on guard** (a read-only inspector that sweeps the vault, plus a safety lock that blocks the one delete you cannot undo). The rules are not just written down; they are enforced.

## Install

```bash
npx skills add breakthrough-edu/my-second-brain
```

Then open Claude Code and say:

> set up my second brain

Ten minutes later you are looking at the graph view of your half-built brain.

Already running it? Updating to the latest version is one line, and it never touches your vault, only the skill files:

```bash
npx skills update my-second-brain
```

One thing the update command cannot do: the two machine guards (the safety lock and session memory) are offered during Setup, so a vault built before they shipped will not have them yet. Say **"add the safety lock"** or **"set up session memory"** in any session and the skill retrofits the one you asked for onto your existing vault.

## The idea underneath

AI execution is cheap now. What is scarce is your data having a home.

When your business lives in one structured vault, any AI can give you real answers about your own operation. When it lives in chat threads, receipts, and one employee's head, no model, however smart, can help you.

So this skill does not try to be the smartest assistant. It builds the thing underneath the assistant: a knowledge base in plain markdown files, structured by written law, owned by you. Models keep changing; your knowledge base stays yours. Your judgment and your operation are never locked into any single AI vendor, because the data layer is just files on your disk.

## Where most second brains fail

The idea only works if the vault survives contact with daily life, and this is where most second brains lose. They keep dying the same few deaths; every opinionated choice in this system exists to dodge one of them. If you have built one before, at least one of these will feel familiar:

| The usual death | What this system does instead |
|---|---|
| **Collect, never settle.** Capture keeps adding until the vault is a junk drawer nobody trusts. | A weekly distill ritual with teeth: a read-only inspector script scans first, then proposals, you rule. See the loop section below. |
| **One sorting logic for everything.** Life and business forced into one tree, so filing turns into guesswork. | Two wings, two axes: PARA for your life, knowledge type for your business. |
| **Rules live in nobody's head.** Filing by mood; consistency dies the day you switch tools or models. | A written constitution inside the vault, plus a filing log, and the inspector checks the vault against it every week. The rules outlive the model. |
| **The AI writes your "insights".** Auto-generated methodology reads smart and belongs to no one. | Layer 3 accepts only what you reviewed and approved, and only your approval can mark anything as reviewed. AI proposes, you rule. |
| **The vault becomes a shadow ERP.** Invoices and receipts flood in until maintenance collapses under the volume. | The rows iron law: high-frequency data stays in the systems built for it; the vault keeps pointers and exceptions. |

## What you get: four modes

<p align="center">
  <img src="assets/modes.svg" alt="Four modes, one conversation: Setup once, Capture room by room, Distill weekly, Create-My-Jarvis once at home" width="100%">
</p>

**Setup** (10 min). Installs Obsidian if needed, builds a fully wired vault (every room has a front desk, navigation live from day zero), asks 3 questions about your industry, offers an optional calendar connection so your morning brief sees the day's schedule, and generates a **personal command-base skill named after your business**. You install one skill; it builds you another one that only fits you.

**Capture** (15 min per room). Your Business Profile first, then one room at a time: clients, products, SOPs, whichever you pick. One question at a time, talking is fine, and there is a bulk lane when you already have material. Every session ends with one observation about your business you had not noticed, plus two good questions.

**Distill** (10 min weekly). The AI tidies the vault (orphans, misfiles, stale maps), then proposes distillations: decision patterns, lessons, rollups. You only rule yes or no. The third layer of your business map fills from your judgment, never from raw capture.

**Create-My-Jarvis** (45 to 60 min, at home). Two interviews, one about you and one about the character, that give your AI a real persona and a real understanding of who you are, so it stops sounding like a vending machine.

## The structure it builds

<p align="center">
  <img src="assets/structure.svg" alt="One vault, two wings: your life in PARA on the left, your business in three layers on the right, a shared spine in the middle, one constitution underneath" width="100%">
</p>

```
Your-Vault/
├── 00_Inbox · 01_Daily            shared capture + timeline
├── 02-05  Projects/Areas/Resources/Archive     your life (PARA)
├── 06_Command-Base/               command center: Home, Decisions, Tasks, dashboard
├── 07_<Your-Business>/            your business, three layers:
│   ├── 01_Assets                  what it is made of (clients, products, docs, people)
│   ├── 02_SOP                     how things get done (named by intent, not department)
│   └── 03_Methodology             why you decide the way you do (fills from judgment)
└── 99_Meta/                       the constitution, templates, state
```

Two sorting axes, deliberately different. Your life is sorted by **actionability** (PARA). Your business is sorted by **knowledge type**: what it is made of, how things get done, why you decide the way you do. Mixing those two logics in one tree is how most vaults die; keeping them in separate wings is the core structural bet of this system.

## Day to day: living with it

After Setup, your daily driver is the command-base skill it generated for you. A normal day looks like this:

| You say | What happens |
|---|---|
| "morning" | A brief: today's schedule (if a calendar is connected), tasks due, red flags, who you are waiting on, business renewals coming up |
| "client X finally signed, closed at RM 4,500" | Captured on the spot, buffered durably, compiled into your daily note at end of day |
| "we decided to drop the entry-level package" | A structured decision record, filed in the central Decisions room with domain and reasoning |
| "follow up with the printer on Friday" | A waiting-for task that will resurface on its own |
| "how do we onboard a new hire again?" | Answered FROM your own SOP note, and if the answer reveals the SOP is stale, it gets updated in the same move |
| "how did we fix this last time?" | Answered from your searchable session history, if session memory is installed, instead of re-deriving a solved problem |
| "compile" (end of day) | The day's captures become a dated daily note, business items append to the business log |
| "distill" (weekly, 10 min) | Vault hygiene scan, then distillation proposals for your methodology layer. You rule yes or no |

The handbook stays alive because answering and updating are the same motion. The vault stays trustworthy because every filing decision follows written law.

## The loop that keeps it alive

Most second brains die the same death: capture keeps adding, nothing ever settles, and three months in, the vault is a junk drawer the owner no longer trusts. The weekly Distill ritual is this system's answer, and it is where the compounding happens.

<p align="center">
  <img src="assets/loop.svg" alt="The weekly loop: capture, tidy scan, propose, you rule, layer 3 grows, and your AI's answers get sharper week after week" width="100%">
</p>

Say "distill" once a week and four things happen, in order:

1. **Tidy scan.** Seven hygiene checks across the vault: orphan notes, misfiled items, stale maps, and the rest. The AI reports; files move only after you approve.
2. **Distillation proposals.** The AI reads the week's decisions, session logs, and daily notes (and, when session memory is installed, your unreviewed AI conversations), then proposes what they add up to: a decision pattern, a lesson, a rollup.
3. **You rule.** Yes or no on each proposal. Nothing writes itself into your methodology layer, ever.
4. **Layer 3 grows.** Approved distillations land in Methodology as your own reviewed judgment. The same scan also watches for functions that have earned a pod, or pods that have gone quiet.

This is the part most tools skip, because it cannot be automated away: the loop only compounds if a human keeps ruling. Ten minutes a week is the whole price. In exchange, the answers your AI gives you stop being generic, because they are grounded in what you actually decided, reviewed, and signed off on.

**A machine does the hygiene half.** The mechanical checks in step 1 (stray folders outside the numbered structure, missing control files, off-vocabulary tags, records with holes in their frontmatter, maintenance that has gone stale) are run by the inspector, a small read-only script, before the human scan starts. Distill runs it for you, and it reports in seconds, grouped by severity. It is strictly report-only: it never moves, renames, or deletes a single file. It finds; you rule. That is the same contract as the rest of the loop, just enforced by a script instead of your attention, so your ten minutes go to the judgment calls a machine cannot make.

## It grows its own memory

Most AI setups have amnesia: every conversation starts from zero, and the fix you found in April gets re-derived in July. **Session memory** (optional, offered at setup, macOS first) closes that gap:

<p align="center">
  <img src="assets/memory.svg" alt="The memory loop: sessions are the negatives, a weekly harvest develops them, you tick what to keep, approved items become memory" width="100%">
</p>

- **Every conversation becomes searchable.** A small local tool indexes Claude Code's own transcripts into a full-text search database, so "how did we solve that before?" gets answered from history. It reads only the transcripts, read-only; it writes only its own database in `~/.my-second-brain/`; it is purely local, with no network code and no background process.
- **A weekly harvest proposes memories.** During Distill, the AI reads the conversations you have not reviewed yet and brings back a short report: things worth remembering, decisions worth logging, ideas worth a note, each with a pointer to the conversation it came from. Nothing is saved until you tick it, and only your approval marks those conversations as reviewed, so a report you ignore costs nothing and nothing is ever silently skipped.

<p align="center">
  <img src="assets/harvest-report.svg" alt="A sample harvest report with fake data: three candidates with checkboxes and session pointers, nothing saved until you tick it" width="100%">
</p>

Same law as everywhere else in this system, now with your own past conversations as one of the inlets: the AI proposes, you rule. That is what "grows its own memory" means here, and it is the part a notes app cannot copy, because the raw material is your working history with the AI itself.

## Machines stand guard

Written rules die without enforcement, so the rules that matter most are backed by machinery, all of it shipped in this skill:

<p align="center">
  <img src="assets/guards.svg" alt="The three guards: the inspector finds, the safety lock blocks, the review bookmark proposes; every arrow reports to one desk, only you rule" width="100%">
</p>

- **The inspector** (`scripts/checkup.py`): a read-only hygiene sweep over the whole vault, run before every weekly tidy.
- **The safety lock** (optional setup step, macOS only): a hook that blocks recursive deletes aimed at your vault or your skills folder, the one category of accident there is no undo for.
- **The review bookmark** in session memory: only human approval can mark a conversation as reviewed, so the memory loop cannot quietly run away from you.

One contract across all three: machines find, block, and propose. Only you rule.

## Create-My-Jarvis: your AI gets a character

Out of the box, every AI assistant is the same person: helpful, generic, nobody's. The fourth mode is where that ends, and it is the part owners remember.

Two interviews, done at home in a quiet hour:

- **The profile interview** (ten questions) writes down who you actually are: how you really make hard decisions (the pattern, not the aspiration), what kind of criticism lands with you, what money does for you. Answers are transcribed near verbatim. Thin answers make a thin profile, and the skill says so instead of inventing personality to fill the gaps.
- **The soul interview** (eight beats) has you author a character: its name and why the name matters, what it should do first when you ship something hard, what it should do first when you are stuck, what it must never do, and at least three voice rules concrete enough to test a single sentence against.

A hard **genericness gate** protects the result. "Be clear and concise" fails the gate. "Never open with 'Great question'. If I write in Chinese, answer in Chinese. Tell me the risk before the plan." passes. When an answer lands generic, the interview pushes for the specific version, because a generic soul produces the same AI you already had.

What this buys you day to day:

- Your morning greeting sounds like the character, and its name surfacing is your proof the soul loaded.
- It holds your real situation in mind during routine work: the actual business, the actual stakes, in your own words.
- It deliberately watches the angles you told it you reliably miss, instead of mirroring you.
- The soul is a markdown file in your vault. Lived use will reshape it in the first weeks; you edit the file and the character follows.

## Design decisions

The choices that make this hold up over months, not weeks:

**The constitution lives in your vault, not in the skill.** Setup writes the full structural law (sorting axes, filing test sentences, iron laws, a rulings table for the genuinely ambiguous calls) to `99_Meta/structure-doctrine.md` inside your vault. Every filing decision reads it first and logs one line to `99_Meta/filing-log.md`. Swap the model, update the skill, the rules do not drift.

**The methodology layer cannot be filled by capture.** Layer 3 starts empty on purpose. Only reviewed judgment fills it: the AI proposes, you rule. A second brain that auto-generates your "methodology" is generating someone else's.

**Insights are observations, never verdicts.** Every capture session ends with one thing you had not noticed plus two good questions. The skill will not promise analytics your data cannot support yet, and it says so.

**Nothing nags.** Overdue maintenance, an uncompiled yesterday, the Jarvis offer: each is raised exactly once, then dropped. A tool that nags gets abandoned in three months, and this system is built for years.

**A crashed session loses nothing.** Every capture lands in a durable buffer file the moment it arrives. If the session dies before you compile, the next morning brief offers to backfill yesterday's note from the buffer.

**High-frequency rows never enter the vault.** Invoices, POs, attendance, receipts stay in the systems built for them; the vault stores pointers, exceptions, and monthly snapshots. This is a knowledge base, not a shadow ERP.

**Bilingual by craft, not by translation.** Interaction is English or 中文, your choice at setup. Chinese output follows native-writing discipline (no translated sentence structures), while folder names and frontmatter stay English so the structure is portable.

## Function pods: when a function earns its own brain

Most business functions stay simple: a room for their materials and a log. But some functions are pure repeated judgment (marketing, pricing, what to say no to), and those deserve to *learn*. When one has built up enough real track record, the companion `pod-maker` skill (installed at setup, symlinked so it updates with this skill) can **graduate** it into a pod.

A pod is not a whole separate business-in-a-box. Honestly sized, a pod **owns two layers** (its own outputs, and its own learning loop of doctrine and rubric that grows from your decisions) and **reads a third** (it shares the business wing's SOP and reference material, never duplicating them). The wing stays the full three-layer map; a pod is one function's local brain bolted onto it.

<p align="center">
  <img src="assets/pods.svg" alt="A function pod owns its outputs and its learning loop, and reads the wing's SOP and reference material without duplicating them" width="100%">
</p>

Two guardrails keep this from bloating your vault: the graduation gate treats "not a pod" as the default answer (a process with a known right answer wants an SOP, not a learning loop), and the weekly maintenance scan proposes shrinking a pod back if it goes quiet (your learning is archived, never lost). One core pod ships ready to seed: **Marketing**, a generic marketing brain your own loop grows into something specific to your business.

## Honest boundaries

- Single-owner system: you plus your AI. Obsidian has no permission layers; if staff need a piece, export that piece.
- Not an ERP, not a CRM, not a multi-user wiki. Structured high-frequency data stays in the systems built for it.
- Early insights are observations, and the skill says so honestly. Depth comes from months of captured judgment, not from week one.
- The two machine guards are platform-gated for now: the safety lock is macOS only, session memory is macOS first. The vault, the four modes, and the inspector work everywhere. Windows owners who want session memory have a documented, self-driven route (see [Windows self-serve path](#windows-self-serve-path)); the safety lock is not ported, so there is no machine-level block on accidental deletes on Windows.

## Requirements

- [Claude Code](https://claude.com/claude-code)
- [Obsidian](https://obsidian.md) (free; the skill can install it for you). Enable the **Bases** core plugin for the dashboard.
- Python 3, for the inspector and session memory. macOS ships everything they need; on Windows use Python from python.org (not Anaconda, whose SQLite lacks the FTS5 extension session memory needs).
- Works on macOS, Windows, Linux. The optional machine guards are macOS-gated for now (safety lock macOS only, session memory macOS first); see Honest boundaries and the [Windows self-serve path](#windows-self-serve-path) below.
- English or 中文 interaction; your choice at setup.

## Windows self-serve path

The vault, the Obsidian layer, the four modes, and the inspector all work on Windows as-is. Two machine-layer pieces have platform boundaries, and this is how a Windows owner gets what is portable and knows what is not.

**Session memory works on native Windows**, as long as your Python ships SQLite with the FTS5 extension. Run Claude Code on native Windows (the PowerShell or CMD installer). WSL works too, but if your vault lives on the Windows drive (reached from WSL as `/mnt/c/...`), file operations and search run 5 to 20 times slower, so native is the recommended path.

1. Install Python from [python.org](https://www.python.org/) (not Anaconda). This is the one that ships SQLite with FTS5, which session memory needs. The Microsoft Store build also works.
2. Install Claude Code for native Windows, then install this skill.
3. Your vault path, Claude Code's session location, and project slugs are all derived automatically, so there are no manual path edits.
4. Run the session-memory tool with the interpreter named explicitly (use `python`, not `python3`, on Windows; the tool's shebang is inert here):
   ```
   python "<skill>/scripts/session-history/sh" ingest
   ```
5. On first run the tool probes for FTS5. If it reports FTS5 missing, you are almost certainly on Anaconda; switch to python.org Python and run it again.
6. The inspector (`checkup.py`) runs the same way and needs nothing special.

**What you do NOT get on Windows: the safety lock.** It is macOS-first and is not ported, so there is no machine-level block on accidental recursive deletes of your vault or skills folder. Lean on your own backups instead.

This path is best-effort and community-validated rather than officially tested on Windows: it is built on macOS and we have no Windows machine to verify against, which is why the FTS5 probe hands you a clear pass or fail rather than the skill claiming "works on Windows." If something breaks, tell us; it feeds the next iteration.

## Repo layout

The skill payload lives in [`my-second-brain/`](my-second-brain/) (the nesting is what the `npx skills` installer ships as a unit: modes, templates, references, and the bundled `pod-maker` skill). `deck/` holds presentation material about the system.

## License

MIT. Built and maintained by [Breakthrough EDU](https://github.com/breakthrough-edu).
