# Decision: Skills are named for what they are or do, never with a bare generic verb

Status: accepted

## Problem

Skill names are hard to change once projects install them: CI steps, lock files, and cross-skill links all carry the path. Names also drive triggering, because agents match requests against skill names and descriptions, and they collide when a project installs several packs.

## Decision

A reference skill is named for the thing it is (`artifact-map`). A workflow skill is named verb-noun for the job it does (`decision-record`, `close-ticket`, and later `shape-work`, `review-change`). No skill takes a bare generic word such as `setup`, `review`, `close`, or `plan`, and no pack prefix is used. The shared-foundation skill is `artifact-map`, and the artifact map is its `SKILL.md`, so loading the skill is reading the map.

## Alternatives considered

**`setup`.** Proposed for the foundation skill. It names one rarely used section, not the map that every other skill consults before writing; it would trigger on unrelated requests such as setting up a dev environment or CI; and other packs already use the word (`setup-matt-pocock-skills`, `ce-setup`).

**`project-artifacts`.** Accurate but long, and it says what the skill covers rather than what it is for.

**A pack prefix such as `sf-`.** Avoids collisions with certainty, but adds noise to every name and every trigger; distinct verb-noun names avoid collisions well enough.

## Consequences

Names are longer than single words. Renaming a skill after projects install it means a coordinated change to their CI and links, so names are settled before a skill is marked ready.
