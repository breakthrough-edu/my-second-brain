# The pod-worthiness gate (#2): four exits, default NO

The counter-intuitive core: **the gate is not yes/no, it is a classifier with four exits, and its most valuable exits are the ones that turn people away.** A pod is expensive. Building one for a function that does not deserve it produces empty scaffolding the vault then has to carry and later demote. The gate's whole job is to protect the "shrinks, does not bloat" north star at the point of entry.

## The four exits

1. **PASS**: build the pod now. All four criteria hold AND there is real, feedback-bearing track record to seed the loop.
2. **THIN-ROOM**: do not build yet. The function may qualify one day, but there is no track record for the loop to learn from; building now produces empty scaffolding. Start (or keep) a thin room and let the graduation doorbell surface it once real decisions accumulate.
3. **REDIRECT-SOP**: never a pod. The function has a knowable correct answer that can be written down as steps. It wants an SOP, not a learning loop.
4. **SPLIT**: this is actually two or more pods. The function qualifies, but its sub-decisions get their verdicts back on very different timescales; one loop would let the fast signal drown the slow lessons.

**The default exit is 2 or 3, not 1.** Carry a strong prior toward "not a pod." Let PASS through only when the evidence is clearly there.

## The four criteria, each with its diagnostic mirror

Do not run a script. Hold up each mirror as a diagnostic question, listen to the honest answer, and route to the failure exit when it fails. This is instruction-light: you get the lens and the failure exit, not a word-for-word interrogation.

| Criterion | Diagnostic question | Failure routes to |
|---|---|---|
| **Repeated judgment under uncertainty** | "Is this making a call where two directions could both be right, or following a known procedure? And does it recur?" | Procedure or one-off → REDIRECT-SOP |
| **A feedback signal exists** | "Afterward, do you find out whether the call was right? What tells you?" | Never knowable → a blind loop; flag, do not build |
| **Compounding** | "If you wrote down what you learned, would the next call be sharper? Or is every case too unique to transfer?" | Does not transfer → the loop spins for nothing |
| **Clean attribution** | "Can you tell whether the outcome was this decision's doing, or is it tangled with a dozen other causes?" | Tangled → the loop learns garbage → REDIRECT or flag |

Plus two structural mirrors:

- **Split diagnostic:** "Do different parts of this get their verdict back on very different timescales?" If yes → **SPLIT** (forge the fast pod and the slow pod separately; do not let the fast loop's noise bury the slow loop's lessons). This is the pricing example: quote-win/loss is fast, true realized margin is slow.
- **Prematurity diagnostic:** "Has this actually been happening, with a record to show for it, or is it still hypothetical?" If no record → **THIN-ROOM** (potential without evidence is a thin room, not a pod).

The attribution mirror is the hiring trap generalized: a function whose outcomes cannot be cleanly credited to the judgment (list-price repricing, cash-timing) teaches the loop the wrong lessons and belongs back in SOP or gets flagged. quote-to-actual and default/no-default are clean; list-price and cash-timing are confounded.

## Why the gate is also the intake (the key economy)

The four diagnostic questions are *exactly* the fields `loop-config.md` needs (see generation.md):

- "Do you find out whether it was right? What tells you?" → the **outcome signal**.
- "How long until you know?" → the **feedback delay** → the **promotion threshold**.
- "Can you cleanly credit the outcome?" → the **attribution trap** → the loop's **guardrails**.
- "Does what you learn transfer?" → **compounding**, which decides whether a loop is worth having at all.

So the gate conversation is not a toll booth you pass and forget. **Its answers become the loop-config's fill.** The hardest questions get asked once, here. Generation (after the gate) is a synthesis step, not a re-interrogation. This is how the pod gets built by "asking the fewest questions."

## Turning-away scripts (a gatekeeper helps, it does not wall off)

The non-PASS exits should feel like help, not rejection. Drafts (adapt to the owner's language and situation):

- **→ REDIRECT-SOP:** "This has a right answer you could write down ahead of time. That is an SOP, not a pod: document it once and you are done. Want to turn it into an SOP instead?"
- **→ THIN-ROOM:** "There is real potential here, but no track record yet for a loop to learn from. Let us keep it as a light room; once it has logged enough real decisions, the weekly scan will nudge you to graduate it. Building a full pod now would just be an empty shell."
- **→ SPLIT:** "Two parts of this learn at very different speeds. One loop would let the fast part's noise bury the slow part's lessons. I would forge two pods: X (fast) and Y (slow). Want to do that?"

## Instruction-light is not opinion-light

Give the model a **strong prior** (default NO) plus the mirrors, not a script. The prior is what lets a free, capable model reliably *doubt*. A free model with no prior, handed a pod request, rubber-stamps it: it sees a pod, it builds a pod. The prior is the difference between a skeptical gatekeeper and a yes-machine. So: light on procedure, heavy on stance.

## Where the gate runs per entry path

- **forge-from-scratch:** the full gate, all four exits live. This is the path that most needs turning away.
- **graduate-room:** the graduation doorbell already applied a coarse recall filter, so worthiness is largely shown. Run a **light confirmation** plus the two structural mirrors that the doorbell cannot test: the SPLIT check and the attribution check. Do not re-litigate the whole gate.
- **load-patch:** the gate is **skipped**. A patch is curated content vetted before shipping; it arrives having already earned its shape. (This is also why offering the shipped Marketing patch at Setup does not violate the prematurity rule: the prematurity rule governs *forging with no seed*, not loading a *pre-seeded, curated patch*.)

## The doorbell / gate pair (recall vs precision)

The maintenance graduation doorbell (over in the my-second-brain distill mode) and this gate are a matched pair:

- The **doorbell** is a cheap, high-recall tripwire: it errs toward surfacing candidates (a false positive costs one sentence to wave off; a false negative means a function never grows a brain). It decides only what to put on the table.
- This **gate** is the deep, high-precision, default-NO interview: it decides what actually gets built.

One guards against missing a real pod; the other guards against building a fake one. Do not collapse them into one.
