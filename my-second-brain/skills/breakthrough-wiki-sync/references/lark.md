# Lark / Feishu adapter

The first provider for `breakthrough-wiki-sync`. Pages go into a Lark **wiki space** (a knowledge base), one node per note, folder nodes mirroring the vault's folders. Everything goes through the official Lark CLI (github.com/larksuite/cli), the same binary the calendar connection uses, so an owner who connected a Lark calendar already has most of this.

## 1. The CLI

1. Install: `npm install -g @larksuite/cli`.
2. Configure app credentials: `lark-cli config init`.
3. Log in as the owner: `lark-cli auth login --recommend`.
4. Verify it can see wiki spaces as the owner: `lark-cli wiki +space-list --as user --format json`. ⚠️ `--as user` matters: without it the CLI often answers as the app and lists the app's spaces, not the owner's.

If the binary is not on PATH, note its full path; `init` takes it as `--lark-bin` and the manifest keeps it.

## 2. The space

Two legal answers, and the owner picks:

- **An existing space** meant for the team: take its `space_id` from the `+space-list` output.
- **A new space:** `lark-cli wiki +space-create --name "<Company> Knowledge" --as user --format json` (user identity only; the create call does not accept the app identity). The result carries `space_id`.

⛔ Not the owner's personal library (`my_library`): the team cannot be given read on that, and the point of the space is that they can.

**The base url** is the tenant's wiki host, the part of any wiki link before `/wiki/` (for example `https://<tenant>.larksuite.com` or `https://<tenant>.feishu.cn`). Read it off any existing wiki link in that tenant, or off the url `lark-cli wiki +node-get --node-token <any node> --as user --format json` returns.

## 3. Init, push, prove

```bash
python3 "<payload>/scripts/wiki-sync/wikisync.py" init "<vault>" --provider lark --space-id <S> --base-url <U> --roots <a,b,c> --owner-name "<name>" [--lark-bin <path>]
python3 "<payload>/scripts/wiki-sync/wikisync.py" plan "<vault>"
python3 "<payload>/scripts/wiki-sync/wikisync.py" push "<vault>"
```

Then the acceptance from the skill file: one real line changed in one note, pushed again, seen in the wiki. Only then is `wiki_provider: lark` recorded.

## 4. What the owner sets in Lark, by hand

This adapter creates nodes and writes pages. It does not change permissions, on purpose: who may read a company's knowledge is the owner's call, made where they can see it.

- **Team as readers:** in the wiki space's member settings, add the team (people, a group, or a department) with **read** permission. ⛔ Not edit: the space is a mirror, and an edit made there is overwritten by the next push.
- **Contribution Space:** create one top-level node in the same space titled `Contribution Space` (the owner can do it in Lark, or `lark-cli wiki +node-create --space-id <S> --title "Contribution Space" --as user`), and give the team **edit** on that node only. That is where suggestions live until the page's owner folds them into the brain.

## 5. Things that look like failures and are not

- The first overwrite into a freshly created, still-empty page can come back with a warning `degrade_code=1011` ("no document changes") while the content did land. The tool reads the page back and trusts the read-back, not the warning.
- A callout's background colour and a custom emoji may come back as the defaults on read-back. Cosmetic.
- A `drive +delete` moves a Drive file to the recycle bin, so an inspected token still resolves for a while; wiki node deletes are immediate. The tool only ever deletes wiki nodes, and only with `--delete-removed`.

## 6. Things that are real failures

- `permission denied` or `missing scope` on any call: stop, do not retry, and show the owner the CLI's own hint (it names the scope or the console url). The usual cause is a login as the app instead of the owner, or a space the owner cannot write to.
- A read-back without the fingerprint of what was just pushed: the tool leaves that page out of the manifest and exits `2`. Say which page; the next push tries it again.
