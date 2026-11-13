---
status: accepted
date: 2026-11-13
decision-makers: DAH Labs maintainers
---

# Use Ruff for Python linting and formatting

## Context and problem statement

Python projects need a formatter, an import sorter and a linter. The classic stack (black, isort, flake8 with plugins, pyupgrade, pydocstyle, bandit) means six tools, six configurations and six versions to keep in sync. DAH Labs repositories already use Ruff partly. Which tools do we standardize?

## Decision drivers

- One tool, one configuration in `pyproject.toml`.
- Fast enough to run on every commit, even on modest laptops.
- Covers style, bugs, security basics and docstrings.

## Considered options

1. Ruff for lint and format.
2. black + isort + flake8 (+ plugins) + pyupgrade + pydocstyle + bandit.
3. Pylint + black.

## Decision outcome

Chosen option: **1. Ruff**, with `line-length = 100` and the rule set of the DAH Labs template.

### Consequences

- Good: one dependency, one `[tool.ruff]` section, very fast (written in Rust).
- Good: `ruff check --fix` corrects many problems automatically.
- Bad: Ruff does not implement every Pylint check and is not a full replacement for bandit or a type checker. Mitigation: mypy (Level 2), CodeQL (Level 2) and SonarQube Cloud cover the rest.
- Bad: rule codes and defaults can change between Ruff versions. Mitigation: the version is locked in `uv.lock` and updated by Dependabot with CI.

### Confirmation

`ruff check` and `ruff format --check` run in pre-commit and in `python-ci.yml`.

## More information

- [Ruff documentation](https://docs.astral.sh/ruff/)
- Standard: [Python](../standards/python.md)
- Line length 100 was chosen because existing DAH Labs repositories already use it.
