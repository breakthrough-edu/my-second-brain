---
type: vocabulary
maintained_by: AI (with owner approval)
last_updated: {{DATE}}
version: 1.0
---

# Tagging Vocabulary

> The controlled tag list for this vault. Only tags on this list get used, in daily logs, decisions, and captures. Off-list tags silently fall out of every dashboard view, so this file is load-bearing.

## Protocol

1. The AI only uses tags from this file. It does not invent tags.
2. A new tag is proposed (literal text + definition + boundary with existing tags), the owner approves, this file is updated FIRST, then the tag is used.
3. Format: lowercase, hyphen-separated, no spaces or special characters.
4. The same propose-approve-first discipline governs frontmatter enum values (statuses, lanes, domains). Those enums are declared in `99_Meta/structure-doctrine.md` §8 and nowhere else, so a new value is an amendment to that file, not a new list here.

## Domain

> Who a record binds. The tag question for decisions: who does this bind, not who is it for.

| Tag | Definition |
|---|---|
| `#personal` | Binds the owner's personal life. |
| `#{{BUSINESS_TAG}}` | Binds {{BUSINESS_NAME}}. |

## Lane

> Which of the four lanes a record belongs to. Mirrors the `lane:` frontmatter enum in doctrine §8, and the ladder that assigns it lives in §1. ⛔ These are not departments: this vault has no departments, and nothing files by which one would own it.

| Tag | Definition |
|---|---|
| `#deliver` | Work for a specific named customer, from pursuit to handover. |
| `#grow` | Work aimed at people who have not bought yet, addressed as an audience. |
| `#run` | Recurring upkeep: work that would still exist if the business never grew. |
| `#build` | Finite internal work that leaves the business different when it is done. |

## State

| Tag | Definition |
|---|---|
| `#decision` | A logged decision (a note in `02_Command-Base/Decisions/`). Light judgments do not get this tag. |
| `#waiting-for` | Blocked on someone else; the record names who. |
| `#renewal` | Anything with a `renew_by` date (licenses, insurance, leases, road tax). |
| `#lesson-candidate` | A pothole or realization flagged for the next maintenance run. Not yet in `04_Methodology`. |
| `#lesson-pooled` | A candidate maintenance picked up and moved into the hypothesis pool: it is being watched, not yet confirmed. Replaces `#lesson-candidate` on that line rather than being added beside it. |
| `#lesson-rejected` | A candidate maintenance looked at and decided was not worth carrying, with the reason written on the same line. The flag stays; only a rejection nobody can find gets re-flagged next month. |

> The three flags above are one lifecycle, not three independent tags. A line is flagged `#lesson-candidate` when it is noticed, and maintenance changes it to exactly one of the other two: **the flag is swapped, never deleted**. Deleting it erases the fact that the pothole was ever noticed, and the same pothole then gets flagged again by whoever hits it next.

## Excluded for now

> Categories deliberately not started. Add through the protocol when real captures demand them: per-person tags, per-project tags, per-outlet tags.

## Revision log

- **{{DATE}}**: v1.0 written at setup. `#lesson-pooled` and `#lesson-rejected` ship on the list rather than waiting to be proposed, because the flag they close (`#lesson-candidate`) ships already used: the doctrine names it as the standing flag and maintenance sweeps by it from week one. A vocabulary carrying the opening flag but neither closing one leaves the first sweep two illegal moves and no legal one, delete the flag or use an off-list tag, and protocol 2 above is what would have to break.
