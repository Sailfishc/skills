---
ticket: <id or slug>
status: shaping  # shaping | building | verifying | reviewing | closing
decisions: []    # links to docs/decisions/... records this work depends on or proposes
---

# Plan: <title>

<!--
Path: work/<ticket>/plan.md
Only for work that spans sessions or agents, or whose plan needs review before code.
Each stage skill reads `status` on entry and updates it on exit.
The close skill distills this directory and deletes it before the ticket's last PR merges.
-->

## Goal

The outcome, in the user's terms.

## Units

Ordered units of work. Each ends in a check that proves it.

1. <unit> — proved by: <test, command, or observation>

## Acceptance checks

What must be observed on the real product before this is done. These are the verify stage's input.

| ID | Check | Required evidence |
| --- | --- | --- |
| A1 | <observable behavior> | <screenshot / recording / log / command output> |

## Open questions

## Handoff

<!-- Updated whenever a session stops mid-ticket: current state, what was tried, what is next. -->
