---
type: loop-config
pod: Marketing
status: seed
feedback_speed: fast
---

# Marketing Loop Config (seed)

> How this pod learns. This is the most important file in the pod: it is the machine that turns rubric candidates into hardened doctrine. The seed doctrine is disposable; this config is not. Tune the values to your market; keep the structure.
>
> Marketing sits at the **fast-feedback head** of the loop spectrum: signals arrive in days, volume is high, attribution is relatively clean. That is why marketing can promote on a confirmation count rather than a long time window. Slower-feedback functions (pricing, hiring, strategy) forge with very different values in this same file.

## Outcome signal (what tells you a piece worked)

- **Default:** a market engagement signal you can read within about a week (saves and shares, qualified leads, replies, or whatever your channel reports as genuine pull rather than vanity reach). Pick the one that best predicts real business movement for you and write it here.
- The signal must be something the *market* produced, not something the team rated. Internal calibration is a veto, not this signal (see `doctrine.md`).

## Feedback delay

- **Default:** short (roughly 7 days for organic pull; 24 hours to 7 days for paid, depending on spend). Fill in your real read window per channel.

## Promotion threshold (rubric candidate to doctrine)

- **Default:** a candidate rule hardens into `doctrine.md` after **3 independent confirmations** (different pieces, different sessions, ideally different channels) AND it survives at least one honest negative test (a case where it should have failed and did not). The owner rules on every promotion; nothing auto-promotes.
- Because feedback is fast here, a confirmation count works. Do not copy this to a slow-feedback pod; there, use a time window and small-N caution instead.
- **Tier ladder (the loop's stages):** raw move logged in `Action-Log.md` (tagged) → pattern observed 2+ times becomes a `rubric/` candidate card with a `confirmations:` counter → 3 confirmations + a negative-test survival + the owner's yes promotes it into `doctrine.md`. Reversal: evidence turns → the rule moves to `retired.md` with a date, and an `Action-Log` line records the reversal.

## Attribution guardrails (keep the loop honest)

- Marketing attribution is *relatively* clean but not free. Before crediting a win to a piece's craft, check for confounds: a spend spike, a seasonal surge, a piece that rode another's coattails, a lucky algorithmic boost. Log the confound when you see it, so the loop does not learn "this hook works" when really "we tripled the budget that week."
- Kill/scale decisions must cite the signal and the window (`thresholds.md`), not a feeling.

## Judge view (where results get read)

- The pod's `01_Assets/` carries a `.base` judge view scoring shipped pieces by their outcome signal. For marketing the judge is near-immediate market response, so the view can score pieces within their read window. (Contrast: a slow-feedback pod's judge view backfills months later.)

## What to tune first

When you have shipped a dozen real pieces, revisit: is the outcome signal actually predicting business movement? Is 3 confirmations too loose or too strict for how fast your market moves? Adjust here, then let the loop run against the new config.
