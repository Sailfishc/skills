---
name: build-work
description: Implement a code change as a surgical diff with a red-green loop, and reconcile every task to Done or Blocked before stopping. Use whenever writing, modifying, or fixing production code or tests. Not for read-only exploration, questions, or code review.
---

# Build work

**Outcome:** the smallest diff that meets the requirement, proved by checks that ran, with every task the user asked for reconciled.

**Done:** every requested task is Done (with the check that proved it) or Blocked (with one concrete question), and the diff touches only the files the work needs.

Read the [Build principles](../artifact-map/references/principles.md#build).

## 1. Pick up the work

If `work/<ticket>/plan.md` exists, read it and take the next unticked unit. If its `status` is still `shaping`, the plan has not been approved: stop and ask, unless the user has said to go ahead. If there is no plan and the goal or approach is unclear, run `shape-work` first.

- **Done when:** you can name the unit you are building and the check that will prove it.

## 2. Ground

Confirm the target symbols, the local patterns to mirror, and the project's test, typecheck, and lint commands from the workspace. Skip what shaping already established in this session or in the plan's Context.

- **Done when:** every file you will edit and every command you will run is confirmed from the workspace, not assumed.

## 3. Red

Pick the case that fits:

- **Behavior changes:** write or update a focused test, or a minimal reproduction, that captures the target behavior. Run it.
- **Pure refactor:** run the existing tests that cover the code.
- **No runtime behavior** (docs, configuration, copy): name the check that will prove the change instead.

- **Done when:** the new test fails for the expected reason, the refactor baseline passes, or the proving check is named.

## 4. Edit

Make the change with the project's own types and idioms. Keep the diff surgical: add no abstraction, option, flag, wrapper, or compatibility layer the requirement does not need, and handle only errors that can actually occur here. Problems you notice outside the task are noted for the report, not fixed.

- **Done when:** every added line traces to the requirement.

## 5. Green

Run the focused test, then the typecheck, lint, and tests that cover the touched paths. When a check fails, read its output and fix the cause before patching again. Never stack workarounds. If two fixes built on the same assumption fail the same check, test the assumption itself.

- **Done when:** all of them pass, and the diff's file list contains only the files this work needs.

## 6. Advance the plan

Skip if there is no plan. Tick the unit. If you are stopping before the ticket is finished, update the Handoff section: current state, what was tried, what is next. When every unit is ticked, set `status: verifying`.

- **Done when:** the plan matches what is actually built.

## 7. Reconcile and report

List every task the user asked for as **Done**, with the check that proved it, or **Blocked**, with one concrete question that would unblock it. Report only checks that actually ran. Put refactors nobody asked for under "Optional next steps", outside the diff.

- **Done when:** no requested task is left without a status.
