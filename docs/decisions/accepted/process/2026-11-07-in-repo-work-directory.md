# Decision: In-flight work lives in the repository and is distilled before merge

Status: accepted

## Problem

Brainstorms, plans, and handoffs are needed while a ticket is open, but kept forever they pile up, go stale, and mislead later agents.

## Decision

Work that spans sessions or agents, or whose plan needs review before code, gets `work/<ticket>/plan.md` in the repository. The plan's front matter carries the ticket status (`shaping`, `building`, `verifying`, `reviewing`, `closing`); status is not synced to an issue tracker. Before the ticket's last PR merges, the close skill distills the directory into decisions, checks, standards, or learnings, deletes the rest, and lists what went where in the PR description. The `check_work.py` gate fails CI on a malformed ticket directory, on a ticket left in `closing`, and, when a project sets an idle limit, on a ticket with no recent commit. Whether a ticket is truly finished cannot be checked mechanically, so the gate catches incomplete closes and abandoned tickets rather than proving every ticket was distilled. Directories are per ticket, not per branch, so one ticket can span stacked PRs.

## Alternatives considered

**Plans in an issue tracker (Matt Pocock's `to-spec` and `to-tickets`).** Keeps the repository clean, but every harness then needs tracker access to resume work, and plans cannot be reviewed in the same diff as the code.

**Plans kept permanently in `docs/plans/` (Compound Engineering).** Nothing retires them: its own repository holds well over a hundred plans that no refresh covers.

**Plans outside the repository (pstack scratch).** Clean, but a second machine or agent cannot pick up the work.

**Status synced to the tracker.** Gives teammates a board view, but adds an integration per tracker and a second source of truth. Deferred.

## Consequences

Distillation becomes a required step with its own skill and gate. Teammates see progress only through PRs, not a board.
