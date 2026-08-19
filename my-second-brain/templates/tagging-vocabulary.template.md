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

> ⛔ **Three lesson flags used to sit here (`#lesson-candidate`, `#lesson-pooled`, `#lesson-rejected`) and all three were retired on 2026-08-20.** They were one lifecycle for a pit that got noticed one week and looked at the next. A pit is now written up as a Lesson at the **closeout of the session it happened in**, with the owner's yes, so there is no waiting period for a flag to mark. ⛔ Do not re-add them, and ⛔ do not invent a replacement flag: the mechanism they served no longer exists, and a flag with no sweeper is a tag that accumulates.

## Excluded for now

> Categories deliberately not started. Add through the protocol when real captures demand them: per-person tags, per-project tags, per-outlet tags.

## Revision log

- **{{DATE}}**: v1.0 written at setup. ⛔ It ships **without** any lesson flag, on purpose: a pit is written up at the closeout of the session it happened in, so nothing needs marking for a later sweep. Earlier versions of this product shipped three such flags and swept them weekly; the note above records why they are gone, so nobody re-derives them from first principles.
