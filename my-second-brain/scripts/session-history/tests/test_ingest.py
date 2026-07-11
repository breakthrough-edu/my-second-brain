"""Automated tests for session-history incremental ingest.

These target the exact bugs the ingest contract must not have:
mtime-only shortcuts, partial trailing lines, truncation dedup, and
idempotency. Run:  python3 -m unittest discover -s tests -v
"""

import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from session_history import connect, ingest, search  # noqa: E402


def mk_user(sid, uuid, text, ts):
    return json.dumps({
        "type": "user", "uuid": uuid, "sessionId": sid, "timestamp": ts,
        "cwd": "/x", "gitBranch": "main", "version": "1.0.0",
        "message": {"role": "user", "content": text},
    }, ensure_ascii=False)


def mk_assistant(sid, uuid, text, ts):
    return json.dumps({
        "type": "assistant", "uuid": uuid, "sessionId": sid, "timestamp": ts,
        "cwd": "/x", "gitBranch": "main", "version": "1.0.0",
        "message": {"role": "assistant", "content": [{"type": "text", "text": text}]},
    }, ensure_ascii=False)


def total_rows(conn):
    return conn.execute("SELECT count(*) FROM messages").fetchone()[0]


def match_count(conn, term):
    return conn.execute(
        "SELECT count(*) FROM messages WHERE messages MATCH ?", (term,)
    ).fetchone()[0]


class IngestTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="sh-test-")
        self.projects = os.path.join(self.tmp, "projects")
        self.pdir = os.path.join(self.projects, "proj-x")
        os.makedirs(self.pdir)
        self.db = os.path.join(self.tmp, "test.db")
        self.sid = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
        self.path = os.path.join(self.pdir, self.sid + ".jsonl")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _conn(self):
        return connect(self.db)

    def _write(self, lines, trailing_newline=True):
        text = "\n".join(lines)
        if trailing_newline and lines:
            text += "\n"
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(text)

    def _append(self, lines, trailing_newline=True):
        text = "\n".join(lines)
        if trailing_newline:
            text += "\n"
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(text)

    # ------------------------------------------------------------------
    # Test 1: mtime moved BACK must not hide new lines (kills mtime shortcut)
    # ------------------------------------------------------------------
    def test_mtime_rollback_still_indexes(self):
        self._write([
            mk_user(self.sid, "u1", "first message about apples", "2026-07-01T10:00:00Z"),
        ])
        st = os.stat(self.path)
        conn = self._conn()
        ingest(conn, self.projects, progress=False)
        base_rows = total_rows(conn)
        self.assertEqual(base_rows, 1)

        # Append new content, then force mtime back to the ORIGINAL value.
        self._append([
            mk_assistant(self.sid, "a1", "second message about bananas", "2026-07-01T10:00:05Z"),
        ])
        os.utime(self.path, (st.st_atime, st.st_mtime))  # mtime rolled back

        ingest(conn, self.projects, progress=False)
        self.assertEqual(total_rows(conn), 2, "new line must be indexed despite older mtime")
        self.assertEqual(match_count(conn, "bananas"), 1)
        conn.close()

    # ------------------------------------------------------------------
    # Test 2: partial trailing line, then completed → exactly one clean row
    # ------------------------------------------------------------------
    def test_partial_line_then_completed(self):
        good = mk_user(self.sid, "u1", "complete line about cats", "2026-07-01T10:00:00Z")
        partial = mk_assistant(self.sid, "a1", "partial line about dogs", "2026-07-01T10:00:05Z")
        # Write good line + newline, then a partial line WITHOUT trailing newline.
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(good + "\n" + partial)  # no trailing \n on the partial

        conn = self._conn()
        ingest(conn, self.projects, progress=False)
        self.assertEqual(total_rows(conn), 1, "partial trailing line must not be indexed")
        self.assertEqual(match_count(conn, "dogs"), 0)

        # Now complete that line by adding the newline.
        with open(self.path, "a", encoding="utf-8") as f:
            f.write("\n")

        ingest(conn, self.projects, progress=False)
        self.assertEqual(total_rows(conn), 2, "completed line must produce exactly one row")
        self.assertEqual(match_count(conn, "dogs"), 1, "no duplicate / corruption")
        conn.close()

    # ------------------------------------------------------------------
    # Test 3: truncation + rewrite → no duplicates, correct final rows
    # ------------------------------------------------------------------
    def test_truncation_rewrite(self):
        self._write([
            mk_user(self.sid, "u1", "original one alpha", "2026-07-01T10:00:00Z"),
            mk_assistant(self.sid, "a1", "original two beta", "2026-07-01T10:00:05Z"),
            mk_user(self.sid, "u2", "original three gamma", "2026-07-01T10:00:10Z"),
        ])
        conn = self._conn()
        ingest(conn, self.projects, progress=False)
        self.assertEqual(total_rows(conn), 3)

        # Rewrite the file smaller with different content (compaction).
        self._write([
            mk_user(self.sid, "u1", "rewritten single delta", "2026-07-01T11:00:00Z"),
        ])
        ingest(conn, self.projects, progress=False)
        self.assertEqual(total_rows(conn), 1, "old rows must be replaced, not duplicated")
        self.assertEqual(match_count(conn, "gamma"), 0, "stale content gone")
        self.assertEqual(match_count(conn, "delta"), 1)
        conn.close()

    # ------------------------------------------------------------------
    # Test 4: idempotency, twice on unchanged corpus = identical counts
    # ------------------------------------------------------------------
    def test_idempotent_reingest(self):
        self._write([
            mk_user(self.sid, "u1", "idem one", "2026-07-01T10:00:00Z"),
            mk_assistant(self.sid, "a1", "idem two with a tool mention", "2026-07-01T10:00:05Z"),
            mk_user(self.sid, "u2", "idem three", "2026-07-01T10:00:10Z"),
        ])
        conn = self._conn()
        s1 = ingest(conn, self.projects, progress=False)
        rows1 = total_rows(conn)
        m1 = match_count(conn, "idem")

        s2 = ingest(conn, self.projects, progress=False)
        rows2 = total_rows(conn)
        m2 = match_count(conn, "idem")

        self.assertEqual(rows1, rows2, "row count must be byte-identical on re-ingest")
        self.assertEqual(m1, m2, "FTS match count must be byte-identical on re-ingest")
        self.assertEqual(s2["rows_inserted"], 0, "second pass inserts nothing")
        self.assertEqual(s2["files_changed"], 0, "second pass sees no changed files")
        conn.close()

    # ------------------------------------------------------------------
    # Test 5: search count stable except the delta when one file changes
    # ------------------------------------------------------------------
    def test_search_count_stable_except_delta(self):
        # Two sessions; only one changes on the second ingest.
        sid2 = "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
        path2 = os.path.join(self.pdir, sid2 + ".jsonl")
        self._write([
            mk_user(self.sid, "u1", "keyword zebra appears once", "2026-07-01T10:00:00Z"),
        ])
        with open(path2, "w", encoding="utf-8") as f:
            f.write(mk_user(sid2, "u1", "keyword zebra appears here too", "2026-07-01T10:00:00Z") + "\n")

        conn = self._conn()
        ingest(conn, self.projects, progress=False)
        before = len(search(conn, "zebra", limit=100))
        self.assertEqual(before, 2)

        # Append one more zebra hit to ONLY the first file.
        self._append([
            mk_assistant(self.sid, "a1", "another zebra reference", "2026-07-01T10:05:00Z"),
        ])
        ingest(conn, self.projects, progress=False)
        after = len(search(conn, "zebra", limit=100))
        self.assertEqual(after, before + 1, "only the delta changes the search count")
        conn.close()


if __name__ == "__main__":
    unittest.main()
