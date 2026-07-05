---
type: pod-thresholds
pod: Marketing
status: seed
---

# Marketing Kill / Scale Thresholds (seed defaults)

> Quantitative triggers for killing or scaling a piece, a campaign, or a channel. **Every number below is a starting default, not a rule.** Cost, audience, channel behavior, and margins differ by market, so a smart business will and should tune these. What is fixed is not the numbers; it is the *discipline* (bottom of this file): that you set triggers up front and that overrides are signal-driven. Tune the numbers to your business; keep the discipline.

## Kill defaults (tune to your market)

**Paid, per piece** (fill in your currency and cost structure):
- Cold-audience acquisition cost above your ceiling, judged over about 7 days, is a kill. Set the ceiling from your customer lifetime value, not from a benchmark you read somewhere.
- A video hook rate below a floor (share of viewers who watch past the first few seconds) after a small spend is a fast kill; you do not need to spend more to learn a hook is dead.
- Retargeting cost should sit well below cold cost; if it does not, the offer or the audience is wrong, not the budget.

**Organic, per piece** (per platform, over the platform's real read window):
- Impressions or open rate below a floor in the first 48 hours to 7 days is a kill. Set the floor from your own baseline, not a generic one.

**Per channel, cumulative:**
- A channel whose blended cost stays above ceiling across several pieces over a couple of weeks is a channel to pause, not a piece to fix.
- A channel whose audience growth stalls below a floor per week over three weeks is a channel to rethink.

## Scale defaults (tune to your market)

- A paid piece well under your cost ceiling with a real lead count is a signal to raise budget (watch frequency and audience saturation as you do).
- An organic piece far above your impression baseline is a signal to increase cadence on that format.
- A channel whose audience is growing fast is a signal to raise cadence there.

## Override discipline (this part is fixed, not a default)

Thresholds can be overridden for a specific period, but every override must:

1. Be logged (in `current-thesis.md` for a mid-period override, and in `Action-Log.md`).
2. Name the doctrine-level threshold it is overriding.
3. State a **signal-driven** reason, not a gut one.
4. Set a review date when the override is re-evaluated.

Valid override example: "Raised the cold-acquisition ceiling for the first two weeks of a launch because no warm audience exists yet; review at day 14." Invalid override examples: "felt like it was working," "did not want to kill a piece we liked," "someone said to wait." Those are preference and hearsay, not signal. This discipline is mechanism (see `doctrine.md`), so it does not get tuned away.
