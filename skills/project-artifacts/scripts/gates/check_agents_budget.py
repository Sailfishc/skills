#!/usr/bin/env python3
"""Check that AGENTS.md stays within its word budget.

AGENTS.md loads into every agent session, so its size is a cost paid on every
task. Words are whitespace-separated tokens, code blocks included.

Usage: check_agents_budget.py [--file AGENTS.md] [--max-words 600]
Exits 1 when the file is over budget.
"""
import argparse
import os
import sys


def count_words(path):
    with open(path, encoding="utf-8") as handle:
        return len(handle.read().split())


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check the AGENTS.md word budget.")
    parser.add_argument("--file", default="AGENTS.md")
    parser.add_argument("--max-words", type=int, default=600)
    args = parser.parse_args(argv)
    if not os.path.isfile(args.file):
        print(f"check_agents_budget: {args.file} not found")
        return 1
    words = count_words(args.file)
    print(f"check_agents_budget: {args.file} has {words} words (budget {args.max_words})")
    if words > args.max_words:
        print("Move detail to the file that owns it and leave a link, or condense. Raise the budget only with a reason in the PR.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
