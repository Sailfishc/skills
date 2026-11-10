# Decision: Skills may carry harness metadata that only controls invocation and display

Status: accepted

## Problem

The pack uses only portable skill features ([portable skills via npx](2026-11-07-portable-skills-via-npx.md)), so it had no way to stop an agent from triggering a skill on its own. Some skills must run only when a person asks, such as `close-ticket` ([manual close](2026-11-07-manual-close-and-retro.md)), and each harness controls that differently: Codex reads `policy.allow_implicit_invocation` from `agents/openai.yaml` and documents no frontmatter field for it, while Claude Code reads `disable-model-invocation` from `SKILL.md` front matter.

## Decision

A skill may carry harness metadata when it changes only how the skill is invoked or displayed, never what the skill does:

- `agents/openai.yaml` with `interface` (display name, short description, default prompt) and `policy.allow_implicit_invocation`.
- `disable-model-invocation: true` in `SKILL.md` front matter, for skills that must run only on request.

Every skill ships `agents/openai.yaml`. A manual-only skill sets both `allow_implicit_invocation: false` and `disable-model-invocation: true`. Behavior, steps, and pass criteria stay in `SKILL.md` and its references, identical for every harness. Hooks, subagent definitions, and tool or dependency declarations remain out.

## Alternatives considered

**Keep skills strictly portable.** Manual-only skills would trigger implicitly in every harness, contradicting the manual-close decision and adding description noise to routing.

**Fold the invocation rule into the description text.** Descriptions such as "only when the user asks" are advisory; the harness still offers the skill for implicit matching.

**Per-harness builds.** Already rejected in the portable-skills record as too much machinery.

## Consequences

Harnesses that read neither field still trigger every skill implicitly, so a manual-only skill's description must also say it runs on request. A strict Agent Skills validator may flag the extra front-matter field; Claude Code and Codex both accept it, and the skills CLI copies `agents/` with the skill.
