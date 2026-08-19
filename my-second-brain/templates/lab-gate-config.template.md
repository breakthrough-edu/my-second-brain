---
type: lab-gate-config
created: {{DATE}}
last_updated: {{DATE}}
maintained_by: the owner (AI proposes amendments, owner approves)
---

# Lab Gate Config

> The thresholds the **`playbook-lab` skill** reads to decide what to put on the table: whether a playbook is really a candidate for a lab, and whether an open lab looks ready to close. ⚠️ **A weekly scan used to read this file and propose candidates unasked; that scan was retired on 2026-08-20.** A lab is opened when the owner asks for one, and this gate is what tells them no. Read `99_Meta/structure-doctrine.md` §9 for what a lab is, the five organs it holds, and the archive-never-destroy law.
>
> **The gate carries a NO-prior.** Prose is the normal, sufficient form of a playbook, and most playbooks never need a lab. These numbers exist to stop a lab being opened out of enthusiasm, not to find as many as possible. Tune them to how this vault actually moves; they are meant to be adjusted.

## Opening a lab: three doors, ALL required

A playbook becomes a candidate only when all three are open. Any one missing and the answer is no, and the missing one usually names the better move.

| Door | What it counts | Default threshold |
|---|---|---|
| **The line is alive** | new outputs of this kind, counted from journal backlinks and the room they land in | >= 4 in the last 30 days |
| **Judgment is accruing** | lessons and decisions related to this playbook | >= 3 |
| **An outside signal exists** | an external, countable feedback signal (inquiries, orders, saves, replies) | at least one, named |

What each miss means, and this is the useful part of the gate:

- **Alive but no judgment** = a lot is happening and nothing is being decided. That wants a better SOP, not a lab.
- **Judgment but not alive** = the thinking is real and the work has stopped. Nothing to feed a loop with.
- **No outside signal** = a lab could only measure self-satisfaction. Find the countable signal first, or do not open.

## Closing a lab: two signals, both propose-only

| Signal | What it counts | Default threshold |
|---|---|---|
| **Silence** | no new output of this kind at all | 90 days |
| **Idling** | outputs continue but scores stop, bets never resolve, proposals never land | 60 days with zero resolved bets |

On an idling signal, ask "recommit?" exactly once before proposing to close. On the owner's yes to closing, the organs and a scoreboard snapshot are archived to `98_Archive/` and the playbook text keeps every criterion it earned. Learning is archived, never destroyed, and a revived line gets its organs back.

## Notes

- This file sets **when to ask**, nothing else. Opening and closing a lab is guided by the `playbook-lab` skill, which shipped with `my-second-brain` and was installed at setup (step 6.6). It runs the gate properly, interviews the rubric into existence, and seeds the register and thresholds. ⛔ Never hand-build a lab's organs.
- If that skill is somehow absent (removed by hand, or a vault built before it shipped), ⛔ do not run the gate by hand and ⛔ do not hand-build the organs. Say what the owner asked for is pending that skill; a finding keeps.
- Counting depends on `lane:` being present on lessons and playbooks. A blank one makes that work invisible to this gate, which is why the weekly schema check flags it.
