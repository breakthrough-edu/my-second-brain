---
name: playbook-lab
description: >
  Open or close a playbook lab: the rare upgrade where a playbook that has
  earned a live feedback loop grows into a small folder holding a rubric, a
  register of live bets, and its thresholds. Runs the three-door gate carrying
  its NO-prior (most playbooks should never get one), interviews the rubric into
  existence, seeds the empty organs, and archives them again when the line goes
  quiet. MUST trigger when the user says "open a lab", "开个 lab", "给它开个
  lab", "give this playbook a lab", "upgrade this playbook", "升级这个
  playbook", "should this playbook get a lab", "这个 playbook 值不值得开 lab",
  "close the lab", "关掉这个 lab", "this playbook is never accurate", "这个
  playbook 怎么都不准", or when the weekly maintenance lab scan has proposed
  candidacy and the owner said yes. NOT for writing or revising a playbook's
  text, NOT for scoring outputs, NOT for SOPs (that is sop-builder), and NOT
  for planning a project (that is project-consultant).
---

# Playbook Lab

You open and close labs. That is the whole job, and it is a rare one.

⛔ **The default answer is NO, and talking an owner out of a lab is half the value of this skill.** Prose is the normal, sufficient, permanent form of a playbook. Most playbooks in a healthy vault never get a lab and that is the expected outcome, not a failure. An owner who is busy but not accumulating judgment does not want a lab, they want a better SOP.

## The law lives in the vault, not in this file

⛔ **Read `99_Meta/structure-doctrine.md` §9 before you do anything here, every time.** That section is the authority on what a lab is, its fixed five-part shape, the loop it runs, the split test, the gate, and the closing signals. This file is the procedure for carrying it out.

⛔ **If §9 is not there, stop.** Say plainly that this vault's constitution does not carry the playbook-lab section, so there is no law to execute, and do not improvise the shape from what is written here. A lab built against a law the vault has not adopted is a folder its own house does not recognise.

## The gate: three doors, all required

Candidacy reaches you two ways: the weekly maintenance lab scan proposes it, or the owner asks directly. **Either way the gate runs**, and it runs carrying its NO-prior.

Defaults live in `99_Meta/lab-gate-config.md`, which the owner may tune. Read that file rather than the numbers below when it exists.

| Door | Default | Why it is a door |
|---|---|---|
| **The line is alive** | 4 or more new outputs in the last 30 days, counted from journal backlinks and the output rooms | A lab measures a running line. There is nothing to score on a line that is not producing |
| **Judgment is accruing** | 3 or more related lessons or decisions | ⭐ This is the door that catches the common false positive: busy with no judgment wants a **better SOP**, not a lab |
| **An external, countable signal exists** | inquiries, orders, saves, replies, anything from outside the building that can be counted | ⛔ A lab without an outside signal can only ever measure self-satisfaction |

**All three, or no proposal.** When one fails, say which one and what would have to change; that is more useful to the owner than a verdict.

### Split before you open

⭐ **Run the split test first, because opening a lab around two lines is much harder to undo than splitting a playbook.** Methodology segments that score **the same outputs** are chapters of one playbook and share one scoreboard. A stream with its own outputs and its own feedback signal is its own playbook. If the candidate is really two lines, propose the split and stop there; the gate can run again afterwards on whichever half earned it.

## Opening: interview the rubric, then seed the organs

The lab folder is `04_Methodology/Playbooks/<Name>/` and the upgrade happens **in place**: the playbook note becomes that folder. ⛔ **No move, no link rewrites.** Everything that pointed at the playbook still points at the playbook.

**The rubric is the only part you interview into existence.** The other organs ship as empty, correctly-shaped ledgers.

Four rules of the craft, and they are not negotiable down:

1. **At most 2 to 3 criteria.** A rubric that takes real thought to apply gets applied twice and then abandoned.
2. **Score the market's behaviour, never a friend's politeness.** "Did anyone act on it" beats "did people like it" every single time.
3. **At least one hard business signal.** Money, enquiries, orders, bookings, retention. Something that would show up whether or not anyone was watching.
4. **At least one identity veto: "does this sound like us?"** A line that optimises purely on numbers drifts into work its owner would not sign.

⭐ **The scoring test: 30 seconds, or nobody does it.** If applying the rubric to one output takes longer than that, cut a criterion. This is the single most common way a lab dies quietly.

Then seed, per §9.2:

- **the rubric**, from the interview
- **the hypothesis register**, an empty ledger. Each future row names which part of the methodology it tests and the condition that would settle it
- **the thresholds**, shipped with defaults and marked owner-tunable
- **`_<Name>-Guide.md`**, the folder's door: reading order, who writes what, when

⛔ **The scoreboard is deliberately not in the lab.** Scores live with the outputs they score. This is law, not preference.

**One organ set per lab.** Plurality lives inside the organs: several rubric cards, several concurrent bets, rows disposable, files permanent.

⛔ **Nothing lands without the owner's yes**, and the whole open runs propose → approve → log like every other structural change in this vault.

## Closing: two signals, both propose-only

- **Silence.** 90 days with no new output on the line.
- **Idling.** Outputs keep coming but the scores stop, the bets never resolve, the proposals never land. ⚠️ **Ask "recommit?" once** before proposing the close; idling is sometimes a busy quarter, not a dead line.

**Closing archives the organs and a snapshot of the scoreboard to `98_Archive/`.** ⛔ **The playbook text is not touched, not one word.** It keeps every criterion it earned; that text is what the lab was for.

⭐ **Learning is archived, never destroyed.** A line that comes back gets its organs back.

## What this skill is not

- ⛔ **Not the daily way to use a playbook.** Reading and applying one needs no skill at all: `CLAUDE.md` says read the handbook first, the SOP links its playbook by `playbook:`, and the lab folder's guide is the door. That chain runs without you.
- ⛔ **Not a writer of playbook text.** Revisions to the playbook come from the loop and the owner's yes, not from this skill's own opinion.
- ⛔ **Not the scorer.** Scoring happens where the outputs live, in seconds, as part of shipping them.
- ⛔ **Not a hand-builder.** ⛔ **Never hand-build a lab's organs from a maintenance pass or from a conversation**; that is exactly what this skill exists to prevent.
