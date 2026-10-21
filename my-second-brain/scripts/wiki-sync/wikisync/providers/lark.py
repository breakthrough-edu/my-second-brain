"""Lark adapter: wraps lark-cli (verified against lark-cli 1.0.97).

Every call runs ``<lark_bin> ... --as user --format json``. Success is the
envelope's ``ok == true``; the error envelope goes to stderr with a non-zero
exit code (see lark-shared-output-contract). No secrets are printed: only the
command verb and the page are logged.
"""
import json
import os
import shutil
import subprocess
import tempfile

from . import Provider, ProviderError

# Warning that lark-cli raises on the first overwrite into a fresh empty node
# ("no document changes"); the content lands and the revision moves, so it
# is noise and not reported.
NOISE_DEGRADE_CODES = ("1011",)


class LarkProvider(Provider):
    name = "lark"

    def __init__(self, manifest, log=None, **_ignored):
        Provider.__init__(self, manifest, log)
        self.bin = manifest.lark_bin or "lark-cli"

    # [subprocess plumbing]

    def _run(self, args, cwd=None):
        cmd = [self.bin] + list(args) + ["--as", "user", "--format", "json"]
        try:
            proc = subprocess.run(
                cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True)
        except FileNotFoundError:
            raise ProviderError(
                "lark binary not found: %s (set lark_bin in the manifest)" % self.bin,
                fatal=True)
        except OSError as exc:
            raise ProviderError("cannot run %s: %s" % (self.bin, exc), fatal=True)

        envelope = _parse_json(proc.stdout) or _parse_json(proc.stderr)
        if proc.returncode == 0 and envelope and envelope.get("ok") is True:
            return envelope.get("data") or {}

        err = (envelope or {}).get("error") or {}
        etype = err.get("type") or ""
        message = err.get("message") or (proc.stderr or proc.stdout or "").strip()[:400]
        hint = err.get("hint") or ""
        fatal = etype in ("authorization", "auth", "authentication") or (
            "login" in message.lower() or "unauthorized" in message.lower())
        text = "lark-cli %s failed" % " ".join(args[:2])
        if etype:
            text += " (%s)" % etype
        if message:
            text += ": %s" % message
        if hint:
            text += " [hint: %s]" % hint
        raise ProviderError(text, fatal=fatal)

    # [adapter hooks]

    def do_create_node(self, title, parent_token):
        args = ["wiki", "+node-create", "--title", title]
        if parent_token:
            args += ["--parent-node-token", parent_token]
        else:
            args += ["--space-id", str(self.manifest.space_id)]
        data = self._run(args)
        token = data.get("node_token")
        if not token:
            raise ProviderError("node-create returned no node_token")
        return {
            "node_token": token,
            "obj_token": data.get("obj_token", ""),
            "url": self.page_url(token),
        }

    def do_overwrite(self, node_token, url, xml):
        url = url or self.page_url(node_token)
        tmpdir = tempfile.mkdtemp(prefix="wikisync-")
        try:
            with open(os.path.join(tmpdir, "page.xml"), "w", encoding="utf-8") as fh:
                fh.write(xml)
            # The @file path must be relative to the cwd: absolute paths are
            # refused as unsafe, hence the temp dir as working directory.
            data = self._run([
                "docs", "+update", "--doc", url, "--command", "overwrite",
                "--doc-format", "xml", "--content", "@./page.xml",
            ], cwd=tmpdir)
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)
        result = data.get("result")
        if result == "failed":
            raise ProviderError("overwrite of %s reported result=failed" % url)
        real_warnings = 0
        for warning in data.get("warnings") or []:
            if _is_noise(warning):
                continue
            real_warnings += 1
            text = warning if isinstance(warning, str) else json.dumps(warning, ensure_ascii=False)
            self._log("warning on %s: %s" % (url, text[:300]))
        # The first overwrite into a freshly created (empty) node comes back as
        # partial_success with only the 1011 noise attached; that is not a
        # failure, and the read-back decides anyway. Only say so when a real
        # warning came with it.
        if result == "partial_success" and real_warnings:
            self._log("overwrite of %s was partial_success; read-back decides" % url)

    def do_read_back(self, node_token, url):
        url = url or self.page_url(node_token)
        data = self._run(["docs", "+fetch", "--doc", url, "--doc-format", "xml"])
        doc = data.get("document") or {}
        content = doc.get("content")
        if content is None:
            raise ProviderError("fetch of %s returned no document content" % url)
        return content

    def do_delete(self, node_token):
        # A raw token needs --obj-type; wiki means "delete the node itself".
        self._run(["wiki", "+node-delete", "--node-token", node_token,
                   "--obj-type", "wiki", "--yes"])

    def do_rename(self, node_token, url, title):
        url = url or self.page_url(node_token)
        self._run(["drive", "+update-title", "--url", url, "--title", title])

    def do_resolve(self, node_token):
        data = self._run(["wiki", "+node-get", "--node-token", node_token])
        token = data.get("node_token") or node_token
        # node-get does not emit a url; it is built from base_url.
        return {
            "url": self.page_url(token),
            "title": data.get("title", ""),
            "obj_type": data.get("obj_type", ""),
            "node_token": token,
        }


def _is_noise(warning):
    """True for the 'no document changes' degrade warning (code 1011)."""
    if isinstance(warning, dict):
        code = str(warning.get("degrade_code", ""))
        return code in NOISE_DEGRADE_CODES
    text = str(warning)
    return any(("degrade_code=%s" % c) in text for c in NOISE_DEGRADE_CODES)


def _parse_json(text):
    text = (text or "").strip()
    if not text:
        return None
    try:
        value = json.loads(text)
    except ValueError:
        # Some failures print a line of prose before the envelope.
        start = text.find("{")
        if start < 0:
            return None
        try:
            value = json.loads(text[start:])
        except ValueError:
            return None
    return value if isinstance(value, dict) else None
