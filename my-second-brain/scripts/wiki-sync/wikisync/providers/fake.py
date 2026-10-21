"""Fake adapter for tests: nodes live in memory, optionally mirrored on disk.

With ``dir`` set, every overwrite also writes ``<dir>/<node_token>.xml`` and
the node table is persisted to ``<dir>/state.json`` so separate CLI runs
against the same directory see the same wiki. ``fail_read_back`` makes
``read_back`` return stale content so a push cannot verify.
"""
import json
import os

from . import Provider, ProviderError


class FakeProvider(Provider):
    name = "fake"

    def __init__(self, manifest, log=None, dir=None, fail_read_back=False, **_ignored):
        Provider.__init__(self, manifest, log)
        self.dir = dir
        self.fail_read_back = fail_read_back
        self.nodes = {}  # token -> {title, parent, content, url}
        self.counter = 0
        self.calls = []  # (verb, token or title) in call order
        if self.dir:
            if not os.path.isdir(self.dir):
                os.makedirs(self.dir)
            self._load_state()

    # [state on disk]

    def _state_path(self):
        return os.path.join(self.dir, "state.json")

    def _load_state(self):
        path = self._state_path()
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as fh:
                state = json.load(fh)
            self.nodes = state.get("nodes", {})
            self.counter = state.get("counter", 0)

    def _save_state(self):
        if not self.dir:
            return
        with open(self._state_path(), "w", encoding="utf-8") as fh:
            json.dump({"nodes": self.nodes, "counter": self.counter}, fh,
                      ensure_ascii=False, indent=1, sort_keys=True)

    # [adapter hooks]

    def do_create_node(self, title, parent_token):
        if parent_token and parent_token not in self.nodes:
            raise ProviderError("parent node does not exist: %s" % parent_token)
        self.counter += 1
        token = "fake%04d" % self.counter
        url = self.page_url(token)
        self.nodes[token] = {"title": title, "parent": parent_token or "",
                             "content": "", "url": url}
        self.calls.append(("create", title))
        self._save_state()
        return {"node_token": token, "obj_token": "obj" + token, "url": url}

    def do_overwrite(self, node_token, url, xml):
        node = self._node(node_token)
        node["content"] = xml
        self.calls.append(("overwrite", node_token))
        if self.dir:
            with open(os.path.join(self.dir, node_token + ".xml"), "w", encoding="utf-8") as fh:
                fh.write(xml)
        self._save_state()

    def do_read_back(self, node_token, url):
        node = self._node(node_token)
        self.calls.append(("read_back", node_token))
        if self.fail_read_back:
            return "<p>stale content, the fetch did not return what was written</p>"
        return node["content"]

    def do_delete(self, node_token):
        self._node(node_token)
        doomed = [node_token] + self._descendants(node_token)
        for t in doomed:
            self.nodes.pop(t, None)
            if self.dir:
                path = os.path.join(self.dir, t + ".xml")
                if os.path.isfile(path):
                    os.remove(path)
        self.calls.append(("delete", node_token))
        self._save_state()

    def do_rename(self, node_token, url, title):
        self._node(node_token)["title"] = title
        self.calls.append(("rename", node_token))
        self._save_state()

    def do_resolve(self, node_token):
        node = self._node(node_token)
        return {"url": node["url"], "title": node["title"], "obj_type": "docx",
                "node_token": node_token}

    # [helpers]

    def _node(self, token):
        if token not in self.nodes:
            raise ProviderError("node does not exist: %s" % token)
        return self.nodes[token]

    def _descendants(self, token):
        out = []
        for t, node in self.nodes.items():
            if node["parent"] == token:
                out.append(t)
                out.extend(self._descendants(t))
        return out

    def calls_of(self, verb):
        return [c for c in self.calls if c[0] == verb]
