#!/usr/bin/env python3
"""Check work/ against the artifact map.

Every entry in work/ must be a ticket directory holding plan.md, whose front
matter has a valid `status`. A ticket left in `closing` fails: the close step
deletes the directory in the same change, so `closing` must never be committed.
With --max-idle-days N, a ticket whose directory has no commit in N days fails.

Usage: check_work.py [--root work] [--max-idle-days N]
Exits 1 and prints one line per problem when any check fails.
"""
import argparse
import os
import re
import subprocess
import sys
import time

STATUSES = ("shaping", "building", "verifying", "reviewing", "closing")


def plan_status(path):
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return None
    status = re.search(r"^status:\s*([a-z-]+)", match.group(1), re.M)
    return status.group(1) if status else None


def last_commit_age_days(path):
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%ct", "--", path],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    if not out:
        return None
    return (time.time() - int(out)) / 86400


def check(root, max_idle_days=None):
    problems = []
    for name in sorted(os.listdir(root)):
        path = os.path.join(root, name)
        if name.startswith(".") and os.path.isfile(path):
            continue
        if not os.path.isdir(path):
            problems.append(f"{path}: files in work/ must sit inside a ticket directory")
            continue
        plan = os.path.join(path, "plan.md")
        if not os.path.isfile(plan):
            problems.append(f"{path}: ticket directory has no plan.md")
            continue
        status = plan_status(plan)
        if status is None:
            problems.append(f"{plan}: front matter must set 'status'")
        elif status not in STATUSES:
            problems.append(f"{plan}: unknown status '{status}' (expected one of {', '.join(STATUSES)})")
        elif status == "closing":
            problems.append(f"{plan}: ticket left in 'closing'; finish the close step, which deletes this directory")
        if max_idle_days is not None:
            age = last_commit_age_days(path)
            if age is not None and age > max_idle_days:
                problems.append(f"{path}: no commit for {age:.0f} days (limit {max_idle_days}); close it or update its handoff")
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check work/ ticket directories.")
    parser.add_argument("--root", default="work")
    parser.add_argument("--max-idle-days", type=int)
    args = parser.parse_args(argv)
    if not os.path.isdir(args.root):
        print(f"check_work: no {args.root}/, nothing to check")
        return 0
    problems = check(args.root, args.max_idle_days)
    for problem in problems:
        print(problem)
    print(f"check_work: {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
