"""The publishable-layers law is found by its words, never by its number."""
import io
import os
import shutil
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

from wikisync.cli import EXIT_NO_LAW, EXIT_OK, main
from wikisync.law import LawNotFound, find_law

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "..", "..", "templates", "structure-doctrine.template.md")

PUBLISHABLE = "**The publishable layers are written for the team to read.** `03_SOP/`, `04_Methodology/`."
SYMLINK = "**A symlink inside the vault never points outside it.** Bridge it outside."


def doctrine(*laws, heading="## 4 · Iron laws"):
    items = "\n".join("%d. %s" % (i + 1, law) for i, law in enumerate(laws))
    return "# Doctrine\n\n## 3 · Before\n\n7. **The publishable layers** are not here.\n\n%s\n\n%s\n\n## 5 · After\n\n1. %s\n" % (
        heading, items, PUBLISHABLE)


class LawTest(unittest.TestCase):
    def setUp(self):
        self.vault = tempfile.mkdtemp(prefix="wikisync-law-")

    def tearDown(self):
        shutil.rmtree(self.vault, ignore_errors=True)

    def write(self, text):
        os.makedirs(os.path.join(self.vault, "99_Meta"), exist_ok=True)
        with open(os.path.join(self.vault, "99_Meta", "structure-doctrine.md"), "w", encoding="utf-8") as fh:
            fh.write(text)

    def run_cli(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_shipped_template_holds_the_law(self):
        with open(TEMPLATE, encoding="utf-8") as fh:
            self.write(fh.read())
        number, lead, _ = find_law(self.vault)
        self.assertEqual(lead, "The publishable layers are written for the team to read.")
        self.assertEqual(number, 7)

    def test_found_under_another_number(self):
        laws = ["**Rows stay home.**"] * 6 + [SYMLINK, PUBLISHABLE]
        self.write(doctrine(*laws))
        number, _, text = find_law(self.vault)
        self.assertEqual(number, 8)
        self.assertIn("03_SOP/", text)

    def test_law_seven_about_something_else_is_not_it(self):
        laws = ["**Rows stay home.**"] * 6 + [SYMLINK]
        self.write(doctrine(*laws))
        with self.assertRaises(LawNotFound):
            find_law(self.vault)

    def test_words_outside_section_four_do_not_count(self):
        self.write(doctrine("**Rows stay home.**"))
        with self.assertRaises(LawNotFound):
            find_law(self.vault)

    def test_no_doctrine(self):
        with self.assertRaises(LawNotFound):
            find_law(self.vault)

    def test_law_verb(self):
        self.write(doctrine(SYMLINK, PUBLISHABLE))
        code, out, _ = self.run_cli(["law", self.vault])
        self.assertEqual(code, EXIT_OK)
        self.assertTrue(out.startswith("law 2: The publishable layers"))

    def test_init_refuses_without_the_law(self):
        self.write(doctrine(SYMLINK))
        code, _, err = self.run_cli(["init", self.vault, "--provider", "fake", "--roots", "03_SOP"])
        self.assertEqual(code, EXIT_NO_LAW)
        self.assertIn("refusing to connect", err)
        self.assertFalse(os.path.exists(os.path.join(self.vault, "99_Meta", "wiki-sync.md")))


if __name__ == "__main__":
    unittest.main()
