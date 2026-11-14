---
status: accepted
date: 2026-11-13
decision-makers: DAH Labs maintainers
---

# Use trunk-based development with `main` as the only long-lived branch

## Context and problem statement

DAH Labs repositories use different branch models: some have `main` only, some have a `development` integration branch and a `main` release branch. New contributors do not know which branch to start from, changes wait on `development` for weeks, and merges between the two branches create conflicts. Which branch model do all repositories use?

## Decision drivers

- Simple for volunteers with different levels of experience.
- Few merge conflicts in an asynchronous, distributed team.
- Every change reviewed and tested before it reaches users.
- Works with automatic releases (release-please).

## Considered options

1. GitHub Flow / trunk-based development: one `main` branch, short feature branches.
2. Git Flow: `main`, `develop`, `release/*`, `hotfix/*` branches.
3. Two branches: `development` for integration and `main` for releases.

## Decision outcome

Chosen option: **1. GitHub Flow / trunk-based development**, because it is the simplest model that keeps `main` always working, and releases are tags made by release-please, so no release branch is needed.

### Consequences

- Good: one place to start from and to merge into; no merges between long-lived branches.
- Good: short branches mean small PRs, faster reviews and fewer conflicts.
- Bad: `main` must always work, so CI and review must be reliable. Mitigation: required checks in the ruleset.
- Bad: unfinished features must be hidden behind configuration flags or split into small PRs.
- Bad: repositories that use `development` must migrate (see the default branch migration guide). This migration is a team decision for each repository.

### Confirmation

GIT-001 and GIT-002 are checked by the ruleset and by `scripts/audit_repository.py`.

## Pros and cons of the options

### GitHub Flow / trunk-based

- Good: minimal rules; used by most large open source projects and by many research labs.
- Bad: needs discipline on small PRs.

### Git Flow

- Good: explicit support for several maintained versions.
- Bad: complex for newcomers; designed for software with scheduled releases, which DAH Labs projects do not have.

### `development` + `main`

- Good: a "stable" branch for users.
- Bad: tags already give stable versions; the extra branch adds merges and confusion.

## More information

- [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [Trunk Based Development](https://trunkbaseddevelopment.com/)
- Standard: [Git branching](../standards/git-branching.md)
