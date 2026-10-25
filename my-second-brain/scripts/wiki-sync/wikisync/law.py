"""Find the publishable-layers law in a vault's own doctrine, by its words.

The law's number is not fixed: a vault that amended §4 before this law
arrived may hold it under another number, or not at all. So the law is the
numbered item in §4 whose bold opening names "publishable layers", and
nothing else counts.
"""
import os
import re

DOCTRINE = os.path.join("99_Meta", "structure-doctrine.md")
SECTION_RE = re.compile(r"^##\s+4\b")
NEXT_SECTION_RE = re.compile(r"^##\s")
ITEM_RE = re.compile(r"^(\d+)\.\s+(.*)$")
LEAD_RE = re.compile(r"\*\*(.+?)\*\*")
WORDS = "publishable layers"


class LawNotFound(Exception):
    pass


def find_law(vault):
    """Return (number, lead, text) for the publishable-layers law.

    Raises LawNotFound with a plain reason when the doctrine is missing, has
    no §4, or §4 holds no law whose bold opening names the publishable
    layers."""
    path = os.path.join(vault, DOCTRINE)
    if not os.path.isfile(path):
        raise LawNotFound("no doctrine at %s" % DOCTRINE)
    with open(path, encoding="utf-8", errors="replace") as fh:
        lines = fh.read().splitlines()
    section = None
    for i, line in enumerate(lines):
        if SECTION_RE.match(line):
            section = []
            for rest in lines[i + 1:]:
                if NEXT_SECTION_RE.match(rest):
                    break
                section.append(rest)
            break
    if section is None:
        raise LawNotFound("%s has no section 4" % DOCTRINE)
    items, current = [], None
    for line in section:
        m = ITEM_RE.match(line)
        if m:
            current = [int(m.group(1)), m.group(2)]
            items.append(current)
        elif current is not None and line.strip():
            current[1] += "\n" + line
        elif not line.strip():
            current = None
    for number, text in items:
        lead = LEAD_RE.search(text)
        if lead and WORDS in lead.group(1).lower():
            return number, lead.group(1), text
    raise LawNotFound("section 4 of %s has no law that opens with the publishable layers" % DOCTRINE)
