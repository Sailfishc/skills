# AGENTS.md

This repository is a pack of agent skills, installed into projects with `npx skills add Sailfishc/skills` and used across several harnesses. It is also its own first pilot project: it keeps its own decisions under `docs/decisions/`.

- Read [references/artifact-map.md](references/artifact-map.md) before adding or moving any artifact. It is the single authority on where things live.
- Skills use only portable Agent Skills features: `SKILL.md`, references, scripts. No hooks, no harness-specific manifests. Harness differences live in `references/harness/`.
- Enforcement lives in CI, through scripts in `scripts/gates/`, not in skill text.
- Write for agents: short imperative rules, one home per fact, links instead of restated text.
- Settled questions are in [docs/decisions/accepted/](docs/decisions/accepted/). Read the matching record before proposing a change to one.
