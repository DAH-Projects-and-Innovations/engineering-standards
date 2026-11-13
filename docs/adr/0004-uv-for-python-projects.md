---
status: accepted
date: 2026-11-13
decision-makers: DAH Labs maintainers
---

# Use uv for Python versions, environments and dependencies

## Context and problem statement

Contributors install Python projects with pip, virtualenv, conda or Poetry. Without a lock file, two people get different versions. Which tool manages Python projects?

## Decision drivers

- Same versions for every contributor and for CI (lock file).
- Simple setup for beginners, on Linux, macOS and WSL.
- Fast installation on slow or expensive internet connections.
- Standard `pyproject.toml` metadata.

## Considered options

1. uv.
2. Poetry.
3. pip + pip-tools + venv.
4. conda / mamba.

## Decision outcome

Chosen option: **1. uv**, with `uv.lock` committed and `uv sync --locked` in CI. DAH Labs repositories already use it.

### Consequences

- Good: one tool installs Python itself, creates the environment and resolves dependencies; `uvx` runs tools such as pre-commit without a global install.
- Good: a global cache makes the second installation almost instant.
- Bad: uv is young and changes quickly. Mitigation: `[tool.uv] required-version` and Dependabot updates.
- Bad: uv is developed by one company (Astral). Mitigation: projects use standard `pyproject.toml` metadata, so moving to another tool stays possible.

### Confirmation

`python-ci.yml` runs `uv sync --locked`; the audit checks that `uv.lock` is committed.

## More information

- [uv documentation](https://docs.astral.sh/uv/)
- Standard: [Python](../standards/python.md)
