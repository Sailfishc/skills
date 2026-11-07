# Decision: Build verification into the pack; no external acceptance dependency yet

Status: accepted

## Problem

Agents claim work is done without proving it on the real product. LobeHub Acceptance solves this with checks, required evidence, and reports, but its sharing and review features depend on LobeHub sign-in and its `lh` CLI.

## Decision

For this phase the pack ships its own `verify` skill and depends on no external service. It adopts Acceptance's contract: a plan of checks, each with required evidence; a check without its evidence is not a pass; reports stay local. It also adopts pstack's idea of a project-specific driver: how to start, drive, and clean up the product lives in the project's `.agents/verify/` adapter. Acceptance checks are written at shaping time in `plan.md`, so verification consumes them directly. A rejected check is logged in the adapter's living log, and a repeated one goes through the cheapest-form ladder.

## Alternatives considered

**Depend on LobeHub Acceptance directly.** Mature and multi-harness, but ties shared review to an outside service. Revisit when the team needs hosted reports with comments.

**pstack's generated `verify` skill alone.** Drives the product but defines no evidence contract or report.

## Consequences

The pack owns the evidence format and report, so it must keep them simple. Switching to Acceptance later is cheap if the check format stays close to it.
