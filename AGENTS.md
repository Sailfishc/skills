# AGENTS.md

This repository is a pack of agent skills, installed into projects with `npx skills add Sailfishc/skills` and used across several harnesses. It is also its own first pilot project: it keeps its own decisions under `docs/decisions/`.

- Each skill is a directory `skills/<name>/` with a `SKILL.md`. Only these directories reach a project, so material shared by several skills lives inside the `artifact-map` skill, and other skills reach it at `../artifact-map/`.
- Read [the artifact map](skills/artifact-map/SKILL.md) before adding or moving any artifact. It is the single authority on where things live.
- Name a reference skill for what it is and a workflow skill verb-noun for what it does; never a bare generic word like `setup` ([why](docs/decisions/accepted/process/2026-11-07-skill-naming.md)).
- Skills use only portable Agent Skills features: `SKILL.md`, references, scripts. No hooks, no harness-specific manifests.
- Enforcement lives in CI, through the gate scripts in `skills/artifact-map/scripts/gates/`, not in skill text. Run `python3 -m unittest discover -s tests` after changing them.
- Write for agents: short imperative rules, one home per fact, links instead of restated text.
- Settled questions are in [docs/decisions/accepted/](docs/decisions/accepted/). Read the matching record before proposing a change to one.
