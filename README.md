# Sailfishc/skills

Agent skills for long-lived projects: shape the work, build it, verify it, review it, close it, and keep the project's knowledge from rotting.

Status: foundation only. The artifact map, templates, and first decisions are in place; the skills come next.

## The loop

| Stage | Skill (planned) | Writes to |
| --- | --- | --- |
| Shape | `shape` | `docs/decisions/proposed/`, `work/<ticket>/plan.md` |
| Build | `build` | code, tests, plan status |
| Verify | `verify` | `.agents/verify/` adapter, local evidence report |
| Review | `review` | findings routed to lint, `CODING_STANDARDS.md`, or learnings |
| Close (manual) | `close` | distills `work/<ticket>/` and runs the retrospective |
| Tend (periodic) | `tend` | refreshes learnings, archives decisions, trims `AGENTS.md` |

## Layout

```
references/   artifact-map.md and, later, principles, subagent guidance, harness mappings
templates/    decision, plan, learning, postmortem, project AGENTS.md
docs/         this repository's own decisions
```

Start with [references/artifact-map.md](references/artifact-map.md).
