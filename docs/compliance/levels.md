# Compliance levels

## TL;DR

- Every rule belongs to one of three levels: **1 · Foundation**, **2 · Standard**, **3 · Excellence**.
- **Level 1** is mandatory for every active repository and takes about one week of work.
- **Level 2** is mandatory for flagship projects (the projects that DAH Labs presents publicly).
- **Level 3** is recommended. It is what world-class labs do.
- Each repository shows its level with a badge in its README and checks it with a quarterly audit.

## The three levels

| | Level 1 · Foundation | Level 2 · Standard | Level 3 · Excellence |
|---|---|---|---|
| **For** | Every active repository | Flagship projects | Recommended for all |
| **Effort** | About 1 week | A few weeks, PR by PR | Continuous |
| **Main content** | Required files, protected `main`, Conventional Commits, Ruff, pre-commit, CI with lint and tests, Dependabot, secret scanning | mypy, coverage threshold, SonarQube Cloud and quality gate, release-please, layered architecture checked by import-linter, ADRs, CodeQL, dependency review | Full mypy strict, total coverage ≥ 80 %, OpenSSF Scorecard, signed commits, complete model and dataset cards, documentation on GitHub Pages, Playwright tests |

A requirement keyword (MUST, SHOULD, MAY) applies **within its level**. For example, a "MUST · Level 2" rule is mandatory for a repository that targets Level 2, and does not apply to a repository that targets Level 1.

The keywords follow [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119):

| Keyword | Meaning |
|---|---|
| **MUST** / **MUST NOT** | Mandatory. No exception without an ADR. |
| **SHOULD** / **SHOULD NOT** | Strongly recommended. A repository that does not follow the rule writes why (in the README, an ADR or the audit issue). |
| **MAY** | Optional. |

The full list of rules, with their level and how they are checked, is the [rules matrix](rules-matrix.md).

## Rules

### LVL-001: Every active repository reaches Level 1

**MUST** · Level 1 · Verified by: quarterly compliance audit (manual)

A repository is **active** when it received a commit in the last 6 months or is used by a DAH Labs project. Inactive repositories are **archived** on GitHub (Settings → Danger Zone → Archive), with a note in the README.

A new repository reaches Level 1 before its first release. An existing repository follows the [migration playbook](../migration/playbook.md).

### LVL-002: Flagship projects reach Level 2

**MUST** · Level 2 · Verified by: quarterly compliance audit (manual)

The list of flagship projects is decided by the DAH Labs team and written in the [README](../../README.md#flagship-projects) of this repository.

### LVL-003: The README shows the compliance level with a badge

**MUST** · Level 1 · Verified by: README review (manual)

Copy the badge of the level that the repository **really** reaches (not the target):

```markdown
[![DAH Labs standards: Level 1](https://img.shields.io/badge/DAH%20Labs%20standards-Level%201%20Foundation-cd7f32)](https://github.com/DAH-Projects-and-Innovations/engineering-standards/blob/main/docs/compliance/levels.md)

[![DAH Labs standards: Level 2](https://img.shields.io/badge/DAH%20Labs%20standards-Level%202%20Standard-c0c0c0)](https://github.com/DAH-Projects-and-Innovations/engineering-standards/blob/main/docs/compliance/levels.md)

[![DAH Labs standards: Level 3](https://img.shields.io/badge/DAH%20Labs%20standards-Level%203%20Excellence-ffd700)](https://github.com/DAH-Projects-and-Innovations/engineering-standards/blob/main/docs/compliance/levels.md)
```

They look like this:

[![DAH Labs standards: Level 1](https://img.shields.io/badge/DAH%20Labs%20standards-Level%201%20Foundation-cd7f32)](levels.md)
[![DAH Labs standards: Level 2](https://img.shields.io/badge/DAH%20Labs%20standards-Level%202%20Standard-c0c0c0)](levels.md)
[![DAH Labs standards: Level 3](https://img.shields.io/badge/DAH%20Labs%20standards-Level%203%20Excellence-ffd700)](levels.md)

The badges are static images from [shields.io](https://shields.io/), a free service. They do not check anything: the audit does.

### LVL-004: Each repository is audited once per quarter

**SHOULD** · Level 1 · Verified by: an issue labeled `compliance-audit` exists for the current quarter (manual)

Open an issue with the **Compliance audit** form ([`audit.yml`](../../templates/github/ISSUE_TEMPLATE/audit.yml)) and follow the [audit checklist](../migration/audit-checklist.md). Write security weaknesses in a private security advisory, not in the issue.

### LVL-005: A repository records the version of the standards it follows

**SHOULD** · Level 1 · Verified by: audit issue (manual)

The standards are versioned (`v1.0.0`, `v1.1.0`…). The audit issue says which version was used. A new **minor** version of the standards may add SHOULD rules and new Level 3 rules; a new **major** version may add MUST rules at Level 1 or 2, and comes with a migration note.

## How to claim a level

1. Run the audit for the target level.
2. Every MUST rule of the level (and of the levels below) is compliant, or has an ADR that explains the exception.
3. Every SHOULD rule is compliant or has a written reason.
4. Update the badge in the README in the same PR as the last fix.

## Checklist

- [ ] The repository knows its target level (1 for all, 2 for flagship projects).
- [ ] The README badge shows the level actually reached.
- [ ] An audit issue exists for the current quarter, with the version of the standards.
- [ ] Every exception to a MUST rule has an ADR.

---

*Last verified: 2026-11-13.*
