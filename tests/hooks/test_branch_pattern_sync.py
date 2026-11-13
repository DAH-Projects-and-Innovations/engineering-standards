"""The branch pattern is written twice: in the Python hook and in the reusable workflow.

This test fails if the two copies are different.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_workflow_pattern_matches_hook_pattern() -> None:
    workflow = (ROOT / ".github" / "workflows" / "pr-conventions.yml").read_text(encoding="utf-8")
    match = re.search(r"pattern='([^']+)'", workflow)
    assert match is not None, "pattern not found in pr-conventions.yml"
    workflow_pattern = match.group(1)

    hook = (ROOT / "hooks" / "check_branch_name.py").read_text(encoding="utf-8")
    types = re.search(r"BRANCH_TYPES = \(([^)]*)\)", hook)
    assert types is not None
    hook_types = re.findall(r'"([a-z]+)"', types.group(1))

    expected = "^(" + "|".join(hook_types) + ")/([0-9]+-)?[a-z0-9]+(-[a-z0-9]+)*$"
    assert workflow_pattern == expected
