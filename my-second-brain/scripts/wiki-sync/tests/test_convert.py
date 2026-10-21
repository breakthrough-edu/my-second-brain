import os
import unittest

from wikisync import manifest as manifest_mod
from wikisync.cli import make_resolver
from wikisync.convert import convert_note, page_title, read_frontmatter

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURE = os.path.join(HERE, "fixtures", "dialect-fixture.md")
FP = "0123abcd4567"


def seeded_manifest():
    m = manifest_mod.Manifest()
    m.base_url = "https://example.larksuite.com"
    m.owner_name = "Manifest Owner"
    m.pages["04_Acme/04_Methodology/Playbooks/lark/_Lark-Guide.md"] = manifest_mod.Page(
        "wikcnGUIDE", "https://example.larksuite.com/wiki/wikcnGUIDE", "aaaaaaaaaaaa", "2026-10-20")
    return m


class ConvertFixtureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(FIXTURE, "r", encoding="utf-8") as fh:
            cls.text = fh.read()
        meta, body = read_frontmatter(cls.text)
        cls.meta = meta
        cls.title = page_title(body, FIXTURE)
        cls.xml, cls.fallbacks = convert_note(
            cls.text, cls.title, "Manifest Owner", FP,
            resolver=make_resolver(seeded_manifest()), today="2026-10-21")

    def test_title_is_first_h1(self):
        self.assertEqual(self.title, "Dialect fixture: what survives the push")

    def test_no_frontmatter_and_no_title_element(self):
        self.assertNotIn("type: sop", self.xml)
        self.assertNotIn("review_by", self.xml)
        self.assertNotIn("<title>", self.xml)
        self.assertNotIn("<h1>", self.xml)

    def test_header_paragraph(self):
        self.assertTrue(self.xml.startswith(
            "<p>Owner: Test Owner · Reviewed: 2026-10-21 · Source: the owner's second brain."))
        self.assertIn("read-only mirror; suggestions go to the Contribution Space.</p>", self.xml)

    def test_unresolved_wikilink_becomes_alias_text(self):
        self.assertIn("Aliased wikilink: the 10/21 decision</li>", self.xml)
        self.assertNotIn("[[", self.xml)
        self.assertNotIn("]]", self.xml)

    def test_resolved_wikilink_becomes_anchor(self):
        self.assertIn('<a href="https://example.larksuite.com/wiki/wikcnGUIDE">_Lark-Guide</a>', self.xml)
        self.assertIn('<a href="https://example.larksuite.com/wiki/wikcnGUIDE">guide</a>', self.xml)

    def test_markdown_link_and_embed(self):
        self.assertIn('<a href="https://www.larksuite.com">Lark</a>', self.xml)
        self.assertIn("<i>[attachment not published: sample-image.png]</i>", self.xml)

    def test_callouts(self):
        self.assertIn('<callout emoji="⚠️"><p><b>Titled warning</b></p>', self.xml)
        self.assertIn('<callout emoji="\U0001F4A1"><p>A plain note callout with one line.</p></callout>', self.xml)
        self.assertIn("<p><b>Collapsed tip</b></p>", self.xml)

    def test_table(self):
        self.assertIn("<table><thead><tr><th><p>Step</p></th>", self.xml)
        self.assertIn("<td><p>Create the record</p></td>", self.xml)
        self.assertIn("<td><p><code>+field-list</code>, never <code>+field-get</code></p></td>", self.xml)

    def test_table_cell_keeps_an_aliased_wikilink_whole(self):
        xml, _ = convert_note(
            "| Step | Who |\n|---|---|\n| Plan [[Spring-Menu|the spring menu]] | Mei |\n",
            "T", "Mei", "abcdef123456", resolver=lambda t: "https://x/" + t)
        self.assertIn('<td><p>Plan <a href="https://x/Spring-Menu">the spring menu</a></p></td>'
                      '<td><p>Mei</p></td>', xml)
        self.assertEqual(xml.count("<td"), 2)

    def test_numbering_continues_across_heading(self):
        self.assertIn('<li seq="3">Third step.</li></ol>', self.xml)
        self.assertIn('<ol><li seq="4">Fourth step', self.xml)
        self.assertIn('<li seq="5">Fifth step.</li>', self.xml)

    def test_nested_bullets_and_checkboxes(self):
        self.assertIn("<ul><li>Parent bullet<ul><li>Child bullet<ul><li>Grandchild bullet</li></ul></li></ul></li></ul>", self.xml)
        self.assertIn('<checkbox done="false">Open task</checkbox>', self.xml)
        self.assertIn('<checkbox done="true">Done task</checkbox>', self.xml)

    def test_code_fence(self):
        self.assertIn('<pre lang="bash"><code>lark-cli drive +import --file ./page.md --type docx</code></pre>', self.xml)

    def test_inline_odds(self):
        self.assertIn("Highlight like this, strikethrough <del>like this</del>, a footnote[1], a tag #sop-test", self.xml)
        self.assertIn("<b>bold</b> and <em>italic</em> and <code>inline code</code>", self.xml)
        self.assertIn("<p>[1] The footnote body.</p>", self.xml)
        self.assertIn("<hr/><blockquote><p>A plain blockquote, not a callout.</p></blockquote>", self.xml)

    def test_fingerprint_line_is_last(self):
        self.assertTrue(self.xml.endswith("<p>Published 2026-10-21 · fingerprint %s</p>" % FP))
        self.assertEqual(self.fallbacks, [])


class ConvertSamplesTest(unittest.TestCase):
    def convert(self, text, title="Sample", **kw):
        return convert_note(text, title, "Owner Name", FP, today="2026-10-21", **kw)

    def test_angle_brackets_are_escaped_everywhere(self):
        text = "# Sample\n\nSend it to <external group> & wait.\n\n```\nif a < b: print(x)\n```\n"
        xml, _ = self.convert(text)
        self.assertIn("<p>Send it to &lt;external group&gt; &amp; wait.</p>", xml)
        self.assertIn("<pre><code>if a &lt; b: print(x)</code></pre>", xml)
        self.assertNotIn("<external", xml)

    def test_owner_falls_back_to_manifest_and_date_to_today(self):
        xml, _ = self.convert("Body only, no frontmatter.")
        self.assertTrue(xml.startswith("<p>Owner: Owner Name · Reviewed: 2026-10-21"))

    def test_last_verified_wins_over_updated(self):
        text = "---\nowner: A\nupdated: 2026-01-01\nlast_verified: 2026-02-02\n---\nHi"
        xml, _ = self.convert(text)
        self.assertIn("Owner: A · Reviewed: 2026-02-02", xml)

    def test_h1_not_equal_to_title_is_kept(self):
        xml, _ = self.convert("# Another heading\n\ntext", title="Sample")
        self.assertIn("<h1>Another heading</h1>", xml)

    def test_table_inside_callout_is_emitted_after_it(self):
        text = "> [!NOTE] Title\n> line one\n> | a | b |\n> |---|---|\n> | 1 | 2 |\n"
        xml, _ = self.convert(text)
        self.assertIn('<callout emoji="\U0001F4A1"><p><b>Title</b></p><p>line one</p></callout><table>', xml)

    def test_html_comment_removed_and_raw_html_falls_back(self):
        text = "para <!-- hidden --> text\n\n<div class=\"x\">raw</div>\n"
        xml, fallbacks = self.convert(text)
        self.assertIn("<p>para  text</p>", xml)
        self.assertIn("<p>&lt;div class=\"x\"&gt;raw&lt;/div&gt;</p>", xml)
        self.assertEqual(len(fallbacks), 1)

    def test_wikilink_resolution_is_case_insensitive_and_strips_heading(self):
        m = seeded_manifest()
        resolver = make_resolver(m)
        xml, _ = self.convert("See [[_lark-guide#Recent runs|the guide]] and [[_Lark-Guide.md]].", resolver=resolver)
        self.assertEqual(xml.count('<a href="https://example.larksuite.com/wiki/wikcnGUIDE">'), 2)
        self.assertIn(">the guide</a>", xml)
        self.assertIn(">_Lark-Guide</a>", xml)


if __name__ == "__main__":
    unittest.main()
