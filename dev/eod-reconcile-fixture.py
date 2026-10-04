#!/usr/bin/env python3
"""
eod-reconcile-fixture.py - builds the throwaway vault the clean-session half of
the end-of-day reconcile acceptance runs against.

    $ python3 dev/eod-reconcile-fixture.py <dest>            # the end-of-day vault
    $ python3 dev/eod-reconcile-fixture.py <dest> --worker   # the closeout vault

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
      briefs describing         _Website-Refresh-Brief, _Spring-Menu-Brief
      yesterday

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
""",
)

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

print(vault)
