---
type: graduation-config
created: {{DATE}}
last_updated: {{DATE}}
maintained_by: the owner (AI proposes amendments, owner approves)
---

# Graduation Config

> The thresholds the weekly distill's **pod altitude scan** reads to decide what to put on the table: which thin function rooms look ready to graduate into pods, and which pods look ready to shrink back. Read [`99_Meta/structure-doctrine.md` section 9](structure-doctrine.md) for what a pod is and the no-lost-learning law.
>
> These numbers are deliberately loose. The scan is a high-recall tripwire, not a verdict: it errs toward surfacing, because a false positive costs one sentence to wave off, while a false negative means a function never grows a brain. The real judgment is the owner's, made at the proposal and (for forging) at the pod-maker gate. Tune the numbers to how this vault actually moves; they are meant to be adjusted, not obeyed.

## Graduation signals (thin room -> pod)

A thin function room is surfaced as a graduation candidate when the **activity gate is open AND at least one reason threshold is crossed**. Activity is the entry ticket; a decision or a pile of orphan lessons is the reason. This combination is what keeps a busy-but-answer-known function (payroll, invoicing) from being mistaken for a pod: it may be active, but it logs no genuine decisions.

| Signal | What it counts | Default threshold |
|---|---|---|
| **Activity gate** (necessary, not sufficient) | the room's `Action-Log.md` | moved in the last 30 days AND >= 8 lines in 90 days |
| **Decision density** (the discriminator) | `06_Command-Base/Decisions/` notes with this `function:` | >= 3 in 90 days |
| **Orphan lessons** (compounding) | lessons tagged to this `function:` with no pod home yet | >= 5 |

Trigger rule: `activity_gate AND (decision_density OR orphan_lessons)`.

## Demotion signals (pod -> thin room / archive)

A graduated pod is surfaced as a demotion candidate when either holds:

| Signal | What it counts | Default threshold |
|---|---|---|
| **Silence** | the pod's `Action-Log`, its `function:` decisions, and its `rubric/` all quiet | zero movement across all three for 180 days |
| **Idle loop** | `rubric/` has candidates but nothing has promoted and `doctrine.md` has not grown | zero promotions for 90 days |

On the owner's yes to demotion, the pod's `doctrine.md`, `rubric/`, and `loop-config.md` are archived (never deleted), per the no-lost-learning law; re-graduating later can re-feed them.

## Notes

- Counting depends on the `function:` field being present on decisions and lessons. A blank `function:` makes that function invisible to this scan; the distill schema check flags blanks for exactly this reason.
- Execution of an approved graduation or demotion runs the `pod-maker` skill's shared flow, not a hand move. This file only sets when to ask.
