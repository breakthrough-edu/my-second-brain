import os
import shutil
import tempfile
import unittest

from wikisync import manifest as manifest_mod
from wikisync.manifest import Manifest, Page


class ManifestTest(unittest.TestCase):
    def setUp(self):
        self.vault = tempfile.mkdtemp(prefix="wikisync-vault-")

    def tearDown(self):
        shutil.rmtree(self.vault, ignore_errors=True)

    def sample(self):
        m = Manifest()
        m.provider = "lark"
        m.space_id = "7699053431809380101"
        m.base_url = "https://example.larksuite.com"
        m.lark_bin = "/usr/local/bin/lark-cli"
        m.owner_name = "Jane Owner"
        m.roots = ["04_Acme-Business-Wing/03_SOP", "04_Acme-Business-Wing/04_Methodology"]
        m.connected_on = "2026-10-21"
        m.last_push = ""
        m.folders["04_Acme-Business-Wing/04_Methodology"] = "wikcnB"
        m.folders["04_Acme-Business-Wing/03_SOP"] = "wikcnA"
        m.pages["04_Acme-Business-Wing/04_Methodology/Lessons/Pit.md"] = Page(
            "wikcnP2", "https://example.larksuite.com/wiki/wikcnP2", "bbbbbbbbbbbb", "2026-10-21")
        m.pages["04_Acme-Business-Wing/03_SOP/Onboarding.md"] = Page(
            "wikcnP1", "https://example.larksuite.com/wiki/wikcnP1", "aaaaaaaaaaaa", "2026-10-21")
        return m

    def test_round_trip(self):
        m = self.sample()
        manifest_mod.save(m, self.vault)
        path = manifest_mod.manifest_path(self.vault)
        self.assertTrue(path.endswith(os.path.join("99_Meta", "wiki-sync.md")))
        back = manifest_mod.load(self.vault)
        self.assertEqual(back.provider, "lark")
        self.assertEqual(back.space_id, "7699053431809380101")
        self.assertEqual(back.base_url, "https://example.larksuite.com")
        self.assertEqual(back.lark_bin, "/usr/local/bin/lark-cli")
        self.assertEqual(back.owner_name, "Jane Owner")
        self.assertEqual(back.roots, m.roots)
        self.assertEqual(back.connected_on, "2026-10-21")
        self.assertEqual(back.last_push, "")
        self.assertEqual(back.folders, m.folders)
        self.assertEqual(back.pages, m.pages)
        self.assertEqual(back.render(), m.render())

    def test_rendered_order_is_sorted_and_has_no_type_key(self):
        text = self.sample().render()
        self.assertNotIn("\ntype:", text)
        self.assertLess(text.index("03_SOP | wikcnA"), text.index("04_Methodology | wikcnB"))
        self.assertLess(text.index("03_SOP/Onboarding.md"), text.index("Lessons/Pit.md"))
        self.assertIn("| vault path | node token | url | fingerprint | pushed |", text)
        self.assertIn("| vault folder | node token |", text)
        self.assertIn("# Wiki sync state", text)

    def test_inline_list_parsing(self):
        text = ("---\nprovider: fake\nroots: [a/b, c_d/e , \"f g\"]\nconnected_on: 2026-10-21\n---\n"
                "\n## Folders\n\n| vault folder | node token |\n|---|---|\n\n## Pages\n\n"
                "| vault path | node token | url | fingerprint | pushed |\n|---|---|---|---|---|\n")
        m = Manifest.parse(text)
        self.assertEqual(m.roots, ["a/b", "c_d/e", "f g"])
        self.assertEqual(m.provider, "fake")
        self.assertEqual(m.lark_bin, "lark-cli")
        self.assertEqual(m.folders, {})
        self.assertEqual(m.pages, {})

    def test_load_missing_returns_none(self):
        self.assertIsNone(manifest_mod.load(self.vault))

    def test_page_url_index(self):
        index = self.sample().page_url_index()
        self.assertEqual(index["pit"], "https://example.larksuite.com/wiki/wikcnP2")
        self.assertEqual(index["04_acme-business-wing/03_sop/onboarding"],
                         "https://example.larksuite.com/wiki/wikcnP1")


if __name__ == "__main__":
    unittest.main()
