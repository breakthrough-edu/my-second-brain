---
type: doctrine
created: {{DATE}}
last_updated: {{DATE}}
maintained_by: the owner (AI proposes amendments, owner approves)
---

# Structure Doctrine

> The constitution of this vault. Every filing decision, by human or AI, follows this file. Any skill or session that touches structure reads this first. Rules live here, in the vault, so they never drift with tool versions.
>
> Amendments follow the same discipline as everything else here: proposed, approved by the owner, then written.

## 1. The shape of the house

One vault, two wings, one home.

- **Personal wing** (`02_Projects` / `03_Areas` / `04_Resources` / `05_Archive`): sorted by **actionability** (the PARA logic). Time-bounded with a deliverable is a Project; ongoing with no end date is an Area; reference material is a Resource; done or dormant is Archive.
- **Business wing** (`07_<Business-Name>/`): sorted by **knowledge type**, three layers:
  - `01_Assets`: what the business is made of (facts, records, materials)
  - `02_SOP`: how things get done (processes)
  - `03_Methodology`: why decisions go the way they go (judgment)
- **Shared rooms**: `00_Inbox` (capture anything, sort later), `01_Daily` (personal timeline), `06_Command-Base` (the OS command center), `99_Meta` (system files).
- A second business becomes `08_<Name>/`, same internal shape.

## 2. The two sorting axes (the master rule)

**Processes are sorted by intent. Assets and records are sorted by ownership.**

- A room in `02_SOP` answers "what does this process achieve?" (onboarding a hire, collecting payment, handling a complaint). Who executes it is irrelevant to where it files; that lives in metadata.
- A room in `01_Assets` answers "who or what is this about, or which function uses it?" Entity rooms hold facts about people and things; function rooms (Marketing, Sales, Finance...) are the home address for each function's materials, logs, and reports. Function names on asset rooms are addresses, not a department taxonomy.
- Department views, when needed, come from the `function:` frontmatter field plus dashboard views, never from folders.

### Layer 1 filing test sentence

**About someone or something -> entity room. Used by a function -> function room.**

### Layer 3 has two inlets, and capture is not one of them

- Decision patterns, distilled from the central Decisions room -> `Decision-Rules/`
- Hard-won lessons, from clippings studied or potholes hit -> `Lessons/`
- Repeatable multi-step plays -> `Playbooks/`. When a playbook matures until every step can be written down and delegated, it demotes INTO an SOP. When an SOP keeps producing the same pothole, the pothole distills UP into a Lesson. The three layers are a living loop, not three drawers.
- **Study lands in Resources, realization lands in Methodology.** Generic learning material goes to the personal wing (`04_Resources`); industry intel serving one function goes to that function room; only owner-confirmed judgment enters Layer 3.

## 3. Iron laws

1. **Rows live in systems, not in the vault.** High-frequency transactional records (invoices, POs, delivery orders, POS receipts, attendance, temperature logs) belong in the tools built for them (POS, accounting software, payroll system, spreadsheets). The vault stores: a pointer to where the rows live, exception narratives, and monthly snapshot summaries. Without this law the vault grows into a shadow ERP and dies within a quarter.
2. **How-to lives in Layer 2, always.** A function room never holds a procedure. Materials, logs, status, reports: yes. Steps for doing something: SOP room, with a `function:` tag.
3. **Blank template vs filled record.** A blank form or checklist is an SOP attachment (Layer 2). A filled-in record is function-room material (Layer 1), and if it is high-frequency, iron law 1 applies and it stays out entirely.
4. **One thing, one note.** One client, one note. One machine, one note. One decision, one note. A note that outgrows itself upgrades into a folder of the same name; the main file keeps its name.
5. **A folder earns its place.** Start with notes lying flat in the room. Only when three or more notes cluster around one entity does that entity get its own folder.
6. **Decisions have exactly one home**: `06_Command-Base/Decisions/`, one decision per note, `domain:` (personal or the business name) and `function:` both required. Wing dashboards pull their own view by domain filter. The tag question is: **who does this decision bind, not who it is for.**
7. **Passwords never enter the vault.** `Operations/IT-Systems/` holds account inventories and system notes; credentials live in a password manager, the vault holds pointers.
8. **AI output and owner capture do not mix silently.** Distillation proposals are approved in-session or staged; they never slide into rooms as if the owner wrote them.

## 4. Fractal MOC rule

Every folder with content gets a front desk: `_<Name>-MOC.md` (underscore keeps it pinned on top; the unique name keeps wikilinks unambiguous).

- A MOC is a **build artifact**: the AI may rebuild it wholesale at any time. It carries `last-refreshed:` in frontmatter.
- Contents: one door-sign line (what lives in this room), the filing test sentence for the room, the current inventory (links), key numbers if any, and navigation links up (parent MOC) and down (child MOCs).
- Capture and maintenance sessions refresh the MOCs they touched. Room-level insights live on the room's MOC, so the front desk gets richer as the room fills.
- **Exception:** the three `03_Methodology` rooms carry no MOC while empty. The empty layer is meant to be felt, not furnished.

## 5. Naming and format

- Folder names, file names, frontmatter keys: **English**, hyphenated, no spaces.
- Daily notes `YYYY-MM-DD.md` (personal in `01_Daily/`, business in `07_<Business>/00_Daily-Log/`).
- Dates in frontmatter: `YYYY-MM-DD`, unquoted. Multi-word keys use `underscore_case`.
- Wikilinks `[[...]]` resolve by file name vault-wide, so files can move without breaking links. Keep note names unique enough to link cleanly.

## 6. Tag discipline

- The controlled vocabulary lives in `99_Meta/tagging-vocabulary.md`. Only tags on that list get used.
- A new tag is proposed (text + definition + boundary), approved by the owner, added to the vocabulary FIRST, then used. Same protocol for new frontmatter enum values.
- Off-list values silently fall out of every dashboard view. The vocabulary file is load-bearing.

## 7. Filing log

Every AI filing action appends one line to `99_Meta/filing-log.md`: date, what, where it went, which rule or ruling decided it. Append-only. This is the audit trail that lets any filing be reviewed and reversed, and it is what keeps filing consistent across sessions instead of drifting with the mood of the model.

## 8. Canonical rulings table

Precedents for the two-way calls. When a filing matches a row here, follow the ruling; do not relitigate. When a genuinely new conflict appears, decide it with the owner and add the row.

| Conflict | Canonical ruling |
|---|---|
| Product spec vs production process (recipe, work instruction) | Spec + costing -> `Products-Services/` (one product, one note); how-to-make-it steps -> SOP |
| Blank template vs filled record | Template -> SOP attachment; filled record -> function-room monthly summary; high-frequency rows -> stay out of the vault (iron law 1) |
| Staff roster / shift schedule | `Operations/` (running the operation); employment lifecycle matters -> HR / `Employees/` |
| Payroll | `HR/Payroll/` (function ownership); statutory payment proofs -> pointer in Finance |
| Delivery / e-commerce platforms (Grab, Shopee...) | Platform as an entity (contract, contacts, commission terms) -> `Vendors/`; account health / penalty scores -> `Marketing/<platform>/`; settlement reconciliation -> Finance |
| Pricing material | Product definition + pricing source of truth -> `Products-Services/`; outward-facing channel price lists -> `Sales/` |
| KOL / freelancer | On payroll -> `Employees/`; invoices you -> `Vendors/` with `role: freelancer` (dashboards can merge views) |
| Case study / testimonial | Case study -> `Marketing/`; testimonial -> client note + pointer in Marketing |
| Lead lifecycle | Before closing, one deal one note -> `Sales/Pipeline/`; on closing -> promote to `Clients/` entity + open an engagement folder (`04_Projects/`) |
| Proposal / quotation / SOW | Pipeline stage -> `Sales/Pipeline/`; on closing, the engagement folder holds the canonical copy; Finance and the client note keep pointers |
| Closed engagement | Four-way distribution: final deliverables pointer -> client note; case study -> Marketing; testimonial -> client note; retro -> `Lessons/` after owner confirms |
| Company-level insurance / licenses / trademarks | `Company-Docs/` (file by "where do I look when it matters", `renew-by:` required) |
| Certificates, by level | SKU-level cert -> the product's note; company-level -> `Company-Docs/`; cross-SKU master list -> `Operations/` |
| Client-provided assets / platform access | Registered on the client note; work materials -> the engagement folder; security-relevant account inventory -> `Operations/IT-Systems/` |
| Aging stock / slow-mover / menu-engineering analyses | Report -> the owning function room's reports; conclusions promote to Methodology only after the owner rules |
| Complaints / reviews / returns | Handling actions -> `Customer-Service/`; ratings rollup -> Marketing; return logistics -> Operations |
| Credit-approval-type decisions | `06_Command-Base/Decisions/` (domain + function); the client note carries only the current terms |
| Employee personal documents (certs, vaccination, warning letters) | `Employees/<name>.md`; policies / handbook / JD -> `HR/` |
| Privacy policy / NDA | Privacy policy -> `Company-Docs/`; outward templates like NDAs -> `Sales/Templates/` |
| Learning material vs business intel | Generic learning -> personal wing `04_Resources`; function-specific industry intel -> that function room; distilled personal doctrine -> Methodology after owner confirms |

## Revision log

- **{{DATE}}**: v1, written at vault setup.
