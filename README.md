# Sailfishc/skills

Agent skills for long-lived projects: shape the work, build it, verify it, review it, close it, and keep the project's knowledge from rotting.

```sh
npx skills add Sailfishc/skills
```

Then ask your agent to set up the project with the `artifact-map` skill.

## Skills

| Skill | Status | What it does |
| --- | --- | --- |
| `artifact-map` | ready | The artifact map, templates, and CI gate scripts every other skill builds on |
| `decision-record` | ready | Propose, accept, reject, supersede, archive, or correct decision records |
| `close-ticket` | ready | Distill `work/<ticket>/` and run an evidence-based retrospective, by hand |
| `shape-work` | planned | Brainstorm, decide, and plan, sized to the work; writes acceptance checks |
| `build-work` | planned | Implement in verifiable units and keep the plan's status current |
| `verify-delivery` | planned | Prove acceptance checks on the real product, with evidence |
| `review-change` | planned | Review a diff against its plan and the project's `CODING_STANDARDS.md` |
| `tend-knowledge` | planned | Periodically refresh learnings, archive decisions, and trim `AGENTS.md` |

Start with [the artifact map](skills/artifact-map/SKILL.md). This repository's own choices are in [docs/decisions/](docs/decisions/).

## Development

```sh
python3 -m unittest discover -s tests
python3 skills/artifact-map/scripts/gates/check_decisions.py
```
