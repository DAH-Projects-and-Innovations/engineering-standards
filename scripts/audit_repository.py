#!/usr/bin/env python3
"""Audit the automatic part of the DAH Labs Level 1 rules for one repository.

The script is READ-ONLY: it only calls GitHub API endpoints with GET requests through the
GitHub CLI (`gh`). It prints a Markdown table that you can paste into the audit issue.

Some endpoints need admin rights on the repository (rulesets details, security settings).
When a value cannot be read, the result is "unknown" and the check must be done by hand.

Usage:
    python scripts/audit_repository.py DAH-Projects-and-Innovations/baraza
    python scripts/audit_repository.py DAH-Projects-and-Innovations/baraza --root backend

See docs/migration/audit-checklist.md for the manual part of the audit.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

OK = "✅"
KO = "❌"
UNKNOWN = "❔"

REQUIRED_FILES = {
    "FILE-001": ["README.md"],
    "FILE-002": ["LICENSE", "LICENSE.md", "LICENSE.txt"],
    "FILE-004": ["CONTRIBUTING.md", ".github/CONTRIBUTING.md", "docs/CONTRIBUTING.md"],
    "FILE-005": ["CODE_OF_CONDUCT.md", ".github/CODE_OF_CONDUCT.md", "docs/CODE_OF_CONDUCT.md"],
    "FILE-006": ["SECURITY.md", ".github/SECURITY.md", "docs/SECURITY.md"],
    "FILE-007": ["CHANGELOG.md"],
    "FILE-008": [".github/CODEOWNERS", "CODEOWNERS", "docs/CODEOWNERS"],
    "FILE-009": [".github/pull_request_template.md", ".github/PULL_REQUEST_TEMPLATE.md"],
    "FILE-010": [".github/ISSUE_TEMPLATE/config.yml"],
    "FILE-011": [".github/dependabot.yml"],
    "FILE-012": [".editorconfig"],
    "FILE-013": [".gitignore"],
    "FILE-014": [".gitattributes"],
    "FILE-016": [".pre-commit-config.yaml"],
}

# Files of Level 2 repositories. Reported with "(Level 2)" so that a Level 1 audit can ignore them.
LEVEL_2_FILES = [
    ("SONAR-003", "sonar-project.properties"),
    ("REL-004", "release-please-config.json"),
    ("REL-004", ".release-please-manifest.json"),
]


@dataclass(frozen=True)
class Finding:
    rule: str
    check: str
    status: str
    detail: str


def gh_api(path: str) -> Any | None:
    """Return the JSON answer of a GET request, or None when it fails."""
    result = subprocess.run(
        ["gh", "api", "--method", "GET", path],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def status(condition: bool | None) -> str:
    if condition is None:
        return UNKNOWN
    return OK if condition else KO


def check_repository(repo: dict[str, Any]) -> list[Finding]:
    security = repo.get("security_and_analysis") or {}

    def enabled(name: str) -> bool | None:
        value = (security.get(name) or {}).get("status")
        return None if value is None else value == "enabled"

    default_branch = repo.get("default_branch")
    merge_ok = (
        repo.get("allow_squash_merge") is True
        and repo.get("allow_merge_commit") is False
        and repo.get("allow_rebase_merge") is False
    )
    topics = repo.get("topics") or []
    return [
        Finding(
            "GIT-001",
            "Default branch is main",
            status(default_branch == "main"),
            f"default branch: {default_branch}",
        ),
        Finding(
            "GH-001",
            "Description is set",
            status(bool(repo.get("description"))),
            repo.get("description") or "empty",
        ),
        Finding(
            "GH-001",
            "Topic dah-labs is set",
            status("dah-labs" in topics),
            ", ".join(topics) or "no topics",
        ),
        Finding(
            "GH-004",
            "Squash merge only",
            status(merge_ok),
            f"squash={repo.get('allow_squash_merge')}, merge={repo.get('allow_merge_commit')}, "
            f"rebase={repo.get('allow_rebase_merge')}",
        ),
        Finding(
            "GH-004",
            "Squash message is PR title and description",
            status(
                repo.get("squash_merge_commit_title") == "PR_TITLE"
                and repo.get("squash_merge_commit_message") == "PR_BODY"
            ),
            f"{repo.get('squash_merge_commit_title')} / {repo.get('squash_merge_commit_message')}",
        ),
        Finding(
            "GH-005",
            "Merged branches are deleted",
            status(repo.get("delete_branch_on_merge")),
            str(repo.get("delete_branch_on_merge")),
        ),
        Finding(
            "GH-006",
            "Wiki is disabled",
            status(repo.get("has_wiki") is False),
            f"has_wiki={repo.get('has_wiki')}",
        ),
        Finding(
            "SEC-001",
            "Dependabot security updates",
            status(enabled("dependabot_security_updates")),
            "needs admin rights to read" if not security else "",
        ),
        Finding("SEC-003", "Secret scanning", status(enabled("secret_scanning")), ""),
        Finding(
            "SEC-003", "Push protection", status(enabled("secret_scanning_push_protection")), ""
        ),
        Finding(
            "FILE-002",
            "License recognized by GitHub",
            status(repo.get("license") is not None),
            (repo.get("license") or {}).get("spdx_id", "none"),
        ),
    ]


def check_private_reporting(full_name: str) -> Finding:
    answer = gh_api(f"repos/{full_name}/private-vulnerability-reporting")
    value = None if answer is None else answer.get("enabled")
    return Finding("SEC-008", "Private vulnerability reporting", status(value), "")


def check_rulesets(full_name: str, default_branch: str) -> list[Finding]:
    rulesets = gh_api(f"repos/{full_name}/rulesets?includes_parents=true")
    if rulesets is None:
        return [Finding("GH-002", "Ruleset on main", UNKNOWN, "cannot read rulesets")]
    active = [
        r for r in rulesets if r.get("enforcement") == "active" and r.get("target") == "branch"
    ]
    if not active:
        return [Finding("GH-002", "Active ruleset on main", KO, "no active branch ruleset")]

    findings: list[Finding] = []
    rule_types: set[str] = set()
    pull_request: dict[str, Any] = {}
    bypass_always = False
    for summary in active:
        detail = gh_api(f"repos/{full_name}/rulesets/{summary['id']}") or {}
        include = ((detail.get("conditions") or {}).get("ref_name") or {}).get("include", [])
        targets_main = any(
            ref in {"~DEFAULT_BRANCH", "~ALL", f"refs/heads/{default_branch}"} for ref in include
        )
        if not targets_main:
            continue
        for rule in detail.get("rules", []):
            rule_types.add(rule["type"])
            if rule["type"] == "pull_request":
                pull_request = rule.get("parameters", {})
        bypass_always |= any(
            a.get("bypass_mode") == "always" for a in detail.get("bypass_actors", [])
        )

    findings.append(
        Finding("GH-002", "Ruleset targets the default branch", status(bool(rule_types)), "")
    )
    expected = {
        "deletion": "Restrict deletions",
        "non_fast_forward": "Block force pushes",
        "required_linear_history": "Require linear history",
        "pull_request": "Require a pull request",
        "required_status_checks": "Require status checks",
    }
    for rule_type, label in expected.items():
        findings.append(Finding("GH-002", label, status(rule_type in rule_types), ""))
    checks: list[tuple[str, str, Callable[[dict[str, Any]], bool]]] = [
        (
            "PR-006",
            "At least 1 approval",
            lambda p: p.get("required_approving_review_count", 0) >= 1,
        ),
        ("PR-006", "Code owner review", lambda p: p.get("require_code_owner_review") is True),
        (
            "PR-009",
            "Conversations resolved",
            lambda p: p.get("required_review_thread_resolution") is True,
        ),
        (
            "PR-010",
            "Stale approvals dismissed",
            lambda p: p.get("dismiss_stale_reviews_on_push") is True,
        ),
        (
            "COM-007",
            "Squash is the only merge method",
            lambda p: p.get("allowed_merge_methods") == ["squash"],
        ),
    ]
    for rule_id, label, predicate in checks:
        findings.append(
            Finding(rule_id, label, status(predicate(pull_request) if pull_request else False), "")
        )
    findings.append(Finding("GH-003", "No bypass in mode 'always'", status(not bypass_always), ""))
    return findings


def check_files(full_name: str, root: str) -> list[Finding]:
    tree = gh_api(f"repos/{full_name}/git/trees/HEAD?recursive=1")
    if tree is None:
        return [Finding("FILE-*", "Required files", UNKNOWN, "cannot read the file tree")]
    paths = {item["path"] for item in tree.get("tree", [])}
    findings = []
    for rule_id, candidates in REQUIRED_FILES.items():
        found = next((c for c in candidates if c in paths), None)
        findings.append(
            Finding(
                rule_id, f"{candidates[0]} exists", status(found is not None), found or "missing"
            )
        )
    for rule_id, path in LEVEL_2_FILES:
        present = path in paths
        findings.append(
            Finding(
                rule_id, f"(Level 2) {path} exists", status(present), "" if present else "missing"
            )
        )
    prefix = f"{root.strip('/')}/" if root else ""
    findings.append(
        Finding("PY-002", "uv.lock is committed", status(f"{prefix}uv.lock" in paths), "")
    )
    lock_files = sorted(p for p in paths if p.endswith(("package-lock.json", "yarn.lock")))
    findings.append(
        Finding("JS-002", "No npm or yarn lock file", status(not lock_files), ", ".join(lock_files))
    )
    tests_in_src = sorted({p.split("/tests/")[0] for p in paths if "/src/" in p and "/tests/" in p})
    findings.append(
        Finding("PY-012", "No tests inside src/", status(not tests_in_src), ", ".join(tests_in_src))
    )
    heavy = sorted(
        p for p in paths if p.endswith((".pt", ".h5", ".safetensors", ".ckpt", ".onnx", ".pkl"))
    )
    findings.append(
        Finding("REPO-006", "No model or data files", status(not heavy), ", ".join(heavy[:5]))
    )
    return findings


def check_branches(full_name: str) -> Finding:
    branches = gh_api(f"repos/{full_name}/branches?per_page=100") or []
    long_lived = sorted(
        b["name"] for b in branches if b["name"] in {"develop", "development", "dev", "staging"}
    )
    return Finding(
        "GIT-001", "No other long-lived branch", status(not long_lived), ", ".join(long_lived)
    )


def render(full_name: str, findings: list[Finding]) -> str:
    passed = sum(f.status == OK for f in findings)
    lines = [
        f"## Automatic audit of `{full_name}`",
        "",
        f"{passed}/{len(findings)} automatic checks pass. {UNKNOWN} = check by hand.",
        "",
        "| Rule | Check | Status | Detail |",
        "|---|---|---|---|",
    ]
    lines += [
        f"| {f.rule} | {f.check} | {f.status} | {f.detail.replace('|', '/')} |" for f in findings
    ]
    lines += ["", "The manual part is in docs/migration/audit-checklist.md."]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Read-only audit of DAH Labs Level 1 rules (and Level 2 files)."
    )
    parser.add_argument(
        "repository", help="owner/name, for example DAH-Projects-and-Innovations/baraza"
    )
    parser.add_argument(
        "--root", default="backend", help="Folder of the Python project (default: backend)."
    )
    args = parser.parse_args(argv)

    repo = gh_api(f"repos/{args.repository}")
    if repo is None:
        print(f"Cannot read {args.repository}. Is `gh` authenticated?", file=sys.stderr)
        return 2

    findings = check_repository(repo)
    findings.append(check_private_reporting(args.repository))
    findings.extend(check_rulesets(args.repository, repo.get("default_branch", "main")))
    findings.append(check_branches(args.repository))
    findings.extend(check_files(args.repository, args.root))
    print(render(args.repository, findings))
    return 0


if __name__ == "__main__":
    sys.exit(main())
