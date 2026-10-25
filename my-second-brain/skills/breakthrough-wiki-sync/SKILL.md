---
name: breakthrough-wiki-sync
description: >
  Mirror the publishable layers of the owner's second brain into a team wiki,
  one way, read-only for the team: SOPs, methodology, IT systems and the own
  brands' assets, nothing else, pushed at a session's closeout and never by a
  background process. Off until the owner connects a wiki. Use when the owner
  says "connect my company wiki", "connect a team wiki", "sync my wiki",
  "publish to the wiki", "push my SOPs to the wiki", "what gets published",
  "is the wiki up to date", "disconnect the wiki", 接 wiki, 同步 wiki, 发布到知识库,
  团队要看 SOP, or asks why the team's wiki is behind the brain. Lark is the
  first provider; the rules read the same for any other. NOT the calendar
  connection (that is the owner's command-base skill), NOT the company data
  hub (records live in the systems that produce them), and NOT a writer of
  the pages themselves: it publishes what has already graduated.
---

# Breakthrough Wiki Sync

**The one job: the second brain is the source, the wiki is a mirror, and the mirror never writes back.**

The owner's brain holds the company's shared knowledge in four layers that are written for the team to read (doctrine §4, the publishable-layers law). The team cannot read a vault. This skill carries those four layers into a team wiki as read-only pages, one page per note, same tree, and keeps them current: every time a session closes out, what changed in those layers goes up. Suggestions from the team come back through a Contribution Space in the wiki, which the page's owner reads and folds into the brain; then the next push carries it up. One owner per page, one direction, no drafts.

⭐ **It sleeps until the owner connects a wiki.** Nothing is offered at setup, nothing runs on a schedule, and no watcher is installed. The brain knows the rule from day one (the law names the layers whether or not anything is mirrored); the mirroring itself starts the day the owner asks for it, and it stops the day they say "disconnect".

## Read first, every time

1. `99_Meta/structure-doctrine.md` **§4, the publishable-layers law**: which layers are publishable in this vault, what a page there may say, and whose name and which date go on it. ⭐ **Find it by its words, never by its number:** run `law` (below), which prints the §4 law whose bold opening names the publishable layers and the number it holds in this vault. Vaults number §4 differently (a law the owner added earlier can hold the slot the product template gives this one), so a number quoted from the template or from another vault can point at a different rule here. Exit `5` means this vault has no such law: see "When the vault has no such law". ⛔ Read at the time, from the vault. Never a list quoted here: the owner's law may name a room this file does not know.
2. `99_Meta/structure-doctrine.md` **§7, the five exits**: why a page in those layers is already reviewed, which is why this skill pushes without asking page by page.
3. `99_Meta/bootstrap-progress.md`, key `wiki_provider:`. Absent or `none`: not connected, see "Connect". Anything else: connected, see "Push".
4. `99_Meta/wiki-sync.md`, the manifest: provider, space, roots, and one row per page already published (its node, its url, the fingerprint last pushed). It is a machine state file and carries no `type:`; the tool below owns it. ⛔ Never hand-edit a row.

## The tool

Everything mechanical lives in this payload at `scripts/wiki-sync/wikisync.py`. Resolve the running skill's folder the way the setup mode does (via a global install it is `~/.claude/skills/my-second-brain/`, resolved at runtime); call that folder `<payload>`. ⛔ If `<payload>/scripts/wiki-sync/wikisync.py` is not there, the installed `my-second-brain` is older than this skill (the tool ships from `v4.6.0`): say so, point the owner at the product's update route, and stop; do not look for the script anywhere else. Six verbs, every one read-only on the vault except for the manifest:

```bash
python3 "<payload>/scripts/wiki-sync/wikisync.py" law "<vault>"
python3 "<payload>/scripts/wiki-sync/wikisync.py" init "<vault>" --provider lark --space-id <S> --base-url <U> --roots <a,b,c> --owner-name "<name>"
python3 "<payload>/scripts/wiki-sync/wikisync.py" plan "<vault>"
python3 "<payload>/scripts/wiki-sync/wikisync.py" push "<vault>"
python3 "<payload>/scripts/wiki-sync/wikisync.py" verify "<vault>"
python3 "<payload>/scripts/wiki-sync/wikisync.py" convert "<vault>" "<note>"
```

`law` finds the publishable-layers law by its words and prints it, or exits `5`; `init` runs the same check and refuses to connect without the law. `plan` says what would go up (new, changed, unchanged, removed). `push` converts each new or changed note, creates or overwrites its wiki page, **reads the page back and checks it carries the fingerprint of what was pushed**, and only then records it in the manifest. `verify` re-reads every published page and reports drift. `convert` shows one note's converted form, for a look before a first push. Exit codes: `0` clean, `1` a usage problem (for example `init` on a vault that already has a manifest, which is the reconnect case), `2` a page failed its read-back, `3` the provider refused (binary missing, not logged in), `4` not connected, `5` this vault's doctrine holds no publishable-layers law. ⛔ Never report a push by its exit code alone: read the summary line it prints and say that.

⭐ **A page keeps its address.** The first push creates the page under the node that mirrors its folder; every later push overwrites that same page, so links between published pages and the team's bookmarks never break. ⛔ Never delete and recreate a page to "refresh" it.

## Connect (the station, run once, only when asked)

**First, find the law.** Run `law`. Exit `0`: go on, and when you name the law to the owner, use the number it printed for this vault. Exit `5`: stop and go to "When the vault has no such law"; nothing below is explained, asked or recorded.

**Explain before you connect.** Three facts, in plain terms, before any question:

- **What goes out:** the publishable layers named by this vault's own publishable-layers law (the text `law` printed), read out loud by their real folder names, one line each. Every page there already passed through one of the five exits, so nothing goes out that the owner has not nodded through.
- **What never goes out:** the operator's desk, the work in flight, the personal wing, clients, vendors, employees, company documents, anything held for somebody else's company, and nothing a page may not say to the team (the law says it: no private, personal, client or student matter, no password, no transactional row). ⛔ The roots recorded at connect are the fence; the tool never reads outside them.
- **What the team can do:** read. Suggestions go into a Contribution Space in the wiki, the page's owner folds them into the brain, and the next push carries them up. ⛔ Nothing ever flows from the wiki into the vault.

Then one question: **which wiki?**

- **Lark / Feishu:** the first adapter, steps in [references/lark.md](references/lark.md). It ends with a space id, a base url, and the binary on PATH or its full path.
- **Another tool:** say plainly that no adapter exists for it yet, record nothing, and point at the provider contract below so the owner knows what one would need. ⛔ Do not improvise an adapter through a generic API in the session.
- **Not now:** record `wiki_provider: none` in `99_Meta/bootstrap-progress.md` and stop. Offer once, never nag.

**On a provider:**

1. Ask once whose name goes on every page as its owner (the law says: the brain's owner; a company with several brains has one owner per page). That is `--owner-name`.
2. Read the publishable roots off the publishable-layers law for this vault, as vault-relative paths, and show them. Those are `--roots`. The law names the brand layer as a pattern (`<Brand>-Brand-Assets/`) and keeps out brand assets held for somebody else's company, so list `01_Assets/` for every `*-Brand-Assets/` folder and confirm with the owner which are their own brands; the others stay home.
3. Run `init`. It writes `99_Meta/wiki-sync.md` and refuses to overwrite one that exists (a reconnect reuses it, so published pages keep their addresses).
4. Run `plan` and read the count out loud: this is the first push's size. A vault whose layers are still stubs pushes nothing, and that is a correct result rather than a problem to fix.
5. Run `push`. Report its summary line.
6. ⭐ **The acceptance, and it is not optional:** change one line in one published note (the owner picks the line), run `push` again, and open that page through the url recorded for it in `99_Meta/wiki-sync.md`, in a browser. The line is there, or it is not. ⛔ A CLI fetch proves the content; only the browser proves the address (a wrong base url pushes green, see the adapter reference). `wiki_provider:` is recorded only after the owner has seen the line in the wiki; a connection that has not moved one real line is not connected, however green the exit codes were. If it was a test edit, put the line back and push once more, so the team never reads the test line: a page is what its last push made it.
7. Record in `99_Meta/bootstrap-progress.md`: `wiki_provider: lark`, `wiki_space_id: <S>`, `wiki_connected_on: <date>`, and `wiki_lark_bin: <path>` only when the binary is not on PATH. ⛔ Nothing is written there before step 6 passed.
8. Say the two things the owner now has to do in the wiki itself, because this skill does not touch permissions: make the team readers of the space (read, not edit), and give them edit on the Contribution Space node only. The adapter reference says where those settings live.

## Push (every closeout, and on "sync my wiki")

When `wiki_provider:` names a provider, the closeout skill (`breakthrough-session-report`) calls this step after its backstops and before it writes the baton. The owner saying "sync my wiki" runs the same step outside a closeout.

1. `law`, then `plan`. If `law` exits `5`, do not push: see "When the vault has no such law". Otherwise say in one line what is going up: `N new, M changed`. ⛔ Not the list, unless the owner asks; the layers are already reviewed, and a closeout is two minutes.
2. `push`. Read its summary line and the names of any page that failed its read-back, and say those.
3. **Removed pages are listed, never deleted on their own.** A note that left a publishable layer (moved, archived, deleted) shows as `removed` in the plan. Say so and ask once; on a yes, `push --delete-removed`. ⛔ A page the team may be reading disappears only on the owner's word.
4. **Fail-soft at a closeout.** A push that cannot run (binary missing, login expired, network) is named in the session report's paragraph in one plain sentence and the closeout goes on. ⛔ Never block or delay a closeout for the wiki, and ⛔ never retry in a loop; "sync my wiki" tomorrow is the retry.

**"Is the wiki up to date?"** runs both `plan` (what the brain has that the wiki does not yet: new, changed, removed) and `verify` (what the wiki lost or somebody edited there: drift), and reports the two numbers; either alone answers half the question. **"What gets published?"** reads the law (through `law`) and the roots from the manifest and answers from them; when `law` exits `5`, the answer is that this vault's law does not name any yet. ⛔ Never from memory of an earlier session.

## When the vault has no such law

`law` exits `5` when §4 of this vault's doctrine holds no law whose bold opening names the publishable layers. It happens to a vault built before that law joined the product's template, and to one whose §4 was amended into other words. Without the law there is no fence: nothing in the vault says which layers the team may read, so this skill does not connect and does not push.

- **Say it plainly, in two sentences:** what is missing (this vault's own rules do not yet say which parts the team may read) and why that stops the wiki (pushing without that rule would publish behind a list nobody ruled on).
- ⛔ **Do not fill the gap from anywhere else**: not the four folders the product template names, not this file, not another vault, not an earlier session. Do not run `init` (it refuses with `5` anyway), and record nothing in `99_Meta/bootstrap-progress.md`, not even `wiki_provider: none`, which records the owner's no and not a gap in the law.
- **Offer the one route:** the law is added through `breakthrough-vault-guardian`, as an amendment that lands only on the owner's yes. The proposal to start from is the template's own wording, the §4 law in `<payload>/templates/structure-doctrine.template.md` that opens "The publishable layers are written for the team to read", taking the next free number in this vault's §4. ⛔ Never renumber a law that is already there. Once the guardian has landed it, `law` exits `0` and "Connect" starts again from the top.
- **Already connected and the law has gone** (`law` exits `5` at a push): do not push, leave the manifest and every published page as they are, and say it in one sentence. At a closeout that sentence goes into the report's paragraph and the closeout goes on, the same as any other push that cannot run.

## Disconnect

"Disconnect the wiki": set `wiki_provider: none` in `99_Meta/bootstrap-progress.md`, say that pushes have stopped, and leave `99_Meta/wiki-sync.md` in place (a reconnect reuses the pages). ⛔ Do not delete the wiki pages: the team may be reading them, and taking them down is a decision the owner makes in the wiki, not a side effect of a flag.

## The converter, and what it owes a page

An Obsidian note does not survive a raw import into a wiki document: the frontmatter block turns into a heading, wikilinks and callouts turn into dead text, and angle brackets vanish. The converter in the tool owes every page these, and `convert` shows the result:

- the frontmatter stripped, and a first line in its place: owner, review date, and that the page is a read-only mirror whose suggestions go to the Contribution Space (the law says whose name and which date);
- every wikilink to a page that is also published becomes a real link to that page; a wikilink to anything unpublished becomes its plain words, with no brackets left;
- callouts become the wiki's own highlight blocks, tables stay tables, numbering survives a heading, checkboxes stay checkboxes, code stays code;
- an embedded image or attachment is named as not published rather than dropped silently;
- the last line of every page carries the fingerprint the read-back checks.

## The provider contract (vendor-neutral, so the logic reads the same for any wiki)

An adapter is one module under `scripts/wiki-sync/wikisync/providers/`, and it must do exactly five things: create a node under a parent (folder or page, titled), overwrite one page's whole content with the converted document, read one page back as text, delete one node, and rename one page. Everything else (what is publishable, the tree, the fingerprint, the manifest, when a push happens) is above the adapter and never varies by vendor. ⭐ **Lark is the first adapter and the only one shipped.** An owner on another tool gets the honest line above, not a half-built bridge.

## What this skill is not

- **Not two-way.** It never reads a wiki page in order to change a note. A suggestion in the Contribution Space is read by a person.
- **Not the data hub.** Records (invoices, orders, attendance) live in the systems that produce them (doctrine §4, law 1); this moves pages, never rows.
- **Not a resident process.** No watcher, no schedule, no daemon. The push happens when a session closes out or when the owner says so, and at no other moment.
- **Not a writer of pages.** SOPs, methods, lessons and brand pillars are written by their own skills and nodded through by the owner; this skill meets them after that.
- **Not a judge of what is private.** The publishable-layers law and the roots are the fence; the owner wrote both. A sentence that should not reach the team should not be in a publishable layer at all.
