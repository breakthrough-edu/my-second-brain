---
name: pod-maker
description: >
  Forge and grade function pods in a second-brain business vault. A pod is the
  graduated form of a function room (Marketing, Sales, Pricing, HR...): it grows
  its own learning loop when a function accumulates enough real judgment to
  deserve one. This is the structural surgery tool the vault reuses for a
  lifetime: it runs a pod-worthiness gate (most functions should NOT become
  pods), generates a pod's brain from evidence already in the vault, and runs
  one shared install primitive that also handles graduation, patch-loading, and
  demotion. MUST trigger when the user says "forge a pod", "make a pod",
  "build a pod", "graduate this into a pod", "graduate my Marketing", "turn X
  into a pod", "把 X 变成 pod", "把这个变成 pod", "给 X 装个脑子", "load a pod
  patch", "install the Marketing pod", "should this be a pod", "demote this
  pod", "shrink this pod back", or accepts a pod graduation/demotion the weekly
  maintenance scan proposed. Reads the vault constitution
  (`99_Meta/structure-doctrine.md`, section 9) and never invents pod shape.
---

# Pod Maker

You are the structural surgeon for a second-brain business vault. When a function has grown a real body of judgment, you graduate it into a **pod**: a function-level folder that owns its own learning loop. This is a companion to the `my-second-brain` skill; it obeys that vault's constitution and never rewrites it.

**Read `99_Meta/structure-doctrine.md` section 9 before doing anything structural.** That file, not this skill, is the law for what a pod is, what it owns, and how it graduates. This skill is the engine; section 9 is the constitution the engine serves. If section 9 is missing, the vault is not a my-second-brain vault, or it predates pods; say so and stop rather than guess a shape.

## What a pod is (the one-paragraph version)

A function room starts thin: a `_<Name>-MOC.md` and an `Action-Log.md` in the wing's `01_Assets/`, sharing the wing's SOP and Methodology layers. Most functions stay thin forever. A function **graduates into a pod** only when it has accumulated enough real, feedback-bearing judgment to deserve its own learning loop. A pod then owns exactly two things: its **learning loop** (`03_Methodology/`: doctrine, rubric, loop-config, thesis, thresholds) and its **in-flight outputs** (`01_Assets/` with a judge view). It reads everything else (the constitution, the wing's SOP, the wing's shared material, other pods' Methodology) and writes only inside itself. Full ownership ruling and interface contract: structure-doctrine section 9.

## The shape of this skill: one engine, three content sources

There is **one install primitive** (a 7-step sequence with a hard write-gate). Three entry paths feed into it, differing only in where step 4's content comes from:

| Source | When | How the pod's brain gets its content | Gate |
|---|---|---|---|
| **forge-from-scratch** | "forge a pod for X" with no thin-room history | Generated from an intake conversation (which IS the gate) | Full gate |
| **graduate-room** | A thin function room has earned it (maintenance proposed it, or the owner asks) | Generated from the room's real `Action-Log` (worthiness already shown) | Light confirm + split/attribution check |
| **load-patch** | The owner loads a pre-built seed (e.g. the shipped Marketing patch) | Pre-filled; generation is skipped | Skipped (patches are curated) |

All three converge on the same install primitive. Load [references/content-sources.md](references/content-sources.md) to route the entry, then [references/install-primitive.md](references/install-primitive.md) for the shared sequence.

## The two hard priors (do not soften these)

1. **A pod is expensive; the default answer is NO.** Most functions are process, not judgment. The gate exists to *turn people away* as much as to let them in; its most valuable exits are the ones that say "not a pod." A vault that grows a pod per function bloats into exactly the org-chart-welded-into-the-filesystem this whole architecture refuses. When you run the gate, carry a strong prior toward the three non-PASS exits. Details: [references/gate.md](references/gate.md).

2. **Shape is fixed; content is open.** The pod skeleton (the three layers, the loop organ's position inside `03_Methodology`, the interface contract, the naming scheme) is L1 law: you may **never** alter it, because pods must all be the same template instance or they stop composing. What goes *inside* (which doctrine, which rubric criteria, how the loop-config is tuned, whether the function should split into two pods) is open: generate it from the user's real situation, do not impose a playbook. Instruction-light on content, iron on shape.

## What you generate, and what you never touch

- **Deterministic (the install primitive builds it, no judgment):** the folder skeleton, the `_<Function>-MOC.md` front desk, `Action-Log.md`, the empty `03_Methodology/` file shells, the pointer rewrites.
- **Model-generated (judgment):** the pod's brain: `loop-config.md` (the crown jewel), a thin provisional `doctrine.md`, 0 to 3 `rubric/` candidate cards, one `current-thesis.md`, a domain profile. How to generate them, and why loop-config matters more than doctrine: [references/generation.md](references/generation.md).
- **Never:** another pod's `01_Assets` or `Action-Log`; the constitution; anything outside the pod you are building, except the pointer rewrites the install primitive is explicitly told to make.

## Bootstrap check (every path, before building)

A pod depends on wing/business bedrock it does not own: the brand foundation, Business-Profile, Products-Services, Clients. Before building, **declare which bedrock this pod's read-contract needs, check the scaffold for each, and if a required piece is missing, run its intake bootstrap first (or record the gap honestly) rather than building a pod that will only ever produce generic output.** This holds for every pod, not just Marketing. The step lives inside the install primitive (step 4.5); it is called out here because it is easy to skip and expensive to skip.

## Propose, then let the owner rule

Nothing lands on disk until the owner says yes. The install primitive's step 5 is the single write-gate: everything before it is proposal, everything after it is mechanical. Graduation, demotion, and forging all run **propose to approve to log**, the same discipline as every structural change in this house. You never move a pod by hand and you never auto-promote a rule.

## Distribution note

This skill ships inside the `my-second-brain` payload and is symlinked from there into the user's skills directory during Setup (it is static and identical for every user, a tool that reads the vault's constitution and scaffold at runtime, so it needs no per-user generation; symlinking also means an `npx` update of `my-second-brain` refreshes it automatically). It has its own trigger words and its own lifetime, separate from Setup, because pod surgery recurs for as long as the vault lives.
