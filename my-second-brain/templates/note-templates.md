# Note Templates

Setup writes each block below into its own file under `<vault>/99_Meta/Templates/`. Capture and command-base sessions start every new record from the matching template. Templater-free on purpose: the AI fills the values, so no plugin is required. Dates `YYYY-MM-DD` unquoted; multi-word keys `underscore_case`. `{{DATE}}` stays literal inside `99_Meta/Templates/` (it is filled at note-creation time, not at scaffold time).

**Every block here is a legal instance of its family in doctrine §8**, which is the whole point of shipping them: a template is how the law gets obeyed by people who never read it. When §8 changes, these change in the same breath, and §8 wins. Templates carry the per-type naming convention in a bottom comment block; the naming system itself lives in §5.

## Guide.md

```markdown
---
type: guide
guide_family: room
updated: {{DATE}}
---

# <Name>

<One line: what lives here.>

**Files here when:** <the filing test for this folder, one sentence.>

## Observations
(what sessions notice about this folder lands here, one dated line each)

<!--
Filename is `_<Name>-Guide.md`, one per folder, and at most one `_`-prefixed file per folder.
guide_family: one of wing / room / lane / brand / lab. A layer folder (01_Assets, 02_Work,
  03_SOP, 04_Methodology) gets NO guide: it is a container of rooms, not a room, and none of
  the five values would be true.
Guides are linked path-qualified, never bare: the same room name repeats across wings, so
  [[04_Acme-Business-Wing/02_Work/Run/_Run-Guide]], not [[_Run-Guide]].
⛔ No inventory and no navigation section. Home.md is the only directory this vault has.
The wing guide is the one that also carries a `## Current state` section.
-->
```

## Brief.md

```markdown
---
type: brief
status: active
updated: {{DATE}}
started:
due:
owner:
brand:
stage:
priority:
---

# <Project Name>

**Goal:** <what done looks like, one sentence>

## Deliverables

## Next step
(and whose move it is)

## Notes

<!--
Filename is `_<Project>-Brief.md`, inside the project folder, inside exactly one lane of
  02_Work/. Briefs are linked BARE ([[_Acme-Rebrand-Brief]]): project names are unique
  vault-wide, so they need no path.
status: active / done / killed. It answers whether the project is alive.
stage: pending / planning / pursuing / executing / closed, optional. It answers how far along.
  The two are different questions: a client job can be status: active + stage: pursuing.
  ⛔ Do not fill stage on a private project just to fill it; unstaged is a legal state.
Tasks live in <Project>/Tasks/ and carry no project, lane or domain key: the path says it.
Everything else in the folder is project material and needs no frontmatter family at all.
-->
```

## Client.md

```markdown
---
type: client
status: active
status_since:
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

<!--
One client, one note, in 01_Assets/Clients/. Filename is the client's name, unique vault-wide.
The JOB you do for them is a separate thing: one project in 02_Work/Deliver/, from pursuit
  through handover, tracked by its brief's `stage:`. This note is who they are; that is what
  is moving.
current_terms holds the terms in force now. A change to them is a decision note PLUS an edit
  here, in the same breath.
status is active or prospective. Someone you are only pitching is prospective, and this note
  exists from that first conversation (doctrine §2). Flip it to active the day they buy. The
  template ships active because most clients already are; ⛔ do not leave it that way for a
  prospect, because active is a legal value and nothing will ever warn you it is false.
-->
```

## Vendor.md

```markdown
---
type: vendor
status: active
status_since:
supplies:
terms:
contact:
tags: []
---

# <Vendor Name>

## What they supply

## Terms and history

## Notes

<!--
One vendor, one note, in 01_Assets/Vendors/. Landlords, lessors, platforms you sell through,
  and freelancers who invoice you all file here.
A freelancer on payroll is an Employee instead. The test is how the money leaves, not the work.
status is active or prospective. A landlord you are still negotiating with, or a supplier you
  are still courting, is prospective, and the note exists from that first conversation (doctrine
  §2). Flip it to active the day the lease or the account is real. The template ships active;
  ⛔ do not leave it that way for a prospect, because active is a legal value and nothing will
  ever warn you it is false.
-->
```

## Employee.md

```markdown
---
type: employee
status: active
status_since:
role:
started:
tags: []
---

# <Employee Name>

## Role and scope

## Documents
(certs, contracts: pointers or filenames, never the credentials themselves)

## History

<!--
One person, one note, in 01_Assets/Employees/. That room also absorbs people-rules: a leave
  policy or a handbook section is its own note in the same room, not a new HR room.
Documents with an expiry get renew_by on the note that owns them.
status is active or prospective. A candidate you are interviewing is prospective, and the note
  exists from that first conversation (doctrine §2). Flip it to active on their first day. The
  template ships active; ⛔ do not leave it that way for a candidate, because active is a legal
  value and nothing will ever warn you it is false.
-->
```

## Product-Service.md

```markdown
---
type: product-service
status: active
status_since:
price:
cost:
tags: []
---

# <Product or Service Name>

## What it is

## Pricing (source of truth)

## Specs / recipe pointer
(spec and costing live here; the how-to-make-it steps live in an SOP)

<!--
One offer, one note, in <Brand>-Brand-Assets/Products-Services/ (it belongs to a brand, not
  to the business at large).
This note is the SINGLE source of price truth for the whole vault. A price change is two
  writes in one breath: a decision note recording the change, and this field holding the
  current number. Never one without the other.
-->
```

## Company-Doc.md

```markdown
---
type: company-doc
status: active
status_since:
doc_kind:
renew_by:
issuer:
location_of_original:
tags: [renewal]
---

# <Document Name>

## What it covers

## Renewal notes

<!--
Company-level papers only, in 01_Assets/Company-Docs/. An outlet's own licence lives on that
  outlet's note; an employee's certificate lives on theirs. File by "when something happens,
  where do I look".
renew_by is the ONE expiry key in this vault, on every family that has a deadline. If a date
  means "act before this day", it goes there and nowhere else.
-->
```

## Equipment.md

```markdown
---
type: equipment
status: active
status_since:
model:
purchased:
renew_by:
last_serviced:
tags: []
---

# <Machine Name>

## Manual / supplier pointer

## Maintenance log
- 

<!--
One machine, one note, in 01_Assets/Equipment/ (the room exists only if the equipment toggle
  was on at setup, or it was proposed and approved later).
renew_by carries whichever date actually needs acting on: warranty end, inspection due, or
  certification expiry. It replaced the old warranty_until key, because one expiry key across
  the whole vault is what makes a single renewal radar possible.
-->
```

## Outlet.md

```markdown
---
type: outlet
status: active
status_since:
address:
renew_by:
licenses:
tags: []
---

# <Outlet Name>

## Lease and licenses

## Utilities and accounts

## Notes

<!--
One location, one note, in 01_Assets/Outlets/ (toggle room, same as Equipment).
renew_by carries the lease end, or the earliest licence expiry if that lands first. It
  replaced the old lease_until key: one expiry key, whole vault.
The landlord is a Vendor. The premises is this note.
-->
```

## IT-System.md

```markdown
---
type: it-system
status: active
status_since:
holder:
renew_by:
tags: []
---

# <System Name>

## What it is and what it produces

## Who holds access
(names and roles; ⛔ never a password, never a key. Credentials live in a password manager,
this note holds the pointer to which manager and whose)

## Where its rows live
(the pointer: which tool, which account, who can see it)

## Monthly snapshot
- 

<!--
One system, one note, in 01_Assets/IT-Systems/: POS, accounting software, the domain name,
  the ad account, the workspace.
This is where the rows iron law is enforced in practice. High-frequency rows never enter the
  vault; this note carries the three things that do: a pointer to where they live, exception
  narratives, and monthly snapshots.
renew_by for a domain or a subscription that would actually hurt if it lapsed.
-->
```

## Marketing-Asset.md

```markdown
---
type: marketing-asset
status: active
status_since:
asset_kind:
where_it_lives:
tags: []
---

# <Asset Name>

## What it is

## Where the original lives
(a pointer is a complete capture; the file itself can live in the folder beside this note)

## Why it worked
(if it did. This is the part nobody writes down and the only part worth rereading)

<!--
Reusable output only, in 01_Assets/Marketing-Assets/: the post that worked, the photo set,
  the testimonial, the deck.
Making the content is a project in 02_Work/Grow/ while it runs; what survives the project
  graduates here when it closes. Platform logins and account health live on an IT-System note.
-->
```

## Property.md

```markdown
---
type: property
status: active
status_since:
address:
renew_by:
tags: []
---

# <Property Name>

## The papers and where they are

## Notes

<!--
Personal wing, 03_Personal-Wing/Property/. Business premises are Outlets in the business wing.
renew_by for whatever has a deadline: tenancy end, insurance, assessment.
-->
```

## Vehicle.md

```markdown
---
type: vehicle
status: active
status_since:
plate:
renew_by:
tags: []
---

# <Vehicle Name>

## Papers and where they are

## Service log
- 

<!--
Personal wing, 03_Personal-Wing/Vehicles/. A company vehicle is Equipment in the business wing.
renew_by carries road tax or insurance, whichever falls first.
-->
```

## Brand-Pillar.md

```markdown
---
type: brand-strategy
pillar: DNA
status: empty
---

# <Pillar Name>

<What this pillar holds, one line.>

**Empty cost:** <what stays broken while this is empty.>

> Status: not defined yet. To fill: run the brand intake, or drop in a brand strategy you already have.

Part of <the room this stub sits in, as a wiki link to that room's guide, path-qualified>

<!--
Eight pillars, one family, across TWO folders: seven in <Brand>-Brand-Assets/Brand-Strategy/,
  and Journey in <Brand>-Brand-Assets/Target-Audience/ (it maps the audience, so it files with
  the audience). Type comes from the family, never from the folder.
The "Part of" line points at the guide of the folder this stub is actually in, so the seven and
  the one point at two different doors. It is one line rather than a navigation section: a stub
  is a note, not a directory, and this is the link that keeps eight files from sitting in the
  graph with no relationship to anything, which is what they did until 2026-08-23.
pillar: one of DNA / Personality / Proposition / Relationship / Sensory-Cues / Positioning /
  Style / Journey. Closed list, and a value outside it will not land.
status flips off `empty` the moment the pillar is actually answered. Anything outward-facing
  reads that flag to know whether it is running generic.
-->
```

## Brand-Research.md

```markdown
---
type: brand-research
updated: {{DATE}}
source:
---

# <The question this note answers>

## What it says

## What it means for the pillars

<!--
<Brand>-Brand-Assets/Brand-Research/, the evidence behind the pillars. One note per question,
  and the question is the filename and the title: section 8 declares no list of research
  topics, so the name is the only place the subject is written. Watch the filename law (§5):
  a name like `Findings.md` or `Notes.md` will not land.
updated: the day this was last checked against reality. Nothing reads the date. It is here so
  whoever opens the note can weigh how old the evidence is before building on it.
source: where it came from. Left blank when the answer came from the owner's own knowledge,
  which is evidence too, and is not worth the same as something looked up.
brand: only in a vault holding more than one.
⛔ The pillar wins. Outward-facing work reads the pillar note in Brand-Strategy/, never this
  file. When a pillar changes later, it changes there; this note stays as it was written,
  because dated evidence that gets edited afterwards is worth nothing.
-->
```

## SOP.md

Copied from the `sop-builder` skill's `references/finalize.md` section 3, which is the shape that skill actually writes. ⛔ Do not edit this block independently: two sources for one shape drift, and the vault would end up with hand-written SOPs and skill-written SOPs that do not match.

```markdown
---
type: sop
lane:
owner:
last_verified:
playbook:
tags: []
---

# <What this process achieves>

## When this runs

**Trigger**: <the event that starts it>
**Finished when**: <the test that says it is done>

| # | Step | R | A | C | I | Done looks like |
|---|---|---|---|---|---|---|
| 1 |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |

## Only the owner can do

(one line per step, tagged authority / skill / access. Empty is a finding, not a gap.)

## Special cases

(branches that are real but do not belong in the main line)

## Known unresolved

(raised, not settled. Kept on purpose so the next reader sees it too.)

## Attachments

(the swimlane and any blank forms live in the folder next to this note)

<!--
How to fill this in (only what §8 of the structure doctrine does not already say)

Filename is the process name, plain, in the folder `03_SOP/`. The swimlane HTML lives in
`03_SOP/<Process-Name>/` next to it: this note is the address, that folder is its closet.

lane: multi-value, from the closed list deliver / grow / run / build. A process that serves a
  named customer is deliver; if it would still exist with zero growth, it is run. Leave empty
  only when this vault has no lane model.
owner: the one person who answers for the whole process. This is the A of every row unless a
  row says otherwise, which is why the table does not repeat it.
last_verified: the date someone actually walked the process and confirmed the steps still match
  reality. Not the date this file was edited. A stale date is information; a date bumped by an
  edit is a lie. The day this note is first written IS a real first verification, because the
  owner just walked the whole process out loud in the session that produced it, so put that
  date in rather than leaving the key empty.
playbook: optional. Link it when a step needs a judgment call rather than an instruction.

Every step needs a verb and something visible in the Done column. If a row's Done column is
empty, that row is not a step yet.
Only the owner can do: an empty section means every step has a backup. That is the good outcome,
so write "None" rather than leaving it blank, or the next reader will think it was skipped.
-->
```

## Decision.md

```markdown
---
cb: decision
date: {{DATE}}
status: active
domain:
lane:
supersedes:
---

**Decided:** 

**Why:** 

**Alternatives:** (rejected because )

<!--
One decision, one note, in 02_Command-Base/Decisions/. Filename YYYY-MM-DD-what-was-decided.md,
  and the DATE IS WHEN IT WAS DECIDED, not when it was typed up. A Monday call written up on
  Friday carries Monday.
The set of ACTIVE decisions, filtered by lane, IS the rulebook. "Never discount below 20%" is
  simply a decision that never expires.
status: active / superseded / closed. A rule that got replaced flips to superseded and the NEW
  note names it in `supersedes:` (written once, at birth). A one-off (hire this person, buy that
  oven) flips to closed once executed, so the active set stays a rulebook and not a junk drawer.
domain answers WHO THIS BINDS, not who it is for: a pricing call binds the business, a
  "no work on Sundays" call binds the owner even though the business feels it.
lane is the lane of the work it governs: pricing and offers grow, delivery rules deliver,
  upkeep run, capability bets build.
If it changes a stored value (a price, a term), update that note in the same breath. The
  decision records the change; the entity note holds the current truth.
-->
```

## Task.md

```markdown
---
cb: task
status: not-started
created: {{DATE}}
start:
due:
waiting_on:
depends_on:
priority:
---

What the task is, in the owner's words.

<!--
Filename is the task itself, hyphenated, unique vault-wide (Regime A): Order-the-new-POS.md.
  ⛔ NOT date-first. A task is not a dated record, so §5's YYYY-MM-DD- form does not apply to
  it: its dates live in `created:` and `due:`, and the day it was typed is not what anyone
  searches for. Left unsaid, two sessions name the same task two ways and both are defensible.
Lives in <Project>/Tasks/. A TASK MUST HAVE A PROJECT: if none fits, propose opening one
  (small is fine) before the task exists. There is no parking lot for homeless tasks.
⛔ No project, lane, or domain key. The folder path already carries all three, and a field
  that repeats the path is a field that will one day disagree with it.
status: not-started / in-progress / waiting / blocked / done.
waiting_on names the person or thing; use it with status: waiting so the morning brief can
  say who is being waited on rather than just that something is stuck.
-->
```

## Daily.md

```markdown
---
type: daily
---

# {{DATE}}

## What moved
- 

## Decided
(one line each; the decision note itself lives in 02_Command-Base/Decisions/)

## Observed
- 

## Reflection

<!--
01_Daily/YYYY-MM-DD.md, and it is the ONLY journal in this vault: personal and business share
  it. There is no separate business log.
END OF DAY ONLY, written at compile. Captures through the day land in 99_Meta/capture-buffer.md
  and get drained into here.
Every line links what it belongs to, and that one link is what makes it findable later: a brief
  BARE ([[_Acme-Rebrand-Brief]]), a guide WITH ITS PATH
  ([[04_Acme-Business-Wing/02_Work/Run/_Run-Guide]]). Link once, derive the rest.
The Reflection section is the owner's voice only. Suggest angles, never fill it.
-->
```

## Weekly-Review.md

```markdown
---
type: weekly-review
week_of: {{DATE}}
reviewed_on: {{DATE}}
---

# Week of {{DATE}}

## Headline

## Top 3

1. 
2. 
3. 

## Drifts
(what slipped, what went stale, what the machine pass flagged)

## The week, compressed

## Active theme

## Pool vitals

- Open: 
- Graduated: 
- Expired: 

## What I noticed

Nothing this week.

<!--
02_Command-Base/Reviews/. week_of is the Monday of the week reviewed; reviewed_on is when the
  review actually happened. They differ often enough that one key cannot answer both.
Written at the close of the weekly ritual: the anti-drift half fills everything down to Pool
  vitals, the distillation half writes What I noticed. Two writers, one file, in that order.
Two sections carry a rule the others do not, and both rules exist to keep the file honest:
  HEADLINE is the owner's own words, one line. Ask for it and paste it back as said; never
    write it for them. It is the only sentence in the whole ritual that is not mechanical.
  WHAT I NOTICED is the AI's reading, and it is deliberately not the headline. It ships holding
    "Nothing this week." and THAT LINE IS A FINISHED ANSWER, not a placeholder to clear: a flat
    week is the normal outcome. Never manufacture insight from insufficient material; a section
    that gets padded weekly is a section the owner learns to skip, which costs more than the
    paragraph was worth.
POOL VITALS counts only what 99_Meta/Hypotheses/ can count about itself: open,
  graduated, expired.
There is no "Next week" section: the hook for next week is spoken at the very end of the
  ritual, from next_suggestion: in 99_Meta/capture-progress.md, and a section nobody fills is a
  section nobody reads.
An empty week gets no review at all. A break is covered by the next one, never by a stub.
-->
```

## Monthly-Theme.md

```markdown
---
type: monthly-theme
month: {{DATE}}
status: active
status_since: {{DATE}}
---

# <Theme>

Follows <the theme this one replaces, as a wiki link; delete this line if this is the first one>

## Why this, this month

## What it means in practice

<!--
02_Command-Base/Reviews/. One theme at a time; the previous one flips status to closed before a
  new one opens, so "what am I on right now" always has exactly one answer. The trigger is the
  new theme opening, not the calendar turning: a theme can stay active across a skipped month
  and get closed later, and status_since records the day the flip actually happened.
The two link lines are what make this layer read as a line rather than a pile. A new theme
  opens with "Follows [[previous]]"; in the same breath, the theme it replaces gets
  "Followed by [[new]]" written under its own title as its status flips to closed. Both
  directions, written at the one moment when whoever is doing it knows both names.
  The first theme in a vault has nothing to follow: delete the line rather than leave it
  pointing at nothing.
Who opens one: the theme check at the close of the weekly review (the anti-drift half of the
  weekly ritual). It only ever proposes; the theme is the owner's word for their own month.
-->
```

## Lesson.md

```markdown
---
type: lesson
date: {{DATE}}
source:
lane:
confirmed_by_owner: false
tags: []
---

# Lesson: <one line>

## What happened

<!-- HISTORY. ⛔ Never edited again. What happened happened; a corrected past is not a
     record, it is a story. Wrong facts get a correcting sentence here, never a rewrite. -->

## What we now do differently

<!-- ALIVE. This is the part that gets edited, and there is exactly one reason to edit it:
     the world changed and the old handling stopped working. ⛔ If the reason is that YOU got
     better at this, that is not an edit here, that is a Method (§7). Mixing the two is how a
     lesson quietly turns into a half-written playbook nobody trusts. -->

<!--
04_Methodology/Lessons/, grouped in a subfolder when a string of pits shares a subject
  (one folder for a tool, a client, a platform).
A lesson is a PIT: something that actually hurt, written down so it never surprises twice.
  Not a good idea, not a note-to-self.
⛔ Capture never writes here. It lands at the CLOSEOUT of the session the pit happened in,
  with the owner saying yes in that moment, which is what confirmed_by_owner records
  (doctrine §8: the owner who was in the room, out loud, then). Until that flag is true,
  this note is a proposal sitting in a draft, not a lesson.
date is when the pit happened, not when it was written up.
-->
```

## Method.md

```markdown
---
type: method
lane:
status: active
confirmed_by_owner: false
tags: []
---

# Method: <the kind of work>

## When I reach for this

## How I do it

## What I judge along the way

<!--
04_Methodology/Playbooks/, flat, beside the playbooks. A method is ONE MOVE OF YOURS: how
  you personally do one kind of work, written at the closeout of the work that taught it,
  with the owner saying yes in that moment (that is what confirmed_by_owner records).
Named for the WORK, never for the case it came out of: <the-work>-method.md. "quoting-a-
  renovation-method.md", not "the-tan-house-method.md". A name that records which case,
  client or project it belongs to becomes a lie the day that moves (doctrine §5).
⛔ Same name, same file. Found a better way? Rewrite this note whole. ⛔ Do NOT create a
  second file with a version in the name: one note per move is what lets the note carry how
  many times you have done this without anybody counting anything.
⛔ There is no kind: key and there will not be one. Which sort of work a method belongs to
  is judged by whoever reads several of them together in the weekly distillation, not
  declared by whoever writes one. Declaring it would put the classification burden on the
  moment you least want it, which is the moment you just finished the job.
status: flips to superseded when the weekly distillation composes this and its relatives
  into a playbook; distilled_into: then names that playbook. Superseded methods are never
  deleted: "which fights did this playbook come out of" has to stay answerable.
-->
```

## Playbook.md

```markdown
---
type: playbook
lane:
status: forming
confirmed_by_owner: false
references: []
tags: []
---

# Playbook: <the kind of work>

## When to run it

## What to weigh

## The moves

<!--
04_Methodology/Playbooks/. A playbook is JUDGMENT COMPOSED: what to weigh and how to decide
  for a kind of work. An SOP is the other thing entirely, dead steps anyone can follow.
It is EARNED in the weekly distillation, when several related methods turn out to be one way
  of working. Those methods flip to status: superseded and carry distilled_into: pointing
  here, so the fights this came out of stay traceable.
references: is written ONCE, right here, at birth: the lessons and decisions this playbook
  leans on. ⛔ Leave it as an empty list when there are none. ⛔ Those notes never register
  that they were cited; a back-list would have to be revisited forever (doctrine §7).
⛔ Types do not transmute. A playbook does not "mature into" an SOP and an SOP does not
  "grow into" a playbook. Only methods BECOME a playbook; lessons and decisions are only
  ever referenced by one. What travels between them otherwise is content: playbooks and
  lessons inform the next SOP someone writes.
Prose is the normal, sufficient form of a playbook. A few earn a live feedback loop and grow
  into a folder with lab organs beside them, in place, no move and no link rewrites. That is
  rare, it is asked for by the owner, and the default answer is no.
-->
```

## Hypothesis.md

```markdown
---
type: hypothesis
status: open
destination: profile
weeks_supported: 0
weeks_silent: 0
---

# <The claim, in one sentence>

## Evidence
- <verbatim quote> · <session pointer>

<!--
99_Meta/Hypotheses/. ⛔ MAINTENANCE'S DISTILLATION HALF WRITES IT. Nothing filed by hand ever
  lands here, and this template exists so the shape is legible, not as an invitation.
  session-report writes it too, at a session's closeout; the anti-drift half only reads it.
The pool is where maintenance parks a claim it has noticed but not yet earned. It graduates
  out on evidence, and evidence means a verbatim quote plus a pointer to where it was said,
  which is why evidence lives in the body where it can be checked rather than in a key.
⛔ This is not an idea box. An idea with no observed instance behind it is an aspiration.
⛔ A lab's bets are NOT hypotheses. Those live in that lab's register, they are the owner's
  own, and they are read every time. This pool is the machine observing the owner, and it
  never enters a session's context.
status: open / expired / graduated / rejected.
destination: profile, and that is the whole list. It answers where this lands IF it graduates,
  and the pool has exactly one landing point: a pattern about the owner that only observation
  could establish. Anything true the moment it is said lands the day it happens instead.
-->
```

## Rubric.md

```markdown
---
type: rubric
updated: {{DATE}}
---

# <Name> Rubric

## <Criterion 1: the hard business signal>
<what a pass looks like, in one line anyone can apply in seconds>

## <Criterion 2>
<what a pass looks like>

## Does this sound like us?
<the identity veto, in one line: what "us" sounds like on this line of work. A no here
overrides every number above.>

<!--
`04_Methodology/Playbooks/<Name>/<Name>-Rubric.md`, one per lab (doctrine section 9.2).
It is the one organ interviewed into existence when the lab opens, by the `playbook-lab`
  skill. At most 2 to 3 criteria, at least one hard business signal (money, enquiries,
  orders, bookings, retention), and the identity veto above.
Score the market's behaviour, never a friend's politeness: "did anyone act on it" beats
  "did people like it".
The scoring test: 30 seconds per output. If applying this to one output takes longer, cut a
  criterion; a rubric that takes real thought gets applied twice and then abandoned.
Cards are disposable, the file is permanent: rewrite a criterion in place rather than opening
  a second rubric.
Scores do not live here. They live with the outputs they score.
updated: the day a criterion last changed, not the day something was last scored.
-->
```

## Lab-Register.md

```markdown
---
type: lab-register
updated: {{DATE}}
---

# <Name> Register

| Opened | The bet | Which part of the playbook it tests | What would settle it | Verdict |
|---|---|---|---|---|
| {{DATE}} | <one sentence> | <the chapter or move> | <the condition> | open |

<!--
`04_Methodology/Playbooks/<Name>/<Name>-Register.md`, one per lab (doctrine section 9.2):
  the ledger of live bets this lab is running. It ships empty and correctly shaped.
Every row names which part of the methodology it tests AND the condition that would settle
  it, and that condition is written when the bet opens, before the evidence arrives.
A lab's bets are NOT the hypothesis pool in `99_Meta/Hypotheses/`. These are the owner's own
  and they are read every time the lab is opened; that pool is the machine observing the
  owner and it never enters a session's context.
Rows are disposable, the file is permanent: a settled bet keeps its row and its verdict.
updated: the day a bet opened or resolved.
-->
```

## Thresholds.md

```markdown
---
type: thresholds
updated: {{DATE}}
---

# <Name> Thresholds

| Trigger line | Default | This lab | What it fires |
|---|---|---|---|
| <the signal that says the playbook needs revising> | <shipped default> | <the owner's number> | a proposal to revise the playbook |

<!--
`04_Methodology/Playbooks/<Name>/<Name>-Thresholds.md`, one per lab (doctrine section 9.2).
Ships with defaults and is owner-tunable: the defaults are a starting line, and a number
  nobody can move is a number everybody ignores.
A threshold firing is a PROPOSAL to revise the playbook, never an edit. The owner's yes is
  what revises the authority file, and everything downstream follows because SOPs link the
  playbook by `playbook:` (doctrine sections 9.3 and 9.7).
Rows are disposable, the file is permanent.
updated: the day a line was last tuned.
-->
```

## Resource.md

```markdown
---
type: clipping
source:
tags: []
---

# <Title>

## The point

## Why I kept it

<!--
02_Command-Base/Resources/, in the matching subfolder (Clippings, Courses, Books, Prompts,
  Tools). type is one of clipping / course / book / prompt / tool-note.
Study lands here. Realization lands in 04_Methodology, and the difference is the owner saying
  "yes, that is now how I operate". Keeping an article is not learning a lesson.
ATTENDING a course, as an undertaking with a start and an end, is a project in 02_Work/Build/.
  The artifact here and the project there are two homes on purpose.
-->
```
