# Stale renders

`png/15-modes-overview.png`, `png/16-setup.png` and `My-Second-Brain-Deck.pdf` were rendered before
2026-08-23 and still show the old ending: "结束在星图" / "See the constellation" / "Ends on the graph
view". Setup no longer ends on the graph view, so those three files carry a promise the product does
not make. The HTML slides and `_qa/build-deck.workflow.js` are correct.

Re-render slides 15 and 16 and reassemble the PDF (`_qa/render.py`, `_qa/crop.py`, `_qa/assemble.py`)
the next time the deck is touched, then delete this file. Note the CJK gotcha before rendering to PDF:
headless Chrome drops Chinese glyphs with the default font stack.
