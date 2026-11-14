---
status: proposed
date: 2026-11-13
decision-makers: DAH Labs maintainers
---

# Use mypy in strict mode, progressively for existing code

## Context and problem statement

Some repositories run mypy in strict mode; others have no type checking. Strict mode on an untyped code base produces hundreds of errors and blocks every PR. How do we check types without blocking contributors?

## Decision drivers

- Catch errors before runtime, document interfaces (ports) precisely.
- Never block contributors with errors they did not create.
- Measurable progress.

## Considered options

1. mypy `strict = true` globally, with per-module overrides for untyped code that only decrease.
2. mypy in default (non-strict) mode.
3. No type checking.
4. Another type checker (Pyright, or the newer Rust-based checkers).

## Decision outcome

Chosen option: **1. mypy strict with decreasing overrides**, mandatory at Level 2; full strict without overrides is Level 3.

### Consequences

- Good: new modules are strict from day one; CI is green from the start of the migration.
- Good: the number of overrides is a simple progress indicator.
- Bad: overrides can stay forever. Mitigation: each override has an issue number, and audits count them.

### Confirmation

`python-ci.yml` runs mypy; the audit counts `[[tool.mypy.overrides]]` entries.

## More information

- ⚠️ **Team decision to validate:** the level of strictness (strict for new code at Level 2, full strict at Level 3) is a proposal.
- Pyright and newer type checkers were not chosen because mypy is already used in DAH Labs repositories and has the Pydantic plugin. This choice is reviewed once a year.
- [mypy documentation: strict mode](https://mypy.readthedocs.io/en/stable/command_line.html#cmdoption-mypy-strict)
- Standard: [Python](../standards/python.md#py-009-mypy-runs-in-strict-mode-on-new-code-with-documented-overrides-for-old-code)
