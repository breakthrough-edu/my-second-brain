# Generating a pod's brain (#3), seed depth (#4), and the sorting knife

This runs after the gate has passed (or after a graduation confirm). By now the hardest questions are already answered, because **the gate conversation was the intake** (see gate.md). Generation is the synthesis step, not a fresh interrogation.

## The flip: loop-config matters more than doctrine

The instinct is to pour effort into `doctrine.md`, the hardened rules. That instinct is wrong here. A freshly forged pod's doctrine is a **seed, destined to be replaced** by the real rules the loop grows over the coming months. Writing it heavily is wasted effort AND it violates "the seed is not the answer": a thick starting doctrine masquerades as settled knowledge the loop should have earned.

The thing worth writing carefully is **`loop-config.md`, the machine that does the replacing.** If loop-config is wrong, the loop learns garbage or never learns at all. So:

> **Put the generation effort into loop-config. Seed the doctrine lightly.**

## The generation flow (after the gate)

1. **Read the bedrock, do not ask for it.** Business-Profile, the brand foundation (`01_Assets/Brand-Strategy/` + `Target-Audience/`), Products-Services, Clients, the central Decisions tagged to this function, and (on the graduation path) the room's `Action-Log`. Infer everything inferable; do not re-ask what the vault already knows.
2. **Synthesize `loop-config.md` (the crown jewel; write it fully and precisely).** Its fields, filled from the gate's answers:
   - **Outcome signal**: what tells you a call was right (the gate's "what tells you?").
   - **Feedback delay**: how long until you know (the gate's "how long?").
   - **Promotion threshold**: how many confirmations, over what time window, before a rubric candidate hardens into doctrine. Fast-feedback functions can use "N confirmations"; slow-feedback functions must use a time window and small-N caution. This is where the loop-config spectrum lives (marketing = fast head; pricing, hiring, strategy = slow head).
   - **Attribution guardrails**: what must be logged to keep the loop honest (the gate's attribution trap: e.g. a hiring pod must log rejection reasons and revisit who was let go; a pricing pod must separate quote-win from realized margin).
3. **Seed `doctrine.md` lightly.** Write only what is already clearly believed AND generically safe. Mark it `provisional`. A handful of lines, not a manifesto.
4. **Seed 0 to 3 `rubric/` candidate cards.** Enough to give the first distill something to chew and to show the card shape, not a full rulebook. Each card: the candidate rule, the evidence behind it, a `confirmations:` counter starting at its real count.
5. **Write one `current-thesis.md`.** The pod's current bet, one paragraph. If this pod has an orchestrator above it, note that the thesis inherits from the upstream pod's thesis (read-only reference, full path).
6. **Domain profile.** If the function has a known framework worth a light seed (marketing has voice + a scorecard shape), seed it thinly; otherwise leave a `status: empty` stub.

The skeleton around all this (folders, MOC, Action-Log, empty file shells) is built deterministically by the install primitive. Generation only fills the brain.

## Seed depth (#4): harden little, keep the rest as hypotheses

The governing rule:

> **Uncertain → a `rubric/` candidate (awaiting the loop's confirmation). Certain and generic → a `doctrine.md` rule.**

A freshly forged pod is therefore **mostly questions (rubric candidates), not answers (doctrine).** That is the physical form of "the seed is not the answer / this is not a template pack": it ships as a small doctrine + a pile of hypotheses + a good loop, and the loop promotes the hypotheses into this business's own doctrine over time. A template pack is static answers; this is a machine that turns hypotheses into answers.

**Two paths seed differently:**
- **forge-from-scratch** has no history, so its seed is generic (portable defaults).
- **graduate-room** pulls its rubric candidates straight from the room's `Action-Log` patterns (real experience becomes candidate hypotheses, so the loop starts with evidence already attached).

Both then grow via the same loop.

## The sorting knife: mechanism vs preference vs identity

When generating a seed (especially when de-personalizing an existing, real body of practice into a portable seed, or when a graduating room's Action-Log carries the owner's personal habits), sort every candidate rule into **three buckets**. This is the guard against the deepest failure mode: a personal preference disguised as universal wisdom, hardened into doctrine, silently constraining every future user.

**Step 0, before sorting: split compound sentences.** Real doctrine lines are usually welded: a mechanism, a parameter, and an identity claim in one sentence. "The market is the judge, save/share at 7 days" is a FIXED mechanism (the market judges) fused to a VARIABLE parameter (save/share at 7d). Split each line into its mechanism clause / parameter clause / identity clause first, then bucket each clause on its own. Bucketing whole compound lines is where sorting goes wrong.

Then, for each clause, ask the knife question:

> **"Would a smart SME reasonably want this to be different?"**

| Bucket | Definition | Knife answer | What ships |
|---|---|---|---|
| **FIXED (mechanism)** | The operating mechanics, with no reasonable alternative | No, it is just how the machine works | Hardened into the seed doctrine (very few lines) |
| **VARIABLE (preference)** | Generically relevant but every business should tune it | Yes, reasonably | A default that is explicitly marked overridable: a loop-config knob or a rubric candidate, NOT a locked rule |
| **PERSONAL (identity)** | This specific business's identity bet | Not applicable; it is theirs, not a general truth | Nothing; dropped from the seed entirely |

**Ties default to VARIABLE** (mirroring the gate's default-NO: when unsure whether something is mechanism or preference, treat it as preference and ship it as an overridable default, never as a locked rule).

**Why this makes "constraining the user" structurally impossible:** if FIXED contains *only* mechanism and governance, with zero taste, then FIXED cannot constrain anyone's preferences, because it expresses none. The danger is never the obvious brand-specific stuff (that is easy to spot and drop). The danger is the smuggled preference that reads like universal marketing law. Keep FIXED strictly mechanism and the danger cannot enter.

- **FIXED example (marketing):** "the market is the judge, not the founder's taste"; "there is a quality gate before publish"; "an override must be signal-driven, not gut-driven." Pure mechanism.
- **VARIABLE example (marketing):** the specific save/share metric, the specific CPL ceiling number, the channel list, a specific quality-bar definition. All ship as defaults marked overridable.
- **PERSONAL example (marketing):** a specific positioning bet, a house content-pillar taxonomy, a signature visual system, named customer avatars, a punctuation rule that is a personal style choice rather than a marketing truth. Dropped.

Visual doctrine is the cleanest PERSONAL case: a business's look lives in its own `Brand-Style-Guide` (the brand-foundation room the scaffold already builds). A seed never ships one business's palette or mark as another's default; the marketing skill reads whatever `Brand-Style-Guide` the user filled.

## How the knife meshes with seed depth

The three buckets map onto seed depth exactly: FIXED = "harden a little" (mechanism only), VARIABLE = "keep the rest as hypotheses" (rubric candidates + overridable loop-config defaults), PERSONAL = out of the seed. VARIABLE ships **with a default value but flagged changeable**, never a blank: the user faces neither a blank page nor a locked cage. That is "the seed is not the answer" made concrete.

## Role-language caveat (v1 single-skill world)

When de-personalizing a seed that came from a multi-skill team (an orchestrator plus workers), any rule phrased in terms of **who does what** ("the CMO judges, the workers produce"; "orchestrator decides, worker executes") goes semantically dead in a single-skill pod. Rewrite such rules as **mechanism** ("there is a gate before publish"; "the market signal decides scale or kill"), not role assignments. The team can split back out later via the gate's SPLIT exit if the business grows to need it; the seed should not presume the team structure.
