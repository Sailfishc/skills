# Decision: Distribute as portable skills through npx, enforce in CI

Status: accepted

## Problem

The team uses more than one agent harness. Each harness supports a different set of plugin features, so anything beyond plain skills behaves differently or not at all from one harness to the next.

## Decision

The pack is installed with `npx skills add Sailfishc/skills`. Skills use only portable features: `SKILL.md`, reference files, and scripts. No hooks, subagent manifests, or harness-specific plugin files. The CLI installs only skill directories, so material shared by several skills (the artifact map, templates, gate scripts) lives inside the `artifact-map` skill, and harness differences, such as how to pick a model for a subagent, will live there too. Rules that must always hold are enforced by gate scripts in `artifact-map/scripts/gates/` that each project's CI runs. Projects commit the installed skills under `.agents/skills/` together with the CLI's `skills-lock.json`; the CLI links each harness's skills directory to that canonical copy, so every harness sees the same version.

## Alternatives considered

**A Claude Code plugin with hooks (agent-rsi, pstack).** Hooks give automatic triggers, but they do not carry over to other harnesses.

**Separate builds per harness (Compound Engineering's converter).** Supports native features everywhere, at the cost of a converter and writer per target. Too much machinery for this pack.

**Relying on the lock file alone, with installed skills untracked.** `skills-lock.json` records each skill's source and content hash and can restore them, but a restore needs the network and the CLI. Committing the installed copy as well lets any agent read the exact skill text from the checkout.

## Consequences

Nothing triggers automatically: stages run when a person or agent invokes them, and CI catches what was skipped. The pack must ship working gate scripts, not just instructions.
