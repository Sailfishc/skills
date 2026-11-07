# Decision: Living decision records instead of snapshot ADRs

Status: accepted

## Problem

Projects need a durable record of why a choice was made and what it beat. The main readers are agents, which treat any text they find as current instruction and cannot tell a stale snapshot from live guidance.

## Decision

Decisions live in `docs/decisions/{proposed,accepted,rejected,archived}/<class>/yyyy-mm-dd-<slug>.md`, with the lifecycle in the path and a `Status:` line that matches it. A proposed record is the RFC; on acceptance it is rewritten into a present-tense Decision, and its facts are kept current in the same change that moves them. A changed decision gets a new record, cross-linked to the old one. Archived records are frozen and never current authority. Admission uses three tests: hard to reverse, surprising without context, a real trade-off. Alternatives are mandatory. Records are short, single-language (English), and unnumbered. The rules live in [the artifact map](../../../../skills/artifact-map/SKILL.md#decision-lifecycle), and `check_decisions.py` in the same skill checks paths, status lines, and sections.

## Alternatives considered

**Snapshot ADRs (Matt Pocock's `domain-modeling`).** Cheap to write and never maintained, but their paths and names rot, and an agent reading an old ADR follows it as if it were current. Optional alternatives also let agents re-propose options that already lost.

**DeepSeek Harness Agent Notes as-is.** The lifecycle model is the one adopted here, but the admission bar is wide (hundreds of implemented notes), every note is an English, Chinese, and sidecar triplet, and the format is enforced by heavy gates. Too costly for a small team at the start.

**Sequential numbering.** Parallel branches collide on the next number; dates plus slugs do not.

## Consequences

Every change that moves a path, name, or default named in an accepted record must update that record, so records need a gate or a review check to stay true. In return, an agent can trust an accepted record as current, and the rejected folder stops settled questions from being reopened.
