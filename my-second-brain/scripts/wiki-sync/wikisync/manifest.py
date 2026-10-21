"""Read and write the sync state file: ``<vault>/99_Meta/wiki-sync.md``.

The manifest is machine state, not a document: it carries no ``type:`` key.
Shape: a frontmatter block of simple ``key: value`` lines (``roots`` is one
inline list), then two markdown tables, ``## Folders`` and ``## Pages``.
The file is rewritten whole on every change, rows sorted by path.
"""
import os
import re

MANIFEST_REL = os.path.join("99_Meta", "wiki-sync.md")

FRONT_KEYS = [
    "provider",
    "space_id",
    "base_url",
    "lark_bin",
    "owner_name",
    "roots",
    "connected_on",
    "last_push",
]

FOLDER_HEADER = ["vault folder", "node token"]
PAGE_HEADER = ["vault path", "node token", "url", "fingerprint", "pushed"]

_SEP_CELL = re.compile(r"^:?-+:?$")


class ManifestError(Exception):
    """Raised when the manifest file cannot be parsed."""


class Page(object):
    """One mirrored page: where it lives in the wiki and what was pushed."""

    __slots__ = ("node_token", "url", "fingerprint", "pushed")

    def __init__(self, node_token="", url="", fingerprint="", pushed=""):
        self.node_token = node_token
        self.url = url
        self.fingerprint = fingerprint
        self.pushed = pushed

    def as_row(self):
        return [self.node_token, self.url, self.fingerprint, self.pushed]

    def __eq__(self, other):
        return isinstance(other, Page) and self.as_row() == other.as_row()

    def __repr__(self):
        return "Page(%r, %r, %r, %r)" % tuple(self.as_row())


class Manifest(object):
    """In-memory form of the state file."""

    def __init__(self):
        self.provider = "lark"
        self.space_id = ""
        self.base_url = ""
        self.lark_bin = "lark-cli"
        self.owner_name = ""
        self.roots = []
        self.connected_on = ""
        self.last_push = ""
        self.folders = {}  # vault folder (relative, forward slashes) -> node token
        self.pages = {}  # vault path (relative, forward slashes) -> Page

    # [parsing]

    @classmethod
    def parse(cls, text):
        m = cls()
        lines = text.split("\n")
        if not lines or lines[0].strip() != "---":
            raise ManifestError("manifest has no frontmatter block")
        end = None
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                end = i
                break
        if end is None:
            raise ManifestError("manifest frontmatter is not closed")
        for raw in lines[1:end]:
            if not raw.strip() or raw.lstrip().startswith("#"):
                continue
            if ":" not in raw:
                raise ManifestError("bad frontmatter line: %r" % raw)
            key, value = raw.split(":", 1)
            key = key.strip()
            value = value.strip()
            if key == "roots":
                m.roots = _parse_inline_list(value)
            elif key in FRONT_KEYS:
                setattr(m, key, _unquote(value))
            # unknown keys are ignored so a future field does not break an old reader
        section = None
        for raw in lines[end + 1:]:
            line = raw.strip()
            if line.startswith("## "):
                section = line[3:].strip().lower()
                continue
            if not line.startswith("|") or section is None:
                continue
            cells = _split_row(line)
            if all(_SEP_CELL.match(c) for c in cells if c) and any(cells):
                continue
            if section == "folders":
                if cells[:2] == FOLDER_HEADER:
                    continue
                cells = _pad(cells, 2)
                if cells[0]:
                    m.folders[cells[0]] = cells[1]
            elif section == "pages":
                if cells[:5] == PAGE_HEADER:
                    continue
                cells = _pad(cells, 5)
                if cells[0]:
                    m.pages[cells[0]] = Page(cells[1], cells[2], cells[3], cells[4])
        return m

    # [rendering]

    def render(self):
        out = ["---"]
        for key in FRONT_KEYS:
            value = getattr(self, key)
            if key == "roots":
                out.append("roots: [%s]" % ", ".join(self.roots))
            else:
                out.append("%s: %s" % (key, value) if value != "" else "%s:" % key)
        out.append("---")
        out.append("")
        out.append("# Wiki sync state")
        out.append("")
        out.append("## Folders")
        out.append("")
        out.append(_row(FOLDER_HEADER))
        out.append(_row(["---"] * 2))
        for folder in sorted(self.folders):
            out.append(_row([folder, self.folders[folder]]))
        out.append("")
        out.append("## Pages")
        out.append("")
        out.append(_row(PAGE_HEADER))
        out.append(_row(["---"] * 5))
        for path in sorted(self.pages):
            out.append(_row([path] + self.pages[path].as_row()))
        out.append("")
        return "\n".join(out)

    # [helpers]

    def page_url_index(self):
        """Lowercase basename (no extension) and lowercase full path -> url.

        Used by the converter to resolve wikilinks. A basename that several
        pages share keeps the first in sorted path order."""
        index = {}
        for path in sorted(self.pages):
            url = self.pages[path].url
            stem = path.rsplit("/", 1)[-1]
            if stem.lower().endswith(".md"):
                stem = stem[:-3]
            full = path[:-3] if path.lower().endswith(".md") else path
            index.setdefault(stem.lower(), url)
            index.setdefault(full.lower(), url)
        return index


def manifest_path(vault):
    return os.path.join(vault, MANIFEST_REL)


def load(vault):
    """Return the Manifest for a vault, or None when it is not connected."""
    path = manifest_path(vault)
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as fh:
        return Manifest.parse(fh.read())


def save(manifest, vault):
    path = manifest_path(vault)
    folder = os.path.dirname(path)
    if not os.path.isdir(folder):
        os.makedirs(folder)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(manifest.render())
    os.replace(tmp, path)


def _row(cells):
    return "| " + " | ".join(cells) + " |"


def _split_row(line):
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [c.strip() for c in body.split("|")]


def _pad(cells, n):
    return (cells + [""] * n)[:n]


def _parse_inline_list(value):
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    items = [_unquote(v.strip()) for v in value.split(",")]
    return [v for v in items if v]


def _unquote(value):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value
