"""End-to-end tests of the query verbs against the static fixture corpus."""

import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from session_history import connect, ingest, search, show, recent, actions  # noqa: E402

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "projects")
S1 = "11111111-1111-1111-1111-111111111111"


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="sh-cli-")
        self.db = os.path.join(self.tmp, "cli.db")
        self.conn = connect(self.db)
        ingest(self.conn, FIXTURES, progress=False)

    def tearDown(self):
        self.conn.close()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_title_extracted(self):
        row = self.conn.execute("SELECT title FROM sessions WHERE id=?", (S1,)).fetchone()
        self.assertEqual(row["title"], "Symlink safety chat")

    def test_search_symlink(self):
        hits = search(self.conn, "rm -rf symlink")
        self.assertTrue(hits)
        self.assertTrue(any("symlink" in h["snippet"].lower() for h in hits))

    def test_search_ghl(self):
        hits = search(self.conn, "product picker Funnel Products tab")
        self.assertTrue(hits)
        self.assertTrue(any("picker" in h["snippet"].lower() for h in hits))

    def test_show_timeline(self):
        res = show(self.conn, S1)
        self.assertEqual(res["session"]["project"], "proj-alpha")
        self.assertTrue(len(res["messages"]) >= 3)

    def test_recent(self):
        rows = recent(self.conn, 5)
        self.assertTrue(rows)
        self.assertIn(rows[0]["id"], (S1, "22222222-2222-2222-2222-222222222222"))

    def test_actions(self):
        acts = actions(self.conn, S1)
        self.assertTrue(any(a["tool_name"] == "Bash" for a in acts))

    def test_prefix_lookup(self):
        res = show(self.conn, "11111111")
        self.assertEqual(res["session"]["id"], S1)


if __name__ == "__main__":
    unittest.main()
