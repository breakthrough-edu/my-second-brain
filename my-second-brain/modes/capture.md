# Capture Mode -- moving the business in, one room at a time

The move-in ritual. Each run: pick one room, the AI asks one thing at a time, the owner talks (typing or voice, both fine), notes land in the right places, and the session ends with one observation the owner had not noticed plus two good questions. Total 15 to 20 minutes for a first room; regulars finish in 10.

Everything files by `99_Meta/structure-doctrine.md`. Every filing appends to `99_Meta/filing-log.md`. Interaction language comes from `bootstrap-progress.md`.

## Entry

1. Read `99_Meta/capture-progress.md` and `99_Meta/bootstrap-progress.md`.
2. Staleness check per SKILL.md (offer once, never nag).
3. Route:
   - `profile_captured: false` -> run **Stage 1, Business Profile** (everyone's first move-in).
   - Profile done -> show the **room menu** (Stage 2) with a suggestion.
   - Mid-room progress recorded -> offer to resume that room.

## Stage 1 -- Business Profile (everyone starts here, ~5 minutes)

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

Then:

- Fill `07_<Business>/01_Assets/Business-Profile.md`: frontmatter fields (`founder_name`, `brand_name`, `industry`, `category`, `location`, `one_line_description`) + body sections from the answers, near verbatim.
- Update `_Map.md` section "What this business is" with a 3-line summary.
- Update `capture-progress.md` (`profile_captured: true`), append a filing-log line.
- Acknowledge operationally, one line: the profile is the anchor every future session reads first.

The profile itself deserves a micro-insight (one observation only, no question pair yet; save the full formula for rooms). Example shape: "You said the business is 8 years old but everything you described still routes through you personally. Noting that; we will see it again when we capture SOPs."

Then go straight to the room menu.

## Stage 2 -- Room menu

Show the map compactly, with move-in state from `capture-progress.md`:

> "The business wing has three layers. Tonight we open one room and move it in.
>
> **Layer 1, Assets** (what the business is made of): Clients · Vendors · Employees · Products and Services · Content Assets · Company Docs [· Equipment] [· Outlets] · plus the function shelves (Marketing / Sales / Customer Service / Operations / HR / Finance)
> **Layer 2, SOP** (how things get done): Staff Onboarding · Client Onboarding · Sales Follow-up · Delivery · Collection · Complaint Handling · Content Production · Purchasing · Payroll and Monthly Closing [· presets]
> **Layer 3, Methodology**: stays empty tonight. It fills from judgment, not from capture.
>
> Which room? If unsure, I suggest starting with <suggestion>."

Suggestion logic (from the profile, one line of reasoning): service business or few-big-clients -> Clients; product or menu business -> Products-Services; has staff and owner mentioned being stretched -> an SOP room (usually the one process they described doing themselves); everything else -> Clients. The user always outranks the suggestion.

## Stage 3 -- Guided capture (~8 to 10 minutes)

Load the chosen room's guide from [../references/rooms-assets.md](../references/rooms-assets.md), [../references/rooms-functions.md](../references/rooms-functions.md), or [../references/rooms-sop.md](../references/rooms-sop.md). The guide gives the door sign, the filing test, the question set, and the insight angles. Rules that apply in every room:

- **One question at a time.** Never a numbered battery. Voice-friendly: every question answerable by talking for 20 seconds.
- **Zero material is fine.** The owner's description IS the asset. If they have material (a price list, a WhatsApp thread, a dictated process), take it: paste or drop, you extract and file.
- **3 to 5 items is a full first capture.** Do not chase completeness. "First few, not all" keeps it 10 minutes and leaves tomorrow's hook honest.
- **One entity, one note**, from the matching `99_Meta/Templates/` template. Fill what was said, leave the rest blank. Blank fields are visible invitations, not failures.
- **Update as you go:** the room MOC inventory after each note, a filing-log line per filing, `capture-progress.md` at room close.
- **Rows iron law watch.** If the owner starts reading out transactions ("then invoice 4512, then 4513..."), catch it warmly: point to where those rows live (their POS or accounting tool), capture the pointer plus any exception stories, move on.
- **New room proposals.** If material clearly needs a room that does not exist (e.g. imports paperwork with no Importing room), propose it with a reason, owner approves, create it, log it.

## Stage 4 -- Insight (~2 to 3 minutes, observation level)

This is the payoff. Calibration is strict:

**Formula: one observation the owner had not noticed + two good questions.** Nothing more.

- The observation comes from what was just captured, stated as a pattern on the map, never a diagnosis. Forward frame. Reference shapes (calibrate against these, do not recite them):
  - Clients room: "Two of the three client sources you named are referrals, and nothing in what you told me is a referral mechanism. It happens to you; you do not run it."
  - Products room: "Your dearest and cheapest offer differ by 8x, and there is nothing in between. The ladder has a missing rung."
  - An SOP room: "Of the six steps you described, three can only be done by you. That is the fragile part of this process."
- The two questions are questions the OWNER is now equipped to think about, not tasks. ("If a referral mechanism existed, who would be the first person it should thank?" / "What would a mid-priced offer even be, in your business?")
- **Honesty rules:** never promise analytics this data cannot support (no cashflow-gap claims, no trend claims from one night of capture). Never verdict ("your problem is..."); always map ("your next breakthrough point might be..."). If the capture genuinely surfaced nothing, say so plainly and give the two questions anyway; a thin room is itself an honest observation.
- Land the insight in two places: say it in chat, AND write it (with today's date) into the room MOC's "Observations" section.

For Chinese sessions, write the insight natively. Sample register (shape, not script): "你刚搬进来的三个客户里, 两个是转介绍来的。但整个流程里没有一个转介绍机制, 它是发生在你身上, 不是你在经营它。两个问题给你想: ..."

## Stage 5 -- The three-layer closing screen

Always end a capture session with this screen, rendered as plain indented text in chat (both languages follow the same shape):

```
07_<Business>/
├── 01_Assets        <- grew tonight: N notes (list the rooms touched)
├── 02_SOP           <- grew tonight: N notes (or: still empty)
└── 03_Methodology   <- empty
```

Then exactly this beat, in the session language, in your own words but keeping all three moves:

1. **The two layers that grew:** name what moved in tonight, concretely.
2. **The layer that did not:** "The top two layers fill by capture. The third one cannot be filled by capture. That layer comes from judgment, from decisions reviewed over time. It stays empty until it is earned." Full stop. No product, no course, no "if you want to go deeper". The empty folder speaks for itself.
3. **Honest extrapolation + tomorrow's hook:** "You moved in the first items only, and it can already see things like tonight's observation. Move one more room in tomorrow morning; ten minutes, same ritual." Optionally: open Obsidian's graph view for a look at the brain growing.

Close out: update `capture-progress.md` (room row + `next_suggestion:`), append one line to `07_<Business>/00_Daily-Log/YYYY-MM-DD.md` (create from template if absent), refresh `_Map.md` "Current state". If the owner wants another room immediately, loop to Stage 2; the closing screen runs once per session, at the true end.
