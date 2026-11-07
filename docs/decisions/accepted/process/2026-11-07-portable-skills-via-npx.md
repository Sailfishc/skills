# Decision: Distribute as portable skills through npx, enforce in CI

Status: accepted

## Problem

The team uses more than one agent harness. Each harness supports a different set of plugin features, so anything beyond plain skills behaves differently or not at all from one harness to the next.

## Decision

The pack is installed with `npx skills add Sailfishc/skills`. Skills use only portable features: `SKILL.md`, reference files, and scripts. No hooks, subagent manifests, or harness-specific plugin files. Harness differences, such as how to pick a model for a subagent, live in `references/harness/<harness>.md`. Rules that must always hold are enforced by gate scripts in `scripts/gates/` that each project's CI runs. Projects commit the installed skills under `.agents/skills/` and symlink each harness's skills directory to it, so the skill version is the git commit and every harness sees the same one.

## Alternatives considered

**A Claude Code plugin with hooks (agent-rsi, pstack).** Hooks give automatic triggers, but they do not carry over to other harnesses.

**Separate builds per harness (Compound Engineering's converter).** Supports native features everywhere, at the cost of a converter and writer per target. Too much machinery for this pack.

**Relying on the skills CLI alone for version pinning.** Not verified to pin versions; committing the installed copy pins them regardless.

## Consequences

Nothing triggers automatically: stages run when a person or agent invokes them, and CI catches what was skipped. The pack must ship working gate scripts, not just instructions.
