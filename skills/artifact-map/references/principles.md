# Principles

Judgment calls no check or standard can hold. A stage skill loads only the section for the step it is on. A principle a check can enforce becomes a lint rule instead, and `tend-knowledge` deletes any principle no review or retrospective has cited.

## Shape

- **model-the-domain.** Choose the core types and state shapes before writing logic. When code branches a lot or repeats a shape assumption across files, the model is missing; name it once and let downstream code follow from it.
- **subtract-before-you-add.** Before adding, remove the dead code, redundant validators, and stale references the addition would build on. Plan the deletion as the first unit.
- **attack-the-premise.** When two fixes resting on the same assumption have failed the same check, write the assumption down and test it directly before writing a third.

## Build

- **sequence-verifiable-units.** Split the work into units that each end in a state you can check, check each before starting the next, and order commits so the sequence proves itself to a reviewer.
- **surgical diff.** Make the smallest change that meets the requirement. Inline single-use logic; add no abstraction, option, flag, or compatibility layer the task does not need. When a new internal API replaces an old one, migrate the callers and delete the old API in the same change.
- **boundary-discipline.** Validate and handle errors where data enters the system: CLI, config, network, external APIs, persisted data. Inside, trust the types. Guard only states that can actually occur.
- **make-operations-idempotent.** A command, job, or handler that can be retried, restarted, or replayed must converge to the same end state however many times it ran partway.
- **fix-root-causes.** Trace a symptom to the first place the system went wrong and fix it there. A guard at the call site is a fix only when the state it handles is legitimate.

## Verify

- **test-behavior-not-implementation.** Assert what users of the code can observe, so the test fails when that behavior breaks and passes when only internals change.
- **prove-it-works.** Done means observed on the real artifact: the feature run, the actual value read, the diff inspected. A passing compile, a self-report, or a proxy metric is not proof. Before trusting a measured number, find what limits it and rule out that it measured something else.

## Sources

Condensed and adapted from the `principle-*` skills of [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan and its [Claude Code port](https://github.com/michael-denyer/pstack-claude) by Michael Denyer, used under the MIT license ([LICENSE-pstack](LICENSE-pstack)). **surgical diff** also draws on pstack's `laziness-protocol` and `migrate-callers-then-delete-legacy-apis`.
