# Decision: Close and retrospective run manually

Status: accepted

## Problem

Lessons are lost if nobody reflects at the end of a ticket, but a retrospective after every turn costs time and fills the record with noise.

## Decision

The `close` skill, which distills `work/<ticket>/` and runs the retrospective, is invoked by hand. Nothing triggers it automatically. The CI gate on `work/` catches tickets merged without distillation. The periodic `tend` stage covers what single tickets miss.

## Alternatives considered

**A Stop hook that asks for a retrospective after real work (agent-rsi).** Never forgets, but adds a turn to most sessions and needs hooks, which this pack does not use.

**Retrospective only, no distillation step (Matt Pocock's `retro`).** Lightweight, but leaves in-flight artifacts behind.

## Consequences

Retrospectives happen when someone judges a ticket worth one, so smooth tickets cost nothing. Lessons from a ticket closed without one are caught only by the next `tend` run.
