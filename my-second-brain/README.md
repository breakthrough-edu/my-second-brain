# My Second Brain

A Claude Code skill that builds and runs a complete second brain for a business owner: one vault, two wings (your life in PARA, your business in a three-layer knowledge map), operated in plain conversation with Obsidian as the viewing deck.

The idea underneath: **AI execution is cheap now; what is scarce is your data having a home.** When your business lives in one structured vault, any AI can give you real answers about your own operation. When it lives in chat threads, receipts, and one employee's head, no model can help you. Models keep changing; your knowledge base stays yours.

## Install

```bash
npx skills add breakthrough-edu/my-second-brain
```

Then open Claude Code and say:

> set up my second brain

## What you get

**Four modes, one skill:**

- **Setup** (10 min): installs Obsidian if needed, builds a fully wired vault (every room has a front desk, navigation live from day zero), asks 3 questions about your industry, generates your personal command-base skill, and ends on the graph view of your half-built brain.
- **Capture** (15 min per room): your Business Profile first, then one room at a time: clients, products, SOPs, whichever you pick. One question at a time, talking is fine. Every session ends with one observation about your business you had not noticed, plus two good questions.
- **Distill** (10 min weekly): the AI tidies the vault (orphans, misfiles, stale maps), then proposes distillations: decision patterns, lessons, rollups. You only rule yes or no. The third layer of your business map fills from your judgment, never from raw capture.
- **Create-My-Jarvis** (45 to 60 min, at home): two interviews that give your AI a real character and a real understanding of who you are, so it stops sounding like a vending machine.

**The structure it builds:**

```
Your-Vault/
├── 00_Inbox · 01_Daily            shared capture + timeline
├── 02-05  Projects/Areas/Resources/Archive     your life (PARA)
├── 06_Command-Base/               command center: Home, Decisions, Tasks, dashboard
├── 07_<Your-Business>/            your business, three layers:
│   ├── 01_Assets                  what it is made of (clients, products, docs, people)
│   ├── 02_SOP                     how things get done (named by intent, not department)
│   └── 03_Methodology             why you decide the way you do (fills from judgment)
└── 99_Meta/                       the constitution, templates, state
```

The structural rules live in your vault (`99_Meta/structure-doctrine.md`), not in the skill, so your vault stays consistent no matter which tool or model touches it.

## Function pods (when a function earns its own brain)

Most business functions stay simple: a room for their materials and a log. But some functions are pure repeated judgment (marketing, pricing, what to say no to), and those deserve to *learn*. When one has built up enough real track record, the companion `pod-maker` skill (installed at setup) can **graduate** it into a pod.

A pod is not a whole separate business-in-a-box. Honestly sized, a pod **owns two layers** (its own outputs, and its own learning loop of doctrine and rubric that grows from your decisions) and **reads a third** (it shares the business wing's SOP and reference material, never duplicating them). The wing stays the full three-layer map; a pod is one function's local brain bolted onto it.

Two guardrails keep this from bloating your vault: `pod-maker`'s gate treats "not a pod" as the default answer (a process with a known right answer wants an SOP, not a loop), and the weekly maintenance scan proposes shrinking a pod back if it goes quiet (your learning is archived, never lost). One core pod ships ready to seed: **Marketing**, a generic marketing brain your own loop grows into something specific to your business.

## Requirements

- [Claude Code](https://claude.com/claude-code)
- [Obsidian](https://obsidian.md) (free; the skill can install it for you). Enable the **Bases** core plugin for the dashboard.
- Works on macOS, Windows, Linux. English or 中文 interaction; your choice at setup.

## Honest boundaries

- Single-owner system: you plus your AI. Obsidian has no permission layers; if staff need a piece, export that piece.
- High-frequency transaction rows (invoices, POs, attendance) stay in the systems built for them. The vault holds pointers, exceptions, and monthly snapshots. This is a knowledge base, not a shadow ERP.
- Early insights are observations, and the skill says so honestly. It will not promise analytics your data cannot support yet.

## License

MIT. Built and maintained by [Breakthrough EDU](https://github.com/breakthrough-edu).
