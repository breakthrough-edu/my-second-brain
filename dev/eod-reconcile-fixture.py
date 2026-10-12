#!/usr/bin/env python3
"""
eod-reconcile-fixture.py - builds the throwaway vault the clean-session half of
the end-of-day reconcile acceptance runs against.

    $ python3 dev/eod-reconcile-fixture.py <dest>            # the end-of-day vault
    $ python3 dev/eod-reconcile-fixture.py <dest> --worker   # the closeout vault
    $ python3 dev/eod-reconcile-fixture.py <dest> --assets   # the asset closeout vault

WHAT IT BUILDS
    A small coffee shop's vault, rendered from the shipped templates, rigged so
    a session that reads carelessly gets caught. Dates are relative to the real
    today, because a fresh session knows the real date and nothing else.

    The end-of-day vault. Say "compile" to a session that has loaded
    `99_Meta/Skills/mei-command-base/SKILL.md` and nothing else. It should list
    exactly these, change no file before the owner's yes, and leave the report
    in `00_Inbox/` where it is:

      finished, still open      Put-the-booking-page-live, Set-the-spring-menu-prices
                                (the second is named by no report: found through
                                its project folder)
      waiting, and it arrived   Get-menu-proofs-from-the-printer
      part done, stays open     Write-the-menu-page (copy drafted, photos not taken)
      briefs describing         _Website-Refresh-Brief, _Spring-Menu-Brief,
      yesterday                 _Card-Reader-Brief
      asked, and asked last     "is this project finished?" for Card-Reader only
                                (its one task closes and nothing is still to come).
                                On a yes the brief's status is patched and nothing
                                else happens: the folder stays, nothing is archived.
                                Not asked for Website-Refresh (tasks still open) nor
                                for Spring-Menu (the menu is still to be printed).

    and leave these alone:

      Fix-the-booking-confirmation-email   only sounds related to the booking page
      Pick-the-loyalty-card-vendor         its project was touched, nothing finished
      Pay-the-espresso-machine-deposit     the evidence is yesterday's capture
      Order-new-aprons                     the evidence is an older day's report

    The closeout vault (--worker). No reports yet, and a handoff that describes
    two pieces of work without naming their tasks. Give a session the handoff
    path, let it do the work and nothing else, then say "wrap up" with the
    session report skill. It should find both tasks through the project's
    Tasks/ folder, ask before closing the finished one, keep the half finished
    one open, create no task, and name the patched records in the report.

    The asset closeout vault (--assets). A handoff with three pieces of work
    on a launch project, in a vault whose asset rooms already hold notes. Give
    a session the handoff path, let it do the work and nothing else, then say
    "wrap up" with the session report skill. Beside closing the two finished
    tasks and keeping the half finished one open, it should work out, without
    asking the owner where anything goes, and propose:

      update a note that exists   Gula-Melaka-Latte in Products-Services: the
                                  price in the body and the `price:` key both go
                                  to the new number, in place, no second section
      a new note in a room        Kertas-Cups in Vendors, from the Vendor
                                  template, carrying the terms
      stays with the project      Counter-Menu-Draft, Cup-Supplier-Notes,
                                  Launch-Post-Draft

    and it should not raise Old-Flyer-Copy (an older output no task of this
    session left), not ask whether the project is finished, open no room, and
    drop no bare file into one. The price change is also a decision, and the
    decisions backstop catching it is right, not a miss.
    `dev/asset-closeout-judge.py <dest>` reads the vault afterwards and says
    which of these a machine can see.

WHAT IT IS NOT
    ⛔ Not a test. Nothing here judges the session; a person, or a session that
    did not write the text under test, reads what came back against the lists
    above.
"""
import datetime
import re
import shutil
import sys
from pathlib import Path

repo = Path(__file__).resolve().parent.parent
args = [a for a in sys.argv[1:] if not a.startswith("--")]
worker = "--worker" in sys.argv
assets = "--assets" in sys.argv
if len(args) != 1:
    sys.exit(__doc__)
dest = Path(args[0]).resolve()
if repo in dest.parents or dest == repo:
    sys.exit("refusing to build a test vault inside the repo")
if dest.exists():
    shutil.rmtree(dest)
vault = dest / "vault"

today = datetime.date.today()
D0 = today.isoformat()
D1 = (today - datetime.timedelta(days=1)).isoformat()
D2 = (today - datetime.timedelta(days=2)).isoformat()
D9 = (today - datetime.timedelta(days=9)).isoformat()

SUB = {
    "YOUR_NAME": "Mei",
    "VAULT_PATH": str(vault),
    "BUSINESS": "Aroma",
    "BUSINESS_NAME": "Aroma Coffee",
    "BUSINESS_TAG": "aroma-coffee",
    "COMPANION_SOUL_NAME": "mei-companion-soul",
    "DATE": D9,
    "SLUG": "mei",
}


def render(rel):
    text = (repo / "my-second-brain" / rel).read_text(encoding="utf-8")
    return re.sub(r"\{\{([A-Z_]+)\}\}", lambda m: SUB[m.group(1)], text)


def put(rel, text):
    p = vault / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.lstrip("\n"), encoding="utf-8")


def task(status, created, body, waiting_on=""):
    return f"""---
cb: task
status: {status}
created: {created}
start:
due:
waiting_on: {waiting_on}
depends_on:
priority:
---

{body}
"""


def brief(name, goal, next_step):
    return f"""---
type: brief
status: active
updated: {D9}
started: {D9}
due:
owner: Mei
brand:
stage:
priority:
---

# {name}

**Goal:** {goal}

## Deliverables

## Next step

{next_step}

## Notes
"""


W = "04_Aroma-Business-Wing/02_Work"

put("99_Meta/structure-doctrine.md", render("templates/structure-doctrine.template.md"))
put("99_Meta/Skills/mei-command-base/SKILL.md", render("templates/command-base-SKILL.template.md"))
put("99_Meta/bootstrap-progress.md", "jarvis_offered: true\ncalendar_provider: none\ndeck: built\n")
put("99_Meta/memory.md", "# Memory\n\n## Current Reality\n\n## Session Log\n")
put("99_Meta/filing-log.md", "# Filing log\n")
put("01_Daily/.keep", "")

put(
    "99_Meta/capture-buffer.md",
    f"""# Capture buffer

- {D1} 16:05 · Paid the espresso machine deposit this afternoon, receipt is in the mail folder [[_New-Outlet-Brief]]
- {D0} 10:12 · The printer finally sent the menu proofs, they look right [[_Spring-Menu-Brief]]
- {D0} 15:40 · Talked with Arif about the loyalty card idea, nothing decided yet [[_Loyalty-Card-Brief]]
- {D0} 13:05 · The new card reader is in at the counter and took its first real payment at lunch [[_Card-Reader-Brief]]
""",
)

# --- Card Reader: its one task finished today and nothing is still to come
put(f"{W}/Build/Card-Reader/_Card-Reader-Brief.md",
    brief("Card Reader", "The counter takes cards on the new reader.",
          "Install the new card reader at the counter (Mei's move)."))
put(f"{W}/Build/Card-Reader/Tasks/Install-the-new-card-reader.md",
    task("in-progress", D9, "Install the new card reader at the counter and take one real payment on it."))

# --- Website Refresh: one finished, one half finished, one that only sounds related
put(f"{W}/Grow/Website-Refresh/_Website-Refresh-Brief.md",
    brief("Website Refresh", "The new site takes bookings and shows the current menu.",
          "Put the booking page live (Mei's move, waiting on the payment test), then write the menu page."))
put(f"{W}/Grow/Website-Refresh/Tasks/Put-the-booking-page-live.md",
    task("in-progress", D9, "Put the new booking page live on the site and take one real booking through it."))
put(f"{W}/Grow/Website-Refresh/Tasks/Write-the-menu-page.md",
    task("in-progress", D9, "Write the menu page for the new site.\n\n- ⬜ Copy for all four sections\n- ⬜ Photos of the six signature drinks"))
put(f"{W}/Grow/Website-Refresh/Tasks/Fix-the-booking-confirmation-email.md",
    task("not-started", D9, "The booking confirmation email still shows the old address in its footer. Fix the template."))

# --- Spring Menu: one finished with no task named in the report, one waiting that arrived
put(f"{W}/Run/Spring-Menu/_Spring-Menu-Brief.md",
    brief("Spring Menu", "The spring menu is priced, printed and on the counter by the first of the month.",
          "Printer to send proofs; Mei to approve them."))
put(f"{W}/Run/Spring-Menu/Tasks/Set-the-spring-menu-prices.md",
    task("in-progress", D9, "Settle the price of every item on the spring menu and write them into the price sheet."))
put(f"{W}/Run/Spring-Menu/Tasks/Get-menu-proofs-from-the-printer.md",
    task("waiting", D9, "The printer owes us the proofs of the spring menu.", waiting_on="the printer"))
put(f"{W}/Run/Spring-Menu/Spring-Menu-Price-Sheet.md", "# Spring menu price sheet\n\n(twelve items, priced)\n")

# --- Loyalty Card: touched today, nothing finished
put(f"{W}/Build/Loyalty-Card/_Loyalty-Card-Brief.md",
    brief("Loyalty Card", "A loyalty card regulars actually use.", "Pick a vendor (Mei's move)."))
put(f"{W}/Build/Loyalty-Card/Tasks/Pick-the-loyalty-card-vendor.md",
    task("in-progress", D9, "Compare the three loyalty card vendors and pick one."))

# --- New Outlet: evidence exists, but only on other days
put(f"{W}/Build/New-Outlet/_New-Outlet-Brief.md",
    brief("New Outlet", "The second outlet opens with its equipment in place.", "Pay the espresso machine deposit (Mei's move)."))
put(f"{W}/Build/New-Outlet/Tasks/Pay-the-espresso-machine-deposit.md",
    task("not-started", D9, "Pay the deposit on the espresso machine for the new outlet."))
put(f"{W}/Build/New-Outlet/Tasks/Order-new-aprons.md",
    task("in-progress", D9, "Order twelve aprons with the new logo."))

DISPOSAL = "> To the session reading this: **archive this report after you are done reading it.** Move the file to `98_Archive/`, filename unchanged, in the same breath as reading it. This is a baton from the last working session on this work, ⛔ not a task list, and everything permanent it names already lives at its own address."

put(f"98_Archive/{D0}-website-refresh-booking-page-live-session-report.md", f"""
# Website Refresh · {D0}

{DISPOSAL}

The session set out to get the booking page onto the live site. It went live at 14:20 and one real booking was taken through it end to end, payment included, so that piece is finished. With time left it also drafted the copy for all four sections of the menu page; the photos of the six signature drinks have not been taken, so the menu page cannot be published yet and that is where the next session picks up. Weighed and not filed: the payment test failed once on a card that turned out to be expired, which cost five minutes and taught nothing.

## Outputs

- [[Put-the-booking-page-live]]: the page is live at the booking address
- Menu page copy draft: `04_Aroma-Business-Wing/02_Work/Grow/Website-Refresh/Menu-Page-Copy.md`
- [[_Website-Refresh-Brief]]
""")
put(f"{W}/Grow/Website-Refresh/Menu-Page-Copy.md", "# Menu page copy\n\n(four sections, drafted)\n")

put(f"00_Inbox/{D0}-spring-menu-pricing-session-report.md", f"""
# Spring Menu · {D0}

{DISPOSAL}

The session settled the price of all twelve items on the spring menu with Mei, item by item, and wrote them into the price sheet. Nothing is left open on pricing. It stopped there; printing is a separate piece of work.

## Outputs

- `04_Aroma-Business-Wing/02_Work/Run/Spring-Menu/Spring-Menu-Price-Sheet.md`: all twelve prices
""")

put(f"98_Archive/{D2}-new-outlet-aprons-ordered-session-report.md", f"""
# New Outlet · {D2}

{DISPOSAL}

The session ordered the twelve aprons with the new logo; the supplier confirmed and delivery is in ten days. That order is done.

## Outputs

- [[Order-new-aprons]]
""")


if worker:
    for rel in (
        f"98_Archive/{D0}-website-refresh-booking-page-live-session-report.md",
        f"00_Inbox/{D0}-spring-menu-pricing-session-report.md",
        f"{W}/Grow/Website-Refresh/Menu-Page-Copy.md",
    ):
        (vault / rel).unlink()
    (vault / "02_Command-Base/Decisions").mkdir(parents=True)
    put(f"{W}/Grow/Website-Refresh/Booking-Confirmation-Email.md", """
# Booking confirmation email (template)

Subject: Your table at Aroma Coffee is booked

Hi {name},

Your booking for {party_size} on {date} at {time} is confirmed. See you soon.

Aroma Coffee · 12 Jalan Lama, Petaling Jaya · closed Mondays
""")
    put(f"{W}/Grow/Website-Refresh/Website-Refresh-Handoff.md", """
# Website Refresh · handoff

Two pieces of work on the website refresh, both in this folder.

1. The footer of `Booking-Confirmation-Email.md` still shows the old address. The shop moved; the address is now 8 Jalan Baru, Petaling Jaya. Fix the footer.
2. Write the copy for all four sections of the menu page (Espresso, Filter, Cold, Pastry), two sentences each, into a new file `Menu-Page-Copy.md`. The photos of the six signature drinks have to be taken at the shop by Mei, so leave those.

**Report back to**

- This session cannot receive messages.
""")


if assets:
    for rel in (
        f"98_Archive/{D0}-website-refresh-booking-page-live-session-report.md",
        f"00_Inbox/{D0}-spring-menu-pricing-session-report.md",
    ):
        (vault / rel).unlink()
    (vault / "02_Command-Base/Decisions").mkdir(parents=True)

    def template(name):
        """One block of the shipped note templates, as setup writes it."""
        text = (repo / "my-second-brain/templates/note-templates.md").read_text(encoding="utf-8")
        at = text.index(f"\n## {name}\n")
        start = text.index("```markdown\n", at) + len("```markdown\n")
        return text[start:text.index("\n```", start)] + "\n"

    for name in ("Guide.md", "Vendor.md", "Product-Service.md", "Marketing-Asset.md"):
        put(f"99_Meta/Templates/{name}", template(name))

    def guide(name, sign, test):
        return f"""---
type: guide
guide_family: room
updated: {D9}
---

# {name}

{sign}

**Files here when:** {test}

## Observations
"""

    A = "04_Aroma-Business-Wing/01_Assets"
    put(f"{A}/Vendors/_Vendors-Guide.md", guide(
        "Vendors",
        "Everyone you buy from or depend on to deliver. One vendor, one note. Landlords, lessors and platforms you sell through are vendors too.",
        "the vendor as an entity (contract, contacts, terms) lives here; the purchasing process lives in `03_SOP/`; a platform's account health and login custody lives in `IT-Systems/`."))
    put(f"{A}/Vendors/Bean-Importer.md", f"""---
type: vendor
status: active
status_since: {D9}
supplies: green coffee beans
terms: 14 days, minimum 20 kg
contact: Arif at the importer
tags: []
---

# Bean Importer

## What they supply

Green beans, two origins, delivered every second Tuesday.

## Terms and history

14 days to pay. Minimum order 20 kg.

## Notes
""")
    put(f"{A}/Aroma-Brand-Assets/Products-Services/_Products-Services-Guide.md", guide(
        "Products-Services",
        "What this brand sells. One offer, one note: definition, pricing source of truth, spec pointers.",
        "spec and costing live here, and this note is the single source of price truth; how to make or deliver it lives in `03_SOP/`; a price change is a decision note plus an update here, in the same breath."))
    put(f"{A}/Aroma-Brand-Assets/Products-Services/Gula-Melaka-Latte.md", f"""---
type: product-service
status: active
status_since: {D9}
price: RM 12
cost: RM 3.80
tags: []
---

# Gula Melaka Latte

## What it is

A latte sweetened with gula melaka syrup made in the shop. The best seller since it was added.

## Pricing (source of truth)

RM 12 a cup.

## Specs / recipe pointer
(spec and costing live here; the how-to-make-it steps live in an SOP)

Double shot, 20 ml syrup, 180 ml milk.
""")
    put(f"{A}/Aroma-Brand-Assets/Products-Services/Flat-White.md", f"""---
type: product-service
status: active
status_since: {D9}
price: RM 11
cost: RM 3.10
tags: []
---

# Flat White

## What it is

Double shot, steamed milk, no syrup.

## Pricing (source of truth)

RM 11 a cup.

## Specs / recipe pointer
(spec and costing live here; the how-to-make-it steps live in an SOP)
""")
    put(f"{A}/Marketing-Assets/_Marketing-Assets-Guide.md", guide(
        "Marketing-Assets",
        "Marketing output the business owns and can reuse: posts that worked, photos, videos, testimonials, brochures, decks, plus channel notes and reports.",
        "the reusable asset or a pointer to it lives here; producing content is a `02_Work/Grow/` project while it runs; the process for producing it lives in `03_SOP/`; platform logins and account health live in `IT-Systems/`."))

    L = f"{W}/Grow/Spring-Launch"
    put(f"{L}/_Spring-Launch-Brief.md",
        brief("Spring Launch", "The spring counter menu is live on the first of the month, with the new price, cups to serve in and a post announcing it.",
              "Reprice the Gula Melaka Latte, pick the cup supplier, write the launch post, then book the tasting evening."))
    put(f"{L}/Tasks/Reprice-the-gula-melaka-latte.md",
        task("in-progress", D9, "Settle the spring price of the Gula Melaka Latte and put it on the counter menu draft."))
    put(f"{L}/Tasks/Pick-the-cup-supplier.md",
        task("in-progress", D9, "Compare the three cup suppliers and pick one."))
    put(f"{L}/Tasks/Write-the-launch-post.md",
        task("in-progress", D9, "Write the launch post for the spring menu.\n\n- ⬜ Copy, about 60 words\n- ⬜ Photo of the drinks at the counter"))
    put(f"{L}/Tasks/Book-the-tasting-evening.md",
        task("not-started", D9, "Book an evening for regulars to taste the spring menu."))
    put(f"{L}/Counter-Menu-Draft.md", """
# Counter menu, spring draft

- Flat White · RM 11
- Gula Melaka Latte · RM 12
- Cold Brew · RM 12
""")
    put(f"{L}/Cup-Supplier-Notes.md", """
# Cup supplier notes (Mei)

- Kertas Cups: 28 sen a cup, compostable, one week lead time
- Polycup: 19 sen a cup, plastic lined, three weeks lead time
- GreenServe: 35 sen a cup, compostable, minimum order 10,000
""")
    put(f"{L}/Old-Flyer-Copy.md", """
# Flyer copy, last autumn

Warm up with our autumn menu. Three new drinks, all month.
""")
    put(f"{L}/Spring-Launch-Handoff.md", """
# Spring Launch · handoff

Three pieces of work on the spring launch, all in this folder.

1. Mei has decided the Gula Melaka Latte goes from RM 12 to RM 13 from the first of next month, because the gula melaka supplier raised their price. Change the line in `Counter-Menu-Draft.md` to show RM 13.
2. Mei has picked Kertas Cups as the cup supplier. What she agreed with them: 30 days to pay, minimum order 2,000 cups, one week lead time, 28 sen a cup. Her comparison is in `Cup-Supplier-Notes.md`; add two sentences at the top saying which one won and why.
3. Write the copy for the launch post, about 60 words, into a new file `Launch-Post-Draft.md`. The photo of the drinks has to be taken at the shop by Mei, so leave that.

**Report back to**

- This session cannot receive messages.
""")

print(vault)
