---
status: accepted
date: 2026-11-13
decision-makers: DAH Labs maintainers
---

# Merge pull requests with squash merge only

## Context and problem statement

Repositories allow merge commits, squash and sometimes rebase. The history of `main` mixes "Merge pull request #…" commits, work-in-progress commits ("wip", "fix", "misc") and good commits. release-please needs a history of Conventional Commits to compute versions. How are pull requests merged?

## Decision drivers

- A readable, linear history on `main`.
- Reliable input for release-please and the CHANGELOG.
- Contributors should not need advanced Git (interactive rebase) to contribute.

## Considered options

1. Squash merge only.
2. Rebase merge only.
3. Merge commits.
4. All methods allowed.

## Decision outcome

Chosen option: **1. Squash merge only**, with the PR title as commit title and the PR description as commit body. The PR title MUST follow Conventional Commits and is checked in CI.

### Consequences

- Good: one commit per PR on `main`, each one reviewed and tested; easy to revert.
- Good: contributors can make any number of small commits on their branch.
- Good: only the PR title must be perfect, and it can be edited on GitHub at any time.
- Bad: the individual commits of a branch are not kept on `main`. Mitigation: they stay visible in the closed PR.
- Bad: a PR that mixes several topics becomes one big commit. Mitigation: PR-005 (one topic per PR).

### Confirmation

Ruleset `allowed_merge_methods: ["squash"]` and `required_linear_history`; `pr-conventions.yml` checks the title.

## Pros and cons of the options

### Rebase merge

- Good: keeps each commit.
- Bad: every commit of every contributor must be clean and follow Conventional Commits; too demanding for beginners.

### Merge commits

- Good: keeps the exact branch history.
- Bad: non-linear history, noisy "Merge pull request" commits, and release-please reads every commit of the branch.

## More information

- [About merge methods on GitHub](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github)
- Standard: [Commits](../standards/commits.md)
