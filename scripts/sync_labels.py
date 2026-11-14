#!/usr/bin/env python3
"""Create or update the standard DAH Labs labels in a repository (rule GH-007).

The labels are defined in templates/github/labels.json. The script never deletes a label: old
labels stay until a maintainer removes them by hand (they may be used by open issues).

Requirements: Python 3.12+ and the GitHub CLI (`gh`), authenticated with write access to the
repository.

Usage:
    python scripts/sync_labels.py DAH-Projects-and-Innovations/baraza
    python scripts/sync_labels.py DAH-Projects-and-Innovations/baraza --dry-run
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

LABELS_FILE = Path(__file__).resolve().parent.parent / "templates" / "github" / "labels.json"


def load_labels(path: Path) -> list[dict[str, str]]:
    """Read and validate the label definitions."""
    labels = json.loads(path.read_text(encoding="utf-8"))
    for label in labels:
        missing = {"name", "color", "description"} - label.keys()
        if missing:
            message = f"label {label!r} is missing {sorted(missing)}"
            raise ValueError(message)
    return labels


def sync(repository: str, labels: list[dict[str, str]], *, dry_run: bool) -> int:
    """Create or update every label. Return the number of failures."""
    failures = 0
    for label in labels:
        command = [
            "gh",
            "label",
            "create",
            label["name"],
            "--repo",
            repository,
            "--color",
            label["color"],
            "--description",
            label["description"],
            "--force",  # Update the label when it already exists.
        ]
        if dry_run:
            print("would run:", " ".join(command))
            continue
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            print(f"ok      {label['name']}")
        else:
            failures += 1
            print(f"FAILED  {label['name']}: {result.stderr.strip()}", file=sys.stderr)
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Synchronize the standard DAH Labs labels.")
    parser.add_argument(
        "repository", help="owner/name, for example DAH-Projects-and-Innovations/baraza"
    )
    parser.add_argument("--dry-run", action="store_true", help="Print the commands only.")
    parser.add_argument("--labels", type=Path, default=LABELS_FILE, help="Label definition file.")
    args = parser.parse_args(argv)

    labels = load_labels(args.labels)
    failures = sync(args.repository, labels, dry_run=args.dry_run)
    if failures:
        print(f"{failures} label(s) failed.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
