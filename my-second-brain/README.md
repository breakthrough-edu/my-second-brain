# My Second Brain

A Claude Code skill that builds and runs a complete second brain for a business owner: one vault, two wings (your life in a personal wing, your business in a four-layer knowledge map), operated in plain conversation with Obsidian as the viewing deck.

The idea underneath: **AI execution is cheap now; what is scarce is your data having a home.** Models keep changing; your knowledge base, plain markdown files on your own disk, stays yours.

The full product story (philosophy, design decisions, day-to-day life with it) lives on the repo front page: [github.com/breakthrough-edu/my-second-brain](https://github.com/breakthrough-edu/my-second-brain).

## Install

```bash
npx skills add breakthrough-edu/my-second-brain
```

Then open Claude Code and say:

> set up my second brain

Update anytime with `npx skills update my-second-brain` (your vault is never touched, only the skill files).

## Four modes, one skill

- **Setup** (10 min): builds the fully wired vault and generates your personal command-base skill, named after your business.
- **Capture** (15 min per room): guided move-in, one room at a time. Every session ends with one observation you had not noticed plus two good questions.
- **Distill** (10 min weekly): tidy scan, then distillation proposals for your methodology layer. You rule yes or no.
- **Create-My-Jarvis** (45 to 60 min): two interviews that give your AI a real character and a real understanding of who you are.

Two companion skills are published separately and installed by you when you want them, and nothing here breaks without either: `sop-builder` writes an SOP properly in its own sitting, and `playbook-lab` opens the rare feedback loop around a playbook that has earned one.

## What is in this folder

This directory is the skill payload that `npx skills` installs as a unit: `SKILL.md` (the router), `modes/` (one file per mode), `templates/` (everything Setup scaffolds into your vault), `references/` (structure specs and room guides), and `scripts/` (the read-only `checkup.py` vault linter the weekly Tidy pass runs, the `rm-guard-hook.sh` safety-lock template, and the vendored `session-history/` session-memory tool).

The structural rules live in your vault after setup (`99_Meta/structure-doctrine.md`), not in this skill, so your vault stays consistent no matter which tool or model touches it.

## Requirements

- [Claude Code](https://claude.com/claude-code)
- [Obsidian](https://obsidian.md) (free; the skill can install it for you). Enable the **Bases** core plugin for the dashboard.
- Python 3, for the inspector and session memory. macOS ships everything they need; on Windows use Python from python.org (not Anaconda, whose SQLite lacks the FTS5 extension session memory needs).
- Works on macOS, Windows, Linux, with two honest caveats. The optional machine guards are macOS-gated for now (safety lock macOS only, session memory macOS first). And **Windows is best-effort rather than tested**: this skill is built on macOS and we have no Windows machine to verify against, so the Windows install path (a `mklink /J` junction for your generated command-base skill, with a folder copy as the fallback) is written to verify itself and fall back cleanly rather than to promise it works. Full detail in Honest boundaries and the Windows self-serve path on the [repo front page](https://github.com/breakthrough-edu/my-second-brain).
- English or 中文 interaction; your choice at setup.

## License

MIT. Built and maintained by [Breakthrough EDU](https://github.com/breakthrough-edu).
