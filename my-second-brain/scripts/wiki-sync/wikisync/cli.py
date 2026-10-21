"""Command line: init, plan, convert, push, verify.

``main(argv, provider_factory=None)`` returns the exit code instead of
exiting, so tests can drive it and inject a provider that keeps state
between runs. Exit codes: 0 clean, 2 read-back failed or drift, 3 provider
error (binary missing, not logged in, command refused), 4 not connected
(no manifest).
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import sys
import tempfile

from . import __version__, manifest as manifest_mod
from .convert import convert_note, fingerprint_of, footer_marker, page_title, read_frontmatter
from .providers import PROVIDER_NAMES, ProviderError, get_provider

EXIT_OK = 0
EXIT_UNVERIFIED = 2
EXIT_PROVIDER = 3
EXIT_NOT_CONNECTED = 4

PREFIX_RE = re.compile(r"^\d+_")


def log(message):
    sys.stderr.write("wiki-sync: %s\n" % message)
    sys.stderr.flush()


def today():
    return datetime.date.today().isoformat()


# [scanning the vault]

def scan(vault, roots):
    """Return {vault_path: fingerprint} for every publishable note under the roots.

    Skips dot-prefixed files and folders and notes whose frontmatter says
    ``status: empty``. Paths are vault-relative with forward slashes."""
    found = {}
    for root in roots:
        root_abs = os.path.join(vault, *root.split("/"))
        if not os.path.isdir(root_abs):
            log("root folder missing on disk: %s" % root)
            continue
        for dirpath, dirnames, filenames in os.walk(root_abs):
            dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
            for name in sorted(filenames):
                if name.startswith(".") or not name.lower().endswith(".md"):
                    continue
                full = os.path.join(dirpath, name)
                with open(full, "rb") as fh:
                    data = fh.read()
                meta, _ = read_frontmatter(data.decode("utf-8", "replace"))
                if meta.get("status", "").strip().lower() == "empty":
                    continue
                rel = os.path.relpath(full, vault).replace(os.sep, "/")
                found[rel] = fingerprint_of(data)
    return found


def make_plan(vault, manifest):
    on_disk = scan(vault, manifest.roots)
    plan = {"new": [], "changed": [], "unchanged": [], "removed": []}
    for path in sorted(on_disk):
        fp = on_disk[path]
        page = manifest.pages.get(path)
        if page is None:
            plan["new"].append({"path": path, "fingerprint": fp})
        elif page.fingerprint != fp:
            plan["changed"].append({"path": path, "fingerprint": fp, "was": page.fingerprint})
        else:
            plan["unchanged"].append({"path": path, "fingerprint": fp})
    for path in sorted(manifest.pages):
        if path not in on_disk:
            plan["removed"].append({"path": path, "node_token": manifest.pages[path].node_token})
    return plan


def summary_line(plan):
    return "plan: new %d, changed %d, unchanged %d, removed %d" % (
        len(plan["new"]), len(plan["changed"]), len(plan["unchanged"]), len(plan["removed"]))


# [conversion helpers]

def folder_title(name):
    return PREFIX_RE.sub("", name) or name


def make_resolver(manifest):
    index = manifest.page_url_index()

    def resolve(target):
        target = target.strip()
        if target.endswith("#"):
            target = target[:-1]
        key = target.lower()
        if key.endswith(".md"):
            key = key[:-3]
        if key in index:
            return index[key]
        base = key.rsplit("/", 1)[-1]
        return index.get(base)

    return resolve


def convert_file(vault, rel_path, manifest, resolver, publish_date=None):
    """Read one note and convert it. Returns (title, xml, fingerprint, fallbacks)."""
    full = os.path.join(vault, *rel_path.split("/"))
    with open(full, "rb") as fh:
        data = fh.read()
    text = data.decode("utf-8", "replace")
    fp = fingerprint_of(data)
    _, body = read_frontmatter(text)
    title = page_title(body, rel_path)
    owner = manifest.owner_name if manifest else ""
    xml, fallbacks = convert_note(text, title, owner, fp, resolver=resolver, today=publish_date)
    return title, xml, fp, fallbacks


# [verbs]

def cmd_init(args):
    vault = os.path.abspath(args.vault)
    if not os.path.isdir(vault):
        print("not a folder: %s" % vault, file=sys.stderr)
        return EXIT_PROVIDER
    path = manifest_mod.manifest_path(vault)
    if os.path.exists(path) and not args.force:
        print("manifest already exists: %s (use --force to overwrite)" % path, file=sys.stderr)
        return 1
    m = manifest_mod.Manifest()
    m.provider = args.provider
    m.space_id = args.space_id or ""
    m.base_url = (args.base_url or "").rstrip("/")
    m.lark_bin = args.lark_bin or "lark-cli"
    m.owner_name = args.owner_name or ""
    m.roots = [r.strip().strip("/") for r in (args.roots or "").split(",") if r.strip()]
    m.connected_on = today()
    m.last_push = ""
    manifest_mod.save(m, vault)
    print("wrote %s (provider %s, %d roots)" % (path, m.provider, len(m.roots)))
    return EXIT_OK


def cmd_plan(args):
    vault = os.path.abspath(args.vault)
    manifest = manifest_mod.load(vault)
    if manifest is None:
        print("not connected: no manifest at %s" % manifest_mod.manifest_path(vault), file=sys.stderr)
        return EXIT_NOT_CONNECTED
    plan = make_plan(vault, manifest)
    print(summary_line(plan))
    if args.json:
        print(json.dumps(plan, indent=2, ensure_ascii=False))
    else:
        for kind in ("new", "changed", "removed"):
            for entry in plan[kind]:
                print("  %-9s %s" % (kind, entry["path"]))
    return EXIT_OK


def cmd_convert(args):
    vault = os.path.abspath(args.vault)
    manifest = manifest_mod.load(vault)
    if manifest is None:
        log("no manifest: wikilinks will not resolve and the owner comes from frontmatter only")
        manifest = manifest_mod.Manifest()
    file_arg = args.file
    if os.path.isabs(file_arg):
        rel = os.path.relpath(file_arg, vault).replace(os.sep, "/")
    else:
        rel = file_arg.replace(os.sep, "/")
    if not os.path.isfile(os.path.join(vault, *rel.split("/"))):
        print("file not found in vault: %s" % rel, file=sys.stderr)
        return 1
    _, xml, _, fallbacks = convert_file(vault, rel, manifest, make_resolver(manifest))
    for fb in fallbacks:
        log("fallback in %s: %s" % (rel, fb))
    sys.stdout.write(xml + "\n")
    return EXIT_OK


class Pusher(object):
    """Runs one push against a provider, saving the manifest after each step."""

    def __init__(self, vault, manifest, provider, dry_run=False):
        self.vault = vault
        self.manifest = manifest
        self.provider = provider
        self.dry_run = dry_run
        self.date = today()
        self.counts = {"new": 0, "changed": 0, "unchanged": 0, "removed": 0,
                       "deleted": 0, "failed": 0}
        self.failures = []

    def save(self):
        if not self.dry_run:
            manifest_mod.save(self.manifest, self.vault)

    # [folders]

    def ensure_folder(self, folder):
        """Return the node token for a vault folder, creating the chain as needed."""
        if folder in self.manifest.folders:
            return self.manifest.folders[folder]
        if folder in self.manifest.roots:
            parent = None
        else:
            parent_folder = folder.rsplit("/", 1)[0] if "/" in folder else ""
            if not parent_folder:
                raise ProviderError("folder %s is outside every root" % folder, fatal=True)
            parent = self.ensure_folder(parent_folder)
        title = folder_title(folder.rsplit("/", 1)[-1])
        if self.dry_run:
            log("would create folder node %r for %s" % (title, folder))
            token = "dry-run"
        else:
            token = self.provider.create_node(title, parent)["node_token"]
        self.manifest.folders[folder] = token
        self.save()
        return token

    def folder_of(self, rel_path):
        """The vault folder a page's node lives in (its own folder, root or below)."""
        folder = rel_path.rsplit("/", 1)[0] if "/" in rel_path else ""
        for root in self.manifest.roots:
            if folder == root or folder.startswith(root + "/"):
                return folder
        raise ProviderError("page %s is outside every root" % rel_path, fatal=True)

    # [pages]

    def verify(self, rel_path, token, url, fp):
        content = self.provider.read_back(token, url)
        marker = footer_marker(fp)
        if marker in content:
            return True
        self.failures.append(rel_path)
        log("read-back of %s does not carry %s" % (rel_path, marker))
        return False

    def reserve_new(self, entry):
        """Create the node for a new page before any page is converted.

        A wikilink resolves from the manifest, so a page that links to another
        page pushed in the same run would come out as plain text if nodes were
        created one by one. Reserving every new node first, with an empty
        fingerprint, lets the links land on the first push. A reserved entry
        that never verifies is removed again in push_new; one left behind by a
        crash shows up as "changed" on the next plan and is filled in then."""
        rel = entry["path"]
        if rel in self.manifest.pages:
            return
        full = os.path.join(self.vault, *rel.split("/"))
        with open(full, "rb") as fh:
            _, body = read_frontmatter(fh.read().decode("utf-8", "replace"))
        title = page_title(body, rel)
        folder_token = self.ensure_folder(self.folder_of(rel))
        if self.dry_run:
            log("would create page %r for %s" % (title, rel))
            return
        node = self.provider.create_node(title, folder_token)
        self.manifest.pages[rel] = manifest_mod.Page(node["node_token"], node["url"], "", "")
        self.save()

    def push_new(self, entry):
        rel = entry["path"]
        resolver = make_resolver(self.manifest)
        title, xml, fp, fallbacks = convert_file(self.vault, rel, self.manifest, resolver, self.date)
        for fb in fallbacks:
            log("fallback in %s: %s" % (rel, fb))
        if self.dry_run:
            log("would overwrite the new page %r for %s" % (title, rel))
            self.counts["new"] += 1
            return
        reserved = self.manifest.pages[rel]
        token, url = reserved.node_token, reserved.url
        self.provider.overwrite(token, url, xml)
        if self.verify(rel, token, url, fp):
            self.manifest.pages[rel] = manifest_mod.Page(token, url, fp, self.date)
            self.save()
            self.counts["new"] += 1
        else:
            self.counts["failed"] += 1
            del self.manifest.pages[rel]
            self.save()
            try:
                self.provider.delete(token)
                log("removed the unverified new node for %s so the next push recreates it" % rel)
            except ProviderError as exc:
                log("could not remove unverified node %s for %s: %s" % (token, rel, exc))

    def push_changed(self, entry):
        rel = entry["path"]
        page = self.manifest.pages[rel]
        resolver = make_resolver(self.manifest)
        title, xml, fp, fallbacks = convert_file(self.vault, rel, self.manifest, resolver, self.date)
        for fb in fallbacks:
            log("fallback in %s: %s" % (rel, fb))
        if self.dry_run:
            log("would overwrite %s (%s)" % (rel, page.url))
            self.counts["changed"] += 1
            return
        url = page.url or self.provider.page_url(page.node_token)
        try:
            current = self.provider.resolve(page.node_token)
            if current.get("title") and current["title"] != title:
                self.provider.rename(page.node_token, url, title)
        except ProviderError as exc:
            if exc.fatal:
                raise
            log("could not check the title of %s: %s" % (rel, exc))
        self.provider.overwrite(page.node_token, url, xml)
        if self.verify(rel, page.node_token, url, fp):
            page.url = url
            page.fingerprint = fp
            page.pushed = self.date
            self.save()
            self.counts["changed"] += 1
        else:
            self.counts["failed"] += 1

    def push_removed(self, entry, delete):
        rel = entry["path"]
        self.counts["removed"] += 1
        if not delete:
            log("removed from the vault, node kept (use --delete-removed): %s" % rel)
            return
        page = self.manifest.pages[rel]
        if self.dry_run:
            log("would delete node %s for %s" % (page.node_token, rel))
            self.counts["deleted"] += 1
            return
        self.provider.delete(page.node_token)
        del self.manifest.pages[rel]
        self.save()
        self.counts["deleted"] += 1

    # [the run]

    def run(self, plan, only=None, delete_removed=False):
        def wanted(entry):
            return only is None or entry["path"] == only

        for entry in plan["new"]:
            if wanted(entry):
                self.reserve_new(entry)
        for entry in plan["new"]:
            if wanted(entry):
                self.push_new(entry)
        for entry in plan["changed"]:
            if wanted(entry):
                self.push_changed(entry)
        self.counts["unchanged"] = len([e for e in plan["unchanged"] if wanted(e)])
        for entry in plan["removed"]:
            if wanted(entry):
                self.push_removed(entry, delete_removed)
        if not self.dry_run and (self.counts["new"] or self.counts["changed"] or self.counts["deleted"]):
            self.manifest.last_push = self.date
            self.save()

    def summary(self):
        c = self.counts
        return "pushed %d (new %d, changed %d), unchanged %d, removed %d (deleted %d), failed %d" % (
            c["new"] + c["changed"], c["new"], c["changed"], c["unchanged"],
            c["removed"], c["deleted"], c["failed"])


def _provider_for(manifest, vault, provider_factory):
    if provider_factory is not None:
        return provider_factory(manifest, vault)
    kwargs = {}
    if manifest.provider == "fake":
        kwargs["dir"] = os.environ.get("WIKISYNC_FAKE_DIR") or os.path.join(
            tempfile.gettempdir(),
            "wikisync-fake-" + hashlib.sha256(vault.encode("utf-8")).hexdigest()[:10])
    return get_provider(manifest.provider, manifest, **kwargs)


def cmd_push(args, provider_factory=None):
    vault = os.path.abspath(args.vault)
    manifest = manifest_mod.load(vault)
    if manifest is None:
        print("not connected: no manifest at %s" % manifest_mod.manifest_path(vault), file=sys.stderr)
        return EXIT_NOT_CONNECTED
    only = args.only.replace(os.sep, "/").strip("/") if args.only else None
    try:
        provider = _provider_for(manifest, vault, provider_factory)
        plan = make_plan(vault, manifest)
        if only is not None and not any(
                e["path"] == only for kind in plan for e in plan[kind]):
            print("--only path is not under the roots or not in the manifest: %s" % only, file=sys.stderr)
            return 1
        pusher = Pusher(vault, manifest, provider, dry_run=args.dry_run)
        pusher.run(plan, only=only, delete_removed=args.delete_removed)
    except ProviderError as exc:
        print("provider error: %s" % exc, file=sys.stderr)
        return EXIT_PROVIDER
    prefix = "dry run: " if args.dry_run else ""
    print(prefix + pusher.summary())
    return EXIT_UNVERIFIED if pusher.counts["failed"] else EXIT_OK


def cmd_verify(args, provider_factory=None):
    vault = os.path.abspath(args.vault)
    manifest = manifest_mod.load(vault)
    if manifest is None:
        print("not connected: no manifest at %s" % manifest_mod.manifest_path(vault), file=sys.stderr)
        return EXIT_NOT_CONNECTED
    try:
        provider = _provider_for(manifest, vault, provider_factory)
    except ProviderError as exc:
        print("provider error: %s" % exc, file=sys.stderr)
        return EXIT_PROVIDER
    clean, drift, unreachable = [], [], []
    for path in sorted(manifest.pages):
        page = manifest.pages[path]
        try:
            content = provider.read_back(page.node_token, page.url)
        except ProviderError as exc:
            if exc.fatal:
                print("provider error: %s" % exc, file=sys.stderr)
                return EXIT_PROVIDER
            unreachable.append(path)
            print("  unreachable %s (%s)" % (path, exc))
            continue
        if footer_marker(page.fingerprint) in content:
            clean.append(path)
        else:
            drift.append(path)
            print("  drift       %s" % path)
    print("verify: clean %d, drift %d, unreachable %d" % (len(clean), len(drift), len(unreachable)))
    return EXIT_UNVERIFIED if (drift or unreachable) else EXIT_OK


# [argument parsing]

def build_parser():
    p = argparse.ArgumentParser(
        prog="wikisync",
        description="Push a second brain's publishable layers into a team wiki, one way.")
    p.add_argument("--version", action="version", version="wikisync %s" % __version__)
    sub = p.add_subparsers(dest="verb")
    sub.required = True

    s = sub.add_parser("init", help="connect a vault: write 99_Meta/wiki-sync.md")
    s.add_argument("vault")
    s.add_argument("--provider", choices=PROVIDER_NAMES, default="lark")
    s.add_argument("--space-id", default="")
    s.add_argument("--base-url", default="")
    s.add_argument("--roots", default="", help="comma-separated vault-relative folders")
    s.add_argument("--owner-name", default="")
    s.add_argument("--lark-bin", default="lark-cli")
    s.add_argument("--force", action="store_true")

    s = sub.add_parser("plan", help="list new, changed, unchanged and removed pages")
    s.add_argument("vault")
    s.add_argument("--json", action="store_true")

    s = sub.add_parser("convert", help="print the DocxXML for one note")
    s.add_argument("vault")
    s.add_argument("file", help="vault-relative or absolute path of the note")
    s.add_argument("--stdout", action="store_true", help="print to stdout (the default)")

    s = sub.add_parser("push", help="create or overwrite wiki pages, verify by read-back")
    s.add_argument("vault")
    s.add_argument("--dry-run", action="store_true")
    s.add_argument("--only", default=None, help="vault-relative path of one page")
    s.add_argument("--delete-removed", action="store_true")

    s = sub.add_parser("verify", help="re-fetch every page and report drift")
    s.add_argument("vault")
    return p


def main(argv=None, provider_factory=None):
    args = build_parser().parse_args(argv)
    if args.verb == "init":
        return cmd_init(args)
    if args.verb == "plan":
        return cmd_plan(args)
    if args.verb == "convert":
        return cmd_convert(args)
    if args.verb == "push":
        return cmd_push(args, provider_factory)
    if args.verb == "verify":
        return cmd_verify(args, provider_factory)
    return 1
