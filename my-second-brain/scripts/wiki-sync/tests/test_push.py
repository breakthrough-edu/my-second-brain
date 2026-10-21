"""End to end against the fake provider: init, plan, push, verify."""
import io
import os
import shutil
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

from wikisync import manifest as manifest_mod
from wikisync.cli import main
from wikisync.providers.fake import FakeProvider

SOP = "04_Acme-Business-Wing/03_SOP"
METH = "04_Acme-Business-Wing/04_Methodology"

NOTES = {
    SOP + "/Deliver/Onboarding.md": "---\ntype: sop\nowner: Jane\n---\n# Onboarding SOP\n\nStep one. See [[Pit]].\n",
    SOP + "/_SOP-Guide.md": "---\ntype: guide\n---\n# How SOPs are kept\n\nThe door.\n",
    METH + "/Lessons/Pit.md": "---\ntype: lesson\n---\n# The pit we fell into\n\nNever again.\n",
    METH + "/Lessons/Empty.md": "---\ntype: lesson\nstatus: empty\n---\n# Not yet\n",
    METH + "/Lessons/.hidden.md": "# hidden\n",
}


class PushTest(unittest.TestCase):
    def setUp(self):
        self.vault = tempfile.mkdtemp(prefix="wikisync-vault-")
        self.wiki = tempfile.mkdtemp(prefix="wikisync-wiki-")
        for rel, text in NOTES.items():
            self.write(rel, text)
        self.run_cli(["init", self.vault, "--provider", "fake", "--space-id", "123",
                      "--base-url", "https://example.larksuite.com",
                      "--roots", SOP + "," + METH, "--owner-name", "Jane Owner"])
        self.fake = FakeProvider(manifest_mod.load(self.vault), log=lambda m: None, dir=self.wiki)
        self.factory = lambda manifest, vault: self.fake

    def tearDown(self):
        shutil.rmtree(self.vault, ignore_errors=True)
        shutil.rmtree(self.wiki, ignore_errors=True)

    # [helpers]

    def write(self, rel, text):
        full = os.path.join(self.vault, *rel.split("/"))
        folder = os.path.dirname(full)
        if not os.path.isdir(folder):
            os.makedirs(folder)
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(text)

    def run_cli(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main(argv, provider_factory=self.factory if hasattr(self, "factory") else None)
        return code, out.getvalue(), err.getvalue()

    def manifest_text(self):
        with open(manifest_mod.manifest_path(self.vault), "r", encoding="utf-8") as fh:
            return fh.read()

    def push(self, *extra):
        self.fake.calls = []
        return self.run_cli(["push", self.vault] + list(extra))

    # [tests]

    def test_init_refuses_to_overwrite_without_force(self):
        code, _, err = self.run_cli(["init", self.vault, "--provider", "fake"])
        self.assertEqual(code, 1)
        self.assertIn("already exists", err)

    def test_plan_before_first_push(self):
        code, out, _ = self.run_cli(["plan", self.vault])
        self.assertEqual(code, 0)
        self.assertIn("plan: new 3, changed 0, unchanged 0, removed 0", out)
        self.assertNotIn("Empty.md", out)
        self.assertNotIn(".hidden.md", out)

    def test_push_without_manifest_exits_4(self):
        os.remove(manifest_mod.manifest_path(self.vault))
        code, _, _ = self.run_cli(["push", self.vault])
        self.assertEqual(code, 4)

    def test_dry_run_touches_nothing(self):
        code, out, _ = self.push("--dry-run")
        self.assertEqual(code, 0)
        self.assertIn("dry run: pushed 3 (new 3, changed 0)", out)
        self.assertEqual(self.fake.calls, [])
        self.assertEqual(manifest_mod.load(self.vault).pages, {})

    def test_full_lifecycle(self):
        # First push: folders with stripped titles, three pages, manifest updated.
        code, out, _ = self.push()
        self.assertEqual(code, 0, out)
        self.assertIn("pushed 3 (new 3, changed 0), unchanged 0, removed 0 (deleted 0), failed 0", out)
        titles = {n["title"]: n for n in self.fake.nodes.values()}
        self.assertEqual(set(titles), {"SOP", "Deliver", "Methodology", "Lessons",
                                       "Onboarding SOP", "How SOPs are kept", "The pit we fell into"})
        self.assertEqual(titles["SOP"]["parent"], "")
        self.assertEqual(titles["Methodology"]["parent"], "")
        sop_token = [t for t, n in self.fake.nodes.items() if n["title"] == "SOP"][0]
        self.assertEqual(titles["Deliver"]["parent"], sop_token)
        deliver_token = [t for t, n in self.fake.nodes.items() if n["title"] == "Deliver"][0]
        self.assertEqual(titles["Onboarding SOP"]["parent"], deliver_token)
        self.assertEqual(titles["How SOPs are kept"]["parent"], sop_token)

        m = manifest_mod.load(self.vault)
        self.assertEqual(set(m.folders), {SOP, SOP + "/Deliver", METH, METH + "/Lessons"})
        self.assertEqual(set(m.pages), {SOP + "/Deliver/Onboarding.md", SOP + "/_SOP-Guide.md",
                                        METH + "/Lessons/Pit.md"})
        self.assertNotEqual(m.last_push, "")
        for page in m.pages.values():
            self.assertEqual(len(page.fingerprint), 12)
            self.assertTrue(page.url.startswith("https://example.larksuite.com/wiki/"))
            self.assertTrue(os.path.isfile(os.path.join(self.wiki, page.node_token + ".xml")))
        onboarding = self.fake.nodes[m.pages[SOP + "/Deliver/Onboarding.md"].node_token]["content"]
        self.assertIn("Owner: Jane", onboarding)
        self.assertIn("fingerprint " + m.pages[SOP + "/Deliver/Onboarding.md"].fingerprint, onboarding)
        # Pit is pushed after Onboarding in sorted order, but every new node is
        # reserved before any page is converted, so the link lands on the
        # first push, and the nodes were all created before the first overwrite.
        pit_url = m.pages[METH + "/Lessons/Pit.md"].url
        self.assertIn('<a href="%s">Pit</a>' % pit_url, onboarding)
        verbs = [c[0] for c in self.fake.calls if c[0] in ("create", "overwrite")]
        self.assertEqual(verbs.index("overwrite"), len(verbs) - verbs.count("overwrite"))

        # Plan is clean, verify is clean.
        code, out, _ = self.run_cli(["plan", self.vault])
        self.assertIn("plan: new 0, changed 0, unchanged 3, removed 0", out)
        code, out, _ = self.run_cli(["verify", self.vault])
        self.assertEqual(code, 0, out)
        self.assertIn("verify: clean 3, drift 0, unreachable 0", out)

        # Second push after editing one note: exactly that page is overwritten,
        # its wikilink now resolves, and the title rename path stays quiet.
        self.write(SOP + "/Deliver/Onboarding.md",
                   "---\ntype: sop\nowner: Jane\n---\n# Onboarding SOP\n\nStep one, revised. See [[Pit]].\n")
        code, out, _ = self.push()
        self.assertEqual(code, 0, out)
        self.assertIn("pushed 1 (new 0, changed 1), unchanged 2, removed 0 (deleted 0), failed 0", out)
        self.assertEqual(len(self.fake.calls_of("overwrite")), 1)
        self.assertEqual(self.fake.calls_of("create"), [])
        self.assertEqual(self.fake.calls_of("rename"), [])
        token = manifest_mod.load(self.vault).pages[SOP + "/Deliver/Onboarding.md"].node_token
        self.assertEqual(self.fake.calls_of("overwrite"), [("overwrite", token)])
        content = self.fake.nodes[token]["content"]
        self.assertIn("Step one, revised.", content)
        pit_url = manifest_mod.load(self.vault).pages[METH + "/Lessons/Pit.md"].url
        self.assertIn('<a href="%s">Pit</a>' % pit_url, content)

        # A changed H1 renames the node.
        self.write(SOP + "/_SOP-Guide.md", "---\ntype: guide\n---\n# How SOPs are kept now\n\nThe door.\n")
        code, out, _ = self.push()
        self.assertEqual(code, 0, out)
        self.assertEqual(len(self.fake.calls_of("rename")), 1)
        guide_token = manifest_mod.load(self.vault).pages[SOP + "/_SOP-Guide.md"].node_token
        self.assertEqual(self.fake.nodes[guide_token]["title"], "How SOPs are kept now")

        # Third push after deleting a note: listed as removed, node kept.
        os.remove(os.path.join(self.vault, *(METH + "/Lessons/Pit.md").split("/")))
        code, out, err = self.push()
        self.assertEqual(code, 0, out)
        self.assertIn("removed 1 (deleted 0)", out)
        self.assertIn("Pit.md", err)
        self.assertEqual(self.fake.calls_of("delete"), [])
        self.assertIn(METH + "/Lessons/Pit.md", manifest_mod.load(self.vault).pages)
        pit_token = manifest_mod.load(self.vault).pages[METH + "/Lessons/Pit.md"].node_token

        # Only with --delete-removed is the node deleted and the row dropped.
        code, out, _ = self.push("--delete-removed")
        self.assertEqual(code, 0, out)
        self.assertIn("removed 1 (deleted 1)", out)
        self.assertEqual(self.fake.calls_of("delete"), [("delete", pit_token)])
        self.assertNotIn(pit_token, self.fake.nodes)
        self.assertNotIn(METH + "/Lessons/Pit.md", manifest_mod.load(self.vault).pages)
        self.assertFalse(os.path.isfile(os.path.join(self.wiki, pit_token + ".xml")))

        # A failed read-back leaves the manifest untouched and exits 2.
        self.write(SOP + "/Deliver/Onboarding.md", "# Onboarding SOP\n\nThird revision.\n")
        before = self.manifest_text()
        self.fake.fail_read_back = True
        code, out, _ = self.push()
        self.assertEqual(code, 2, out)
        self.assertIn("failed 1", out)
        self.assertEqual(self.manifest_text(), before)
        self.fake.fail_read_back = False

        # A new page that fails read-back is rolled back, so no orphan node.
        self.write(METH + "/Lessons/New.md", "# Brand new\n\ntext\n")
        self.fake.fail_read_back = True
        node_count = len(self.fake.nodes)
        code, out, _ = self.push("--only", METH + "/Lessons/New.md")
        self.assertEqual(code, 2, out)
        self.assertEqual(len(self.fake.nodes), node_count)
        self.assertNotIn(METH + "/Lessons/New.md", manifest_mod.load(self.vault).pages)
        self.fake.fail_read_back = False

        # Verify reports drift when the wiki side changed under us.
        code, out, _ = self.push()
        self.assertEqual(code, 0, out)
        self.fake.nodes[token]["content"] = "<p>someone edited the mirror</p>"
        code, out, _ = self.run_cli(["verify", self.vault])
        self.assertEqual(code, 2)
        self.assertIn("drift       " + SOP + "/Deliver/Onboarding.md", out)

    def test_only_restricts_the_push(self):
        code, out, _ = self.push("--only", METH + "/Lessons/Pit.md")
        self.assertEqual(code, 0, out)
        self.assertIn("pushed 1 (new 1, changed 0)", out)
        self.assertEqual(set(manifest_mod.load(self.vault).pages), {METH + "/Lessons/Pit.md"})
        self.assertEqual(set(n["title"] for n in self.fake.nodes.values()),
                         {"Methodology", "Lessons", "The pit we fell into"})

    def test_convert_verb_uses_manifest_links(self):
        self.push()
        code, out, err = self.run_cli(["convert", self.vault, SOP + "/Deliver/Onboarding.md"])
        self.assertEqual(code, 0)
        pit_url = manifest_mod.load(self.vault).pages[METH + "/Lessons/Pit.md"].url
        self.assertIn('<a href="%s">Pit</a>' % pit_url, out)
        self.assertNotIn("<title>", out)


if __name__ == "__main__":
    unittest.main()
