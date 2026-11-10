---
name: shape-work
description: Shape a feature, change, or bug fix before code. Scout the codebase with a bounded search, settle real choices as decision records, and size the output to the work - a one-line approach, a short brief, or work/<ticket>/plan.md with acceptance checks. Use when starting work that is not a one-line fix, when requirements are fuzzy, or when asked to brainstorm, scope, or plan.
---

# Shape work

**Outcome:** before any file is edited, the goal is stated in the user's terms, the code that governs it is mapped with citations, every real choice is settled, and the plan is no heavier than the work needs.

**Done:** either the user approved a plan, or the work was sized Direct or Brief and handed to `build-work`. No product code was edited during shaping.

Read the [Shape principles](../artifact-map/references/principles.md#shape). Write only where the [artifact map](../artifact-map/SKILL.md) allows.

## 1. Frame the goal

Restate the request as one outcome a user could observe, and note what would make it fail.

- **Done when:** the goal fits in one sentence a user would recognize, without naming files or functions.

## 2. Scout

Map the code that governs the goal with a bounded search. Read only; edit nothing.

1. Launch one parallel batch of varied searches: entry points, core types, existing tests, and the terms of the goal in `docs/learnings/` and `docs/decisions/accepted/`.
2. Read the top hits. Trace only symbols you will change and the contracts you rely on; skip transitive callers whose signatures stay the same.
3. **Stop** when you can name the exact files and symbols to change, or the top hits converge (~70%) on one area. If signals conflict, run one refined batch, then stop.

- **Done when:** every symbol to change and every caller whose contract depends on it is listed with `file:line`, the project's test, typecheck, and lint commands are found in its config, and every claim cites a file or config entry.

## 3. Resolve open questions

Ask the user only what the code cannot answer and whose answer changes the plan. Ask one question at a time, each with your recommended answer and why. Facts found while scouting are stated, not asked.

- **Done when:** no open question blocks the first unit of work.

## 4. Settle choices

For each choice between real alternatives, apply the admission test in `decision-record`. If it passes, use `decision-record` to write a proposed record. If not, state the choice and its reason in one line of the brief or plan.

- **Done when:** every real choice is either a proposed decision record or a one-line rationale.

## 5. Size the output

| Size | When | Output |
| --- | --- | --- |
| **Direct** | One session; no real choice; low risk | One or two sentences in the reply: goal and approach |
| **Brief** | One session; has a choice or a risk worth naming | A short brief in the reply: goal, approach, files, how it will be verified |
| **Plan** | Spans sessions or agents, or the plan needs review before code | `work/<ticket>/plan.md` from the [plan template](../artifact-map/templates/plan.md) |

When unsure between two sizes, take the lighter one.

For a Plan: fill Context from step 2, list Out of scope, split the work into units that each end in a proof, and write Acceptance checks as observable behavior with the evidence each needs (screenshot, recording, log, command output). Set `status: shaping`.

- **Done when:** the size is stated with its reason in one line; for a Plan, every unit names its proof, every acceptance check names its evidence, and `check_work.py` passes.

## 6. Hand off

- **Plan:** stop and ask the user to review it. On approval, set `status: building`.
- **Direct or Brief:** continue with `build-work`.

- **Done when:** the user approved the plan, or the work was handed to `build-work`.
