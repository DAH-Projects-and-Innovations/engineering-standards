# SonarQube Cloud

## TL;DR

- Level 2 repositories are analyzed by **SonarQube Cloud**, in the DAH Labs organization, on every pull request and every push to `main`.
- The analysis runs **in CI** with the [`sonar.yml`](../../.github/workflows/sonar.yml) reusable workflow, after the test jobs, so that it imports the **coverage** reports. Automatic analysis is turned off.
- The quality gate is the built-in **Sonar way** gate. It checks **new code** only: old code does not block a PR, but new code must be clean ("clean as you code").
- The gate is a **required check**: a PR with a failed gate is not merged.
- `SONAR_TOKEN` is an organization secret. Pull requests from forks are analyzed after the merge, on `main`.

Decision: [ADR 0008](../adr/0008-sonarqube-cloud-for-code-quality.md).

## What the quality gate checks

The built-in Sonar way gate fails when the **new code** of a pull request (or of `main` since the start of the new code period) has:

| Condition | Threshold |
|---|---|
| Coverage | less than 80 % |
| Duplicated lines | more than 3 % |
| Reliability, security or maintainability rating | worse than A |
| Security hotspots | not all reviewed |

Coverage and duplication conditions are ignored when the change has fewer than 20 new lines. Checked on 2026-11-14 in the [SonarQube Cloud documentation on quality gates](https://docs.sonarsource.com/sonarqube-cloud/improving/quality-gates/).

## Plans and limits

Checked on 2026-11-14 in [SonarQube Cloud subscription plans](https://docs.sonarsource.com/sonarqube-cloud/administering-sonarcloud/managing-subscription/subscription-plans/):

| | Free | OSS |
|---|---|---|
| Public projects | Unlimited | Unlimited |
| Private projects | Up to 50k lines of code | Not allowed |
| Organization members | 5 | ⚠️ To verify |
| Branches | `main` only; PRs that target `main` | All branches and PRs |
| Custom quality gates and profiles | No | Yes |

DAH Labs uses the built-in gate and profile, and only short branches that target `main` ([GIT-001](git-branching.md#git-001-main-is-the-only-long-lived-branch-and-the-default-branch)), so the **Free** plan is enough. The "members" are the people who administer SonarQube Cloud, not the contributors: contributors only see the results in their PRs.

> ⚠️ To verify: how an organization moves to the OSS plan (eligibility, application) and whether it brings anything that DAH Labs needs.

## Set up SonarQube Cloud (once for the organization)

An owner of the GitHub organization does this:

1. Sign in to [SonarQube Cloud](https://sonarcloud.io) with GitHub.
2. **+ → Create new organization → Import from a DevOps platform → GitHub**. Install the **SonarQube Cloud** GitHub App on the organization. Give it access to the Level 2 repositories only (or to all repositories).
3. Choose the **Free** plan. The organization key is `dah-projects-and-innovations`.
4. In **Administration → New code** of the organization, keep the default: **number of days, 30** ([SONAR-007](#sonar-007-the-new-code-period-is-30-days)).
5. Create an analysis token (**My account → Security**). Store it as the **organization** secret `SONAR_TOKEN` in GitHub (**Settings → Secrets and variables → Actions**), available to the Level 2 repositories.

> ⚠️ To verify: whether scoped organization tokens are available on the Free plan. If not, the token belongs to a maintainer's personal account: name it `github-actions-dah`, set an expiry date, and rotate it when the person leaves the maintainers team.

## Add a repository (for each Level 2 repository)

1. In SonarQube Cloud: **+ → Analyze new project**, choose the repository.
2. In the project, **Administration → Analysis Method**: turn **off** Automatic Analysis ([SONAR-002](#sonar-002-analysis-runs-in-ci-with-the-reusable-workflow-and-automatic-analysis-is-off)).
3. Copy [`templates/sonar/sonar-project.properties`](../../templates/sonar/sonar-project.properties) to the root of the repository and fill the TODO markers ([SONAR-003](#sonar-003-sonar-projectproperties-describes-the-scope-of-the-analysis)).
4. Add the `sonar` job to `.github/workflows/ci.yml` (it is in the [CI template](../../templates/github/workflows/ci.yml)):

   ```yaml
   sonar:
     name: sonar
     needs: [backend, frontend]
     uses: DAH-Projects-and-Innovations/engineering-standards/.github/workflows/sonar.yml@v1
     with:
       python-working-directory: backend
       node-working-directory: frontend
     secrets:
       SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
   ```

5. Open a PR. When the analysis appears in the PR, add the check **`sonar / SonarQube Cloud analysis`** to the required status checks of the `main` ruleset ([SONAR-004](#sonar-004-the-quality-gate-is-the-built-in-sonar-way-gate-and-blocks-the-merge)).
6. Add the badges to the README ([SONAR-009](#sonar-009-the-readme-shows-the-quality-gate-and-coverage-badges)).

## Rules

### SONAR-001: Level 2 repositories are analyzed by SonarQube Cloud

**MUST** · Level 2 · Verified by: audit checklist (manual)

Every Level 2 repository is a project of the `dah-projects-and-innovations` SonarQube Cloud organization. A repository has **one** project: a full-stack repository lists its folders in `sonar.sources` (for example `backend/src,frontend/src`).

**Why:** one place to see the quality of every flagship project, with the same rules.

### SONAR-002: Analysis runs in CI with the reusable workflow, and automatic analysis is off

**MUST** · Level 2 · Verified by: `sonar` job in `ci.yml` (automatic); project Administration → Analysis Method (manual)

- The `sonar` job calls `sonar.yml@v1` and `needs` the jobs that produce coverage (`python-ci.yml`, `node-ci.yml`).
- Automatic analysis is turned off. SonarQube Cloud does not allow both methods on the same project, and automatic analysis does not import coverage.

**Why:** coverage on new code is the most useful condition of the gate; only CI-based analysis can provide it.

### SONAR-003: `sonar-project.properties` describes the scope of the analysis

**MUST** · Level 2 · Verified by: code review (manual)

- `sonar.sources` lists production code only; `sonar.tests` lists test code. Tests are never counted as sources.
- Generated code, migrations and vendored files are in `sonar.exclusions`.
- `sonar.python.version` matches `requires-python`.
- The organization and project keys are in the file, not in the workflow.

**Examples:**

- ✅ `sonar.sources=backend/src` and `sonar.tests=backend/tests`
- ❌ `sonar.sources=.` (tests, notebooks and configuration are analyzed as production code)

### SONAR-004: The quality gate is the built-in Sonar way gate and blocks the merge

**MUST** · Level 2 · Verified by: GitHub ruleset required check `sonar / SonarQube Cloud analysis` (automatic)

- The project uses the default gate. Projects do not lower its thresholds.
- `sonar.yml` waits for the gate (`sonar.qualitygate.wait=true`), so a failed gate fails the check.
- A failed gate is fixed in the PR. It is never bypassed by an admin.

**Why:** a gate that can be ignored is not a gate. Because it checks only new code, an old repository can pass it from the first day.

### SONAR-005: Coverage reports are imported for every language

**MUST** · Level 2 · Verified by: SonarQube Cloud project overview shows coverage (manual)

- Python: `sonar.python.coverage.reportPaths` points to the `coverage.xml` produced by `python-ci.yml` (Cobertura XML from pytest-cov).
- TypeScript: `sonar.javascript.lcov.reportPaths` points to the `lcov.info` produced by Vitest (`node-ci.yml` input `coverage-path`).
- `sonar.coverage.exclusions` contains only entry points, configuration and generated code, never business logic.

**Examples:**

- ✅ `sonar.coverage.exclusions=frontend/src/main.tsx,**/*.config.ts`
- ❌ `sonar.coverage.exclusions=backend/src/**/services/**` (hides the code that most needs tests)

### SONAR-006: The token is an organization secret; fork PRs are analyzed after the merge

**MUST** · Level 2 · Verified by: `secret scanning` and code review (automatic and manual)

- `SONAR_TOKEN` is passed explicitly to `sonar.yml` (`secrets: SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}`). It never appears in a file.
- GitHub does not give secrets to pull requests from forks. `sonar.yml` then skips the analysis with a notice, and the check passes. The code is analyzed when it reaches `main`.
- Do **not** use `pull_request_target` to get the token in fork PRs ([CI-009](ci-cd.md#ci-009-pull-requests-from-forks-never-get-secrets)).

**Why:** a token given to code from a fork can be stolen by that code.

### SONAR-007: The new code period is 30 days

**SHOULD** · Level 2 · Verified by: SonarQube Cloud organization settings (manual)

Keep the default new code definition (**number of days: 30**) at the organization level. A project does not change it without an ADR.

**Why:** pull requests are always compared with `main`; the period only decides what counts as "new" on the `main` dashboard. The same period everywhere makes projects comparable.

### SONAR-008: Issues are fixed, or closed with a reason

**SHOULD** · Level 2 · Verified by: code review (manual)

- Fix issues in the PR that introduces them.
- Mark an issue **Accepted** or **False positive** only with a comment that explains why, and only by a maintainer.
- Review every security hotspot: **Safe** with a reason, or **Fix**.

**Why:** closing issues without a reason hides problems and makes the measures meaningless.

### SONAR-009: The README shows the quality gate and coverage badges

**SHOULD** · Level 2 · Verified by: README review (manual)

The [README template](../../templates/docs/README.md) contains the badges. Replace `<sonar-project-key>` with the project key.

### SONAR-010: The whole code base meets the gate conditions, not only new code

**SHOULD** · Level 3 · Verified by: SonarQube Cloud project overview, "Overall code" tab (manual)

Overall code has A ratings and at least 80 % coverage (see [PY-018](python.md#py-018-total-coverage-is-at-least-80-)).

## Troubleshooting

| Problem | Solution |
|---|---|
| "Automatic analysis is enabled" error | Turn it off in the project: Administration → Analysis Method. |
| Coverage is 0 % | Check that the test jobs uploaded the artifacts (`upload-coverage`, `coverage-path`) and that the paths in `sonar-project.properties` match the working directories. |
| The check passes but nothing is analyzed | The PR comes from a fork, or `SONAR_TOKEN` is not available to the repository. Look for the notice in the job summary. |
| "Shallow clone detected" warning | Do not change `fetch-depth`: `sonar.yml` already checks out the full history. |

## Checklist

- [ ] The project exists in the `dah-projects-and-innovations` SonarQube Cloud organization; automatic analysis is off.
- [ ] `sonar-project.properties` is at the root with sources, tests, exclusions and coverage paths.
- [ ] The `sonar` job calls `sonar.yml@v1` after the test jobs and passes `SONAR_TOKEN`.
- [ ] `sonar / SonarQube Cloud analysis` is a required check of the `main` ruleset.
- [ ] The quality gate is the built-in Sonar way gate, and it is green on `main`.
- [ ] The README shows the quality gate and coverage badges.

---

*Last verified: 2026-11-14.*
