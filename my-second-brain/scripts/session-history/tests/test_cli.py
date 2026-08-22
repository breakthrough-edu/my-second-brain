"""End-to-end tests of the query verbs against the static fixture corpus."""

import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from session_history import (  # noqa: E402
    IndexNotBuilt,
    actions,
    connect,
    index_built,
    ingest,
    recent,
    search,
    show,
)
from session_history.__main__ import main  # noqa: E402
from session_history.core import THINKING_TOOL_NAME  # noqa: E402

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


class NoIndexYetTests(unittest.TestCase):
    """A query verb run before `ingest` fails soft, and stays a read.

    The tool's own CLAUDE.md tells an owner to run `search` on day one, so the
    first thing a fresh install ever does is query a database `ingest` has not
    touched yet. That has to end in a plain-language fix, not a traceback, and
    it must not quietly index anything on the way.
    """

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="sh-noindex-")
        self.db = os.path.join(self.tmp, "empty.db")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_search_before_ingest_fails_soft(self):
        conn = connect(self.db)
        try:
            self.assertFalse(index_built(conn))
            with self.assertRaises(IndexNotBuilt):
                search(conn, "rm -rf symlink")
        finally:
            conn.close()

        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc = main(["--db", self.db, "search", "rm -rf symlink"])
        self.assertNotEqual(rc, 0, "an unbuilt index must exit non-zero")
        self.assertEqual(rc, 4)
        self.assertIn("ingest", err.getvalue())

        # Still a read: the failed search must not have built the index.
        conn = connect(self.db)
        try:
            self.assertFalse(index_built(conn))
        finally:
            conn.close()


class ThinkingBlockTests(unittest.TestCase):
    """`actions` lists tool calls, and a thinking block is not one.

    The README's own contract, in two halves that have to hold together:
    "Just the tool calls a session made" over `actions`, and one row per
    thinking block "so `search` still finds it while `actions` does not list
    it as a tool call". Thinking is stored with a pseudo tool name, which is
    what makes it reachable by search AND what would make it leak into
    `actions` the moment the filter goes: the row looks exactly like a tool
    call to any query that only asks for a non-null `tool_name`. Nothing else
    in this suite would notice, because the static fixture corpus carries no
    thinking blocks at all, so this class brings its own.
    """

    SID = "33333333-3333-3333-3333-333333333333"
    THOUGHT = "weighing whether the symlink guard covers junctions too"

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="sh-thinking-")
        pdir = os.path.join(self.tmp, "projects", "proj-thinking")
        os.makedirs(pdir)
        line = json.dumps({
            "type": "assistant", "uuid": "a1", "sessionId": self.SID,
            "timestamp": "2026-07-02T09:00:00Z",
            "cwd": "/x", "gitBranch": "main", "version": "1.0.0",
            "message": {"role": "assistant", "content": [
                {"type": "thinking", "thinking": self.THOUGHT},
                {"type": "text", "text": "Removing the link itself, not the target."},
                {"type": "tool_use", "id": "t1", "name": "Bash",
                 "input": {"command": "rm mylink"}},
            ]},
        }, ensure_ascii=False)
        with io.open(os.path.join(pdir, self.SID + ".jsonl"), "w", encoding="utf-8") as fh:
            fh.write(line + "\n")
        self.conn = connect(os.path.join(self.tmp, "thinking.db"))
        ingest(self.conn, os.path.join(self.tmp, "projects"), progress=False)

    def tearDown(self):
        self.conn.close()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_actions_excludes_thinking(self):
        # First the two facts that keep the real assertion from being vacuous:
        # the fixture did grow a thinking row, and search still reaches it.
        row = self.conn.execute(
            "SELECT count(*) AS n FROM messages WHERE session_id=? AND tool_name=?",
            (self.SID, THINKING_TOOL_NAME),
        ).fetchone()
        self.assertEqual(row["n"], 1, "fixture grew no thinking row to filter")
        hits = search(self.conn, "junctions")
        self.assertTrue(
            any(h["tool_name"] == THINKING_TOOL_NAME for h in hits),
            "search must still reach a thinking block",
        )

        acts = actions(self.conn, self.SID)
        self.assertTrue(any(a["tool_name"] == "Bash" for a in acts))
        self.assertNotIn(
            THINKING_TOOL_NAME, [a["tool_name"] for a in acts],
            "a thinking block is not a tool call and must not be listed as one",
        )
        self.assertNotIn(
            self.THOUGHT, " ".join(a["text"] or "" for a in acts),
            "the thinking text leaked into the actions listing",
        )


if __name__ == "__main__":
    unittest.main()
