---
type: sop
status: active
updated: 2026-10-21
owner: Test Owner
review_by: 2026-12-01
lane: run
---

# Dialect fixture: what survives the push

A test page. Every construct below is one thing Obsidian writes that a wiki converter may drop.

## 1. Links

- Bare wikilink: [[_Lark-Guide]]
- Aliased wikilink: [[2026-10-21-company-knowledge-sot-is-each-hods-second-brain-one-way-synced-to-the-wiki|the 10/21 decision]]
- Heading wikilink: [[_Lark-Guide#Recent runs]]
- Path-qualified wikilink: [[04_Breakthrough-Business-Wing/04_Methodology/Playbooks/lark/_Lark-Guide|guide]]
- Ordinary markdown link: [Lark](https://www.larksuite.com)
- Embedded image: ![[sample-image.png]]

## 2. Callouts

> [!NOTE]
> A plain note callout with one line.

> [!WARNING] Titled warning
> Two lines in the body.
> Second line here.

> [!TIP]- Collapsed tip
> This one starts folded.

## 3. Table

| Step | Who | Reads back with |
|---|---|---|
| Create the record | Owner | `+record-list` |
| Change a field | Sync owner | `+field-list`, never `+field-get` |
| Delete | Nobody | n/a |

## 4. Numbered list crossing a heading

1. First step.
2. Second step, with **bold** and *italic* and `inline code`.
3. Third step.

### 4a. Sub-heading between the numbers

4. Fourth step, numbering should continue at 4.
5. Fifth step.

## 5. Nested bullets and tasks

- Parent bullet
  - Child bullet
    - Grandchild bullet
- [ ] Open task
- [x] Done task

## 6. Code block

```bash
lark-cli drive +import --file ./page.md --type docx
```

## 7. Inline odds and ends

Highlight ==like this==, strikethrough ~~like this~~, a footnote[^1], a tag #sop-test, and an emoji marker ⛔ plus a star ⭐.

[^1]: The footnote body.

## 8. Horizontal rule and blockquote

---

> A plain blockquote, not a callout.

End of fixture.
