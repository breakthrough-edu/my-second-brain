"""Markdown (Obsidian dialect) to Lark DocxXML.

One pass over the lines with a small block state machine; no third-party
parser. Only tags from the DocxXML reference are emitted. The output has no
``<title>`` element: the page title is set when the node is created, and an
overwrite that carried a title would rename the page.

Public entry points: ``convert_note``, ``read_frontmatter``, ``page_title``,
``fingerprint_of``.
"""
import datetime
import hashlib
import html
import os
import re

HEADER_TEMPLATE = (
    "Owner: {owner} · Reviewed: {date} · Source: the owner's second brain. "
    "This page is a read-only mirror; suggestions go to the Contribution Space."
)
FOOTER_TEMPLATE = "Published {date} · fingerprint {fingerprint}"

# Children a callout (and, to be safe, a blockquote) may hold.
CONTAINER_CHILDREN = ("p", "ul", "ol", "checkbox")

CALLOUT_EMOJI = {
    "note": "\U0001F4A1", "info": "\U0001F4A1", "abstract": "\U0001F4A1",
    "summary": "\U0001F4A1", "tip": "\U0001F4A1", "hint": "\U0001F4A1",
    "important": "\U0001F4A1",
    "warning": "⚠️", "caution": "⚠️", "attention": "⚠️",
    "danger": "⛔", "error": "⛔", "bug": "⛔", "failure": "⛔",
    "example": "\U0001F4DD", "todo": "\U0001F4DD",
    "quote": "\U0001F4AC", "cite": "\U0001F4AC",
    "question": "❓", "help": "❓", "faq": "❓",
    "success": "✅", "check": "✅", "done": "✅",
}
DEFAULT_EMOJI = "\U0001F4A1"

# [line-level regexes]

FENCE_OPEN_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})\s*([^`\s]*)\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
HR_RE = re.compile(r"^\s{0,3}(?:-\s*){3,}$|^\s{0,3}(?:\*\s*){3,}$|^\s{0,3}(?:_\s*){3,}$")
LIST_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
CHECKBOX_RE = re.compile(r"^\[([ xX])\]\s+(.*)$")
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$")
FOOTDEF_RE = re.compile(r"^\[\^([^\]]+)\]:\s*(.*)$")
CALLOUT_RE = re.compile(r"^\[!([A-Za-z0-9_-]+)\]([+-]?)\s*(.*)$")
EMBED_ALONE_RE = re.compile(r"^!\[\[([^\]]+?)\]\]$")
IMAGE_ALONE_RE = re.compile(r"^!\[[^\]]*\]\(([^)]+)\)$")
RAW_HTML_RE = re.compile(
    r"^<(?:/?)(?:div|span|table|thead|tbody|tr|td|th|iframe|details|summary|br|img|"
    r"center|font|u|b|i|em|strong|sup|sub|kbd|mark|video|audio|a|p|ul|ol|li|"
    r"h[1-6]|pre|code|blockquote|hr|style|script|svg)\b[^>]*>",
    re.I,
)
MATH_BLOCK_RE = re.compile(r"^\$\$")

# [inline regexes]

CODE_SPAN_RE = re.compile(r"(`+)(.+?)\1")
EMBED_RE = re.compile(r"!\[\[([^\]]+?)\]\]")
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
WIKILINK_RE = re.compile(r"\[\[([^\]|#]*)(#[^\]|]*)?(?:\|([^\]]*))?\]\]")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FOOTREF_RE = re.compile(r"\[\^([^\]]+)\]")
PLACEHOLDER_RE = re.compile("\x00(\\d+)\x00")


def esc(text):
    """Escape text content: only &, < and > (quotes stay as they are)."""
    return html.escape(text, quote=False)


def esc_attr(text):
    return html.escape(text, quote=True)


def fingerprint_of(data):
    """First 12 hex of sha256 over the raw file bytes."""
    return hashlib.sha256(data).hexdigest()[:12]


# [frontmatter and title]

def read_frontmatter(text):
    """Return (meta, body). Only top-level ``key: value`` lines are read."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}, text
    for i in range(1, len(lines)):
        if lines[i].strip() in ("---", "..."):
            meta = {}
            for raw in lines[1:i]:
                m = re.match(r"^([A-Za-z0-9_\-]+):\s*(.*)$", raw)
                if m:
                    value = m.group(2).strip()
                    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                        value = value[1:-1]
                    meta[m.group(1)] = value
            return meta, "\n".join(lines[i + 1:])
    return {}, text


def page_title(body, filename):
    """First H1 of the body (outside code fences), else the file stem."""
    in_fence = None
    for line in body.split("\n"):
        m = FENCE_OPEN_RE.match(line)
        if in_fence is None and m:
            in_fence = m.group(1)[0]
            continue
        if in_fence is not None:
            if re.match(r"^\s{0,3}%s{3,}\s*$" % re.escape(in_fence), line):
                in_fence = None
            continue
        h = HEADING_RE.match(line)
        if h and len(h.group(1)) == 1:
            return h.group(2).strip()
    return os.path.splitext(os.path.basename(filename))[0]


# [inline rendering]

class Inline(object):
    """Renders inline markdown to XML text. Text is escaped, tags are not.

    Spans that must survive escaping untouched (code, links, attachments) are
    pulled out into placeholders first, the remaining text is escaped and
    given emphasis tags, then the placeholders are put back."""

    def __init__(self, resolver=None):
        self.resolver = resolver or (lambda target: None)
        self._store = []

    def render(self, text):
        self._store = []
        text = CODE_SPAN_RE.sub(
            lambda m: self._hold("<code>%s</code>" % esc(m.group(2).strip())), text)
        text = EMBED_RE.sub(
            lambda m: self._hold(attachment_inline(m.group(1))), text)
        text = IMAGE_RE.sub(
            lambda m: self._hold(attachment_inline(m.group(2))), text)
        text = WIKILINK_RE.sub(self._wikilink, text)
        text = LINK_RE.sub(
            lambda m: self._hold('<a href="%s">%s</a>' % (
                esc_attr(m.group(2)), self._emphasis(m.group(1)))), text)
        text = FOOTREF_RE.sub(r"[\1]", text)
        out = self._emphasis(text)
        while PLACEHOLDER_RE.search(out):
            out = PLACEHOLDER_RE.sub(lambda m: self._store[int(m.group(1))], out)
        return out

    def _hold(self, xml):
        self._store.append(xml)
        return "\x00%d\x00" % (len(self._store) - 1)

    def _wikilink(self, m):
        target = (m.group(1) or "").strip()
        alias = m.group(3)
        base = target.rsplit("/", 1)[-1]
        if base.lower().endswith(".md"):
            base = base[:-3]
        label = alias.strip() if alias and alias.strip() else base
        url = self.resolver(target) if target else None
        if url:
            return self._hold('<a href="%s">%s</a>' % (esc_attr(url), esc(label)))
        return self._hold(esc(label))

    @staticmethod
    def _emphasis(text):
        text = esc(text)
        text = re.sub(r"~~(.+?)~~", r"<del>\1</del>", text)
        text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
        text = re.sub(r"(?<!\w)__(.+?)__(?!\w)", r"<b>\1</b>", text)
        text = re.sub(r"(?<![\w*])\*(?![\s*])(.+?)(?<![\s*])\*(?![\w*])", r"<em>\1</em>", text)
        text = re.sub(r"(?<!\w)_(?![\s_])(.+?)(?<![\s_])_(?!\w)", r"<em>\1</em>", text)
        text = re.sub(r"==(.+?)==", r"\1", text)
        return text


def attachment_inline(name):
    name = name.split("|", 1)[0].strip()
    return "<i>[attachment not published: %s]</i>" % esc(name)


# [block parsing]

class Block(object):
    __slots__ = ("kind", "xml")

    def __init__(self, kind, xml):
        self.kind = kind
        self.xml = xml


class _Item(object):
    __slots__ = ("indent", "ordered", "seq", "done", "text", "children")

    def __init__(self, indent, ordered, seq, done, text):
        self.indent = indent
        self.ordered = ordered
        self.seq = seq
        self.done = done  # None, "true" or "false"
        self.text = text
        self.children = []


class Parser(object):
    """Turns a list of body lines into Blocks. Re-entered for quote bodies."""

    def __init__(self, inline):
        self.inline = inline
        self.fallbacks = []
        self.footnotes = []

    def parse(self, lines):
        blocks = []
        para = []
        n = len(lines)
        i = 0

        def flush():
            if para:
                blocks.append(Block("p", "<p>%s</p>" % "<br/>".join(
                    self.inline.render(l.strip()) for l in para)))
                del para[:]

        while i < n:
            line = lines[i]
            stripped = line.strip()

            m = FENCE_OPEN_RE.match(line)
            if m:
                flush()
                fence_char = m.group(1)[0]
                lang = m.group(2)
                close = re.compile(r"^\s{0,3}%s{3,}\s*$" % re.escape(fence_char))
                j = i + 1
                code = []
                while j < n and not close.match(lines[j]):
                    code.append(lines[j])
                    j += 1
                attr = ' lang="%s"' % esc_attr(lang) if lang else ""
                blocks.append(Block("pre", "<pre%s><code>%s</code></pre>" % (
                    attr, esc("\n".join(code)))))
                i = j + 1
                continue

            if not stripped:
                flush()
                i += 1
                continue

            m = HEADING_RE.match(line)
            if m:
                flush()
                level = len(m.group(1))
                blocks.append(Block("h%d" % level, "<h%d>%s</h%d>" % (
                    level, self.inline.render(m.group(2)), level)))
                i += 1
                continue

            if HR_RE.match(line):
                flush()
                blocks.append(Block("hr", "<hr/>"))
                i += 1
                continue

            if stripped.startswith(">"):
                flush()
                j = i
                qlines = []
                while j < n and lines[j].lstrip().startswith(">"):
                    qlines.append(re.sub(r"^\s*>\s?", "", lines[j]))
                    j += 1
                blocks.extend(self._quote(qlines))
                i = j
                continue

            if stripped.startswith("|") and i + 1 < n and TABLE_SEP_RE.match(lines[i + 1]) \
                    and lines[i + 1].strip().startswith("|"):
                flush()
                j = i
                rows = []
                while j < n and lines[j].strip().startswith("|"):
                    rows.append(lines[j])
                    j += 1
                blocks.append(self._table(rows))
                i = j
                continue

            m = LIST_RE.match(line)
            if m:
                flush()
                j = i
                items = []
                while j < n:
                    lm = LIST_RE.match(lines[j])
                    if lm:
                        items.append(self._item(lm))
                    elif lines[j].strip() and lines[j][0] in " \t" and items:
                        items[-1].text += " " + lines[j].strip()
                    else:
                        break
                    j += 1
                blocks.extend(self._list_blocks(items))
                i = j
                continue

            m = FOOTDEF_RE.match(stripped)
            if m:
                flush()
                self.footnotes.append((m.group(1), m.group(2)))
                i += 1
                continue

            m = EMBED_ALONE_RE.match(stripped) or IMAGE_ALONE_RE.match(stripped)
            if m:
                flush()
                blocks.append(Block("p", "<p>%s</p>" % attachment_inline(m.group(1))))
                i += 1
                continue

            if RAW_HTML_RE.match(stripped) or MATH_BLOCK_RE.match(stripped):
                flush()
                blocks.append(Block("p", "<p>%s</p>" % esc(stripped)))
                self.fallbacks.append("unmapped line kept as escaped text: %s" % stripped[:60])
                i += 1
                continue

            para.append(line)
            i += 1

        flush()
        return blocks

    # [quotes and callouts]

    def _quote(self, qlines):
        m = CALLOUT_RE.match(qlines[0].strip()) if qlines else None
        if m:
            kind = m.group(1).lower()
            title = m.group(3).strip()
            inner = self.parse(qlines[1:])
            inside = [b for b in inner if b.kind in CONTAINER_CHILDREN]
            after = [b for b in inner if b.kind not in CONTAINER_CHILDREN]
            parts = []
            if title:
                parts.append("<p><b>%s</b></p>" % self.inline.render(title))
            parts.extend(b.xml for b in inside)
            if not parts:
                parts.append("<p></p>")
            xml = '<callout emoji="%s">%s</callout>' % (
                CALLOUT_EMOJI.get(kind, DEFAULT_EMOJI), "".join(parts))
            return [Block("callout", xml)] + after
        inner = self.parse(qlines)
        inside = [b for b in inner if b.kind in CONTAINER_CHILDREN]
        after = [b for b in inner if b.kind not in CONTAINER_CHILDREN]
        if not inside:
            inside = [Block("p", "<p></p>")]
        xml = "<blockquote>%s</blockquote>" % "".join(b.xml for b in inside)
        return [Block("blockquote", xml)] + after

    # [tables]

    def _table(self, rows):
        cells = [_split_cells(r) for r in rows]
        header = cells[0]
        width = len(header)
        body = [c for c in cells[2:]]
        out = ["<table><thead><tr>"]
        for cell in header:
            out.append("<th><p>%s</p></th>" % self.inline.render(cell))
        out.append("</tr></thead><tbody>")
        for row in body:
            row = (row + [""] * width)[:width]
            out.append("<tr>")
            for cell in row:
                out.append("<td><p>%s</p></td>" % self.inline.render(cell))
            out.append("</tr>")
        out.append("</tbody></table>")
        return Block("table", "".join(out))

    # [lists]

    @staticmethod
    def _item(m):
        indent = len(m.group(1).replace("\t", "    "))
        marker = m.group(2)
        text = m.group(3)
        ordered = marker[0].isdigit()
        seq = int(marker[:-1]) if ordered else None
        done = None
        cm = CHECKBOX_RE.match(text)
        if cm and not ordered:
            done = "true" if cm.group(1).lower() == "x" else "false"
            text = cm.group(2)
        return _Item(indent, ordered, seq, done, text)

    def _list_blocks(self, items):
        root = []
        stack = [(-1, root)]
        for it in items:
            while stack and stack[-1][0] >= it.indent:
                stack.pop()
            stack[-1][1].append(it)
            stack.append((it.indent, it.children))
        blocks = []
        run = []
        for it in root:
            if it.done is not None:
                if run:
                    blocks.append(self._run_block(run))
                    run = []
                blocks.append(Block("checkbox", '<checkbox done="%s">%s</checkbox>' % (
                    it.done, self.inline.render(it.text))))
                if it.children:
                    blocks.append(self._run_block(it.children))
                continue
            if run and run[-1].ordered != it.ordered:
                blocks.append(self._run_block(run))
                run = []
            run.append(it)
        if run:
            blocks.append(self._run_block(run))
        return blocks

    def _run_block(self, run):
        """Render one run of sibling items that share a list kind."""
        ordered = run[0].ordered
        tag = "ol" if ordered else "ul"
        return Block(tag, "<%s>%s</%s>" % (tag, "".join(self._li(it) for it in run), tag))

    def _li(self, it):
        text = it.text
        if it.done is not None:
            text = ("☑ " if it.done == "true" else "☐ ") + text
        attr = ' seq="%d"' % it.seq if it.ordered and it.seq is not None else ""
        body = self.inline.render(text)
        if it.children:
            body += "".join(self._nested(it.children))
        return "<li%s>%s</li>" % (attr, body)

    def _nested(self, children):
        runs = []
        run = []
        for c in children:
            if run and run[-1].ordered != c.ordered:
                runs.append(run)
                run = []
            run.append(c)
        if run:
            runs.append(run)
        return [self._run_block(r).xml for r in runs]


WIKILINK_SPAN_RE = re.compile(r"\[\[[^\]]*\]\]")


def _split_cells(line):
    # A wikilink alias also uses "|" ([[target|alias]]); it is not a cell
    # border, so wikilinks are set aside before the row is split.
    holes = []

    def stash(m):
        holes.append(m.group(0))
        return "\x00%d\x00" % (len(holes) - 1)

    body = WIKILINK_SPAN_RE.sub(stash, line.strip())
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    cells = re.split(r"(?<!\\)\|", body)
    restore = lambda c: re.sub(r"\x00(\d+)\x00", lambda m: holes[int(m.group(1))], c)
    return [restore(c).strip().replace("\\|", "|") for c in cells]


# [the whole note]

def strip_comments(body):
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    body = re.sub(r"%%.*?%%", "", body, flags=re.S)
    return body


def convert_note(text, title, owner_name, fingerprint, resolver=None, today=None):
    """Convert one note. Returns (xml, fallbacks).

    ``title`` is the page title the node was created with (see page_title);
    a leading H1 equal to it is dropped. ``resolver`` maps a wikilink target
    to a url or None. ``today`` defaults to the current date."""
    today = today or datetime.date.today().isoformat()
    meta, body = read_frontmatter(text)
    body = strip_comments(body)
    owner = meta.get("owner") or owner_name or "unknown"
    date = meta.get("last_verified") or meta.get("updated") or today

    lines = body.split("\n")
    k = 0
    while k < len(lines) and not lines[k].strip():
        k += 1
    if k < len(lines):
        m = HEADING_RE.match(lines[k])
        if m and len(m.group(1)) == 1 and m.group(2).strip() == title:
            lines = lines[k + 1:]

    inline = Inline(resolver)
    parser = Parser(inline)
    blocks = parser.parse(lines)

    parts = ["<p>%s</p>" % esc(HEADER_TEMPLATE.format(owner=owner, date=date))]
    parts.extend(b.xml for b in blocks)
    for ident, note in parser.footnotes:
        parts.append("<p>[%s] %s</p>" % (esc(ident), inline.render(note)))
    parts.append("<p>%s</p>" % esc(FOOTER_TEMPLATE.format(date=today, fingerprint=fingerprint)))
    return "".join(parts), parser.fallbacks


def footer_marker(fingerprint):
    """The exact substring push and verify look for in a read-back."""
    return "fingerprint %s" % fingerprint
