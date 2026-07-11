"""Tests for the WS2 harvest pipeline.

Target the bookmark-discipline contract that makes proposals safe to re-run:
`harvest` selects only harvested=0 + quiescent + real-conversation sessions, writes
a report whose frontmatter lists exactly the covered ids, and NEVER flips the
`harvested` bookmark. Only `harvest commit` flips it, for exactly those ids, and is
idempotent. Runs against a hand-built fixture corpus, never the live data.
"""

import datetime
import json
import os
import re
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from session_history import (  # noqa: E402
    connect,
    ingest,
    harvest,
    harvest_commit,
    select_harvest_candidates,
    compressed_view,
    filter_batch_echoes,
    default_db_path,
    default_inbox_dir,
)

NOW = "2026-07-11"  # reference instant; cutoff = 2026-07-10T00:00:00Z
_UTC = datetime.timezone.utc


def _epoch(iso: str) -> float:
    return datetime.datetime.fromisoformat(iso).replace(tzinfo=_UTC).timestamp()


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


def read_frontmatter_sessions(report_text):
    fm = report_text.split("\n---", 1)[0]
    m = re.search(r"^sessions:\s*\[(.*)\]\s*$", fm, re.MULTILINE)
    if not m:
        return []
    return [x.strip() for x in m.group(1).split(",") if x.strip()]


class HarvestTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="sh-harvest-")
        self.projects = os.path.join(self.tmp, "projects")
        self.pdir = os.path.join(self.projects, "proj-x")
        os.makedirs(self.pdir)
        self.db = os.path.join(self.tmp, "harvest.db")
        self.report = os.path.join(self.tmp, "2026-07-11-Harvest-Report.md")

        # id -> (lines, mtime_iso, harvested_preset)
        # A/B: quiescent (mtime well before cutoff), real conversation → qualify
        # C: recent mtime (after cutoff) → excluded as still-live
        # D: quiescent but preset harvested=1 → excluded
        # E: quiescent but assistant-only (no user turn) → excluded as bookkeeping
        self.sids = {
            "A": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "B": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
            "C": "cccccccc-cccc-cccc-cccc-cccccccccccc",
            "D": "dddddddd-dddd-dddd-dddd-dddddddddddd",
            "E": "eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee",
        }
        self._write("A", [
            mk_user(self.sids["A"], "u1", "no, don't use the Lark bot token, it 403s", "2026-07-05T10:00:00Z"),
            mk_assistant(self.sids["A"], "a1", "understood, shelling out to lark-cli instead", "2026-07-05T10:00:05Z"),
        ], "2026-07-05T10:00:10")
        self._write("B", [
            mk_user(self.sids["B"], "u1", "let's go with option A for the hero copy", "2026-07-06T10:00:00Z"),
            mk_assistant(self.sids["B"], "a1", "the build failed with a 500 error, turns out the anchor id was wrong", "2026-07-06T10:00:05Z"),
        ], "2026-07-06T10:00:10")
        self._write("C", [
            mk_user(self.sids["C"], "u1", "recent live session still being written", "2026-07-11T05:00:00Z"),
            mk_assistant(self.sids["C"], "a1", "working on it", "2026-07-11T05:00:05Z"),
        ], "2026-07-11T05:30:00")
        self._write("D", [
            mk_user(self.sids["D"], "u1", "already harvested session decision to lock v1.1", "2026-07-04T10:00:00Z"),
            mk_assistant(self.sids["D"], "a1", "logged", "2026-07-04T10:00:05Z"),
        ], "2026-07-04T10:00:10")
        # E: assistant-only, no user text turn.
        self._write("E", [
            mk_assistant(self.sids["E"], "a1", "internal bookkeeping only, no user", "2026-07-03T10:00:00Z"),
        ], "2026-07-03T10:00:10")

        self.conn = connect(self.db)
        ingest(self.conn, self.projects, progress=False)
        # Preset D as already harvested.
        self.conn.execute(
            "UPDATE sessions SET harvested=1, harvested_at='2026-07-04' WHERE id=?",
            (self.sids["D"],),
        )
        self.conn.commit()
        # Force mtimes AFTER ingest (ingest touches nothing, but be explicit).
        for key, (_, mtime, _) in self._specs.items():
            path = os.path.join(self.pdir, self.sids[key] + ".jsonl")
            e = _epoch(mtime)
            os.utime(path, (e, e))

    def tearDown(self):
        self.conn.close()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _write(self, key, lines, mtime_iso):
        if not hasattr(self, "_specs"):
            self._specs = {}
        self._specs[key] = (lines, mtime_iso, 0)
        path = os.path.join(self.pdir, self.sids[key] + ".jsonl")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    def _harvested_map(self):
        return {
            r["id"]: (r["harvested"], r["harvested_at"])
            for r in self.conn.execute(
                "SELECT id, harvested, harvested_at FROM sessions"
            ).fetchall()
        }

    # ------------------------------------------------------------------
    def test_selection_only_qualifying(self):
        sel = select_harvest_candidates(self.conn, NOW)
        ids = {r["id"] for r in sel["selected"]}
        self.assertIn(self.sids["A"], ids)
        self.assertIn(self.sids["B"], ids)
        self.assertNotIn(self.sids["C"], ids, "recent-mtime session must be excluded")
        self.assertNotIn(self.sids["D"], ids, "already-harvested session must be excluded")
        self.assertNotIn(self.sids["E"], ids, "no-user-conversation session must be excluded")
        self.assertEqual(sel["qualified"], 2)
        self.assertEqual(sel["capped_out"], 0)

    def test_report_frontmatter_lists_exact_ids(self):
        stats = harvest(self.conn, now=NOW, out_path=self.report)
        with open(self.report, encoding="utf-8") as f:
            text = f.read()
        fm_ids = set(read_frontmatter_sessions(text))
        self.assertEqual(fm_ids, {self.sids["A"], self.sids["B"]})
        self.assertEqual(set(stats["sessions"]), fm_ids)
        # frontmatter counts present
        self.assertIn("type: harvest-report", text)
        self.assertIn("sessions_qualified: 2", text)
        self.assertIn("sessions_in_report: 2", text)
        self.assertIn("sessions_capped_out: 0", text)

    def test_harvest_does_not_flip_flags(self):
        before = self._harvested_map()
        harvest(self.conn, now=NOW, out_path=self.report)
        after = self._harvested_map()
        self.assertEqual(before, after, "harvest must NOT change any harvested flag")
        # Explicit: A and B still harvested=0.
        self.assertEqual(after[self.sids["A"]][0], 0)
        self.assertEqual(after[self.sids["B"]][0], 0)

    def test_commit_flips_exact_ids_and_idempotent(self):
        harvest(self.conn, now=NOW, out_path=self.report)
        res = harvest_commit(self.conn, self.report, now=NOW)
        self.assertEqual(res["flipped"], 2)
        after = self._harvested_map()
        self.assertEqual(after[self.sids["A"]], (1, "2026-07-11"))
        self.assertEqual(after[self.sids["B"]], (1, "2026-07-11"))
        # untouched sessions
        self.assertEqual(after[self.sids["C"]][0], 0)
        self.assertEqual(after[self.sids["E"]][0], 0)
        # D was preset harvested with its own date; commit must not restamp it.
        self.assertEqual(after[self.sids["D"]], (1, "2026-07-04"))

        # Idempotent second commit flips nothing new (even with a later date).
        res2 = harvest_commit(self.conn, self.report, now="2026-07-12")
        self.assertEqual(res2["flipped"], 0)
        self.assertEqual(res2["already"], 2)
        self.assertEqual(self._harvested_map()[self.sids["A"]], (1, "2026-07-11"))

    def test_reproposes_same_sessions_before_commit(self):
        s1 = harvest(self.conn, now=NOW, out_path=self.report)
        r2 = os.path.join(self.tmp, "second.md")
        s2 = harvest(self.conn, now=NOW, out_path=r2)
        self.assertEqual(set(s1["sessions"]), set(s2["sessions"]),
                         "re-running harvest before commit must repropose the same sessions")

    def test_cap_reports_overflow(self):
        sel = select_harvest_candidates(self.conn, NOW, max_sessions=1)
        self.assertEqual(sel["in_report"], 1)
        self.assertEqual(sel["qualified"], 2)
        self.assertEqual(sel["capped_out"], 1)
        stats = harvest(self.conn, now=NOW, out_path=self.report, max_sessions=1)
        with open(self.report, encoding="utf-8") as f:
            text = f.read()
        self.assertIn("sessions_capped_out: 1", text)
        self.assertEqual(len(stats["sessions"]), 1)

    def test_compressed_view_extracts_signals(self):
        v = compressed_view(self.conn, self.sids["A"])
        self.assertTrue(any("403" in c or "don't" in c.lower() for c in v["corrections"]))
        vb = compressed_view(self.conn, self.sids["B"])
        self.assertTrue(any("go with" in d.lower() for d in vb["decisions"]))
        self.assertTrue(any("failed" in g.lower() or "500" in g for g in vb["gotchas"]))


class NoiseCalibrationTests(unittest.TestCase):
    """The two calibrated noise sources: subagent briefs and injected-context echo."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="sh-noise-")
        self.projects = os.path.join(self.tmp, "projects")
        self.pdir = os.path.join(self.projects, "proj-x")
        os.makedirs(self.pdir)
        self.db = os.path.join(self.tmp, "noise.db")

        self.main_sid = "ffffffff-ffff-ffff-ffff-ffffffffffff"
        reminder_text = (
            "<system-reminder>\n"
            "House rule: 不要 use em dashes anywhere, never override this.\n"
            "</system-reminder>\n"
            "actually, let's rename the report header, the old one is wrong"
        )
        with open(os.path.join(self.pdir, self.main_sid + ".jsonl"), "w",
                  encoding="utf-8") as f:
            f.write(mk_user(self.main_sid, "u1", reminder_text, "2026-07-05T10:00:00Z") + "\n")
            f.write(mk_assistant(self.main_sid, "a1", "renamed as asked", "2026-07-05T10:00:05Z") + "\n")

        self.agent_sid = "agent-a0000000000000001"
        subdir = os.path.join(self.pdir, self.main_sid, "subagents")
        os.makedirs(subdir)
        with open(os.path.join(subdir, self.agent_sid + ".jsonl"), "w",
                  encoding="utf-8") as f:
            f.write(mk_user(self.agent_sid, "u1",
                            "You are a subagent. Don't use tables, avoid bullet walls, "
                            "never write to the vault. Build the summary.",
                            "2026-07-05T11:00:00Z") + "\n")
            f.write(mk_assistant(self.agent_sid, "a1",
                                 "the render failed with a 500 error, turns out the anchor was wrong",
                                 "2026-07-05T11:00:05Z") + "\n")

        self.conn = connect(self.db)
        ingest(self.conn, self.projects, progress=False)
        # Make both transcripts quiescent relative to NOW.
        for p in (
            os.path.join(self.pdir, self.main_sid + ".jsonl"),
            os.path.join(subdir, self.agent_sid + ".jsonl"),
        ):
            e = _epoch("2026-07-05T12:00:00")
            os.utime(p, (e, e))

    def tearDown(self):
        self.conn.close()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_subagent_transcripts_not_selected_for_harvest(self):
        sel = select_harvest_candidates(self.conn, NOW)
        ids = {r["id"] for r in sel["selected"]}
        self.assertIn(self.main_sid, ids)
        self.assertNotIn(self.agent_sid, ids,
                         "subagent transcripts are searchable but never harvested")
        self.assertEqual(sel["qualified"], 1)

    def test_subagent_brief_not_mined_as_corrections(self):
        v = compressed_view(self.conn, self.agent_sid)
        self.assertEqual(v["corrections"], [],
                         "orchestrator brief must never read as owner corrections")
        # The brief's imperative wording must not surface as decisions either.
        self.assertFalse(any("never write to the vault" in d for d in v["decisions"]))
        # Real assistant-side signal survives.
        self.assertTrue(any("500" in g or "failed" in g for g in v["gotchas"]))
        # The brief still names the session.
        self.assertTrue(v["first_user"].startswith("You are a subagent"))

    def test_system_reminder_span_skipped(self):
        v = compressed_view(self.conn, self.main_sid)
        self.assertFalse(any("em dashes" in c for c in v["corrections"]),
                         "lines inside <system-reminder> spans must not be mined")
        self.assertTrue(any("rename the report header" in c for c in v["corrections"]),
                        "real user text after the span must still be mined")

    def test_echo_filter_drops_verbatim_repeats(self):
        echo_line = "House rule: never recreate a Lark base, always reuse the canonical one"
        views = []
        for i in range(4):
            views.append({
                "id": f"s{i}", "corrections": [echo_line],
                "decisions": [f"unique decision {i}: let's go with option {i}"],
                "gotchas": [echo_line] if i < 3 else [],
            })
        views, dropped = filter_batch_echoes(views, min_sessions=3)
        self.assertEqual(dropped, 1)
        for v in views:
            self.assertNotIn(echo_line, v["corrections"])
            self.assertNotIn(echo_line, v["gotchas"])
        self.assertTrue(all(len(v["decisions"]) == 1 for v in views),
                        "unique lines must survive the echo filter")

    def test_echo_filter_keeps_below_threshold(self):
        line = "no, use the staging key"
        views = [
            {"id": "s1", "corrections": [line], "decisions": [], "gotchas": []},
            {"id": "s2", "corrections": [line], "decisions": [], "gotchas": []},
        ]
        views, dropped = filter_batch_echoes(views, min_sessions=3)
        self.assertEqual(dropped, 0)
        self.assertEqual(views[0]["corrections"], [line])


class ConfigTests(unittest.TestCase):
    """Path resolution: flag > env > config file > generic default."""

    ENV_KEYS = ("SESSION_HISTORY_CONFIG", "SESSION_HISTORY_DB",
                "SESSION_HISTORY_PROJECTS", "SESSION_HISTORY_INBOX")

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="sh-config-")
        self._saved = {k: os.environ.get(k) for k in self.ENV_KEYS}
        for k in self.ENV_KEYS:
            os.environ.pop(k, None)
        # Point config discovery at a file we control, never the real one.
        self.cfg_path = os.path.join(self.tmp, "session-history.json")
        os.environ["SESSION_HISTORY_CONFIG"] = self.cfg_path

    def tearDown(self):
        for k, v in self._saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _write_cfg(self, cfg):
        with open(self.cfg_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f)

    def test_defaults_without_config(self):
        self.assertTrue(default_db_path().endswith(
            os.path.join(".my-second-brain", "session-history.db")))
        self.assertIsNone(default_inbox_dir(),
                          "no config, no env -> no report destination")

    def test_config_vault_derives_inbox(self):
        vault = os.path.join(self.tmp, "My-Vault")
        self._write_cfg({"vault": vault, "db": os.path.join(self.tmp, "x.db")})
        self.assertEqual(default_inbox_dir(), os.path.join(vault, "00_Inbox"))
        self.assertEqual(default_db_path(), os.path.join(self.tmp, "x.db"))

    def test_explicit_inbox_beats_vault(self):
        self._write_cfg({"vault": os.path.join(self.tmp, "V"),
                         "inbox": os.path.join(self.tmp, "Elsewhere")})
        self.assertEqual(default_inbox_dir(), os.path.join(self.tmp, "Elsewhere"))

    def test_env_beats_config(self):
        self._write_cfg({"db": os.path.join(self.tmp, "config.db")})
        os.environ["SESSION_HISTORY_DB"] = os.path.join(self.tmp, "env.db")
        self.assertEqual(default_db_path(), os.path.join(self.tmp, "env.db"))

    def test_malformed_config_degrades_to_defaults(self):
        with open(self.cfg_path, "w", encoding="utf-8") as f:
            f.write("{not json")
        self.assertTrue(default_db_path().endswith("session-history.db"))
        self.assertIsNone(default_inbox_dir())


if __name__ == "__main__":
    unittest.main()
