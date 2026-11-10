---
name: decision-record
description: Propose, accept, reject, supersede, archive, or correct a decision record under docs/decisions/. Use when a choice is hard to reverse, surprising without context, and a real trade-off; when a proposed decision has shipped; when an accepted decision is being reversed; or when a change moves a path, name, or default that an accepted record states.
---

# Decision record

**Outcome:** the decision lives in exactly one record whose folder matches its status, states the alternatives it beat, and passes `check_decisions.py`.

**Done:** the record is written or moved, every inbound link resolves, the gate passes, and you have reported one line naming the record and what changed.

Read the [decision lifecycle](../artifact-map/SKILL.md#decision-lifecycle) and the [template](../artifact-map/templates/decision.md) first. This skill needs the `artifact-map` skill installed beside it.

## 1. Pick the job

| The situation | Job |
| --- | --- |
| A choice is about to be made and passes admission | **Propose** in `proposed/` |
| The choice was already made and shipped in this change | **Accept** directly in `accepted/` |
| A proposed record has shipped | **Accept**: move it and rewrite it |
| A proposed record will not be built | **Reject**, or delete it if the idea would never be proposed again |
| An accepted decision is reversed or replaced | **Supersede** with a new record |
| A change moves a path, name, or default an accepted record states | **Correct** the facts in place |
| An accepted record no longer guides any future change | **Archive**, or delete it if it only recorded a small or mechanical change |

- **Done when:** exactly one job is named.

## 2. Check admission (propose and accept only)

Write a record only when all three hold. Otherwise write nothing and say which test failed.

1. **Hard to reverse:** changing course later costs real work, data migration, or broken users.
2. **Surprising without context:** a future reader would ask "why did they do it this way?"
3. **A real trade-off:** there were genuine alternatives and this one was picked for stated reasons.

- **Done when:** all three tests pass, or the failing test is reported and nothing is written.

## 3. Search for overlap

Search `docs/decisions/` (all lifecycles except `archived/`) for the same decision, mechanism, or rejected alternative, using the terms a future reader would search for.

- An active record already owns this decision: update that record instead of writing a second one.
- A new record fully replaces an accepted one: archive the old one in this change, or delete it if the new record preserves every reason, alternative, and consequence it held.
- A new record replaces part of an accepted one: keep both, link each to the other, and correct any fact in the old one that is no longer true.
- A rejected record covers the idea being proposed: read why it lost. Propose it again only with a new reason, and link the rejected record.

- **Done when:** the search terms were run and every overlapping record is either the one being updated or named with how it is handled.

## 4. Write

- Path: `docs/decisions/<lifecycle>/<class>/yyyy-mm-dd-<slug>.md`. The date is when the topic was first proposed; keep it when the record moves. Classes: `feature`, `bug-fix`, `simplification`, `architecture`, `process`, `testing`.
- Keep it short. One or two sentences per section is enough. The value is that the decision and its reasons exist.
- **Alternatives are recorded, never invented.** List only options that were actually considered, each with why it lost. If the record of what was considered is missing, ask the user instead of reconstructing it.
- Link related records and evidence with relative Markdown links.

Per job:

- **Accept a proposed record:** `git mv` it to `accepted/`, set `Status: accepted`, rename `## Proposal` to `## Decision` and rewrite it in the present tense to describe what shipped, fold acceptance criteria and risks into `## Consequences`, and delete plans and open questions.
- **Reject:** `git mv` to `rejected/`, set `Status: rejected — <why, in one line>`, and change nothing else.
- **Supersede:** write the new record, then archive, delete, or cross-link the old one as step 3 says. Never edit an accepted record into a different decision.
- **Correct:** rewrite the stale fact in place. Do not append history; git holds it.
- **Archive:** `git mv` to `archived/<class>/`, keep `Status: accepted`, insert `Archived: yyyy-mm-dd` as the fourth line, and change nothing else. From then on the file is frozen and is never cited as current behavior.
- **Delete:** remove the file and repair or remove every inbound link.

- **Done when:** the record sits in the folder its job requires and every alternative it lists was actually considered.

## 5. Validate

Find inbound links to any moved or deleted record with a repository search for its file name, and fix them. Then run:

```sh
python3 .agents/skills/artifact-map/scripts/gates/check_decisions.py
```

Adjust the path if the pack is installed elsewhere. Fix every problem it reports before you hand back.

- **Done when:** no inbound link points at a moved or deleted path and the gate reports 0 problems.

## 6. Report

One line, for example: `Decision: accepted docs/decisions/accepted/architecture/2026-11-07-order-idempotency.md (moved from proposed/, Decision rewritten).`
