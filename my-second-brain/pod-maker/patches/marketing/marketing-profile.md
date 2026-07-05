---
type: domain-profile
pod: Marketing
status: seed
---

# Marketing Profile (seed)

> Domain-specific reference for this pod: voice and a scorecard shape. Kept deliberately thin and generic. The parts that define *your* marketing (your voice register, your palette, your positioning) do not live here; they live in your **brand foundation** (`01_Assets/Brand-Strategy/` and `Target-Audience/`), which this pod reads. This file only holds the generic scaffolding.

## Voice

The seed carries **no fixed voice**. A voice is identity, and identity lives in your brand foundation:

- **How the brand talks** (personality, tone, what it would never say): `01_Assets/Brand-Strategy/Brand-Personality.md`.
- **Visual voice** (color, type, logo use): `01_Assets/Brand-Strategy/Brand-Style-Guide.md`.
- **Who it talks to**: `01_Assets/Target-Audience/`.

If those are empty, the marketing skill runs in honest generic mode and says so. Fill the brand foundation to make the voice specific; do not hard-code a voice here.

One portable mechanism (not a voice, a discipline): **write natively in your market's language.** Content for a given language market should originate in that language, not be translated from another. See the rubric candidate on native-language origination.

## Scorecard shape

A judge view (`01_Assets/<pod>.base` or an inline table) scores each shipped piece against the outcome signal from `loop-config.md`. Generic columns to start:

| Column | What it holds |
|---|---|
| Piece | link to the shipped piece |
| Channel | where it ran |
| Ship date | when |
| Outcome signal | the market signal (from loop-config), backfilled within the read window |
| Verdict | scale / hold / kill (against `thresholds.md`) |
| Note | the confound or lesson, if any |

Tune the columns to the signal you chose. The point is one honest place to read whether a piece worked, so the loop has evidence to promote from.
