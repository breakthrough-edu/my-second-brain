# wiki-sync

Pushes the publishable layers of a second brain (an Obsidian vault) one way into a team wiki as a read-only mirror. Lark is the first provider; a `fake` provider exists for tests. The push runs at a session's closeout; this script does the mechanical part: decide what changed, convert each note to the wiki's document XML, create or overwrite the page, read it back to verify, and record state in a manifest inside the vault.

Standard library only, Python 3.9 or newer. Lark calls go through `lark-cli` (verified against 1.0.97) as the logged-in user.

## State

`<vault>/99_Meta/wiki-sync.md` is the manifest: a small frontmatter (provider, space, base url, binary, owner, roots, dates) and two tables, one for mirrored folders, one for mirrored pages (vault path, node token, url, fingerprint, push date). It carries no `type:` key on purpose: it is machine state, not a document. The tool rewrites it whole after every successful step, rows sorted by path.

## Verbs

```
python3 wikisync.py init <vault> --provider lark|fake --space-id S --base-url U --roots a,b,c --owner-name NAME [--lark-bin PATH] [--force]
python3 wikisync.py plan <vault> [--json]
python3 wikisync.py convert <vault> <file> [--stdout]
python3 wikisync.py push <vault> [--dry-run] [--only <vault path>] [--delete-removed]
python3 wikisync.py verify <vault>
```

- `init` writes the manifest; refuses to overwrite one unless `--force`.
- `plan` lists every `.md` under the roots (recursive), skipping notes with `status: empty` and anything dot-prefixed, and classes each as new, changed, unchanged or removed (in the manifest, gone from disk). Fingerprint = first 12 hex of sha256 over the file bytes.
- `convert` prints the DocxXML for one note, wikilinks resolved through the manifest. One stderr line per construct that fell back to escaped text.
- `push` creates the mirrored folder nodes as needed (one node per vault folder below a root, plus the root itself, titled by the folder name with a leading `NN_` stripped), reserves a node for every new page first (titled by its first H1, fallback: file stem) so that links between pages pushed in the same run resolve, then overwrites new and changed pages, and after every overwrite reads the page back and checks for the fingerprint line. The manifest is updated only for pages whose read-back verified; a new node that fails verification is deleted again so the next push can recreate it. Removed pages are listed, and deleted only with `--delete-removed`. Every write is logged to stderr in one line.
- `verify` re-fetches every manifest page and reports drift (fingerprint no longer present) or unreachable pages.

## Exit codes

| code | meaning |
|---|---|
| 0 | clean |
| 1 | usage problem (manifest exists, bad path) |
| 2 | at least one read-back failed (push) or drift found (verify) |
| 3 | provider error: binary missing, not logged in, command refused |
| 4 | not connected: no manifest in the vault |

## What the converter emits

Only tags from the DocxXML reference: `p`, `h1` to `h6`, `b`, `em`, `del`, `code`, `pre`, `a`, `ul`, `ol`, `li` (with `seq`), `checkbox`, `table`/`thead`/`tbody`/`tr`/`th`/`td`, `blockquote`, `callout`, `hr`, `br`, `i`. No `<title>` element: the page title is set on the node, and an overwrite carrying a title would rename it. First block is the mirror header (owner, reviewed date, source line), last block is `Published <date> · fingerprint <12 hex>`, which is what push and verify look for in the read-back. Frontmatter is stripped; `owner` and `last_verified` / `updated` feed the header. Callouts keep only `p`, `ul`, `ol` and `checkbox` children; a table or code fence inside one is emitted right after it.

## Tests

```
cd scripts/wiki-sync && python3 -m unittest discover -s tests -v
```

The fake provider keeps nodes in memory and, when given a directory, mirrors each page's XML to `<dir>/<node_token>.xml` and persists its node table to `<dir>/state.json`. Running the CLI with `--provider fake` uses `$WIKISYNC_FAKE_DIR` or a per-vault folder under the system temp directory.
