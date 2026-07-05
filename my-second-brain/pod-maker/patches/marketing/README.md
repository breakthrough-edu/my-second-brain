# Marketing patch (the shipped core pod seed)

The one pod seed that ships with pod-maker. It is a **generic, portable marketing brain**, de-personalized from a real, battle-tested marketing practice: only the mechanism and the tunable defaults survived; one specific business's identity (its positioning, its visual system, its voice register, its named avatars, its punctuation habits) was deliberately left out. The loop localizes the generic seed into each business's own marketing doctrine over time. That localization is the product magic: a static template pack would stay generic forever; this seed plus a running loop grows into something specific to each business.

## What is in the patch

| File | Role | Bucket it came from |
|---|---|---|
| `doctrine.md` | Light, hardened marketing **mechanism** only | FIXED |
| `loop-config.md` | The crown jewel: how this pod learns (fast-feedback marketing) | mechanism + tunable |
| `thresholds.md` | Kill/scale **defaults** (tunable) + override discipline (fixed) | VARIABLE defaults + FIXED discipline |
| `current-thesis.md` | A neutral placeholder bet | tunable |
| `marketing-profile.md` | Thin voice + scorecard scaffolding (voice itself lives in the brand foundation) | mechanism + pointer |
| `rubric/*.md` | 0 to 3 candidate rules: good marketing wisdom shipped as **unproven hypotheses** | VARIABLE, as candidates |
| `marketing-SKILL.template.md` | The `<slug>-marketing` operational skill this patch installs | the executor |

What is NOT in the patch (dropped as one business's identity): specific positioning bets, content-pillar taxonomies, visual systems and palettes, voice registers, punctuation rules, named customer avatars. Those either live in the user's own brand foundation or do not belong in a portable seed at all. See `../../references/generation.md` (the sorting knife) for the method.

## How it installs

The Marketing patch is a **hybrid** of the load-patch and graduate-room content sources (see `../../references/content-sources.md`):

- **Content source = load-patch:** the brain files above are copied in pre-filled, so there is a usable generic marketing brain on day zero. Generation is skipped.
- **Mechanics = graduation:** because a my-second-brain Setup always builds a thin `Marketing/` room, installing this patch is mechanically a graduation (move the thin room up to `07_<BIZ>/Marketing/`, carry its `Action-Log` intact, grow the interior, leave `_MOVED` pointers, run the inbound-link sweep). It runs the full install primitive from step 5 (propose to approve, build, wire, verify).

On install, the placeholders in the files (`{{BUSINESS_NAME}}`, `{{BUSINESS}}`, `{{SLUG}}`, `{{VAULT_PATH}}`, `{{LANGUAGE}}`) are filled from the vault's `bootstrap-progress.md`, and the operational skill is written to `<vault>/04_Resources/Skills/<slug>-marketing/SKILL.md` and symlinked into `~/.claude/skills/` (same channel as the command-base skill).

## Why offering it at Setup is sound

The prematurity rule ("no track record, so send it back to a thin room") governs *forging a pod with no seed*. This patch arrives *with* a seed, so it is a working brain on day zero, not an empty shell. What waits for real activity is the pod's **learning**, not its usability: the loop only starts promoting rules once there is real marketing activity and feedback to learn from. Say that plainly when offering it (Setup step 8.5).

## The read-contract of the operational skill

The `<slug>-marketing` skill reads (and only reads) the wing's shared material; it writes only inside the Marketing pod. Full read order is in `marketing-SKILL.template.md`. Its most important dependency is the **brand foundation** (`01_Assets/Brand-Strategy/` + `Target-Audience/`): when those are `status: empty`, the skill runs in honest degraded mode and says the output will be generic until the foundation is filled.
