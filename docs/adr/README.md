# Architecture Decision Records

## TL;DR

- This folder records the structuring decisions of the DAH Labs engineering standards, in the [MADR 4.0](https://adr.github.io/madr/) format.
- One file per decision: `NNNN-short-title.md`. Numbers are never reused.
- A decision is changed by a **new** ADR that supersedes the old one, never by rewriting history.
- Start from [`0000-template.md`](0000-template.md). Projects use the same template: [`templates/docs/adr.md`](../../templates/docs/adr.md).

## Index

| ADR | Title | Status |
|---|---|---|
| [0001](0001-trunk-based-development.md) | Use trunk-based development with `main` as the only long-lived branch | accepted |
| [0002](0002-squash-merge-only.md) | Merge pull requests with squash merge only | accepted |
| [0003](0003-ruff-for-linting-and-formatting.md) | Use Ruff for Python linting and formatting | accepted |
| [0004](0004-uv-for-python-projects.md) | Use uv for Python versions, environments and dependencies | accepted |
| [0005](0005-pnpm-for-javascript-projects.md) | Use pnpm for JavaScript and TypeScript projects | accepted |
| [0006](0006-mypy-strict-progressive.md) | Use mypy in strict mode, progressively for existing code | proposed |
| [0007](0007-apache-2-0-default-license.md) | Use Apache-2.0 as the default license for code | proposed |
| 0008 | Use SonarQube Cloud for code quality (reserved, next version) | — |
| [0009](0009-central-reusable-workflows.md) | Centralize CI in reusable workflows | accepted |

"Proposed" decisions are applied in these standards but wait for the validation of the DAH Labs team.

## Checklist

- [ ] The new ADR has the next free number and follows the template.
- [ ] Its status is `proposed` until the team accepts it in the PR.
- [ ] The index above is updated.

---

*Last verified: 2026-11-13.*
