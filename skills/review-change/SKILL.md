---
name: review-change
description: Review a diff in a separate context against what it was meant to do, the project's CODING_STANDARDS.md, correctness, and surgical minimalism, and report verified findings by severity. Use when asked to review a change, a PR, or the current diff, and before a ticket moves to close.
---

# Review change

**Outcome:** every real defect in the diff is found and explained well enough to fix, and nothing that is not a defect is reported.

**Done:** the report lists verified findings ordered by severity, each with `file:line`, how it fails, and the fix, or says **Clean diff**; recurring finding types are logged for the project.

Read the [Build](../artifact-map/references/principles.md#build) and [Verify](../artifact-map/references/principles.md#verify) principles. Read [subagents.md](../artifact-map/references/subagents.md) for how to run in a separate context. Do not edit code unless the user asks after the report.

## 1. Collect the inputs

- **The diff:** the PR, or `git diff <base>...HEAD` plus uncommitted changes. Ask which base when it is unclear.
- **The intent:** `work/<ticket>/plan.md` (Goal, Out of scope, Acceptance checks, linked decisions), else the PR description, else the user's request. If none exists, ask for the intent in one sentence before reviewing.
- **The rules:** the `CODING_STANDARDS.md` nearest each changed file, and the accepted decision records the plan links or the diff touches.
- **The project adapter**, if present: `.agents/review-change/PROJECT.md` (extra review axes and commands) and `.agents/review-change/common-mistakes.md` (findings this project has repeated).

If a plan exists and every unit is ticked, set its `status: reviewing`; otherwise leave the status unchanged.

- **Done when:** the diff, the intent, and the applicable rules are each identified, or the missing intent was asked for.

## 2. Separate the reviewer

Run the review in a fresh context, as [subagents.md](../artifact-map/references/subagents.md) describes: the reviewer receives only the inputs from step 1, never the builder's transcript or reasoning. Use the strongest available model. The reviewer runs steps 3 to 5 and returns its findings; you run step 6 after checking each cited line. If this session wrote the code and no fresh context is available, say so and label the report **Self-review, not independent**.

- **Done when:** the reviewer's context holds none of the builder's reasoning, the user was told to rerun the review in a new session, or the report carries the label.

## 3. Run the project's checks

Run the test, typecheck, and lint commands that cover the changed files. A failing check is a finding. Do not report by hand what these checks already catch.

- **Done when:** every relevant check ran and its result is recorded.

## 4. Review each axis

Read every hunk and the code around it. Check four axes, plus any the project adapter adds:

1. **Intent:** the diff does what the intent says, every acceptance check is addressable, nothing listed as out of scope was done, and no accepted decision is contradicted.
2. **Correctness:** the root cause is fixed, not masked at a call site; state transitions, error paths, and retries hold under real inputs; public signatures, serialized formats, and callers outside the diff still work; tests assert observable behavior.
3. **Standards:** each condition in the applicable `CODING_STANDARDS.md` that fits the changed code is met. Cite the condition.
4. **Minimalism:** no abstraction, option, flag, wrapper, or compatibility layer the intent does not need; no guard for a state that cannot occur; no dead code, comments that restate code, or churn in unrelated lines.

- **Done when:** every hunk was checked against every axis.

## 5. Verify each finding

For each candidate, re-read the code and state the concrete failure: the input or state, and the wrong result. Drop any candidate where you cannot. Assign severity:

| Severity | Meaning |
| --- | --- |
| **Critical** | Wrong behavior, data loss, security exposure, or a broken contract |
| **Major** | A likely bug, a standards violation, scope the intent did not ask for, or an unmet acceptance check |
| **Nit** | Minimalism and hygiene |

- **Done when:** every remaining finding has a failure scenario and a severity.

## 6. Report

Order findings Critical, Major, Nit. Each one: `file:line`, the failure scenario, and the exact fix (the deletion or replacement). With no findings, write **Clean diff** and one sentence on any risk the checks could not cover.

If a plan exists: with any Critical or Major finding, add one unticked unit per finding to its Units (`- [ ] Fix <finding> — proved by: <check>`) and set `status: building`. Otherwise, if the status is `reviewing`, keep it and say the ticket is ready for `close-ticket`.

For each Critical or Major finding, append one line to `.agents/review-change/common-mistakes.md`, creating it if needed: `yyyy-mm-dd | <axis>/<kebab-slug> | <file>`, for example `minimalism/dead-guard`. Reuse a slug already in the file when one fits, so `close-ticket` can count repeats and turn them into checks or standards.

- **Done when:** the report is delivered; if a plan exists, its status is set and every Critical or Major finding is a unit in it; and every Critical or Major finding is logged.
