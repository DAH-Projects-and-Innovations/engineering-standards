"""Tests of hooks/check_branch_name.py."""

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "check_branch_name", ROOT / "hooks" / "check_branch_name.py"
)
assert SPEC is not None
assert SPEC.loader is not None
check_branch_name = importlib.util.module_from_spec(SPEC)
sys.modules["check_branch_name"] = check_branch_name
SPEC.loader.exec_module(check_branch_name)


@pytest.mark.parametrize(
    "branch",
    [
        "feat/42-add-cohere-embedder",
        "fix/57-chunker-overlap",
        "docs/readme",
        "exp/12-african-languages-tokenizer",
        "hotfix/101-cors-origins",
        "dependabot/uv/backend/fastapi-0.161.1",
        "release-please--branches--main",
    ],
)
def test_main_accepts_valid_or_exempt_branch(branch: str) -> None:
    assert check_branch_name.main(["--branch", branch]) == 0


@pytest.mark.parametrize(
    "branch",
    [
        "development",
        "abel",
        "feature/42-add-embedder",
        "feat/42_add_embedder",
        "feat/Add-Embedder",
        "feat/42-",
        "feat/",
        "fix/issue-10-chunker-infinite-loop-when-chunk-overlap-is-greater-than-size",
    ],
)
def test_main_rejects_invalid_branch(branch: str) -> None:
    assert check_branch_name.main(["--branch", branch]) == 1


def test_main_rejects_direct_push_to_main() -> None:
    assert check_branch_name.main(["--branch", "main"]) == 1


def test_main_accepts_custom_protected_branch_list() -> None:
    assert check_branch_name.main(["--branch", "main", "--protected", "trunk"]) == 1


def test_current_branch_ignores_tag_pushes(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PRE_COMMIT_REMOTE_BRANCH", "refs/tags/v1.0.0")

    assert check_branch_name.current_branch() == ""


def test_current_branch_reads_remote_branch(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PRE_COMMIT_REMOTE_BRANCH", "refs/heads/feat/1-x")

    assert check_branch_name.current_branch() == "feat/1-x"
