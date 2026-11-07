#!/usr/bin/env python3
"""Check decision records under docs/decisions/ against the artifact map.

Checks each record's path (lifecycle/class/yyyy-mm-dd-slug.md), its header and
Status line, the sections its lifecycle requires or forbids, and that its
relative links resolve. Archived records are checked for path and header only.

Usage: check_decisions.py [--root docs/decisions]
Exits 1 and prints one line per problem when any check fails.
"""
import argparse
import os
import re
import sys

LIFECYCLES = ("proposed", "accepted", "rejected", "archived")
CLASSES = ("feature", "bug-fix", "simplification", "architecture", "process", "testing")
NAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
REQUIRED = {
    "proposed": ("Problem", "Proposal", "Alternatives considered", "Consequences"),
    "accepted": ("Problem", "Decision", "Alternatives considered", "Consequences"),
    "rejected": ("Problem", "Proposal", "Alternatives considered"),
}
FORBIDDEN = {
    "proposed": ("Decision",),
    "accepted": ("Proposal", "Plan", "Migration plan", "Acceptance criteria"),
}


def check_header(lines, lifecycle):
    problems = []
    if not lines or not lines[0].startswith("# Decision: ") or len(lines[0]) <= len("# Decision: "):
        problems.append("first line must be '# Decision: <title>'")
    if len(lines) < 3 or lines[1] != "":
        problems.append("second line must be blank")
        return problems
    status = lines[2]
    if lifecycle == "rejected":
        if not re.fullmatch(r"Status: rejected — \S.*", status):
            problems.append("third line must be 'Status: rejected — <why>'")
    elif lifecycle == "archived":
        if status != "Status: accepted":
            problems.append("third line must be 'Status: accepted'")
        if len(lines) < 4 or not re.fullmatch(r"Archived: \d{4}-\d{2}-\d{2}", lines[3]):
            problems.append("fourth line must be 'Archived: yyyy-mm-dd'")
    elif status != f"Status: {lifecycle}":
        problems.append(f"third line must be 'Status: {lifecycle}'")
    return problems


def check_sections(text, lifecycle):
    headings = re.findall(r"^## (.+?)\s*$", text, re.M)
    problems = []
    for name in REQUIRED.get(lifecycle, ()):
        if name not in headings:
            problems.append(f"missing section '## {name}'")
    for name in FORBIDDEN.get(lifecycle, ()):
        if name in headings:
            problems.append(f"section '## {name}' is not allowed in a {lifecycle} record")
    if headings and headings[0] != "Problem":
        problems.append("the first section must be '## Problem'")
    return problems


def check_links(path, text):
    problems = []
    for target in LINK_RE.findall(text):
        target = target.split("#", 1)[0]
        if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target):
            continue
        resolved = os.path.normpath(os.path.join(os.path.dirname(path), target))
        if not os.path.exists(resolved):
            problems.append(f"broken link '{target}'")
    return problems


def check_record(path, root):
    rel = os.path.relpath(path, root)
    parts = rel.split(os.sep)
    if len(parts) != 3:
        return [f"must sit at <lifecycle>/<class>/<file>, found '{rel}'"]
    lifecycle, klass, name = parts
    problems = []
    if lifecycle not in LIFECYCLES:
        problems.append(f"unknown lifecycle '{lifecycle}' (expected one of {', '.join(LIFECYCLES)})")
    if klass not in CLASSES:
        problems.append(f"unknown class '{klass}' (expected one of {', '.join(CLASSES)})")
    if not NAME_RE.match(name):
        problems.append("file name must be yyyy-mm-dd-<lowercase-slug>.md")
    if problems:
        return problems
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    lines = text.split("\n")
    problems += check_header(lines, lifecycle)
    if lifecycle != "archived":
        problems += check_sections(text, lifecycle)
        problems += check_links(path, text)
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check decision records.")
    parser.add_argument("--root", default="docs/decisions")
    args = parser.parse_args(argv)
    if not os.path.isdir(args.root):
        print(f"check_decisions: no {args.root}/, nothing to check")
        return 0
    failures = 0
    count = 0
    for directory, _, files in os.walk(args.root):
        for name in sorted(files):
            if not name.endswith(".md") or name == "README.md":
                continue
            path = os.path.join(directory, name)
            count += 1
            for problem in check_record(path, args.root):
                print(f"{path}: {problem}")
                failures += 1
    print(f"check_decisions: {count} records, {failures} problems")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
