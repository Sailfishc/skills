---
name: close-ticket
description: Close a ticket by hand. Distill work/<ticket>/ into decision records, checks, coding standards, or learnings, delete the rest, and run a short evidence-based retrospective on what made the work harder than it needed to be. Use when the user asks to close, wrap up, distill, or retro a ticket, or before the last PR of a ticket merges.
---

# Close ticket

**Outcome:** nothing the ticket taught is lost, nothing it no longer needs is kept, and each lesson sits in the strongest form that stops it from happening again.

**Done:** `work/<ticket>/` is deleted, the gates pass, and the PR description carries a "Distilled from" block listing where every item went. If nothing was worth keeping, the block says so.

Read the [artifact map](../project-artifacts/references/artifact-map.md) first. This skill needs `project-artifacts` and `decision-record` installed beside it. It runs only when someone invokes it.

## 1. Find the ticket

Use the ticket the user names. Otherwise use the single directory under `work/`, or the one the current branch's commits touch. If more than one fits, ask. If there is no `work/` directory for this ticket, skip to step 4 and run the retrospective alone.

If more PRs are still planned for this ticket, stop: close runs with the ticket's last PR. Say so, and offer to update the plan's Handoff section instead.

Set `status: closing` in `plan.md` while you work. Never commit that state: this run ends by deleting the directory.

## 2. Sort every item

Read every file in `work/<ticket>/`. Sort each distinct item (a choice, a finding, a note, a check) into one bucket:

| Bucket | Examples | Goes to |
| --- | --- | --- |
| Decision | A choice between real alternatives | Step 3 |
| Lesson | A mistake, a surprise, a method that saved time | Step 4 |
| Spent | Plan steps that were done, handoff notes, open questions that were answered, logs | Deleted |
| Unfinished | Work that is still wanted but is not part of this ticket | A new ticket, or the user decides |

An item already fully explained by the final code, tests, or existing docs is Spent.

## 3. Settle decisions

Use the `decision-record` skill for each Decision item. A proposed record this ticket shipped is accepted and rewritten. A choice made during the work that passes admission gets a record. Plan text that only restates a decision is Spent.

## 4. Retrospective

Gather evidence before judging: review comments on the PRs, CI failures and reruns, user corrections in the session, and the project's living logs under `.agents/*/` if present. Then look for what made the work harder than it needed to be:

- **Navigation:** finding the right file or fact took many steps. A pointer in `AGENTS.md` or `docs/architecture.md` would have shortened it.
- **Missing check:** a mistake reached review, CI, or the user that a test, type, or lint rule could have caught. Read the project's existing check commands first: a check that exists but is not wired in is the finding.
- **Review gap:** the reviewer missed something it should have caught.
- **Missing information:** something the agent needed was not reachable, such as logs or a service's state.
- **Expensive tooling:** a command or tool that was slow, repeated, or wasteful every time.
- **Standing-instruction noise:** an `AGENTS.md` rule that was ignored, wrong, or changed nothing.

Every finding cites its evidence: the command, the failed run, the review comment, or the correction. **No evidence, no finding.** Do not write general advice to fill these categories. A smooth ticket has no findings, and that is a valid result.

Each finding becomes a Lesson for step 5.

## 5. Put each lesson in its cheapest durable form

Handle one lesson at a time. Try these forms in order and take the first that holds:

1. **Remove the second way.** The mistake was possible because two ways to do the same thing exist. Consolidating them changes product code: report it as follow-up work, and continue down the list for what can be held now.
2. **A check.** A test, type, or lint rule the project already runs can detect it, and its failure says what to fix. Add it, then prove it twice: it passes on the current tree, and it fails on the defect in a throwaway copy of the tree. Never put the defect in the working tree. If you cannot show both, remove the check and move to the next form.
3. **A standard.** An author must avoid it while writing and a reviewer can see it in a diff, and no check can hold it. Add one condition to the `CODING_STANDARDS.md` nearest the affected code, in that file's style. Only add a standard when the defect appeared in a review finding, a fix commit, or this ticket's evidence. If the project has no `CODING_STANDARDS.md`, do not create one; write a learning instead.
4. **A learning.** Reasoning that code, tests, and standards cannot carry. Write it only if it passes the counterfactual: if this document disappeared, would someone reading the final code still repeat the mistake or redo the investigation? Search `docs/learnings/` first and update an existing learning rather than adding a near-duplicate. Use the [learning template](../project-artifacts/templates/learning.md).
5. **A pointer.** Navigation findings become one line in `AGENTS.md` or `docs/architecture.md` that links to the owning file. Add to `AGENTS.md` only when every session needs it.

If a check or standard already states the lesson, the lesson was not new: write nothing and note which file holds it.

## 6. Delete and verify

Delete `work/<ticket>/`. Then run the gates from the project root:

```sh
python3 .agents/skills/project-artifacts/scripts/gates/check_decisions.py
python3 .agents/skills/project-artifacts/scripts/gates/check_work.py
python3 .agents/skills/project-artifacts/scripts/gates/check_agents_budget.py
```

Fix every failure before handing back. Run the tests for any check you added.

## 7. Report

Add this block to the PR description, or print it when there is no PR:

```
Distilled from work/<ticket>:
- Decision → docs/decisions/accepted/<class>/<file>.md
- Check → <test or lint rule> (passes on the tree, fails on the defect)
- Standard → CODING_STANDARDS.md: <condition>
- Learning → docs/learnings/<file>.md
- Follow-up → <reported work, such as removing a second way>
- Deleted: plan.md, <other files>
Retrospective: <one line per finding with its evidence, or "no findings">
```

Leave committing to the user's normal flow unless they ask you to commit.
