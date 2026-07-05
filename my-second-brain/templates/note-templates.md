# Note Templates

Setup writes each block below into its own file under `<vault>/99_Meta/Templates/`. Capture and command-base sessions start every new record from the matching template. Templater-free on purpose: the AI fills the values, so no plugin is required. Dates `YYYY-MM-DD` unquoted; multi-word keys `underscore_case`. `{{DATE}}` stays literal inside `99_Meta/Templates/` (it is filled at note-creation time, not at scaffold time).

## Client.md

```markdown
---
type: client
status: active
source:
since:
current_terms:
tags: []
---

# <Client Name>

## Who they are

## What they buy from us

## History highlights

## Notes
```

## Vendor.md

```markdown
---
type: vendor
role: vendor
supplies:
terms:
contact:
tags: []
---

# <Vendor Name>

## What they supply

## Terms and history

## Notes
```

## Employee.md

```markdown
---
type: employee
role:
started:
status: active
tags: []
---

# <Employee Name>

## Role and scope

## Documents
(certs, contracts: pointers or filenames)

## History
```

## Product-Service.md

```markdown
---
type: product-service
price:
cost:
status: active
tags: []
---

# <Product or Service Name>

## What it is

## Pricing (source of truth)

## Specs / recipe pointer
(spec and costing live here; the how-to-make-it steps live in an SOP)
```

## Company-Doc.md

```markdown
---
type: company-doc
doc_kind:
renew_by:
issuer:
location_of_original:
tags: [renewal]
---

# <Document Name>

## What it covers

## Renewal notes
```

## Equipment.md

```markdown
---
type: equipment
model:
purchased:
warranty_until:
last_serviced:
tags: []
---

# <Machine Name>

## Manual / supplier pointer

## Maintenance log
- 
```

## Outlet.md

```markdown
---
type: outlet
address:
lease_until:
licenses:
tags: []
---

# <Outlet Name>

## Lease and licenses
(each with its renew-by date)

## Utilities and accounts

## Notes
```

## SOP.md

```markdown
---
type: sop
function:
owner:
last_verified: {{DATE}}
tags: []
---

# SOP: <What this process achieves>

## When this runs

## Steps
1. 

## Only-the-boss-can-do steps
(mark any step only one person can perform; these are the fragile ones)

## Attachments
(blank templates and checklists live with this SOP)
```

## Decision.md

```markdown
---
cb: decision
date: {{DATE}}
status: active
domain:
function:
tags: [decision]
---

**Decided:** 

**Why:** 

**Alternatives:** (rejected because )
```

## Task.md

```markdown
---
cb: task
status: not-started
domain:
function:
due:
waiting_on:
created: {{DATE}}
---

What the task is, in the owner's words.
```

## Session.md

```markdown
---
cb: session
session_type: meeting
status: upcoming
date:
domain:
---

## Prep

## Reflection (fill after; flip status to needs-reflection, then done)
```

## Business-Daily-Log.md

```markdown
---
type: business-daily-log
date: {{DATE}}
business:
tags: []
---

# {{DATE}}

## What moved today
- 

## Decided today
(one line each; the decision note itself lives in 06_Command-Base/Decisions/)

## Observed
- 
```

## Engagement.md

```markdown
---
type: engagement
client:
engagement_type: project
status: active
started: {{DATE}}
tags: []
---

# <Client>: <Engagement>

## Scope

## Working files

## Closeout (four-way distribution when done)
- finals pointer -> client note
- case study -> Marketing
- testimonial -> client note
- retro -> Lessons (after owner confirms)
```

## Lesson.md

```markdown
---
type: lesson
date: {{DATE}}
source:
function:
confirmed_by_owner: false
tags: []
---

# Lesson: <one line>

## What happened

## What we now do differently
```

## Playbook.md

```markdown
---
type: playbook
status: forming
last_used:
confirmed_by_owner: false
tags: []
---

# Playbook: <the play>

## When to run it

## The moves

## Maturity note
(when every step can be written down and delegated, this demotes into an SOP)
```
