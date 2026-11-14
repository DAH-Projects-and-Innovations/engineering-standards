---
status: accepted
date: 2026-11-14
decision-makers: DAH Labs maintainers
---

# Use SonarQube Cloud for code quality and coverage on new code

## Context and problem statement

Linters (Ruff, ESLint) check each file against rules, but nobody sees the overall quality of a repository: duplicated code, complexity, security hotspots, coverage of the code changed by a pull request. Reviewers cannot check these points by hand in every PR. Which tool gives a measured quality view and blocks pull requests that make the code worse, without any server and without cost?

## Decision drivers

- Zero infrastructure and zero budget.
- Python and TypeScript in the same repository.
- A clear signal in each pull request (pass or fail), not only a dashboard.
- Focus on **new code**: old repositories cannot fix everything at once, but they must not get worse ("clean as you code").
- Public showcase: badges in the README.

## Considered options

1. SonarQube Cloud, with CI-based analysis in GitHub Actions.
2. Codecov or Coveralls for coverage only, plus the linters.
3. Self-hosted SonarQube Community Build.
4. No quality platform; rely on linters and reviews.

## Decision outcome

Chosen option: **1. SonarQube Cloud with CI-based analysis**, run by the `sonar.yml` reusable workflow after the test jobs, so that the coverage reports of `python-ci.yml` and `node-ci.yml` are imported. The quality gate is the built-in **Sonar way** gate (conditions on new code, including 80 % coverage and at most 3 % duplication).

### Consequences

- Good: one quality gate for Python and TypeScript, shown as a check and a comment on each pull request.
- Good: the new code definition lets old repositories adopt it now: only changed code must meet the gate.
- Good: free for public projects. The built-in gate means DAH Labs needs no custom configuration that a plan might not allow.
- Bad: an external SaaS with its own account and its own plan limits. The Free plan limits private code (50k lines), organization members (5) and analyzes only the main branch and pull requests that target it; this fits trunk-based development ([ADR 0001](0001-trunk-based-development.md)).
- Bad: CI-based analysis needs the `SONAR_TOKEN` secret, which GitHub does not give to pull requests from forks. Those PRs are analyzed after the merge on `main`. Mitigation: maintainers check the analysis of `main` and fix regressions in a follow-up PR.
- Bad: automatic analysis must be turned off, because it does not import coverage and cannot run together with CI-based analysis.

### Confirmation

The audit checks that Level 2 repositories have `sonar-project.properties`, a `sonar` job in CI, and a passing quality gate on `main` (badge in the README).

## Pros and cons of the other options

- **Codecov / Coveralls:** good coverage reports, free for open source, but no duplication, complexity or security hotspots. Two tools would be needed.
- **Self-hosted SonarQube:** full control, but needs a server, updates and backups: not possible without infrastructure.
- **Linters only:** no measure of coverage on new code, no global view; quality depends on each reviewer.

## More information

- [SonarQube Cloud: plans](https://docs.sonarsource.com/sonarqube-cloud/administering-sonarcloud/managing-subscription/subscription-plans/)
- [SonarQube Cloud: quality gates](https://docs.sonarsource.com/sonarqube-cloud/improving/quality-gates/)
- [SonarQube Cloud: GitHub Actions](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/ci-based-analysis/github-actions-for-sonarcloud/)
- Standard: [SonarQube Cloud](../standards/sonar.md)
