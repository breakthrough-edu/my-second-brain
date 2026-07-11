"""Regenerate the static fixture corpus under tests/fixtures/projects/.

Hand-made, tiny, and safe to commit. NOT the live 1.3 GB corpus.
Run:  python3 tests/fixtures/make_fixtures.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "projects")


def line(obj):
    return json.dumps(obj, ensure_ascii=False)


def user(sid, uuid, text, ts, cwd="/x", branch="main"):
    return line({
        "type": "user", "uuid": uuid, "parentUuid": None, "sessionId": sid,
        "timestamp": ts, "cwd": cwd, "gitBranch": branch, "version": "1.0.0",
        "message": {"role": "user", "content": text},
    })


def assistant_text(sid, uuid, text, ts):
    return line({
        "type": "assistant", "uuid": uuid, "sessionId": sid, "timestamp": ts,
        "cwd": "/x", "gitBranch": "main", "version": "1.0.0",
        "message": {"role": "assistant", "content": [{"type": "text", "text": text}]},
    })


def assistant_tool(sid, uuid, name, inp, ts):
    return line({
        "type": "assistant", "uuid": uuid, "sessionId": sid, "timestamp": ts,
        "cwd": "/x", "gitBranch": "main", "version": "1.0.0",
        "message": {"role": "assistant", "content": [
            {"type": "tool_use", "id": "t1", "name": name, "input": inp},
        ]},
    })


def tool_result(sid, uuid, content, ts):
    return line({
        "type": "user", "uuid": uuid, "sessionId": sid, "timestamp": ts,
        "cwd": "/x", "gitBranch": "main", "version": "1.0.0",
        "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "t1", "content": content},
        ]},
    })


def title(sid, t):
    return line({"type": "custom-title", "customTitle": t, "sessionId": sid})


def build():
    os.makedirs(os.path.join(ROOT, "proj-alpha"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "proj-beta"), exist_ok=True)

    s1 = "11111111-1111-1111-1111-111111111111"
    p1 = os.path.join(ROOT, "proj-alpha", s1 + ".jsonl")
    with open(p1, "w", encoding="utf-8") as f:
        f.write("\n".join([
            title(s1, "Symlink safety chat"),
            user(s1, "u1", "how do I remove a symlink dir safely", "2026-07-01T10:00:00Z"),
            assistant_text(s1, "a1", "never rm -rf a symlink directory, it passes through and destroys the target", "2026-07-01T10:00:05Z"),
            assistant_tool(s1, "a2", "Bash", {"command": "rm mylink"}, "2026-07-01T10:00:10Z"),
            tool_result(s1, "u2", "removed", "2026-07-01T10:00:11Z"),
        ]) + "\n")

    s2 = "22222222-2222-2222-2222-222222222222"
    p2 = os.path.join(ROOT, "proj-beta", s2 + ".jsonl")
    with open(p2, "w", encoding="utf-8") as f:
        f.write("\n".join([
            user(s2, "u1", "the GHL order form product picker is missing", "2026-07-02T09:00:00Z"),
            assistant_text(s2, "a1", "product picker lives on the Funnel step Products tab not the element panel", "2026-07-02T09:00:05Z"),
        ]) + "\n")

    print("wrote fixtures to", ROOT)


if __name__ == "__main__":
    build()
