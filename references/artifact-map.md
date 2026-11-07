# Artifact map

The single authority for where every project artifact lives, who reads it, and when it leaves. Every skill in this pack writes only to the locations named here. When a skill and this file disagree, fix one so they match.

## Two rules above all others

1. **One home per fact.** Each fact lives in the one layer whose job it is. Everywhere else links to it.
2. **Cheapest durable form first.** A lesson goes into the strongest form that holds it: remove the second way of doing the thing, then a check (test, type, lint), then a standard, then a learning. Prose is the last resort, not the default.

## Layers

| Layer | Artifact | Path | Reader and moment | Lifecycle |
| --- | --- | --- | --- | --- |
| L0 Enforced | Tests, types, lint rules, CI gates | the code, CI config, `scripts/gates/` | Machines, on every change | Kept green. The target form for every lesson that can be checked |
| L1 Standing | `AGENTS.md` | repo root (`CLAUDE.md` contains `@AGENTS.md`) | Every agent session | Current state. Word budget. Standing orders and pointers only |
| L2 Situational | `CODING_STANDARDS.md` | repo root | The reviewer, at review time only | Current state. Judgement rules no check can hold |
| | `architecture.md` | `docs/` | Before changing structure | Current state. A map, not rationale |
| | `GLOSSARY.md` | `docs/` | When naming things | Current state. Terms only, no implementation |
| | Cookbook | `docs/cookbook/` | When doing that procedure | Current state. Numbered steps with verify steps |
| | Project skill adapters | `.agents/<skill>/` | When that skill runs | Current state. Project commands, extra review axes, living logs |
| L3 Decisions | Decision records | `docs/decisions/{proposed,accepted,rejected,archived}/<class>/` | Searched on demand; before reopening a settled question | See [Decision lifecycle](#decision-lifecycle) |
| L4 Experience | Learnings | `docs/learnings/` | Searched while shaping and building | Living. Refreshed: keep, update, consolidate, replace, or delete |
| | Postmortems | `docs/postmortems/` | People reviewing an incident | Immutable. Never current authority |
| L5 In flight | Plans, notes, handoffs | `work/<ticket>/` | The agents working that ticket | Distilled and deleted before the ticket's last PR merges |

"Current state" means the artifact must match the code: update it in the same change that makes it wrong.

## Decision lifecycle

A decision record is written only when all three hold: the choice is **hard to reverse**, a future reader would find it **surprising without context**, and it was **a real trade-off** between genuine alternatives.

- `proposed/` — the RFC. Written before building. May speak in the future tense.
- `accepted/` — the decision shipped. On acceptance, rewrite Proposal into a present-tense Decision. Afterwards keep its facts (paths, names, defaults) current in the same change that moves them. Never edit it into a different decision: write a new record and cross-link both.
- `rejected/` — kept only while the losing idea is still tempting enough to be proposed again. Otherwise delete it.
- `archived/` — accepted records whose rationale no longer guides future work but still has historical value. Frozen: never edited, never current authority.

Every record states the alternatives it beat. Agents start each session from zero and will re-propose a rejected option unless the record says why it lost.

Classes: `feature`, `bug-fix`, `simplification`, `architecture` (the shipped source), `process` (tooling and workflow around the source), `testing`.

## Learning admission

Write a learning only when it passes the counterfactual: if this document disappeared, would a future engineer reading the final code, tests, and standards still be likely to repeat the mistake or redo substantial investigation? Effort spent and diff size do not count. If a check or standard already holds the lesson, write nothing.

## Postmortem admission

Write a postmortem only for an incident: production or user impact, or a failure that blocked work for a meaningful time. Its action items go through the cheapest-form ladder. Anything that must guide future work is extracted into L0, L2, or L4; the postmortem itself is evidence, not guidance.

## `work/` rules

- Create `work/<ticket>/` only for a task that spans sessions or agents, or whose plan needs review before code. A task one session can finish needs no `work/` directory.
- `plan.md` carries the ticket's status in its front matter: `shaping`, `building`, `verifying`, `reviewing`, `closing`. Each stage skill reads it on entry and updates it on exit.
- Before the ticket's last PR merges, the close skill distills the directory: decisions to L3, lessons through the cheapest-form ladder, the rest deleted. The PR description lists what went where.
- A CI gate fails when a merged `work/<ticket>/` still has content.

## Scope: pack versus project

| Belongs to the pack (this repository) | Belongs to each project |
| --- | --- |
| Workflow skills and their pass criteria | `AGENTS.md`, `CODING_STANDARDS.md`, lint and CI configuration |
| This map, principles, subagent guidance, templates | `docs/` content and `work/` |
| Generic gate scripts | `.agents/<skill>/` adapters and living logs |

A project adapter decides **how to run** something in that project; the pack skill decides **what counts as done**. A project rule that shows up in a second project moves up into the pack. A pack rule that projects keep overriding moves down.
