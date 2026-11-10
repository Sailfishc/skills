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
| `close-ticket` | ready | Distill `work/<ticket>/` and run an evidence-based retrospective; manual only |
| `shape-work` | ready | Scout with a bounded search, settle choices, and size the plan to the work; writes acceptance checks |
| `build-work` | ready | Surgical red-green implementation; reconciles every task to Done or Blocked |
| `verify-delivery` | planned | Prove acceptance checks on the real product, with evidence |
| `review-change` | ready | Independent review of a diff for intent, correctness, standards, and minimalism |
| `tend-knowledge` | planned | Periodically refresh learnings, archive decisions, and trim `AGENTS.md` |

Start with [the artifact map](skills/artifact-map/SKILL.md). This repository's own choices are in [docs/decisions/](docs/decisions/).

## Development

```sh
python3 -m unittest discover -s tests
python3 skills/artifact-map/scripts/gates/check_decisions.py
```
