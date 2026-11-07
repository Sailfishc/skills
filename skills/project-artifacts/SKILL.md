---
name: project-artifacts
description: Where a project's agent-facing knowledge lives (AGENTS.md, CODING_STANDARDS.md, docs/decisions, docs/learnings, docs/postmortems, work/), with templates and CI gate scripts. Use before creating, moving, or deleting any of these files, and when setting up a project for this skill pack.
---

# Project artifacts

**Outcome:** every artifact this pack produces lands in the one place [the artifact map](references/artifact-map.md) assigns it, in the shape its template gives it, and the project's CI checks the rules a script can check.

Read [references/artifact-map.md](references/artifact-map.md) before writing any artifact. It decides where a fact goes, who reads it, and when it leaves. Other skills in this pack read this skill's files at `../project-artifacts/`.

## Templates

| Artifact | Template | Written by |
| --- | --- | --- |
| Decision record | [templates/decision.md](templates/decision.md) | `decision-record` |
| Plan for work in flight | [templates/plan.md](templates/plan.md) | the shaping stage |
| Learning | [templates/learning.md](templates/learning.md) | `close-ticket` |
| Postmortem | [templates/postmortem.md](templates/postmortem.md) | by hand, after an incident |
| Project `AGENTS.md` | [templates/project-AGENTS.md](templates/project-AGENTS.md) | setup, below |

## Gate scripts

Standard-library Python, run from the project root. Each prints one line per problem and exits 1 on failure.

| Script | Checks |
| --- | --- |
| `scripts/gates/check_decisions.py` | Decision record paths, header and `Status:` line, required and forbidden sections, relative links |
| `scripts/gates/check_work.py` | `work/` holds only ticket directories with a valid `plan.md` status, none left in `closing`; `--max-idle-days N` also fails idle tickets |
| `scripts/gates/check_agents_budget.py` | `AGENTS.md` word count, `--max-words` (default 600) |

## Set up a project

Do each step only if the project does not already have it.

1. Install the pack with `npx skills add Sailfishc/skills` and commit `.agents/skills/` together with `skills-lock.json`.
2. Create `AGENTS.md` from the project template, filling in the real commands. Make `CLAUDE.md` contain only `@AGENTS.md`.
3. Create directories lazily, when their first file is written. Never commit empty placeholders.
4. Add the three gates to the project's CI, for example:

   ```yaml
   - run: python3 .agents/skills/project-artifacts/scripts/gates/check_decisions.py
   - run: python3 .agents/skills/project-artifacts/scripts/gates/check_work.py
   - run: python3 .agents/skills/project-artifacts/scripts/gates/check_agents_budget.py
   ```

5. Run the three gates locally and confirm they pass before handing back.
