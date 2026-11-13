#!/usr/bin/env python3
"""Generate docs/compliance/rules-matrix.md from the rules written in the documentation.

Rules live in docs/standards/*.md, plus docs/getting-started/first-day.md (ONB-*) and
docs/compliance/levels.md (LVL-*).

Every rule in a standards page uses this exact format:

    ### GIT-001: Use `main` as the only long-lived branch

    **MUST** · Level 1 · Verified by: GitHub ruleset (automatic)

The script also checks that:

* every rule ID is unique;
* every rule has a valid requirement keyword, level and verification method;
* every rule ID prefix belongs to the page it is written in.

Usage:
    python scripts/generate_rules_matrix.py          # rewrite the matrix
    python scripts/generate_rules_matrix.py --check  # fail if the matrix is out of date
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "docs"
STANDARDS_DIR = DOCS_DIR / "standards"
MATRIX_PATH = ROOT / "docs" / "compliance" / "rules-matrix.md"

RULE_HEADING = re.compile(r"^### (?P<id>[A-Z]+-\d{3}): (?P<title>.+)$")
RULE_META = re.compile(
    r"^\*\*(?P<keyword>MUST NOT|MUST|SHOULD NOT|SHOULD|MAY)\*\* · Level (?P<level>[123])"
    r" · Verified by: (?P<verification>.+)$"
)
LEVEL_NAMES = {"1": "1 · Foundation", "2": "2 · Standard", "3": "3 · Excellence"}

# Page order in the matrix (paths relative to docs/), and the rule prefixes each page defines.
PAGES: dict[str, tuple[str, ...]] = {
    "standards/git-branching.md": ("GIT",),
    "standards/commits.md": ("COM",),
    "standards/pull-requests.md": ("PR",),
    "standards/code-review.md": ("REV",),
    "standards/releases.md": ("REL",),
    "standards/python.md": ("PY",),
    "standards/javascript.md": ("JS",),
    "standards/architecture.md": ("ARCH",),
    "standards/clean-code.md": ("CC",),
    "standards/testing.md": ("TEST",),
    "standards/repository-structure.md": ("REPO",),
    "standards/required-files.md": ("FILE",),
    "standards/git-hooks.md": ("HOOK",),
    "standards/ci-cd.md": ("CI",),
    "standards/sonar.md": ("SONAR",),
    "standards/security.md": ("SEC",),
    "standards/github-settings.md": ("GH",),
    "standards/ml-research.md": ("ML",),
    "standards/documentation.md": ("DOC",),
    "getting-started/first-day.md": ("ONB",),
    "compliance/levels.md": ("LVL",),
}


@dataclass(frozen=True)
class Rule:
    rule_id: str
    title: str
    keyword: str
    level: str
    verification: str
    page: str


def parse_page(path: Path) -> tuple[list[Rule], list[str]]:
    """Return the rules found in ``path`` and the errors detected."""
    rules: list[Rule] = []
    errors: list[str] = []
    page_key = path.relative_to(DOCS_DIR).as_posix() if path.is_relative_to(DOCS_DIR) else path.name
    allowed_prefixes = PAGES.get(page_key, PAGES.get(f"standards/{path.name}", ()))
    lines = path.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines):
        heading = RULE_HEADING.match(line)
        if not heading:
            continue
        rule_id = heading["id"]
        location = f"{path.relative_to(ROOT)}:{index + 1}"
        if rule_id.split("-")[0] not in allowed_prefixes:
            errors.append(f"{location}: {rule_id} does not belong in {path.name}")
        meta_line = next((candidate for candidate in lines[index + 1 :] if candidate.strip()), "")
        meta = RULE_META.match(meta_line)
        if not meta:
            errors.append(
                f"{location}: {rule_id} must be followed by a line like "
                "'**MUST** · Level 1 · Verified by: ...'"
            )
            continue
        rules.append(
            Rule(
                rule_id=rule_id,
                title=heading["title"].strip(),
                keyword=meta["keyword"],
                level=meta["level"],
                verification=meta["verification"].strip(),
                page=page_key,
            )
        )
    return rules, errors


def collect() -> tuple[list[Rule], list[str]]:
    rules: list[Rule] = []
    errors: list[str] = []
    for page in PAGES:
        path = DOCS_DIR / page
        if path.exists():
            page_rules, page_errors = parse_page(path)
            rules.extend(page_rules)
            errors.extend(page_errors)
    for path in sorted(STANDARDS_DIR.glob("*.md")):
        if f"standards/{path.name}" not in PAGES:
            errors.append(f"{path.relative_to(ROOT)}: page is not listed in PAGES")
    seen: set[str] = set()
    for rule in rules:
        if rule.rule_id in seen:
            errors.append(f"duplicate rule ID {rule.rule_id}")
        seen.add(rule.rule_id)
    return rules, errors


def escape(text: str) -> str:
    return text.replace("|", "\\|")


def render(rules: list[Rule]) -> str:
    def count(level: str, keywords: tuple[str, ...]) -> int:
        return sum(1 for rule in rules if rule.level == level and rule.keyword in keywords)

    mandatory = ("MUST", "MUST NOT")
    recommended = ("SHOULD", "SHOULD NOT")
    out = [
        "<!-- GENERATED FILE: do not edit by hand. -->",
        "<!-- Run `python scripts/generate_rules_matrix.py` to update it. -->",
        "",
        "# Rules matrix",
        "",
        "## TL;DR",
        "",
        "- This page lists every rule of the DAH Labs engineering standards in one table.",
        "- It is generated from the standards pages, so it is always up to date.",
        "- Use it to audit a repository: filter by level, then check each rule.",
        "- Levels are explained in [Compliance levels](levels.md).",
        "",
        "## Summary",
        "",
        "| Level | MUST / MUST NOT | SHOULD / SHOULD NOT | MAY | Total |",
        "|---|---|---|---|---|",
    ]
    for level, name in LEVEL_NAMES.items():
        row = [count(level, mandatory), count(level, recommended), count(level, ("MAY",))]
        out.append(f"| {name} | {row[0]} | {row[1]} | {row[2]} | {sum(row)} |")
    out += [
        f"| **All levels** | | | | **{len(rules)}** |",
        "",
        "Many Level 1 rules are checked by tools that the templates already configure: copying the",
        "templates and the reusable workflows makes most of them compliant at once.",
        "",
        "## All rules",
        "",
    ]
    out += [
        "| ID | Rule | Requirement | Level | Verified by |",
        "|---|---|---|---|---|",
    ]
    for rule in rules:
        # Same algorithm as GitHub: lower case, drop punctuation, spaces become hyphens.
        anchor = re.sub(r"[^a-z0-9 _-]", "", f"{rule.rule_id}: {rule.title}".lower())
        anchor = anchor.replace(" ", "-")
        link = f"[{rule.rule_id}](../{rule.page}#{anchor})"
        out.append(
            f"| {link} | {escape(rule.title)} | {rule.keyword} | {rule.level} "
            f"| {escape(rule.verification)} |"
        )
    out += [
        "",
        "## Checklist",
        "",
        "- [ ] I filtered the rules of the level my repository targets.",
        "- [ ] I recorded each rule as compliant, not compliant or not applicable.",
        "- [ ] I opened one issue per non-compliant rule (see the "
        "[migration playbook](../migration/playbook.md)).",
        "",
        "---",
        "",
        "*Generated from the rules in `docs/`. Last verified: see the footer of each page.*",
        "",
    ]
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate the rules matrix.")
    parser.add_argument("--check", action="store_true", help="Fail if the matrix is outdated.")
    args = parser.parse_args(argv)

    rules, errors = collect()
    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    if errors:
        return 1

    content = render(rules)
    current = MATRIX_PATH.read_text(encoding="utf-8") if MATRIX_PATH.exists() else ""
    if content == current:
        return 0
    if args.check:
        print(f"{MATRIX_PATH.relative_to(ROOT)} is out of date. Run:", file=sys.stderr)
        print("  python scripts/generate_rules_matrix.py", file=sys.stderr)
        return 1
    MATRIX_PATH.write_text(content, encoding="utf-8")
    print(f"Updated {MATRIX_PATH.relative_to(ROOT)} ({len(rules)} rules).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
