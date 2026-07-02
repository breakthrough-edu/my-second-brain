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
4. The same propose-approve-first discipline governs frontmatter enum values (statuses, functions, domains).

## Domain

> Who a record binds. The tag question for decisions: who does this bind, not who is it for.

| Tag | Definition |
|---|---|
| `#personal` | Binds the owner's personal life. |
| `#{{BUSINESS_TAG}}` | Binds {{BUSINESS_NAME}}. |

## Function

> Which part of the business a record serves. Mirrors the `function:` frontmatter enum: `Marketing` / `Sales` / `Customer-Service` / `Operations` / `HR` / `Finance` / `Personal`.

| Tag | Definition |
|---|---|
| `#marketing` | Attention, content, promotion. |
| `#sales` | Conversion, pipeline, deals. |
| `#customer-service` | Post-sale handling, complaints, retention actions. |
| `#operations` | Running the operation day to day. |
| `#hr` | Hiring, people, payroll matters. |
| `#finance` | Money flow, statements, tax, banking. |

## State

| Tag | Definition |
|---|---|
| `#decision` | A logged decision (a note in `06_Command-Base/Decisions/`). Light judgments do not get this tag. |
| `#waiting-for` | Blocked on someone else; the record names who. |
| `#renewal` | Anything with a `renew-by:` date (licenses, insurance, leases). |
| `#lesson-candidate` | A pothole or realization flagged for the next distill run. Not yet Layer 3. |

## Excluded for now

> Categories deliberately not started. Add through the protocol when real captures demand them: per-person tags, per-project tags, per-outlet tags.

## Revision log

- **{{DATE}}**: v1.0 written at setup.
