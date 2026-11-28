"""Tests of scripts/generate_rules_matrix.py."""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "generate_rules_matrix", ROOT / "scripts" / "generate_rules_matrix.py"
)
assert SPEC is not None
assert SPEC.loader is not None
matrix = importlib.util.module_from_spec(SPEC)
sys.modules["generate_rules_matrix"] = matrix
SPEC.loader.exec_module(matrix)


def write_page(tmp_path: Path, name: str, body: str) -> Path:
    page = tmp_path / name
    page.write_text(body, encoding="utf-8")
    return page


def test_parse_page_reads_rule(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(matrix, "ROOT", tmp_path)
    page = write_page(
        tmp_path,
        "commits.md",
        "### COM-001: Use Conventional Commits\n\n"
        "**MUST** · Level 1 · Verified by: commit-msg hook (automatic)\n",
    )

    rules, errors = matrix.parse_page(page)

    assert errors == []
    assert rules[0].rule_id == "COM-001"
    assert rules[0].keyword == "MUST"
    assert rules[0].level == "1"


def test_parse_page_reports_missing_metadata(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(matrix, "ROOT", tmp_path)
    page = write_page(tmp_path, "commits.md", "### COM-001: Use Conventional Commits\n\nText.\n")

    rules, errors = matrix.parse_page(page)

    assert rules == []
    assert "must be followed by" in errors[0]


def test_parse_page_reports_wrong_prefix(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(matrix, "ROOT", tmp_path)
    page = write_page(
        tmp_path,
        "commits.md",
        "### GIT-001: Wrong page\n\n**MUST** · Level 1 · Verified by: review (manual)\n",
    )

    _, errors = matrix.parse_page(page)

    assert "does not belong" in errors[0]


def test_parse_page_reports_link_in_verification(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(matrix, "ROOT", tmp_path)
    page = write_page(
        tmp_path,
        "commits.md",
        "### COM-001: Use Conventional Commits\n\n"
        "**MUST** · Level 1 · Verified by: see [hooks](git-hooks.md) (automatic)\n",
    )

    _, errors = matrix.parse_page(page)

    assert "must not contain links" in errors[0]


def test_repository_rules_are_valid() -> None:
    _, errors = matrix.collect()

    assert errors == []
