# My Second Brain

A Claude Code skill that builds and runs a complete second brain for a business owner: one vault, two wings (your life in a personal wing, your business in a four-layer knowledge map), operated in plain conversation with Obsidian as the viewing deck.

The idea underneath: **AI execution is cheap now; what is scarce is your data having a home.** Models keep changing; your knowledge base, plain markdown files on your own disk, stays yours.

The full product story (philosophy, design decisions, day-to-day life with it) lives on the repo front page: [github.com/breakthrough-edu/my-second-brain](https://github.com/breakthrough-edu/my-second-brain).

## Install

```bash
npx skills add -g breakthrough-edu/my-second-brain
```

The `-g` is not optional here: without it the install lands in the current project folder, and this skill has to sit at the user level to find its own payload.

Then open Claude Code and say:

> set up my second brain

Update anytime with `npx skills update my-second-brain` (your vault is never touched, only the skill files). ⚠️ The skill does not work out which generation of the product built your vault, and it never reshapes an older one on that basis: nothing structural is created or moved without your yes, whatever shape your vault is in. See "Updating" on the repo front page.

## Four modes, one skill

- **Setup** (three stations, in order: the foundation, the dashboard, the rest): builds the fully wired vault, generates your personal command-base skill named after your business, and ends each station with something on your machine to look at.
- **Capture** (15 to 20 min for a first room, 10 for a regular one): guided move-in, one room at a time. Every session ends with one observation you had not noticed plus two good questions.
- **Distill** (weekly, two passes behind one doorbell): first the anti-drift pass, which keeps the house from rotting, then distillation proposals for your methodology layer. You rule yes or no.
- **Create-My-Jarvis** (a light tier in one 45 to 60 min sitting, or a deep tier across three separate conversations): interviews that give your AI a real character and a real understanding of who you are.

The companion skills (`breakthrough-project-consultant`, `breakthrough-session-report`, `breakthrough-method-builder`, `breakthrough-vault-guardian`, `breakthrough-vault-migrator`) ride in this payload and setup installs them for you, so they update when this skill updates. Other tools are published separately and installed by you when you want them, and nothing here breaks while they are missing: `breakthrough-sop-builder` writes an SOP properly in its own sitting, and `breakthrough-brand-strategy` carries the brand pillar stubs setup leaves behind off `status: empty`. The repo front page lists both, plus the skills from the same workshop that do work this vault does not do.

## What is in this folder

This directory is the skill payload that `npx skills` installs as a unit: `SKILL.md` (the router), `modes/` (one file per mode), `templates/` (everything Setup scaffolds into your vault), `references/` (structure specs and room guides), and `scripts/` (the read-only `checkup.py` vault linter the anti-drift pass runs, `deck.py` with `deck-template.html`, which generate the Command Deck dashboard, `doctrine_schema.py`, which reads your vault's own record schema, the `rm-guard-hook.sh` and `fm-guard-hook.sh` machine-guard templates, and the vendored `session-history/` session-memory tool).

The structural rules live in your vault after setup (`99_Meta/structure-doctrine.md`), not in this skill, so your vault stays consistent no matter which tool or model touches it.

## Requirements

- [Claude Code](https://claude.com/claude-code)
- [Obsidian](https://obsidian.md) (free; the skill can install it for you). It is the reading and graph surface. The dashboard is a generated HTML file that opens in any browser, so it needs no plugin.
- Python 3, for the inspector and session memory. macOS ships everything they need; on Windows use Python from python.org (not Anaconda, whose SQLite lacks the FTS5 extension session memory needs).
- Works on macOS, Windows, Linux, with two honest caveats. The optional machine guards are macOS-gated: the safety lock is macOS only, and the session-memory install step is written for macOS. And **Windows is best-effort rather than tested**: this skill is built on macOS and we have no Windows machine to verify against, so the Windows install path (a plain folder copy for your generated command-base skill by default, with a `mklink /J` junction available on request once Setup has told you what you give up by taking it) is written to verify itself and fall back cleanly rather than to promise it works. Full detail in Honest boundaries and the Windows self-serve path on the [repo front page](https://github.com/breakthrough-edu/my-second-brain).

## License

MIT. Built and maintained by [Breakthrough EDU](https://github.com/breakthrough-edu).
