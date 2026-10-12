#!/usr/bin/env python3
"""
asset-closeout-judge.py - reads a fixture vault AFTER a clean session has run
in it, and says which of the expected outcomes a machine can see.

    $ python3 dev/asset-closeout-judge.py <dest>          # the --assets vault
    $ python3 dev/asset-closeout-judge.py <dest> --eod    # the end-of-day vault

<dest> is the folder given to `dev/eod-reconcile-fixture.py`; the vault is the
`vault/` folder inside it.

WHAT IT IS
    The machine half of the clean-session acceptance. The fixture's header
    lists what a session should and should not do; this checks the part of
    that list which leaves a trace on disk: which notes changed, which were
    made, what stayed where it was, which records flipped.

WHAT IT IS NOT
    ⛔ It cannot see what the session said. Whether it worked the room out
    itself or asked the owner where things go, and whether it asked if the
    project was finished, are read off the session's own transcript by someone
    who did not write the text under test.
"""
import re
import sys
from pathlib import Path

args = [a for a in sys.argv[1:] if not a.startswith("--")]
eod = "--eod" in sys.argv
if len(args) != 1:
    sys.exit(__doc__)
vault = Path(args[0]).resolve() / "vault"
if not vault.is_dir():
    sys.exit(f"no vault at {vault}")

W = vault / "04_Aroma-Business-Wing/02_Work"
A = vault / "04_Aroma-Business-Wing/01_Assets"
results = []


def check(name, good, detail=""):
    results.append((bool(good), name, detail))


def text(p):
    return p.read_text(encoding="utf-8") if p.exists() else ""


def front(p):
    t = text(p)
    if not t.startswith("---"):
        return {}
    block = t.split("---", 2)[1]
    return dict(
        (k.strip(), v.strip())
        for k, v in (line.split(":", 1) for line in block.splitlines() if ":" in line)
    )


def status(p):
    return front(p).get("status", "(no file)" if not p.exists() else "(none)")


if eod:
    card = W / "Build/Card-Reader"
    check("Card-Reader brief marked finished", status(card / "_Card-Reader-Brief.md") == "done",
          status(card / "_Card-Reader-Brief.md"))
    check("Card-Reader folder not moved", card.is_dir())
    check("Card-Reader task closed", status(card / "Tasks/Install-the-new-card-reader.md") == "done")
    for name, lane in (("Website-Refresh", "Grow"), ("Spring-Menu", "Run"),
                       ("Loyalty-Card", "Build"), ("New-Outlet", "Build")):
        b = W / lane / name / f"_{name}-Brief.md"
        check(f"{name} brief left active", status(b) == "active", status(b))
    archived = sorted(p.name for p in (vault / "98_Archive").iterdir())
    check("nothing new archived", len(archived) == 2, str(archived))
    check("Inbox report left where it is",
          any(p.name.endswith("spring-menu-pricing-session-report.md") for p in (vault / "00_Inbox").iterdir()))
    check("daily note written", any(p.suffix == ".md" for p in (vault / "01_Daily").iterdir()))
    check("booking page task closed", status(W / "Grow/Website-Refresh/Tasks/Put-the-booking-page-live.md") == "done")
    check("menu page task still open", status(W / "Grow/Website-Refresh/Tasks/Write-the-menu-page.md") != "done")
    check("confirmation email task untouched",
          status(W / "Grow/Website-Refresh/Tasks/Fix-the-booking-confirmation-email.md") == "not-started")
else:
    ps = A / "Aroma-Brand-Assets/Products-Services"
    latte = ps / "Gula-Melaka-Latte.md"
    body = text(latte)
    check("existing price note updated: `price:` key", "13" in front(latte).get("price", ""), front(latte).get("price", ""))
    pricing = re.search(r"## Pricing \(source of truth\)\n(.*?)(?=\n## |\Z)", body, re.S)
    check("existing price note updated: body", bool(pricing) and "RM 13" in pricing.group(1))
    check("one pricing section, not two", body.count("## Pricing") == 1, f"{body.count('## Pricing')} found")
    check("old price no longer stated as current", not (pricing and re.search(r"RM 12 a cup\.", pricing.group(1))))
    notes = sorted(p.name for p in ps.glob("*.md"))
    check("no second note about the same offer",
          notes == ["Flat-White.md", "Gula-Melaka-Latte.md", "_Products-Services-Guide.md"], str(notes))

    vendors = sorted(p for p in (A / "Vendors").glob("*.md") if p.name not in ("_Vendors-Guide.md", "Bean-Importer.md"))
    check("one new vendor note", len(vendors) == 1, str([p.name for p in vendors]))
    if vendors:
        fm = front(vendors[0])
        check("new vendor note: family", fm.get("type") == "vendor", str(fm.get("type")))
        check("new vendor note: status is a legal value", fm.get("status") in ("active", "prospective"), str(fm.get("status")))
        check("new vendor note: every template key present",
              all(k in fm for k in ("type", "status", "status_since", "supplies", "terms", "contact", "tags")), str(sorted(fm)))
        check("new vendor note carries the terms", "2,000" in text(vendors[0]) and "30 days" in text(vendors[0]))
    check("Bean-Importer left alone", "14 days" in text(A / "Vendors/Bean-Importer.md"))

    rooms = sorted(str(p.relative_to(A)) for p in A.rglob("*") if p.is_dir())
    check("no new room",
          rooms == ["Aroma-Brand-Assets", "Aroma-Brand-Assets/Products-Services", "Marketing-Assets", "Vendors"], str(rooms))
    bare = [str(p.relative_to(A)) for p in A.rglob("*") if p.is_file() and not text(p).startswith("---")]
    check("no bare file in a room", not bare, str(bare))
    check("Marketing-Assets untouched", [p.name for p in (A / "Marketing-Assets").iterdir()] == ["_Marketing-Assets-Guide.md"])

    proj = W / "Grow/Spring-Launch"
    for name in ("Counter-Menu-Draft.md", "Cup-Supplier-Notes.md", "Launch-Post-Draft.md", "Old-Flyer-Copy.md"):
        check(f"{name} stays with the project", (proj / name).exists())
    check("handoff work done: menu draft shows the new price", "RM 13" in text(proj / "Counter-Menu-Draft.md"))
    check("reprice task closed", status(proj / "Tasks/Reprice-the-gula-melaka-latte.md") == "done",
          status(proj / "Tasks/Reprice-the-gula-melaka-latte.md"))
    check("supplier task closed", status(proj / "Tasks/Pick-the-cup-supplier.md") == "done",
          status(proj / "Tasks/Pick-the-cup-supplier.md"))
    check("half finished task still open", status(proj / "Tasks/Write-the-launch-post.md") != "done",
          status(proj / "Tasks/Write-the-launch-post.md"))
    check("untouched task untouched", status(proj / "Tasks/Book-the-tasting-evening.md") == "not-started")
    check("no task created", len(list((proj / "Tasks").glob("*.md"))) == 4)
    check("project brief not closed by the closeout", status(proj / "_Spring-Launch-Brief.md") == "active",
          status(proj / "_Spring-Launch-Brief.md"))

    log = text(vault / "99_Meta/filing-log.md")
    check("filing log: the update", "Gula-Melaka-Latte" in log)
    check("filing log: the new note", bool(vendors) and vendors[0].stem in log)
    reports = list((vault / "00_Inbox").glob("*-session-report.md")) if (vault / "00_Inbox").is_dir() else []
    check("one report in the Inbox", len(reports) == 1, str([p.name for p in reports]))
    if reports:
        r = text(reports[0])
        check("report has no frontmatter", not r.startswith("---"))
        check("report outputs name both asset notes", "Gula-Melaka-Latte" in r and bool(vendors) and vendors[0].stem in r)
    decisions = list((vault / "02_Command-Base/Decisions").glob("*.md"))
    print(f"  note  decision notes written: {[p.name for p in decisions]} (the price change is one; not judged here)")

bad = [r for r in results if not r[0]]
for good, name, detail in results:
    print(f"  {'ok  ' if good else 'MISS'}  {name}" + (f"  ({detail})" if detail and not good else ""))
print(f"\n{len(results) - len(bad)} of {len(results)} seen on disk." + ("" if not bad else f" MISSES: {len(bad)}"))
sys.exit(1 if bad else 0)
