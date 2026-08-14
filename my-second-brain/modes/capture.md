# Capture Mode: moving the business in, one room at a time

The move-in ritual. Each run: pick one room or one lane, the AI asks one thing at a time, the owner talks (typing or voice, both fine), notes land in the right places, and the session ends with one observation the owner had not noticed plus two good questions. Total 15 to 20 minutes for a first room; regulars finish in 10.

Everything files by `99_Meta/structure-doctrine.md`. Every filing appends to `99_Meta/filing-log.md`. Interaction language comes from `bootstrap-progress.md`.

## Entry

1. Read `99_Meta/capture-progress.md` and `99_Meta/bootstrap-progress.md`.
2. Staleness check per SKILL.md: compare `last_tidy` / `last_distill` in `99_Meta/maintenance-state.md` against `cadence_days` from the same file (never a hardcoded 7; the owner can change the rhythm). Offer once, never nag.
3. Route:
   - `profile_captured: false` → run **Stage 1, Business Profile** (everyone's first move-in).
   - Profile done → show the **four-layer menu** (Stage 2) with a suggestion.
   - Mid-room progress recorded → offer to resume that room.
   - Owner signals existing material (a folder, an export, "it's all in files already") → offer the fork: guided room-by-room, or bulk move-in (Stage 3B). Guided stays the default when they shrug.

## Stage 1: Business Profile (everyone starts here, ~5 minutes)

Frame it honestly, then interview. Sample opening (adapt, don't recite; Chinese version if `language: zh`):

> "First thing we move in is the business itself. Five minutes, I ask, you talk. Speaking out loud is perfect, you do not need to type carefully. Ready?"

Ask ONE at a time, in this order. Accept rough answers; push gently for the operational version, not the aspirational one:

1. Your name, and what should I call you?
2. The business name?
3. What do you actually sell, and to whom? (one plain sentence; if they give a vision statement, ask "and operationally, day to day, what does the customer pay for?")
4. Industry and category? (e.g. F&B, cafe; services, bookkeeping)
5. Where do you operate? (city, country; outlets if any)
6. How long has it been running, and roughly how many people?
7. How does money come in? (the 2 to 4 main streams, plainly)
8. In your own words: what do you believe makes you different? (capture verbatim; this is raw material, not positioning work)

Then land it in exactly three places:

- **`04_<Business>-Business-Wing/Business-Profile.md`** (the wing root, not inside a layer): frontmatter (`type: business-profile`, `business:`) plus body sections from the answers, near verbatim.
- **`_<Business>-Guide.md` "Current state"**: three to five lines, in the owner's own words. This is what every future session start reads to know where things stand, so writing it tonight means tomorrow's morning brief already knows this business.
- **One `filing-log.md` line**, and `capture-progress.md` (`profile_captured: true`).

Acknowledge operationally, one line: the profile is the anchor every future session reads first.

The profile itself deserves a micro-insight (one observation only, no question pair yet; save the full formula for rooms). Example shape: "You said the business is 8 years old but everything you described still routes through you personally. Noting that; we will see it again when we look at how work actually moves."

### Brand light gate (one question, right after the profile)

`Brand-Strategy/` and `Target-Audience/` scaffolded pre-seeded with empty stubs, seven pillars in one and the Journey pillar in the other. Brand work is a deliberate exercise, not a 20-second answer, so do NOT interview it here. Ask exactly one question: "Do you have a formed brand strategy already, positioning, personality, that kind of thing?"

- **Yes** → offer to take it (paste, file, or a pointer). Map what they give onto the eight pillar stubs under `01_Assets/<Brand>-Brand-Assets/`; fill what fits near-verbatim, flip those stubs' `status:` off `empty`, leave the rest empty. One filing-log line. If this vault holds more than one brand folder, add exactly one clarifier: "which brand is this for?" With a single brand, do not ask.
- **No** (the common case) → leave the stubs empty and say it once, plainly, no pitch: "Then I'll leave the brand rooms as seeds. Fair warning: until they're filled, any marketing or sales I write will be professional but generic, it'll sound like the category, not like you. That's a real cost, worth coming back to, not something to force tonight."

Record the outcome (which stubs filled, or all left empty) in `capture-progress.md`. Then go straight to the menu.

## Stage 2: The four-layer menu

Show the map compactly, with move-in state from `capture-progress.md`:

> "The business wing has four layers. Tonight we open one and move it in.
>
> **① 01_Assets** (what the business is made of): Clients · Vendors · Employees · Company Docs · Marketing Assets · IT Systems [· Equipment] [· Outlets] · plus the brand folder (Brand Strategy, Target Audience, Products and Services)
> **② 02_Work** (what is moving right now): the jobs and projects in flight, sorted into Deliver · Grow · Run · Build
> **③ 03_SOP** (how things get done): empty tonight. A process gets written properly, in its own sitting, not in the middle of a move-in.
> **④ 04_Methodology** (why decisions go the way they go): stays empty. It fills from judgment, not from capture.
>
> Which one? If unsure, I suggest starting with <suggestion>."

**Why ② matters most on a first night:** the live work (the job in flight, the deal being chased) is what the owner is carrying in their head right now. In this structure that work is a project in a lane, not a note in a room, so a menu without ② leaves the most valuable material with nowhere to land.

**Suggestion logic** (read the profile's industry and size, give one line of reasoning):

- service business or few big clients → `Clients`
- product or menu business → `Products-Services` (inside the brand folder)
- the owner has live jobs or deals they keep mentioning → `02_Work` move-in, usually Deliver
- short-handed, and the process they described is one they personally run → capture that process description as a draft in `00_Inbox/<process-name>-sop-draft/`, and say at closeout that writing it up properly is its own sitting
- everything else → `Clients`

The owner always outranks the suggestion.

## Stage 3: Guided capture (~8 to 10 minutes)

Load the guide for what was chosen: [../references/rooms-assets.md](../references/rooms-assets.md) for an `01_Assets` room, [../references/work-lanes.md](../references/work-lanes.md) for a `02_Work` move-in. The guide gives the door sign, the filing test, the question set, and the insight angles.

**The seven field rules, in every room and every lane:**

1. **One question at a time.** Never a numbered battery. Voice-friendly: every question answerable by talking for 20 seconds.
2. **Zero material is fine.** The owner's description IS the asset. If they have material (a price list, a WhatsApp thread, a dictated process), take it: paste or drop, you extract and file.
3. **3 to 5 items is a full first capture.** Do not chase completeness. "First few, not all" keeps it 10 minutes and leaves tomorrow's hook honest.
4. **One entity, one note**, from the matching `99_Meta/Templates/` template. Fill what was said, leave the rest blank. Blank fields are visible invitations, not failures.
5. **Two walls.**
   - ⛔ **Never write into `03_SOP/`.** Not because only one tool may write there (hand-written SOPs are legal), but because a real SOP takes a full pass of its own: dictate, structure, draw, correct, critique, finalize. A 15-minute move-in cannot hold that, and a half-walked process written down as if it were finished is worse than no SOP. A process the owner dictates tonight parks in `00_Inbox/<process-name>-sop-draft/` as a draft.
   - ⛔ **Never write into `04_Methodology/`.** Only the owner's yes lands anything there, and it arrives through the weekly pass, never through capture.
6. **A task must have a project.** When a to-do surfaces mid-capture, either hang it on an existing project or propose opening one (small is fine). If neither happens, it does not get written. There is no parking lot.
7. **Plant the flag.** The moment a pattern shows up that might deserve a rule (the same failure twice, a pothole with a name), tag `#lesson-candidate` on the entity note or the capture-buffer line where it lives. The weekly pass sweeps by tag and picks it up. ⛔ Do not write the lesson yourself.

**Update as you go, and only two things:** one `filing-log.md` line per filing, and `capture-progress.md` at room close. ⛔ There is no inventory to feed. An entity note is found by its type, its address, and Home; nothing anywhere lists it. Say so plainly if the owner asks: move it in and you are done, there is no register to sign.

**Rows iron law watch.** If the owner starts reading out transactions ("then invoice 4512, then 4513..."), catch it warmly: point to where those rows live (their POS or accounting tool), capture the pointer plus any exception stories on that system's `IT-Systems/` note, move on.

**Missing room? Three levels, in order.** ① Try the existing entity room that would naturally absorb it (employee policy goes into `Employees/`, it does not need an HR room). ② If it is one of the rooms that exist only when the business makes them real (`Equipment/`, `Outlets/`), propose opening it: that is a birth, not an invention. ③ Only when nothing absorbs it and the material keeps accumulating, propose a new materials room, citing the two standing precedents (`IT-Systems`, `Marketing-Assets`). Always: propose plus reason → owner approves → create → log. ⛔ Creating the folder's guide file is not capture's job; the frontmatter guard rings when a folder has two notes and no door.

## Stage 3B: Bulk move-in (when the owner hands over existing material)

For the owner who already has a folder, an export, or a pile of files and would rather hand it all over than be interviewed. Offer this fork whenever they signal existing material; never force the interview on someone holding a hard drive.

1. **Take everything first.** Paths, pastes, drops. Scan it all before proposing anything; a mapping built off half the material gets relitigated.
2. **Produce ONE mapping table:** item · destination · which rule sent it there (doctrine §0 decision tree, or a row of the §2 precedent table). An item no rule covers gets an honest "needs a new precedent" row, never a silent guess. Four kinds of destination, and the fourth is easy to forget: an entity room · a central home (a decision, an SOP) · `02_Command-Base/Resources/` · **material for work in flight, which moves as a whole folder into that project in its lane and needs no frontmatter family at all.**
3. **The owner rules** with the same grammar as the tidy report: file all, file by group, or walk item by item. Nothing moves before the ruling.
4. **Execute what was approved:** one entity one note from the matching templates where they fit, one filing-log line per filing, `capture-progress.md` rows updated at the end.
5. **Rows iron law still applies.** Transactional exports (invoice lists, POS dumps, attendance sheets) do not get imported; capture the pointer plus any exception stories, and say why in one line.
6. **The ritual payoff survives the shortcut:** still end with Stage 4 (one observation + two questions; bulk material usually gives the observation MORE to work with) and Stage 5 (the closing screen).

## Stage 4: Insight (~2 to 3 minutes, observation level)

This is the payoff. Calibration is strict:

**Formula: one observation the owner had not noticed + two good questions.** Nothing more.

- The observation comes from what was just captured, stated as a pattern on the map, never a diagnosis. Forward frame. Reference shapes (calibrate against these, do not recite them):
  - Clients room: "Two of the three client sources you named are referrals, and nothing in what you told me is a referral mechanism. It happens to you; you do not run it."
  - Products room: "Your dearest and cheapest offer differ by 8x, and there is nothing in between. The ladder has a missing rung."
  - A `02_Work` move-in: "Of the five things you are carrying, four are waiting on you for the next move. That is not a workload problem, it is a queue with one server."
- The two questions are questions the OWNER is now equipped to think about, not tasks. ("If a referral mechanism existed, who would be the first person it should thank?" / "What would a mid-priced offer even be, in your business?")
- **Honesty rules:** never promise analytics this data cannot support (no cashflow-gap claims, no trend claims from one night of capture). Never verdict ("your problem is..."); always map ("your next breakthrough point might be..."). If the capture genuinely surfaced nothing, say so plainly and give the two questions anyway; a thin room is itself an honest observation.
- **Land the insight in two places:** say it in chat, AND write it with today's date into the `## Observations` section of that folder's `_<Name>-Guide.md`. A `02_Work` move-in lands in the lane's guide, same section. That is what a guide collects (doctrine §3), and it is why guides get richer as rooms fill.

For Chinese sessions, write the insight natively. Sample register (shape, not script): "你刚搬进来的三个客户里, 两个是转介绍来的。但整个流程里没有一个转介绍机制, 它是发生在你身上, 不是你在经营它。两个问题给你想: ..."

## Stage 5: The four-layer closing screen

Always end a capture session with this screen, rendered as plain indented text in chat (both languages follow the same shape):

```
04_<Business>-Business-Wing/
├── 01_Assets        <- grew tonight: N notes (list the rooms touched)
├── 02_Work          <- N projects in flight (or: nothing moved in yet)
├── 03_SOP           <- still empty (or: N drafts waiting in the Inbox)
└── 04_Methodology   <- empty
```

Then exactly this beat, in the session language, in your own words but keeping all three moves:

1. **What grew tonight:** name it concretely.
2. **The two that are still empty, and they are empty in different ways.** Do not blur them into one story. `03_SOP` is not filled by capture: a process becomes an SOP when someone sits down and writes it properly, and any process dictated tonight is already queued as a draft in the Inbox. `04_Methodology` cannot be written into at all: it holds judgment the owner has confirmed, and it stays empty until it is earned. Full stop. No product, no course, no "if you want to go deeper". The empty folders speak for themselves.
3. **Honest extrapolation + tomorrow's hook:** "You moved in the first items only, and it can already see things like tonight's observation. Move one more room in tomorrow morning; ten minutes, same ritual." Optionally: open Obsidian's graph view for a look at the brain growing.

**Closeout actions, four of them:**

- **Write one line into `99_Meta/capture-buffer.md`**, not into the daily note. `01_Daily/` is end-of-day compile only, so the buffer is the channel: the command-base skill drains it at compile. That line carries its anchor as a wikilink, and the two link styles are not interchangeable: a brief is linked bare (`[[_Acme-Rebrand-Brief]]`), a guide is always linked with its path (`[[04_<Business>-Business-Wing/01_Assets/Clients/_Clients-Guide]]`), because guide names repeat across wings.
- Refresh `## Current state` in `_<Business>-Guide.md` if tonight changed it.
- Update `capture-progress.md` (the room or lane row, plus `next_suggestion:`).
- If a process was dictated tonight, say one sentence about it: the draft is parked in the Inbox, and writing it up properly is a separate sitting that runs on a separate skill the owner installs themselves. ⛔ Do not imply that tool ships with this one.

If the owner wants another room immediately, loop to Stage 2; the closing screen runs once per session, at the true end.
