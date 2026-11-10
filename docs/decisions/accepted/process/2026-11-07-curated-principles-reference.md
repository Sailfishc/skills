# Decision: Curated principles as a reference, not as skills

Status: accepted

## Problem

pstack ships 23 `principle-*` skills with good judgment guidance. Installed as skills, every description sits in every session's context, and their hidden-from-user flag and routing do not carry over to every harness.

## Decision

Ten principles, condensed and grouped by stage (Shape, Build, Verify), live in [`artifact-map/references/principles.md`](../../../../skills/artifact-map/references/principles.md). Each stage skill links only the section for the step it is on. Principles a check can enforce become lint rules instead, and the tend stage deletes a principle that no review or retrospective has cited. The file credits pstack and carries its MIT license. pstack's `encode-lessons-in-structure` is not copied because the artifact map's cheapest-durable-form rule already states it.

## Alternatives considered

**Install all pstack principle skills.** Full coverage, at a constant context cost and with routing that depends on pstack's own entry skill.

**No principles at all.** Leaves judgment calls that no check or standard covers without guidance.

## Consequences

Some guidance is dropped on purpose, for example UX-first trade-offs and prototype bake-offs. The selection needs revisiting as retrospectives show which principles matter.
