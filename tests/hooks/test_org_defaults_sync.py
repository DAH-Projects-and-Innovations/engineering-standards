"""The workflow templates of org-defaults/ are exact copies of templates/github/workflows/."""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
COPIES = {
    "org-defaults/workflow-templates/dah-ci.yml": "templates/github/workflows/ci.yml",
    "org-defaults/workflow-templates/dah-release.yml": "templates/github/workflows/release.yml",
}


@pytest.mark.parametrize(("copy", "source"), COPIES.items())
def test_workflow_template_is_identical_to_its_source(copy: str, source: str) -> None:
    assert (ROOT / copy).read_text(encoding="utf-8") == (ROOT / source).read_text(
        encoding="utf-8"
    ), f"Copy {source} to {copy} again."


@pytest.mark.parametrize("copy", COPIES)
def test_workflow_template_has_properties(copy: str) -> None:
    properties = json.loads(
        (ROOT / copy).with_suffix(".properties.json").read_text(encoding="utf-8")
    )

    assert properties["name"].startswith("DAH Labs")
    assert properties["description"]
