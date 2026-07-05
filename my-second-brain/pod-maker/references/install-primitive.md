# The install primitive: one sequence, three entry paths

Every pod operation (forge, graduate, load a patch) converges here. The paths differ only at step 4 (where the pod's brain content comes from). Step 5 is the **single write-gate**: everything before it is proposal held in the session, everything after it writes to disk. Nothing lands until the owner says yes.

Read `99_Meta/structure-doctrine.md` section 9 first; this sequence executes that law, it does not redefine it.

## The nine steps

| Step | Action | Where it lands in a my-second-brain vault |
|---|---|---|
| **0. Precheck (gate)** | Confirm the vault is real: L0 (the vault + `07_<BIZ>/`), L1 (`99_Meta/structure-doctrine.md` with section 9), the host registry (`_Map.md`, MOCs). | Reuse: read the constitution + registry. |
| **1. Precheck cont.** | Confirm the specific bedrock this pod will read exists (see step 4.5). | Reuse the scaffold. |
| **2. Trigger + intent** | One of the three entry paths (see content-sources.md). Establish which function, which path. | Reuse. |
| **3. Conflict detection** | Does the target already exist? Three outcomes: **fresh** (no room), **graduation** (a thin room of that name exists), **already a pod** (stop, offer to edit instead). | In a my-second-brain vault a thin room almost always exists, so this is almost always **graduation** (see H1). |
| **4. Resolve spec + content source** | Get the pod's brain content from the path's source (intake / Action-Log / patch). `loop-config.md` is REQUIRED; a pod with no loop-config does not pass this step (H6). Validate the spec against the fixed skeleton. | The shape is section 9; the content is generation.md. |
| **4.5. Bedrock check** | Declare the read-contract's bedrock dependencies, check each in the scaffold, bootstrap the missing required ones (or record the gap). | Reuse / extend the scaffold's intake. |
| **5. Propose to approve (GATE)** | Show the owner the full plan: what folders, what brain content, what pointer rewrites, what moves. Nothing is written before an explicit yes. | The one write-gate (H5). |
| **6. Build / graduate + install skill + wire** | Create or move the skeleton, generate the brain files, generate the pod's thin operational skill, wire the read-only reference edges. | Skill uses the `Skills/ + symlink` channel (same as command-base). |
| **7. Reinject pointers + verify + self-heal** | Write the pod into the product-native registry (`_Map`, `_Assets-MOC`, relevant MOCs) AND rewrite every inbound link across the vault. Verify; heal any orphan. | Write `_Map`/MOCs; the inbound-link sweep is H3's fix. |
| **8. Runtime (later)** | The pod's operational skill reads Methodology, produces into Assets, proposes rubric candidates, appends Action-Log. | Ongoing. |
| **9. Learning loop + maintenance (later)** | Promotion / graduation / demotion scans run in the one global weekly distill. | Reuse the maintenance ritual. |

Steps 8 and 9 are not this run; they are what the pod does afterward. This skill builds through step 7 and hands off.

## Step 3 in detail: graduation is the normal case

A my-second-brain Setup **always** builds six thin function rooms (`Marketing`, `Sales`, `Customer-Service`, `HR`, `Finance`, `Operations`), each with a `_<Name>-MOC.md` and an `Action-Log.md`. So installing a pod for any of those functions is **graduation, never fresh install**: the thin room already exists and its `Action-Log` may already hold real history. (H1: graduation never overwrites; the existing `Action-Log` is carried up intact.)

Fresh install (step 3 "fresh") only happens for a function with no thin room at all (a genuinely new function the Setup toggles never created). Even then, prefer creating the thin room first and letting it earn graduation, unless the owner explicitly wants a pod now with a patch to seed it.

## Step 6 in detail: what graduation physically does

Graduation is a **cross-layer move**, decided in structure-doctrine section 9 (the alternative, upgrading in place, was rejected because it buries a Layer-3 brain inside a Layer-1 room and breaks the sort-by-knowledge-type story):

1. Move the thin room from `07_<BIZ>/01_Assets/<Function>/` up to a wing-level sibling `07_<BIZ>/<Function>/`.
2. Carry the existing `Action-Log.md` up **intact** (never overwritten, H1).
3. Grow the interior around it: `03_Methodology/` (doctrine, rubric/, loop-config, current-thesis, thresholds, `<function>-profile`), `01_Assets/` (the pod's own outputs + judge view), `02_SOP/` is **NOT** created (a pod carries no SOP folder; its procedures live in the wing `02_SOP/` with a `function:` tag, section 9).
4. Rename the front desk to the pod convention `_<Function>-MOC.md` (it was already `_<Function>-MOC.md` as a thin room, so this is usually a move, not a rename; fold the thin room's Inventory/Observations content into the pod MOC).
5. Leave a `_MOVED` pointer at the old `01_Assets/<Function>/` location so no inbound link dies.
6. Install the pod's operational skill (step 6 skill install).
7. Wire the read-only edges: the pod's read-contract references (wing bedrock, other pods' Methodology, upstream thesis) are recorded as full-path references, never bare wikilinks (section 9).

## Step 7 in detail: the inbound-link sweep (H3 + H7's fix)

A filesystem move does **not** update Obsidian wikilinks; only moving inside the Obsidian app does. So after any graduation move, daily notes, Decisions, and other rooms' MOCs that linked to a moved file are now dangling, and a full-path wikilink to the old path will spawn a ghost file (a real, observed failure mode in this vault class).

The install primitive's verify is therefore not just "did the pointers I wrote resolve." It must:

1. Scan the **whole vault** for inbound links to every moved file (search for the old path and the moved files' basenames).
2. Rewrite each to the new path, OR leave a same-named `_MOVED` stub at every old file location (not just one at the folder level).
3. Re-verify: zero dangling links, zero ghost files. Report the count rewritten.

This is the same lesson as the Lark dim-insert boundary-row bug generalized: file operations have no transaction, so verify explicitly and heal, every time.

## Demotion (the symmetric branch)

When the maintenance scan proposes demotion (a pod gone silent, or a loop idling), the primitive runs in reverse:

1. Propose to approve to log, same gate.
2. Move the pod back down to a thin `01_Assets/<Function>/` room (or to `05_Archive/` if the owner chooses archive).
3. **Preserve learning (the mirror of H1's no-overwrite law).** A pod's `doctrine.md`, `rubric/`, and `loop-config.md` are the one irreplaceable thing it grew (months of loop output). On demotion they are **archived, never deleted**: move them to the demoted room's `_archived/` (or `05_Archive/<Function>-pod-<date>/`), so a later re-graduation can re-feed them. Losing them would turn "shrinks gracefully" into "forgets what it learned."
4. Run the same inbound-link sweep (step 7) for every file that moved.
5. Update `_Map` and MOCs; leave `_MOVED` pointers.

## Vulnerability grading (H1 to H7, pinned along the sequence)

The seven ways this can go wrong, graded by when to defend against them:

**Must block first (past the gate, they corrupt data or structure):**
- **H1. Overwrite loses data** (heaviest). Graduation must never overwrite the thin room's `Action-Log` or existing content. Defended by the no-overwrite law in step 6; carry content up intact.
- **H3. Orphan pointers.** File moves have no transaction. Step 7's whole-vault inbound-link sweep + verify + self-heal is the defense.

**Must block, but cheap (before the gate, validation only):**
- **H6. Empty loop-config.** A pod with no `loop-config.md` cannot learn; it is a dead pod. Required at step 4; fails the step if absent.
- **H5. Hallucinated pod.** The model wants to build a pod that should not exist. The step 5 propose-to-approve gate is the catch; plus the strong prior in the gate itself.
- **H2. Missing precheck.** No vault, no L1, no registry. Step 0 catches it; bootstrap L0/L1 first or stop.

**Deferred (known risk, written into doctrine as a discipline, not a runtime mechanism):**
- **H4. Trigger-word collision.** Two pods' operational skills could grab the same phrase. Defended by naming discipline (function-named, uniform) + a collision scan at skill-install time that flags and asks, not a runtime sandbox.
- **H7. Interface contract is convention-only.** Plain text has no runtime sandbox stopping a pod from reaching into another pod's `01_Assets`. Defended by writing the contract as a hard constraint in this skill and in section 9, plus a maintenance spot-check, not by enforcement code.

H4 and H7 are accepted residual risk for v1: the cost of a runtime enforcement layer exceeds the cost of the discipline, given a single-owner vault with a human in every write-gate.
