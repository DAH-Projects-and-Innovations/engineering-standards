---
status: accepted
date: 2026-11-13
decision-makers: DAH Labs maintainers
---

# Centralize CI in reusable workflows of the engineering-standards repository

## Context and problem statement

Each repository writes its own CI. The workflows differ, use different action versions and different security settings, and every improvement must be copied by hand. How do we share CI between repositories without any infrastructure of our own?

## Decision drivers

- No servers and no paid tools.
- One fix improves every repository.
- Projects keep control: they choose when to upgrade.
- Security best practices (pinned actions, minimal permissions) applied everywhere.

## Considered options

1. Reusable workflows (`on: workflow_call`) in this repository, called with a version tag (`@v1`).
2. Workflow templates in the organization `.github` repository (copied once, then diverge).
3. Composite actions in a separate repository.
4. Copy-paste of a reference workflow.

## Decision outcome

Chosen option: **1. Reusable workflows in `engineering-standards`**, versioned with release tags and a moving major tag (`v1`). This repository tests them on fixtures in `tests/fixtures/` before each release.

### Consequences

- Good: a security fix or a new check reaches every project at the next `v1` update.
- Good: project workflows become short and readable.
- Bad: the repository MUST be **public**, because a public repository cannot call a reusable workflow stored in a private repository.
- Bad: GitHub limits nesting (10 levels including the caller) and the number of reusable workflows per file (50). Our design uses only one level.
- Bad: a breaking change in a reusable workflow affects everybody. Mitigation: integration tests on fixtures, Semantic Versioning, and a new major tag for breaking changes.
- Bad: jobs inside a reusable workflow cannot be customized beyond their inputs. Mitigation: projects add their own jobs next to the reusable ones (for example integration tests with services).

### Confirmation

`example-integration.yml` calls every reusable workflow on the fixtures; the audit checks that projects use `@v1` or a SHA.

## More information

- [GitHub Docs: reusing workflow configurations](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations)
- Standard: [CI/CD](../standards/ci-cd.md)
