import contextlib
import importlib.util
import io
import os
import subprocess
import tempfile
import unittest

GATES = os.path.join(os.path.dirname(__file__), "..", "skills", "artifact-map", "scripts", "gates")


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(GATES, f"{name}.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


check_decisions = load("check_decisions")
check_work = load("check_work")
check_agents_budget = load("check_agents_budget")

ACCEPTED = """# Decision: Use X

Status: accepted

## Problem

p

## Decision

d

## Alternatives considered

**Y.** lost.

## Consequences

c
"""


def write(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    return path


def run(main, argv):
    with contextlib.redirect_stdout(io.StringIO()) as out:
        code = main(argv)
    return code, out.getvalue()


class DecisionGateTest(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()

    def problems(self, rel, text):
        path = write(self.root, rel, text)
        return check_decisions.check_record(path, self.root)

    def test_valid_accepted_record_passes(self):
        self.assertEqual(self.problems("accepted/process/2026-11-07-use-x.md", ACCEPTED), [])

    def test_status_must_match_lifecycle_folder(self):
        problems = self.problems("proposed/process/2026-11-07-use-x.md", ACCEPTED)
        self.assertIn("third line must be 'Status: proposed'", problems)

    def test_accepted_record_rejects_proposal_section(self):
        text = ACCEPTED.replace("## Decision", "## Proposal")
        problems = self.problems("accepted/process/2026-11-07-use-x.md", text)
        self.assertIn("missing section '## Decision'", problems)
        self.assertIn("section '## Proposal' is not allowed in a accepted record", problems)

    def test_alternatives_are_required(self):
        text = ACCEPTED.replace("## Alternatives considered", "## Notes")
        problems = self.problems("accepted/process/2026-11-07-use-x.md", text)
        self.assertIn("missing section '## Alternatives considered'", problems)

    def test_rejected_record_needs_a_reason(self):
        text = ACCEPTED.replace("Status: accepted", "Status: rejected").replace("## Decision", "## Proposal")
        problems = self.problems("rejected/process/2026-11-07-use-x.md", text)
        self.assertIn("third line must be 'Status: rejected — <why>'", problems)

    def test_archived_record_needs_archive_date(self):
        problems = self.problems("archived/process/2026-11-07-use-x.md", ACCEPTED)
        self.assertIn("fourth line must be 'Archived: yyyy-mm-dd'", problems)

    def test_unknown_class_and_bad_name(self):
        problems = self.problems("accepted/refactor/use-x.md", ACCEPTED)
        self.assertTrue(any("unknown class 'refactor'" in p for p in problems))
        self.assertIn("file name must be yyyy-mm-dd-<lowercase-slug>.md", problems)

    def test_broken_relative_link(self):
        text = ACCEPTED.replace("d\n", "See [other](../../missing.md).\n", 1)
        problems = self.problems("accepted/process/2026-11-07-use-x.md", text)
        self.assertIn("broken link '../../missing.md'", problems)

    def test_main_reports_failure(self):
        write(self.root, "accepted/process/2026-11-07-use-x.md", ACCEPTED.replace("Status: accepted", "Status: done"))
        code, out = run(check_decisions.main, ["--root", self.root])
        self.assertEqual(code, 1)
        self.assertIn("1 records, 1 problems", out)


class WorkGateTest(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()

    def test_missing_root_passes(self):
        code, _ = run(check_work.main, ["--root", os.path.join(self.root, "absent")])
        self.assertEqual(code, 0)

    def test_valid_ticket_passes(self):
        write(self.root, "T-1/plan.md", "---\nticket: T-1\nstatus: building\n---\n# Plan\n")
        self.assertEqual(check_work.check(self.root), [])

    def test_closing_ticket_fails(self):
        write(self.root, "T-1/plan.md", "---\nstatus: closing\n---\n")
        problems = check_work.check(self.root)
        self.assertTrue(any("left in 'closing'" in p for p in problems))

    def test_ticket_without_plan_and_stray_file_fail(self):
        write(self.root, "T-1/notes.md", "x")
        write(self.root, "loose.md", "x")
        problems = check_work.check(self.root)
        self.assertTrue(any("has no plan.md" in p for p in problems))
        self.assertTrue(any("must sit inside a ticket directory" in p for p in problems))

    def test_unknown_or_missing_status_fails(self):
        write(self.root, "T-1/plan.md", "---\nstatus: done\n---\n")
        write(self.root, "T-2/plan.md", "# no front matter\n")
        problems = check_work.check(self.root)
        self.assertTrue(any("unknown status 'done'" in p for p in problems))
        self.assertTrue(any("must set 'status'" in p for p in problems))

    def test_idle_ticket_fails_when_limit_set(self):
        repo = tempfile.mkdtemp()
        env = dict(os.environ, GIT_AUTHOR_DATE="2020-01-01T00:00:00", GIT_COMMITTER_DATE="2020-01-01T00:00:00")
        write(repo, "work/T-1/plan.md", "---\nstatus: building\n---\n")
        for command in (["git", "init", "-q"], ["git", "add", "."],
                        ["git", "-c", "user.name=t", "-c", "user.email=t@example.com", "commit", "-q", "-m", "x"]):
            subprocess.run(command, cwd=repo, check=True, env=env)
        cwd = os.getcwd()
        os.chdir(repo)
        try:
            self.assertEqual(check_work.check("work"), [])
            problems = check_work.check("work", max_idle_days=30)
        finally:
            os.chdir(cwd)
        self.assertTrue(any("no commit for" in p for p in problems))


class AgentsBudgetGateTest(unittest.TestCase):
    def test_budget(self):
        path = write(tempfile.mkdtemp(), "AGENTS.md", "one two three four")
        self.assertEqual(run(check_agents_budget.main, ["--file", path, "--max-words", "4"])[0], 0)
        self.assertEqual(run(check_agents_budget.main, ["--file", path, "--max-words", "3"])[0], 1)

    def test_missing_file_fails(self):
        self.assertEqual(run(check_agents_budget.main, ["--file", "/nonexistent/AGENTS.md"])[0], 1)


if __name__ == "__main__":
    unittest.main()
