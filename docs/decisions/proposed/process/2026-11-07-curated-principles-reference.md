# Decision: Curated principles as a reference, not as skills

Status: proposed

## Problem

pstack ships 23 `principle-*` skills with good judgment guidance. Installed as skills, every description sits in every session's context, and their hidden-from-user flag and routing do not carry over to every harness.

## Proposal

Select eight to ten principles and merge them into `project-artifacts/references/principles.md`, each two or three lines and tagged with the stage it applies to. Each stage skill loads only the principles for the step it is on. Principles a check can enforce become lint rules instead. The tend stage deletes a principle that no review or retrospective has cited. Attribution follows pstack's license and notice files.

## Alternatives considered

**Install all pstack principle skills.** Full coverage, at a constant context cost and with routing that depends on pstack's own entry skill.

**No principles at all.** Leaves judgment calls that no check or standard covers without guidance.

## Consequences

Some guidance is dropped on purpose. The selection needs revisiting as retrospectives show which principles matter.
