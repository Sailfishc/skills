# Decision: Generic pack skills, project-specific adapters

Status: accepted

## Problem

Projects share working patterns (how to plan, review, verify) but differ in their constraints: lint rules, review criteria, how to start and drive the product. Copying one set of standards into every project drifts; one shared set fits none of them.

## Decision

Two dimensions. The pack holds workflow skills, their pass criteria, templates, principles, and generic gates. Each project holds its own constraints: `AGENTS.md`, `CODING_STANDARDS.md`, lint and CI configuration, and an adapter per skill under `.agents/<skill>/` (project commands, extra review axes, living logs of past mistakes). The adapter decides how to run something in that project; the pack skill decides what counts as done. A project rule that recurs in a second project moves into the pack; a pack rule that projects keep overriding moves out. The adapter shape follows LobeHub Acceptance's `.agents/acceptance/` project layer.

## Alternatives considered

**Copy standards into each project.** Simple at first; no way to improve the shared part once.

**One shared standards file for every project.** Ignores real differences, for example money handling in a trading system versus a data platform.

## Consequences

Every pack skill must define which adapter files it reads and what happens when they are missing. Moving rules between the two dimensions needs judgment during the tend stage.
