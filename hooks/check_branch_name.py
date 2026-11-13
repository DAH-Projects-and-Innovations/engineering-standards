#!/usr/bin/env python3
"""Check that a Git branch name follows the DAH Labs convention (rules GIT-002 and GIT-003).

The script uses only the Python standard library, so it runs on Linux, macOS and Windows
without installing anything.

It is used in two places:

* as a ``pre-push`` hook through pre-commit (see ``.pre-commit-hooks.yaml``);
* in CI, with an explicit branch: ``python hooks/check_branch_name.py --branch feat/42-x``.

Exit codes: 0 when the name is valid, 1 when it is not.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

BRANCH_TYPES = (
    "feat",
    "fix",
    "docs",
    "refactor",
    "test",
    "chore",
    "ci",
    "build",
    "perf",
    "hotfix",
    "exp",
)

# <type>/<issue-number>-<short-description> or <type>/<short-description>, in kebab-case.
BRANCH_PATTERN = re.compile(
    r"^(?:" + "|".join(BRANCH_TYPES) + r")/(?:[0-9]+-)?[a-z0-9]+(?:-[a-z0-9]+)*$"
)
MAX_LENGTH = 60

# Branches created by bots on GitHub. They never come from a contributor's machine.
DEFAULT_EXEMPT_PREFIXES = ("dependabot/", "release-please--", "gh-readonly-queue/")
DEFAULT_PROTECTED = ("main",)


def current_branch() -> str:
    """Return the branch being pushed, or the checked-out branch as a fallback."""
    remote_branch = os.environ.get("PRE_COMMIT_REMOTE_BRANCH", "")
    if remote_branch.startswith("refs/heads/"):
        return remote_branch.removeprefix("refs/heads/")
    if remote_branch:
        # Tags and other refs are not branches: nothing to check.
        return ""
    local_branch = os.environ.get("PRE_COMMIT_LOCAL_BRANCH", "")
    if local_branch.startswith("refs/heads/"):
        return local_branch.removeprefix("refs/heads/")
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip()


def check(branch: str, protected: tuple[str, ...], exempt: tuple[str, ...]) -> list[str]:
    """Return the list of problems found in ``branch``. An empty list means valid."""
    if not branch or branch == "HEAD":
        return []
    if branch in protected:
        return [
            f"Direct pushes to '{branch}' are not allowed (rule GIT-002).",
            "Create a branch and open a pull request instead:",
            "  git switch -c feat/42-short-description",
        ]
    if branch.startswith(exempt):
        return []
    problems: list[str] = []
    if not BRANCH_PATTERN.match(branch):
        problems.append(f"Branch name '{branch}' does not follow the convention (rule GIT-003).")
        problems.append("Expected: <type>/<issue-number>-<short-description> in kebab-case.")
        problems.append(f"Allowed types: {', '.join(BRANCH_TYPES)}.")
        problems.append(
            "Examples: feat/42-add-cohere-embedder, fix/57-chunker-overlap, docs/readme"
        )
    if len(branch) > MAX_LENGTH:
        problems.append(f"Branch name is {len(branch)} characters long; maximum is {MAX_LENGTH}.")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--branch", help="Branch name to check (default: current branch).")
    parser.add_argument(
        "--protected",
        action="append",
        help="Protected branch that must not receive direct pushes (repeatable).",
    )
    parser.add_argument(
        "--exempt-prefix",
        action="append",
        help="Branch prefix that is not checked, for bot branches (repeatable).",
    )
    # pre-commit may pass file names; they are not used.
    parser.add_argument("filenames", nargs="*", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)

    branch = args.branch if args.branch is not None else current_branch()
    protected = tuple(args.protected or DEFAULT_PROTECTED)
    exempt = DEFAULT_EXEMPT_PREFIXES + tuple(args.exempt_prefix or ())

    problems = check(branch, protected, exempt)
    for line in problems:
        print(line, file=sys.stderr)
    if problems:
        print("To rename the current branch: git branch -m <new-name>", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
