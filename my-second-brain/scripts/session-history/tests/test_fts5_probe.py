"""Tests for the FTS5 runtime probe (WS8 Windows self-serve defensive check).

The whole index is a FTS5 virtual table, so a SQLite without FTS5 (typically
Anaconda) must fail soft with a plain-language fix, not a cryptic
`no such module: fts5`. These tests pin that contract without needing an actual
FTS5-less interpreter: they monkeypatch the probe to simulate the missing case.
"""

import contextlib
import io
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from session_history import (  # noqa: E402
    FTS5_MISSING_MESSAGE,
    FTS5Unavailable,
    connect,
    fts5_available,
)
from session_history import core  # noqa: E402
from session_history.__main__ import main  # noqa: E402


class Fts5ProbeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="sh-fts5-")
        self.db = os.path.join(self.tmp, "probe.db")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_probe_true_on_this_python(self):
        # The dev bench and CI run on FTS5-capable Python; if this fails, the
        # environment itself lacks FTS5 and the tool genuinely cannot run.
        self.assertTrue(fts5_available())

    def test_connect_raises_when_fts5_missing(self):
        orig = core.fts5_available
        core.fts5_available = lambda: False
        try:
            with self.assertRaises(FTS5Unavailable):
                connect(self.db)
        finally:
            core.fts5_available = orig
        # No DB file should have been created on the failing path.
        self.assertFalse(os.path.exists(self.db))

    def test_message_names_the_fix(self):
        # The message must steer the user off Anaconda and onto python.org.
        self.assertIn("FTS5", FTS5_MISSING_MESSAGE)
        self.assertIn("Anaconda", FTS5_MISSING_MESSAGE)
        self.assertIn("python.org", FTS5_MISSING_MESSAGE)

    def test_main_exits_soft_with_message(self):
        orig = core.fts5_available
        core.fts5_available = lambda: False
        err = io.StringIO()
        try:
            with contextlib.redirect_stderr(err):
                rc = main(["--db", self.db, "recent"])
        finally:
            core.fts5_available = orig
        self.assertEqual(rc, 3, "missing FTS5 must exit soft (non-zero), not crash")
        self.assertIn("Anaconda", err.getvalue())
        self.assertIn("python.org", err.getvalue())


if __name__ == "__main__":
    unittest.main()
