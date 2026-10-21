"""Provider abstraction: what a wiki backend must offer, plus the registry.

Every write goes through the public methods of ``Provider``, which log one
line to stderr (what, which page) and then call the adapter's ``do_*``
method. Adapters raise ``ProviderError``; ``fatal`` marks the class of error
that should stop a push (binary missing, not logged in, command refused).
"""
import sys


class ProviderError(Exception):
    def __init__(self, message, fatal=False):
        Exception.__init__(self, message)
        self.fatal = fatal


class Provider(object):
    name = "base"

    def __init__(self, manifest, log=None):
        self.manifest = manifest
        self._log = log or _stderr_log

    # [public, logged]

    def create_node(self, title, parent_token=None):
        """Create a docx node. Returns {node_token, obj_token, url}."""
        self._log("create node %r under %s" % (title, parent_token or "space root"))
        return self.do_create_node(title, parent_token)

    def overwrite(self, node_token, url, xml):
        self._log("overwrite %s" % (url or node_token))
        return self.do_overwrite(node_token, url, xml)

    def delete(self, node_token):
        self._log("delete node %s" % node_token)
        return self.do_delete(node_token)

    def rename(self, node_token, url, title):
        self._log("rename %s to %r" % (url or node_token, title))
        return self.do_rename(node_token, url, title)

    # [public, read only]

    def read_back(self, node_token, url):
        """Return the page content as XML text."""
        return self.do_read_back(node_token, url)

    def resolve(self, node_token):
        """Return {url, title, obj_type} for a node."""
        return self.do_resolve(node_token)

    def page_url(self, node_token):
        base = (self.manifest.base_url or "").rstrip("/")
        return "%s/wiki/%s" % (base, node_token)

    # [adapter hooks]

    def do_create_node(self, title, parent_token):
        raise NotImplementedError

    def do_overwrite(self, node_token, url, xml):
        raise NotImplementedError

    def do_read_back(self, node_token, url):
        raise NotImplementedError

    def do_delete(self, node_token):
        raise NotImplementedError

    def do_rename(self, node_token, url, title):
        raise NotImplementedError

    def do_resolve(self, node_token):
        raise NotImplementedError


def _stderr_log(message):
    sys.stderr.write("wiki-sync: %s\n" % message)
    sys.stderr.flush()


def get_provider(name, manifest, **kwargs):
    """Instantiate a provider by name. Imports lazily to keep startup light."""
    if name == "lark":
        from .lark import LarkProvider
        return LarkProvider(manifest, **kwargs)
    if name == "fake":
        from .fake import FakeProvider
        return FakeProvider(manifest, **kwargs)
    raise ProviderError("unknown provider: %s" % name, fatal=True)


PROVIDER_NAMES = ("lark", "fake")
