# Room Guides: every room's door, and the business rooms' question sets

For each room: the door sign (also used on its `_<Name>-Guide.md`), the filing test, and, for the business rooms, the guided question set and insight angles. Ask ONE question at a time; every question is answerable by talking for 20 seconds. 3 to 5 items is a full first capture. Insight formula and honesty rules live in capture mode Stage 4; the angles here are raw material for it, not scripts.

`01_Assets` is what the business is **made of**. Work that is moving lives in `02_Work/` and has its own reference ([work-lanes.md](work-lanes.md)). There are no function rooms in this vault: this house has no departments, so nothing files by which department would own it.

⭐ **Every room scaffold builds has its door sign and filing test in this file or in [work-lanes.md](work-lanes.md), and setup copies them rather than writing its own.** The business rooms are below; the personal wing's seven doors and the `Resources/` door are in the last two sections, and those carry no question set on purpose (capture never interviews them: personal rooms fill as life happens, and the library fills as things are saved). ⛔ Never improvise a door sign at install time. A door file is read every time anyone works in that folder, so two installs that invent two sets of door signs have built two different products.

---

## The brand folder: `<Brand>-Brand-Assets/`

One folder per brand, holding three rooms: `Brand-Strategy/`, `Target-Audience/`, `Products-Services/`. A single-brand business has exactly one, named after the business; ask which brand something belongs to only when a second one exists.

**Door sign** (for `_<Brand>-Brand-Assets-Guide.md`, the folder's own door): everything that makes this brand this brand: what it stands for (`Brand-Strategy/`), who it is for (`Target-Audience/`), and what it sells (`Products-Services/`).
**Filing test:** an answer ABOUT the brand files in one of the three rooms below; the reusable output that expresses the brand (the post, the photo set, the deck) lives in `Marketing-Assets/`; the METHOD for doing brand work lives in `04_Methodology/`.

⚠️ **`guide_family` on these four doors, because the two sources read differently and the doctrine wins.** §8's own comment defines `brand` as "a subfolder of `<Brand>-Brand-Assets/`", so all three subfolders (`Brand-Strategy/`, `Target-Audience/` **and** `Products-Services/`) carry `guide_family: brand`. The `<Brand>-Brand-Assets/` folder itself is not a subfolder of one, it IS one, and doctrine §1 lists it among the entity rooms of `01_Assets/`, so its own door carries `guide_family: room`.

### Brand-Strategy and Target-Audience (filled by intake, not by interview)

These two rooms are unlike the rest. They scaffold pre-populated with empty stubs (see [scaffold-spec.md](scaffold-spec.md)), and they are **not** captured through a question battery. Brand work is a deliberate exercise, not a 20-second answer, so capture uses a **light gate**, not an interview.

**Brand-Strategy door sign:** your brand foundation, seven of the eight pillars (Positioning, DNA, Personality, Proposition, Relationship, Sensory Cues, Style).
**Target-Audience door sign:** who this brand is for, drawn sharply enough to repel who it isn't, plus the customer journey (the eighth pillar).
**Filing test:** descriptive brand identity (what the brand IS) lives in `Brand-Strategy/`; who it is FOR, and the journey they travel, lives in `Target-Audience/`; the METHOD for doing brand strategy lives in `04_Methodology/`; how to PRODUCE branded content is an SOP.

⚠️ All eight pillars are one family (`type: brand-strategy`) even though they sit in two folders. Type comes from the family, never from the folder.

**The light gate (one question, at Business-Profile close):** "Do you have a formed brand strategy already?"
- **Yes** → guide them to drop it in; map what they have onto the eight stubs, fill what fits, leave the rest `status: empty`.
- **No** → leave the stubs empty and say plainly (once, no pitch): the rooms stay as seeds; marketing and sales run generic until they are filled, and that is a real cost, not a nag. Do not run a brand-strategy exercise inside capture; that work has its own home.

**Insight angle (the only one):** which stubs are still `status: empty`, and the most expensive one to leave empty given what the Business-Profile already said (a differentiation-led business with an empty Brand-DNA, say). Name it, do not fix it.

### Products-Services

**Door sign:** what this brand sells. One offer, one note: definition, pricing source of truth, spec pointers.
**Filing test:** spec and costing live here, and this note is the **single source of price truth**; how to make or deliver it lives in `03_SOP/`; a price CHANGE is a decision note plus an update here, in the same breath.

**Questions:**
1. List what you sell, top of head. (just names first)
2. Which one makes the most money? Which one do you sell the most of? (they often differ; note both)
3. For your main offer: price, and roughly what it costs you? (skip cost if not known offhand; note "cost unknown" as a fact)
4. What is the cheapest thing someone can buy from you? The most expensive?
5. Anything you sell that you privately wish you could stop selling?

**Insight angles:**
- The price ladder: cheapest vs dearest gap, missing middle rungs, no entry offer, no premium tier.
- Volume vs margin split: the best-seller and the best-earner are different products and get the same attention.
- Zombie offers: the thing still on the menu that nobody has bought in months (and what keeping it costs).
- Cost blindness: "cost unknown" showing up on the main offer is itself the observation.

---

## Clients

**Door sign:** the people and companies who pay you. One client, one note.
**Filing test:** facts about a specific client live here; how you win or serve clients lives in `03_SOP/`; a job you are doing FOR them (pursuit through delivery) is one project in `02_Work/Deliver/`.

**Questions:**
1. Think of your three most important clients right now. Who is first? (name is enough to start)
2. What do they buy from you, and roughly how often?
3. How did they find you? (referral, walk-in, ads, an old colleague...)
4. Anything about them a new staff member should know before talking to them? (temperament, payment habits, history)
5. Same for the second client... (repeat 2 to 4 per client, lighter each round)
6. Of everyone who pays you, roughly what share came through someone recommending you?

**Insight angles:**
- Source concentration: how many of the named clients arrived by referral, and does any mechanism exist for that? (the classic: referrals happen TO the business, nobody runs them)
- Dependency: does one client dominate revenue or attention? What does the map look like if they leave?
- Knowledge location: how much of what was just captured lived only in the owner's head? Who else knows client X pays 60 days late?
- **The complaint that keeps coming back in different costumes.** If the owner describes the same failure repeating across customers, that is a process gap wearing a service costume: record it on the client note it happened to, and **say out loud that it is a pattern** so it gets written up as a Lesson at this session's closeout. ⛔ There is no flag to leave for a later sweep. ⛔ Do not open a complaints room either; there are no function rooms here.

## Vendors

**Door sign:** everyone you buy from or depend on to deliver. One vendor, one note. Landlords, lessors and platforms you sell through are vendors too.
**Filing test:** the vendor as an entity (contract, contacts, terms) lives here; the purchasing process lives in `03_SOP/`; a platform's account health and login custody lives in `IT-Systems/`.

**Questions:**
1. Who are the three suppliers or service providers your business cannot run a week without?
2. For the first: what do they supply, and on what terms? (credit days, MOQ, anything unusual)
3. If they disappeared tomorrow, what happens? Is there a backup?
4. Who is the actual human you contact there?
5. Any history worth recording? (a price hike, a quality incident, a favor owed)

**Insight angles:**
- Single point of failure: which vendor has no backup, and how core is what they supply?
- Terms asymmetry: are clients paying the owner slower than the owner pays vendors?
- Relationship equity: which vendor relationship is personal to the owner alone? (walks out with the owner's phone)

## Employees

**Door sign:** your people, one per note: role, scope, documents, history. The room also absorbs people-rules: policies, JDs, handbook material.
**Filing test:** facts about a specific person live on their note; rules that apply to everyone live in this room as their own note; how you onboard anyone lives in `03_SOP/`.

**Questions:**
1. How many people, and who has been here longest?
2. Take your key person: what do they actually do? (the real scope, not the title)
3. What can they do that nobody else in the company can?
4. Any documents that matter? (contract, certs, work permit; pointers are enough)
5. Anyone you worry about losing, and why?
6. Do written rules exist anywhere? (leave, lateness, claims; "in my head" and "we follow feel" are honest captures)
7. When someone new joins, what exists to hand them? (anything written, or person-shadowing only)

**Insight angles:**
- Hidden single points of failure: which capability lives in exactly one head (often the owner's own)?
- Title vs reality gaps: the "admin" who actually runs operations.
- Succession blanks: longest-serving person's knowledge, where is it written? (usually nowhere, which is exactly what `03_SOP/` is for)
- Rules by folklore: policy exists only as precedent memory, so every dispute is relitigated from scratch.

## IT-Systems

**Door sign:** the systems the business runs on, one system one note: what it is, who holds the login, what it produces. Passwords never enter the vault (iron law 2), only pointers to where they live.
**Filing test:** a system or account lives here; the rows that system produces (invoices, POS lines, ad spend) stay in the system, and this note carries the **pointer plus the monthly snapshot**; the vendor contract behind the system lives in `Vendors/`.

**Questions:**
1. What systems and accounts does the business run on? (POS, accounting software, Google Workspace, the domain name, the ad account...) Who holds each login?
2. Where do the passwords live? (if the answer is "my head" or "a notebook", capture the fact and recommend a password manager; ⛔ do NOT capture the passwords)
3. Any account states worth recording? (who is admin of the FB page, a penalized platform account, a dormant account with followers)
4. Which of these systems produces numbers you actually look at, and how often?

**Insight angles:**
- Account custody: the domain name, POS admin or ad account registered under someone's personal email, sometimes an ex-staffer's or an old agency's. This is the cheapest catastrophic risk in the whole vault to find and the cheapest to fix.
- The absence map: which daily operations break when one specific person is away. Usually the owner's first sight of their true bus factor.
- Measurement void: money moving through a system whose numbers nobody ever reads. The monthly snapshot this room invites is the smallest fix with the biggest sight gain.

⚠️ **Rows watch, hardest here.** If the owner starts reading out transactions, stop warmly and capture three things instead: where the rows live, who can see them, and what the monthly summary should say. The vault holds pointers, exception stories, and snapshots. Nothing else (iron law 1).

## Marketing-Assets

**Door sign:** marketing output the business owns and can reuse: posts that worked, photos, videos, testimonials, brochures, decks, plus channel notes and reports.
**Filing test:** the reusable asset or a pointer to it lives here; producing content is a `02_Work/Grow/` project while it runs; the process for producing it lives in `03_SOP/`; platform logins and account health live in `IT-Systems/`.

⚠️ The room is named for what it **holds**, not for a department. There is no Marketing room in this vault, because `Marketing` alone reads as an activity and activities live in `02_Work/`.

**Questions:**
1. Where does your content live right now? (phone gallery, FB page, a designer's Google Drive...)
2. Which single piece brought the most business? (a viral post, one photo, a review)
3. Do you have testimonials or reviews anywhere? Where?
4. Where do customers actually hear about you today? (name the real channels, not the aspirational ones)
5. Which channel do you spend money on, and roughly how much a month? Which channel do you spend TIME on, and whose time?
6. If a new designer joined tomorrow, what would you hand them so output looks like your brand? (logo files, colors, past examples; pointers are fine)

**Insight angles:**
- The one-hit wonder: the best-performing piece was never repeated or systematized. Why it worked was never written down.
- Asset scatter: assets living in N places including ex-staff accounts; a pointer inventory is tonight's honest win.
- Testimonial leakage: praise exists in chats and reviews but is captured nowhere reusable.
- Spend vs attention mismatch: money on channel A, time on channel B, belief in channel C.

## Company-Docs

**Door sign:** the company's own papers: registration, licenses, insurance, trademarks, the company-level lease. Each with a `renew_by` date.
**Filing test:** file by "when something happens, where do I look": company-level docs here; outlet-specific licenses on that outlet's note; employee documents on the employee's note.

**Questions:**
1. Company registration: where is the actual document right now? (drawer, accountant, cosec; a pointer is the capture)
2. What licenses does the business hold, and when does each expire? (top of head is fine, mark "to confirm" freely)
3. Any insurance on the business? (fire, liability, vehicles) Who is the agent?
4. Trademark or brand registration: exists, in progress, or never done?
5. Who gets the renewal reminder today, and what happens if they miss it?

**Insight angles:**
- The renewal single-thread: every expiry date lives in one person's memory (or one agent's goodwill). The `renew_by` fields just captured are the first backup that ever existed.
- "To confirm" density: how many license dates the owner could not name is itself the map of exposure.
- Trademark gap for a brand the owner says differentiates them.

## Equipment (toggle: machines)

**Door sign:** your machines, one per note: manual pointer, service history, inspection certs.
**Filing test:** the machine as a thing lives here; how to operate or maintain it lives in `03_SOP/`; keeping it serviced week to week is `02_Work/Run/`.

**Questions:**
1. Which machine, if it died this morning, hurts the most?
2. For that one: brand and model? When bought, roughly?
3. When was it last serviced, and by whom? Is there a schedule, or "when it makes noise"?
4. Where is the manual? Any certs or inspections it needs, with dates? (those dates are `renew_by`)
5. Any machine already half-dead that everyone works around?

**Insight angles:**
- Reactive maintenance: no schedule exists; service happens at breakdown. The service log started tonight is the schedule's seed.
- Tribal operation: only one person can run or fix the critical machine.
- The workaround tax: the half-dead machine everyone quietly routes around, never costed.

## Outlets (toggle: physical locations)

**Door sign:** one outlet, one note: lease, licenses, utilities, quirks.
**Filing test:** facts about the place live here; how to open and close it daily lives in `03_SOP/`; company-level (non-outlet) documents live in `Company-Docs/`; the landlord lives in `Vendors/`.

**Questions:**
1. How many locations? Take the main one: address, and when does its lease end? (that date is `renew_by`)
2. What licenses hang on that outlet specifically, and when do they expire? ("to confirm" is a fine answer)
3. Utilities and accounts tied to the location: whose name are they under?
4. Anything about this location a new manager must know? (parking chaos, the landlord's temper, the aircon trick)
5. Same pass, lighter, for the next outlet.

**Insight angles:**
- Lease cliff: lease end vs licenses vs renovation investment, seen on one timeline for the first time.
- Name entanglement: utilities or licenses under a personal name or a landlord arrangement that would not survive a transfer.
- Quirk knowledge: the operational quirks just captured lived in zero documents; that is the difference between an outlet and a franchise-able outlet.

---

## Where the money questions went

There is no Finance room. Money lives in the systems built for it, and the vault holds three things about it, all of them on the `IT-Systems/` note of the system that produces the numbers: **a pointer** to where the rows live, **exception narratives**, and **monthly snapshots** (iron law 1). A money DECISION is a decision note in `02_Command-Base/Decisions/`, never a room entry.

Two money questions belong in the `IT-Systems/` pass, because they are about sight, not about rows:

- "When did you last see a P&L, and did you believe it?" (the believability gap: books exist but the owner decides by glancing at the bank balance)
- "Is there a number you wish you knew every Monday morning?" (capture it verbatim; it is the owner's own design brief for what any future dashboard should surface)

---

# The personal wing: `03_Personal-Wing/`

Seven doors plus the wing's own, all created at setup, no question asked (doctrine §1 states the wing's contents flatly, so a vault missing them does not match its own law). ⛔ **No question set here, and that is deliberate:** capture interviews the business because the owner came to move a business in, and a battery of questions about their family on night one is an interrogation, not a payoff. These rooms fill the day something actually happens.

⚠️ The test that separates this wing from the business wing is **whose thing it is**, never what kind of thing it is: the same object files on both sides depending on who owns it. A company van is `01_Assets/Equipment/`; the owner's car is `Vehicles/`. Business premises are `01_Assets/Outlets/`; the owner's house is `Property/`.

## The wing door (`03_Personal-Wing/_Personal-Wing-Guide.md`, `guide_family: wing`)

**Door sign:** your life outside the business: what you are running for yourself, and six rooms for the things a life accumulates.
**Filing test:** if it is yours rather than the business's, it files on this side; the same paper on the business's side files in the business wing; a personal call you want to hold yourself to is still a decision note in `02_Command-Base/Decisions/`, carrying one of the personal lanes.

## Personal-Projects

**Door sign:** the things you are running for yourself that have an end. One project, one folder, with its own brief.
**Filing test:** personal work with a finish line lives here as a project; a standing fact about your life lives in one of the six rooms below; anything the business is doing belongs in a `02_Work/` lane, even when you are the only one doing it.

## Family

**Door sign:** the people closest to you, one per note, plus the household papers and dates that belong to no one person.
**Filing test:** someone you are related to or live with files here; a friend, mentor or professional you deal with as yourself is `People/`; anyone the business pays or is paid by files in the business wing.

## Health

**Door sign:** your health and your household's: conditions, medications, providers, policies, and the dates any of it renews.
**Filing test:** anything a doctor or an insurer would ask about files here, with `renew_by` on whatever expires; an employee's medical benefit is a people-rule and lives in `01_Assets/Employees/`.

## Finance-Personal

**Door sign:** personal money: accounts, policies, loans, and where each statement actually lives. Pointers and snapshots only.
**Filing test:** money that is yours files here; money that is the business's stays in the system that produces it and is pointed at from `01_Assets/IT-Systems/`; ⛔ rows and passwords enter neither side (iron laws 1 and 2).

## Property

**Door sign:** places you own or rent for yourself: the papers, the dates, the quirks. One property, one note.
**Filing test:** a home or a personally-held property files here; business premises are `01_Assets/Outlets/`; the tenancy end, the insurance or the assessment date is `renew_by`.

## Vehicles

**Door sign:** your cars and bikes: papers, service history, and the dates that must not lapse.
**Filing test:** a vehicle you own personally files here; a company vehicle is `01_Assets/Equipment/`; road tax and insurance, whichever falls first, are `renew_by`.

## People

**Door sign:** people who are neither family nor a business relationship: friends, mentors, the doctor, the person who fixes things. One person, one note.
**Filing test:** someone you deal with as yourself files here; a relative is `Family/`; a client, vendor or employee files in the business wing, in the room that names the relationship.

---

# The library: `02_Command-Base/Resources/`

## Resources

**Door sign:** what you saved to read, study or reuse, on five shelves: `Clippings/` `Courses/` `Books/` `Prompts/` `Tools/`.
**Filing test:** the artifact you kept files here (the article, the course notes, the prompt); what you now DO differently because of it is a lesson or a playbook in `04_Methodology/`, and it only gets there when you say so. ⚠️ ATTENDING a course, as an undertaking with a start and an end, is a `02_Work/Build/` project while the notes stay here: two homes, on purpose (doctrine §2).

⛔ The five shelves ship as folders and get **no doors of their own**: the shelf name is the whole explanation, and one door per room already covers them.
