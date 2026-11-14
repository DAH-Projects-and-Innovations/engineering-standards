<!-- GENERATED FILE: do not edit by hand. -->
<!-- Run `python scripts/generate_rules_matrix.py` to update it. -->

# Rules matrix

## TL;DR

- This page lists every rule of the DAH Labs engineering standards in one table.
- It is generated from the standards pages, so it is always up to date.
- Use it to audit a repository: filter by level, then check each rule.
- Levels are explained in [Compliance levels](levels.md).

## Summary

| Level | MUST / MUST NOT | SHOULD / SHOULD NOT | MAY | Total |
|---|---|---|---|---|
| 1 · Foundation | 101 | 31 | 0 | 132 |
| 2 · Standard | 11 | 11 | 1 | 23 |
| 3 · Excellence | 0 | 4 | 1 | 5 |
| **All levels** | | | | **160** |

Many Level 1 rules are checked by tools that the templates already configure: copying the
templates and the reusable workflows makes most of them compliant at once.

## All rules

| ID | Rule | Requirement | Level | Verified by |
|---|---|---|---|---|
| [GIT-001](../standards/git-branching.md#git-001-main-is-the-only-long-lived-branch-and-the-default-branch) | `main` is the only long-lived branch and the default branch | MUST | 1 | GitHub settings audit (manual, `gh repo view --json defaultBranchRef`) |
| [GIT-002](../standards/git-branching.md#git-002-nobody-pushes-directly-to-main) | Nobody pushes directly to `main` | MUST | 1 | GitHub ruleset on `main` (automatic) and `dah-branch-name` pre-push hook |
| [GIT-003](../standards/git-branching.md#git-003-branch-names-follow-typeissue-number-short-description) | Branch names follow `<type>/<issue-number>-<short-description>` | MUST | 1 | `dah-branch-name` pre-push hook and `pr-conventions.yml` CI check (automatic) |
| [GIT-004](../standards/git-branching.md#git-004-branches-start-from-an-up-to-date-main) | Branches start from an up-to-date `main` | SHOULD | 1 | code review (manual) |
| [GIT-005](../standards/git-branching.md#git-005-branches-are-short-lived) | Branches are short-lived | SHOULD | 1 | monthly review of open branches (manual, `git branch -r --sort=-committerdate`) |
| [GIT-006](../standards/git-branching.md#git-006-exp-branches-are-never-merged-as-they-are) | `exp/` branches are never merged as they are | MUST NOT | 1 | code review (manual) |
| [GIT-007](../standards/git-branching.md#git-007-merged-branches-are-deleted) | Merged branches are deleted | MUST | 1 | repository setting "Automatically delete head branches" (automatic) |
| [GIT-008](../standards/git-branching.md#git-008-shared-branches-are-never-rewritten) | Shared branches are never rewritten | MUST NOT | 1 | code review (manual) |
| [COM-001](../standards/commits.md#com-001-commit-messages-follow-conventional-commits-100) | Commit messages follow Conventional Commits 1.0.0 | MUST | 1 | `conventional-pre-commit` commit-msg hook and PR title check in `pr-conventions.yml` (automatic) |
| [COM-002](../standards/commits.md#com-002-only-the-standard-types-are-used) | Only the standard types are used | MUST | 1 | commit-msg hook and PR title check (automatic) |
| [COM-003](../standards/commits.md#com-003-the-description-is-short-english-imperative-lower-case-without-a-final-period) | The description is short, English, imperative, lower case, without a final period | MUST | 1 | PR title check (`subjectPattern`, automatic) and code review (manual) |
| [COM-004](../standards/commits.md#com-004-the-header-is-at-most-72-characters) | The header is at most 72 characters | MUST | 1 | PR title length check in `pr-conventions.yml` (automatic) |
| [COM-005](../standards/commits.md#com-005-the-body-explains-why) | The body explains why | SHOULD | 1 | code review (manual) |
| [COM-006](../standards/commits.md#com-006-breaking-changes-are-marked) | Breaking changes are marked | MUST | 1 | code review (manual); release-please reads the marker (automatic) |
| [COM-007](../standards/commits.md#com-007-pull-requests-are-squash-merged-and-the-pr-title-follows-com-001-to-com-004) | Pull requests are squash merged and the PR title follows COM-001 to COM-004 | MUST | 1 | ruleset `allowed_merge_methods: [squash]` and `pr-conventions.yml` (automatic) |
| [COM-008](../standards/commits.md#com-008-commits-on-a-branch-are-small-and-meaningful) | Commits on a branch are small and meaningful | SHOULD | 1 | code review (manual) |
| [COM-009](../standards/commits.md#com-009-scopes-come-from-a-list-written-in-contributingmd) | Scopes come from a list written in CONTRIBUTING.md | SHOULD | 1 | code review (manual); `scopes` input of `pr-conventions.yml` (automatic, optional) |
| [COM-010](../standards/commits.md#com-010-commits-are-signed) | Commits are signed | SHOULD | 3 | ruleset rule "Require signed commits" (automatic) |
| [PR-001](../standards/pull-requests.md#pr-001-every-pr-uses-the-template-and-fills-every-section) | Every PR uses the template and fills every section | MUST | 1 | `.github/pull_request_template.md` present (automatic); code review (manual) |
| [PR-002](../standards/pull-requests.md#pr-002-a-pr-is-linked-to-an-issue) | A PR is linked to an issue | SHOULD | 1 | code review (manual) |
| [PR-003](../standards/pull-requests.md#pr-003-a-pr-changes-less-than-400-lines) | A PR changes less than 400 lines | SHOULD | 1 | code review (manual; the line count is shown in the "Files changed" tab) |
| [PR-004](../standards/pull-requests.md#pr-004-a-pr-is-opened-as-a-draft-until-it-is-ready) | A PR is opened as a draft until it is ready | SHOULD | 1 | code review (manual) |
| [PR-005](../standards/pull-requests.md#pr-005-a-pr-has-one-topic) | A PR has one topic | MUST | 1 | code review (manual) |
| [PR-006](../standards/pull-requests.md#pr-006-a-pr-needs-at-least-1-approval-from-a-code-owner) | A PR needs at least 1 approval from a code owner | MUST | 1 | ruleset `required_approving_review_count: 1` and `require_code_owner_review: true` (automatic) |
| [PR-007](../standards/pull-requests.md#pr-007-architecture-security-and-ci-changes-need-2-approvals) | Architecture, security and CI changes need 2 approvals | SHOULD | 2 | code review (manual); CODEOWNERS entries for sensitive paths (automatic) |
| [PR-008](../standards/pull-requests.md#pr-008-ci-is-green-before-merge) | CI is green before merge | MUST | 1 | ruleset required status checks (automatic) |
| [PR-009](../standards/pull-requests.md#pr-009-all-review-conversations-are-resolved-before-merge) | All review conversations are resolved before merge | MUST | 1 | ruleset `required_review_thread_resolution: true` (automatic) |
| [PR-010](../standards/pull-requests.md#pr-010-approvals-are-dismissed-when-new-commits-are-pushed) | Approvals are dismissed when new commits are pushed | MUST | 1 | ruleset `dismiss_stale_reviews_on_push: true` (automatic) |
| [PR-011](../standards/pull-requests.md#pr-011-ui-changes-include-screenshots) | UI changes include screenshots | SHOULD | 1 | code review (manual) |
| [PR-012](../standards/pull-requests.md#pr-012-the-author-keeps-the-pr-moving) | The author keeps the PR moving | SHOULD | 1 | monthly review of open PRs (manual) |
| [REV-001](../standards/code-review.md#rev-001-a-first-review-happens-within-2-working-days) | A first review happens within 2 working days | SHOULD | 1 | monthly review of open PRs (manual) |
| [REV-002](../standards/code-review.md#rev-002-the-reviewer-follows-the-review-order-above) | The reviewer follows the review order above | MUST | 1 | code review (manual) |
| [REV-003](../standards/code-review.md#rev-003-every-comment-has-a-prefix) | Every comment has a prefix | SHOULD | 1 | code review (manual) |
| [REV-004](../standards/code-review.md#rev-004-comments-are-kind-and-about-the-code) | Comments are kind and about the code | MUST | 1 | Code of Conduct (manual) |
| [REV-005](../standards/code-review.md#rev-005-request-changes-is-only-for-blocking-problems) | "Request changes" is only for blocking problems | SHOULD | 1 | code review (manual) |
| [REV-006](../standards/code-review.md#rev-006-the-person-who-opens-a-conversation-resolves-it) | The person who opens a conversation resolves it | SHOULD | 1 | code review (manual) |
| [REV-007](../standards/code-review.md#rev-007-the-author-understands-every-line-including-ai-generated-code) | The author understands every line, including AI-generated code | MUST | 1 | code review (manual) |
| [REV-008](../standards/code-review.md#rev-008-reviewers-run-the-code-for-non-trivial-changes) | Reviewers run the code for non-trivial changes | MAY | 2 | code review (manual) |
| [PY-001](../standards/python.md#py-001-the-project-supports-python-312-or-newer) | The project supports Python 3.12 or newer | MUST | 1 | `python-version` input of `python-ci.yml` (automatic); code review of `pyproject.toml` (manual) |
| [PY-002](../standards/python.md#py-002-uv-manages-environments-and-dependencies-and-uvlock-is-committed) | uv manages environments and dependencies, and `uv.lock` is committed | MUST | 1 | `uv sync --locked` in `python-ci.yml` fails when the lock file is missing or outdated (automatic) |
| [PY-003](../standards/python.md#py-003-pyprojecttoml-is-the-single-source-of-configuration) | `pyproject.toml` is the single source of configuration | MUST | 1 | code review (manual); audit checklist (manual) |
| [PY-004](../standards/python.md#py-004-ruff-lints-and-formats-all-python-code-with-a-line-length-of-100) | Ruff lints and formats all Python code, with a line length of 100 | MUST | 1 | `ruff check` and `ruff format --check` in pre-commit and `python-ci.yml` (automatic) |
| [PY-005](../standards/python.md#py-005-level-1-enables-at-least-the-base-rule-set) | Level 1 enables at least the base rule set | MUST | 1 | code review of `[tool.ruff.lint]` (manual); `ruff check` (automatic) |
| [PY-006](../standards/python.md#py-006-level-2-enables-the-full-dah-labs-rule-set) | Level 2 enables the full DAH Labs rule set | MUST | 2 | code review of `[tool.ruff.lint]` (manual); `ruff check` (automatic) |
| [PY-007](../standards/python.md#py-007-every-noqa-names-the-rule-and-gives-a-reason) | Every `noqa` names the rule and gives a reason | MUST | 1 | Ruff `PGH004` and `RUF100` (automatic); code review (manual) |
| [PY-008](../standards/python.md#py-008-public-functions-methods-and-classes-have-type-annotations) | Public functions, methods and classes have type annotations | MUST | 2 | mypy `strict` (`disallow_untyped_defs`) in `python-ci.yml` (automatic) |
| [PY-009](../standards/python.md#py-009-mypy-runs-in-strict-mode-on-new-code-with-documented-overrides-for-old-code) | mypy runs in strict mode on new code, with documented overrides for old code | MUST | 2 | `mypy` in `python-ci.yml` (automatic); review of `[[tool.mypy.overrides]]` (manual) |
| [PY-010](../standards/python.md#py-010-the-whole-code-base-passes-mypy-strict-without-overrides) | The whole code base passes mypy strict without overrides | SHOULD | 3 | no `[[tool.mypy.overrides]]` that relaxes checks on project modules (manual) |
| [PY-011](../standards/python.md#py-011-public-api-has-google-style-docstrings) | Public API has Google-style docstrings | MUST | 2 | Ruff `D` rules with `convention = "google"` (automatic) |
| [PY-012](../standards/python.md#py-012-tests-live-outside-the-package-in-testsunit-testsintegration-and-testse2e) | Tests live outside the package, in `tests/unit`, `tests/integration` and `tests/e2e` | MUST | 1 | code review (manual); audit checklist (manual) |
| [PY-013](../standards/python.md#py-013-tests-use-pytest-pytest-cov-and-declared-markers) | Tests use pytest, pytest-cov and declared markers | MUST | 1 | `--strict-markers` in `[tool.pytest.ini_options]` (automatic); `python-ci.yml` (automatic) |
| [PY-014](../standards/python.md#py-014-tests-are-named-test_unit_expected_behavior-and-follow-arrange-act-assert) | Tests are named `test_<unit>_<expected_behavior>` and follow Arrange-Act-Assert | SHOULD | 1 | code review (manual) |
| [PY-015](../standards/python.md#py-015-unit-tests-are-fast-deterministic-and-offline) | Unit tests are fast, deterministic and offline | MUST | 1 | CI runs without network secrets (automatic); code review (manual) |
| [PY-016](../standards/python.md#py-016-calls-to-llm-and-embedding-providers-are-mocked-in-ci) | Calls to LLM and embedding providers are mocked in CI | MUST | 1 | CI has no provider API key (automatic); code review (manual) |
| [PY-017](../standards/python.md#py-017-ci-measures-coverage-and-the-global-threshold-never-goes-down) | CI measures coverage and the global threshold never goes down | MUST | 2 | `coverage-fail-under` input of `python-ci.yml` (automatic) |
| [PY-018](../standards/python.md#py-018-total-coverage-is-at-least-80-) | Total coverage is at least 80 % | SHOULD | 3 | `coverage-fail-under: 80` in CI (automatic) |
| [PY-019](../standards/python.md#py-019-code-uses-logging-never-print) | Code uses `logging`, never `print` | MUST | 1 | Ruff `T20` (automatic) |
| [PY-020](../standards/python.md#py-020-logs-contain-no-secrets-and-no-personal-data) | Logs contain no secrets and no personal data | MUST | 1 | code review (manual) |
| [PY-021](../standards/python.md#py-021-configuration-uses-pydantic-settings-environment-variables-and-validation-at-startup) | Configuration uses `pydantic-settings`, environment variables and validation at startup | MUST | 1 | code review (manual) |
| [PY-022](../standards/python.md#py-022-the-code-lives-in-srcpackage_name-and-the-package-has-a-real-name) | The code lives in `src/<package_name>/` and the package has a real name | MUST | 1 | code review (manual) |
| [PY-023](../standards/python.md#py-023-runtime-and-development-dependencies-are-separated) | Runtime and development dependencies are separated | MUST | 1 | code review of `pyproject.toml` (manual) |
| [PY-024](../standards/python.md#py-024-pyprojecttoml-gives-lower-bounds-exact-versions-live-in-uvlock) | `pyproject.toml` gives lower bounds; exact versions live in `uv.lock` | SHOULD | 1 | code review (manual) |
| [PY-025](../standards/python.md#py-025-integration-tests-that-need-services-run-in-their-own-ci-job) | Integration tests that need services run in their own CI job | SHOULD | 2 | CI workflow review (manual) |
| [JS-001](../standards/javascript.md#js-001-new-front-end-code-is-typescript-with-strict-true) | New front-end code is TypeScript with `strict: true` | MUST | 1 | `pnpm run typecheck` (`tsc --noEmit`) in `node-ci.yml` (automatic) |
| [JS-002](../standards/javascript.md#js-002-pnpm-is-the-only-package-manager-and-its-lock-file-is-committed) | pnpm is the only package manager, and its lock file is committed | MUST | 1 | `pnpm install --frozen-lockfile` in `node-ci.yml` (automatic); no `package-lock.json` or `yarn.lock` (manual) |
| [JS-003](../standards/javascript.md#js-003-the-nodejs-version-is-pinned-to-24-lts) | The Node.js version is pinned to 24 LTS | MUST | 1 | `node-version-file: .nvmrc` in `node-ci.yml` (automatic) |
| [JS-004](../standards/javascript.md#js-004-eslint-flat-config-and-prettier-check-every-project) | ESLint (flat config) and Prettier check every project | MUST | 1 | `pnpm run lint` and `pnpm run format:check` in `node-ci.yml` (automatic) |
| [JS-005](../standards/javascript.md#js-005-tests-run-with-pnpm-test-in-ci) | Tests run with `pnpm test` in CI | MUST | 1 | `pnpm run test` in `node-ci.yml` (automatic) |
| [JS-006](../standards/javascript.md#js-006-tests-use-vitest-and-testing-library) | Tests use Vitest and Testing Library | MUST | 2 | `devDependencies` review (manual); `node-ci.yml` (automatic) |
| [JS-007](../standards/javascript.md#js-007-packagejson-defines-the-standard-scripts) | `package.json` defines the standard scripts | MUST | 1 | `node-ci.yml` fails when a script is missing (automatic) |
| [JS-008](../standards/javascript.md#js-008-end-to-end-tests-use-playwright) | End-to-end tests use Playwright | MAY | 3 | CI workflow review (manual) |
| [JS-009](../standards/javascript.md#js-009-the-front-end-bundle-contains-no-secret) | The front-end bundle contains no secret | MUST | 1 | code review (manual); secret scanning (automatic) |
| [JS-010](../standards/javascript.md#js-010-the-folder-structure-follows-the-framework-conventions) | The folder structure follows the framework conventions | SHOULD | 2 | code review (manual) |
| [JS-011](../standards/javascript.md#js-011-no-consolelog-in-application-code) | No `console.log` in application code | MUST | 1 | ESLint `no-console` (automatic) |
| [JS-012](../standards/javascript.md#js-012-type-aware-eslint-rules-are-enabled) | Type-aware ESLint rules are enabled | SHOULD | 2 | `eslint.config.js` review (manual); `pnpm run lint` (automatic) |
| [REPO-001](../standards/repository-structure.md#repo-001-the-root-holds-standard-files-and-one-folder-per-part) | The root holds standard files and one folder per part | MUST | 1 | code review (manual); audit checklist (manual) |
| [REPO-002](../standards/repository-structure.md#repo-002-a-service-repository-follows-the-service-layout) | A service repository follows the service layout | SHOULD | 1 | code review (manual) |
| [REPO-003](../standards/repository-structure.md#repo-003-a-python-library-uses-the-src-layout) | A Python library uses the `src/` layout | MUST | 1 | code review (manual) |
| [REPO-004](../standards/repository-structure.md#repo-004-a-research-or-ml-repository-follows-the-research-layout) | A research or ML repository follows the research layout | SHOULD | 1 | code review (manual) |
| [REPO-005](../standards/repository-structure.md#repo-005-documentation-lives-in-docs-not-in-the-source-package) | Documentation lives in `docs/`, not in the source package | MUST | 1 | code review (manual) |
| [REPO-006](../standards/repository-structure.md#repo-006-generated-files-data-and-models-are-not-committed) | Generated files, data and models are not committed | MUST | 1 | `check-added-large-files` pre-commit hook (automatic); `.gitignore` review (manual) |
| [REPO-007](../standards/repository-structure.md#repo-007-examples-and-notebooks-are-outside-the-package) | Examples and notebooks are outside the package | SHOULD | 1 | code review (manual) |
| [REPO-008](../standards/repository-structure.md#repo-008-new-repository-names-are-lower-case-kebab-case-english-words) | New repository names are lower-case kebab-case English words | MUST | 1 | organization review (manual) |
| [FILE-001](../standards/required-files.md#file-001-readmemd-follows-the-dah-labs-template) | `README.md` follows the DAH Labs template | MUST | 1 | audit checklist (manual) |
| [FILE-002](../standards/required-files.md#file-002-the-repository-has-a-license-file-that-github-recognizes) | The repository has a `LICENSE` file that GitHub recognizes | MUST | 1 | the license appears in the repository sidebar (`gh repo view --json licenseInfo`, automatic) |
| [FILE-003](../standards/required-files.md#file-003-code-is-apache-20-by-default-documentation-and-data-are-cc-by-40-exceptions-are-documented) | Code is Apache-2.0 by default; documentation and data are CC BY 4.0; exceptions are documented | MUST | 1 | `LICENSE` review and `license` field of `pyproject.toml` / `package.json` (manual) |
| [FILE-004](../standards/required-files.md#file-004-contributingmd-lets-a-newcomer-set-up-the-project-in-less-than-10-minutes) | `CONTRIBUTING.md` lets a newcomer set up the project in less than 10 minutes | MUST | 1 | a new contributor follows it once per quarter and times it (manual) |
| [FILE-005](../standards/required-files.md#file-005-code_of_conductmd-is-the-contributor-covenant-30) | `CODE_OF_CONDUCT.md` is the Contributor Covenant 3.0 | MUST | 1 | file present (automatic, GitHub community profile) |
| [FILE-006](../standards/required-files.md#file-006-securitymd-explains-how-to-report-a-vulnerability-privately) | `SECURITY.md` explains how to report a vulnerability privately | MUST | 1 | file present and private vulnerability reporting enabled (automatic) |
| [FILE-007](../standards/required-files.md#file-007-changelogmd-lists-the-notable-changes-of-each-version) | `CHANGELOG.md` lists the notable changes of each version | MUST | 1 | file present (manual) |
| [FILE-008](../standards/required-files.md#file-008-githubcodeowners-names-a-team-never-a-person) | `.github/CODEOWNERS` names a team, never a person | MUST | 1 | CODEOWNERS errors are shown on the file page on GitHub (automatic); review (manual) |
| [FILE-009](../standards/required-files.md#file-009-githubpull_request_templatemd-exists) | `.github/pull_request_template.md` exists | MUST | 1 | file present (automatic) |
| [FILE-010](../standards/required-files.md#file-010-issue-forms-exist-for-bugs-features-and-questions) | Issue forms exist for bugs, features and questions | MUST | 1 | files present (automatic) |
| [FILE-011](../standards/required-files.md#file-011-githubdependabotyml-covers-every-ecosystem-of-the-repository) | `.github/dependabot.yml` covers every ecosystem of the repository | MUST | 1 | Insights → Dependency graph → Dependabot (automatic) |
| [FILE-012](../standards/required-files.md#file-012-editorconfig-sets-the-basic-text-style) | `.editorconfig` sets the basic text style | MUST | 1 | file present (manual) |
| [FILE-013](../standards/required-files.md#file-013-gitignore-covers-python-node-ml-outputs-and-secrets) | `.gitignore` covers Python, Node, ML outputs and secrets | MUST | 1 | file present; `git status` is clean after a build and a test run (manual) |
| [FILE-014](../standards/required-files.md#file-014-gitattributes-normalizes-line-endings) | `.gitattributes` normalizes line endings | MUST | 1 | file present (manual) |
| [FILE-015](../standards/required-files.md#file-015-envexample-lists-every-environment-variable) | `.env.example` lists every environment variable | MUST | 1 | code review (manual) |
| [FILE-016](../standards/required-files.md#file-016-pre-commit-configyaml-exists) | `.pre-commit-config.yaml` exists | MUST | 1 | CI runs `pre-commit run --all-files` (automatic) |
| [FILE-017](../standards/required-files.md#file-017-research-repositories-have-a-citationcff-file) | Research repositories have a `CITATION.cff` file | MUST | 1 | "Cite this repository" button on GitHub (automatic) |
| [FILE-018](../standards/required-files.md#file-018-a-mass-reformat-commit-is-listed-in-git-blame-ignore-revs) | A mass reformat commit is listed in `.git-blame-ignore-revs` | SHOULD | 1 | code review (manual) |
| [FILE-019](../standards/required-files.md#file-019-sonar-projectproperties-configures-the-sonarqube-cloud-analysis) | `sonar-project.properties` configures the SonarQube Cloud analysis | MUST | 2 | Sonar analysis in CI (automatic) |
| [HOOK-001](../standards/git-hooks.md#hook-001-the-repository-uses-pre-commit-with-the-three-hook-stages) | The repository uses pre-commit with the three hook stages | MUST | 1 | `.pre-commit-config.yaml` review (manual); `pre-commit.yml` in CI (automatic) |
| [HOOK-002](../standards/git-hooks.md#hook-002-the-pre-commit-stage-is-fast-and-fixes-what-it-can) | The pre-commit stage is fast and fixes what it can | MUST | 1 | `pre-commit.yml` in CI (automatic) |
| [HOOK-003](../standards/git-hooks.md#hook-003-gitleaks-scans-every-commit-for-secrets) | gitleaks scans every commit for secrets | MUST | 1 | `gitleaks` hook (automatic); `security.yml` scans the history in CI (automatic) |
| [HOOK-004](../standards/git-hooks.md#hook-004-the-commit-msg-stage-checks-conventional-commits) | The commit-msg stage checks Conventional Commits | MUST | 1 | `conventional-pre-commit` hook (automatic) |
| [HOOK-005](../standards/git-hooks.md#hook-005-the-pre-push-stage-checks-the-branch-name-types-and-fast-tests) | The pre-push stage checks the branch name, types and fast tests | SHOULD | 1 | `.pre-commit-config.yaml` review (manual) |
| [HOOK-006](../standards/git-hooks.md#hook-006-hook-versions-are-pinned-and-updated-by-dependabot) | Hook versions are pinned and updated by Dependabot | MUST | 1 | `rev:` values are tags, not branches (manual); Dependabot `pre-commit` ecosystem (automatic) |
| [HOOK-007](../standards/git-hooks.md#hook-007-ci-runs-every-pre-commit-hook-again-on-all-files) | CI runs every pre-commit hook again on all files | MUST | 1 | `pre-commit.yml` reusable workflow is a required check (automatic) |
| [HOOK-008](../standards/git-hooks.md#hook-008-hooks-are-not-skipped-without-a-reason) | Hooks are not skipped without a reason | SHOULD | 1 | CI (automatic) |
| [HOOK-009](../standards/git-hooks.md#hook-009-notebook-outputs-are-stripped-before-commit) | Notebook outputs are stripped before commit | MUST | 1 | `nbstripout` hook (automatic) |
| [HOOK-010](../standards/git-hooks.md#hook-010-dockerfiles-are-checked-by-hadolint) | Dockerfiles are checked by hadolint | SHOULD | 1 | `hadolint` hook (automatic) |
| [CI-001](../standards/ci-cd.md#ci-001-every-repository-has-a-ci-workflow-on-pull-requests-and-on-main) | Every repository has a CI workflow on pull requests and on `main` | MUST | 1 | `.github/workflows/` review (manual); required checks in the ruleset (automatic) |
| [CI-002](../standards/ci-cd.md#ci-002-projects-call-the-dah-labs-reusable-workflows-pinned-to-a-release) | Projects call the DAH Labs reusable workflows, pinned to a release | MUST | 1 | workflow review (manual) |
| [CI-003](../standards/ci-cd.md#ci-003-ci-runs-lint-and-tests-level-1-plus-type-check-and-coverage-level-2) | CI runs lint and tests (Level 1), plus type check and coverage (Level 2) | MUST | 1 | required checks (automatic) |
| [CI-004](../standards/ci-cd.md#ci-004-workflows-use-minimal-permissions) | Workflows use minimal permissions | MUST | 1 | workflow review (manual); OpenSSF Scorecard "Token-Permissions" (automatic, Level 3) |
| [CI-005](../standards/ci-cd.md#ci-005-actions-are-pinned-by-full-commit-sha-with-the-version-in-a-comment) | Actions are pinned by full commit SHA, with the version in a comment | MUST | 1 | workflow review (manual); OpenSSF Scorecard "Pinned-Dependencies" (automatic, Level 3) |
| [CI-006](../standards/ci-cd.md#ci-006-workflows-cancel-outdated-runs) | Workflows cancel outdated runs | MUST | 1 | workflow review (manual) |
| [CI-007](../standards/ci-cd.md#ci-007-every-job-has-timeout-minutes) | Every job has `timeout-minutes` | MUST | 1 | workflow review (manual) |
| [CI-008](../standards/ci-cd.md#ci-008-dependencies-are-cached) | Dependencies are cached | SHOULD | 1 | workflow review (manual) |
| [CI-009](../standards/ci-cd.md#ci-009-pull-requests-from-forks-never-get-secrets) | Pull requests from forks never get secrets | MUST NOT | 1 | workflow review (manual) |
| [CI-010](../standards/ci-cd.md#ci-010-secrets-are-stored-in-github-at-the-organization-level-when-shared) | Secrets are stored in GitHub, at the organization level when shared | MUST | 1 | settings audit (manual); secret scanning (automatic) |
| [CI-011](../standards/ci-cd.md#ci-011-untrusted-input-is-never-written-directly-in-a-run-script) | Untrusted input is never written directly in a `run:` script | MUST | 1 | workflow review (manual); actionlint (automatic, partly) |
| [CI-012](../standards/ci-cd.md#ci-012-workflows-are-linted-by-actionlint) | Workflows are linted by actionlint | SHOULD | 1 | `actionlint` pre-commit hook (automatic) |
| [CI-013](../standards/ci-cd.md#ci-013-artifacts-are-published-only-from-a-release-with-short-lived-credentials) | Artifacts are published only from a release, with short-lived credentials | SHOULD | 2 | workflow review (manual) |
| [CI-014](../standards/ci-cd.md#ci-014-pull-request-feedback-takes-less-than-10-minutes) | Pull request feedback takes less than 10 minutes | SHOULD | 2 | Actions run durations (manual) |
| [SEC-001](../standards/security.md#sec-001-dependabot-alerts-and-security-updates-are-enabled) | Dependabot alerts and security updates are enabled | MUST | 1 | Settings → Advanced Security (automatic, `gh api repos/{owner}/{repo} --jq .security_and_analysis`) |
| [SEC-002](../standards/security.md#sec-002-dependabot-version-updates-run-weekly-and-are-grouped) | Dependabot version updates run weekly and are grouped | MUST | 1 | `.github/dependabot.yml` review (manual) |
| [SEC-003](../standards/security.md#sec-003-secret-scanning-and-push-protection-are-enabled) | Secret scanning and push protection are enabled | MUST | 1 | Settings → Advanced Security (automatic); `security.yml` gitleaks job (automatic) |
| [SEC-004](../standards/security.md#sec-004-no-secret-is-ever-committed-and-a-leaked-secret-is-revoked-first) | No secret is ever committed, and a leaked secret is revoked first | MUST | 1 | gitleaks and secret scanning (automatic); code review (manual) |
| [SEC-005](../standards/security.md#sec-005-codeql-code-scanning-uses-the-default-setup) | CodeQL code scanning uses the default setup | MUST | 2 | Security → Code scanning shows CodeQL results (automatic) |
| [SEC-006](../standards/security.md#sec-006-pull-requests-are-checked-for-vulnerable-new-dependencies) | Pull requests are checked for vulnerable new dependencies | MUST | 2 | `dependency-review` job of `security.yml` (automatic) |
| [SEC-007](../standards/security.md#sec-007-locked-dependencies-are-audited) | Locked dependencies are audited | SHOULD | 2 | `python-audit` and `node-audit` jobs of `security.yml` (automatic) |
| [SEC-008](../standards/security.md#sec-008-private-vulnerability-reporting-is-enabled-and-securitymd-explains-it) | Private vulnerability reporting is enabled and `SECURITY.md` explains it | MUST | 1 | `gh api repos/{owner}/{repo}/private-vulnerability-reporting` returns `"enabled": true` (automatic) |
| [SEC-009](../standards/security.md#sec-009-docker-images-run-as-non-root-from-a-pinned-base-image) | Docker images run as non-root from a pinned base image | MUST | 2 | hadolint (automatic); Dockerfile review (manual) |
| [SEC-010](../standards/security.md#sec-010-no-real-personal-data-in-the-repository-tests-or-fixtures) | No real personal data in the repository, tests or fixtures | MUST | 1 | code review (manual) |
| [SEC-011](../standards/security.md#sec-011-security-fixes-are-merged-quickly) | Security fixes are merged quickly | SHOULD | 2 | Security → Dependabot alerts age (manual) |
| [SEC-012](../standards/security.md#sec-012-dependencies-have-licenses-that-are-compatible-with-the-project) | Dependencies have licenses that are compatible with the project | SHOULD | 2 | dependency review (automatic, with a license policy); code review (manual) |
| [SEC-013](../standards/security.md#sec-013-openssf-scorecard-measures-the-security-practices) | OpenSSF Scorecard measures the security practices | SHOULD | 3 | Scorecard workflow results (automatic) |
| [GH-001](../standards/github-settings.md#gh-001-the-repository-has-a-description-topics-and-a-website) | The repository has a description, topics and a website | MUST | 1 | `gh repo view --json description,repositoryTopics` (automatic) |
| [GH-002](../standards/github-settings.md#gh-002-a-ruleset-protects-main) | A ruleset protects `main` | MUST | 1 | Settings → Rules → Rulesets (automatic, `gh api repos/{owner}/{repo}/rulesets`) |
| [GH-003](../standards/github-settings.md#gh-003-nobody-bypasses-the-ruleset-or-administrators-bypass-in-pull-request-only-mode) | Nobody bypasses the ruleset, or administrators bypass in "pull request only" mode | MUST | 1 | ruleset `bypass_actors` (automatic, `gh api repos/{owner}/{repo}/rulesets/{id} --jq .bypass_actors`) |
| [GH-004](../standards/github-settings.md#gh-004-only-squash-merge-is-allowed-and-the-commit-message-comes-from-the-pr) | Only squash merge is allowed, and the commit message comes from the PR | MUST | 1 | `gh api repos/{owner}/{repo} --jq '{allow_squash_merge, allow_merge_commit, allow_rebase_merge, squash_merge_commit_title, squash_merge_commit_message}'` (automatic) |
| [GH-005](../standards/github-settings.md#gh-005-merged-branches-are-deleted-automatically) | Merged branches are deleted automatically | MUST | 1 | `delete_branch_on_merge` is `true` (automatic) |
| [GH-006](../standards/github-settings.md#gh-006-issues-are-on-the-wiki-is-off-discussions-are-optional) | Issues are on, the wiki is off, Discussions are optional | SHOULD | 1 | `gh repo view --json hasIssuesEnabled,hasWikiEnabled` (automatic) |
| [GH-007](../standards/github-settings.md#gh-007-the-repository-uses-the-standard-labels) | The repository uses the standard labels | SHOULD | 1 | `gh label list` (automatic) |
| [GH-008](../standards/github-settings.md#gh-008-two-factor-authentication-is-required-for-every-member) | Two-factor authentication is required for every member | MUST | 1 | `gh api orgs/DAH-Projects-and-Innovations --jq .two_factor_requirement_enabled` returns `true` (automatic) |
| [GH-009](../standards/github-settings.md#gh-009-the-base-permission-is-read-and-access-is-given-through-teams) | The base permission is Read and access is given through teams | MUST | 1 | `gh api orgs/DAH-Projects-and-Innovations --jq .default_repository_permission` returns `read` (automatic) |
| [GH-010](../standards/github-settings.md#gh-010-the-codeowners-team-has-write-access) | The CODEOWNERS team has write access | MUST | 1 | no error shown on the CODEOWNERS file page (automatic) |
| [GH-011](../standards/github-settings.md#gh-011-shared-secrets-are-organization-secrets-with-selected-repositories) | Shared secrets are organization secrets with selected repositories | SHOULD | 2 | Settings → Secrets and variables → Actions (manual) |
| [GH-012](../standards/github-settings.md#gh-012-the-workflow-token-is-read-only-by-default) | The workflow token is read-only by default | MUST | 1 | Settings → Actions → General → Workflow permissions (manual) |
| [ONB-001](../getting-started/first-day.md#onb-001-each-repository-keeps-a-few-well-described-good-first-issue-issues) | Each repository keeps a few well-described `good first issue` issues | SHOULD | 1 | `gh issue list --label "good first issue"` returns at least 3 open issues (manual) |
| [ONB-002](../getting-started/first-day.md#onb-002-first-time-contributors-get-an-answer-within-2-working-days) | First-time contributors get an answer within 2 working days | SHOULD | 1 | monthly review of open issues and PRs from first-time contributors (manual) |
| [ONB-003](../getting-started/first-day.md#onb-003-contributors-use-a-configured-git-identity-and-two-factor-authentication) | Contributors use a configured Git identity and two-factor authentication | MUST | 1 | commits show a GitHub account (manual); organization 2FA requirement (automatic, GH-008) |
| [ONB-004](../getting-started/first-day.md#onb-004-contributor-setup-is-tested-by-a-newcomer-every-quarter) | Contributor setup is tested by a newcomer every quarter | SHOULD | 2 | audit issue mentions the test (manual) |
| [LVL-001](../compliance/levels.md#lvl-001-every-active-repository-reaches-level-1) | Every active repository reaches Level 1 | MUST | 1 | quarterly compliance audit (manual) |
| [LVL-002](../compliance/levels.md#lvl-002-flagship-projects-reach-level-2) | Flagship projects reach Level 2 | MUST | 2 | quarterly compliance audit (manual) |
| [LVL-003](../compliance/levels.md#lvl-003-the-readme-shows-the-compliance-level-with-a-badge) | The README shows the compliance level with a badge | MUST | 1 | README review (manual) |
| [LVL-004](../compliance/levels.md#lvl-004-each-repository-is-audited-once-per-quarter) | Each repository is audited once per quarter | SHOULD | 1 | an issue labeled `compliance-audit` exists for the current quarter (manual) |
| [LVL-005](../compliance/levels.md#lvl-005-a-repository-records-the-version-of-the-standards-it-follows) | A repository records the version of the standards it follows | SHOULD | 1 | audit issue (manual) |

## Checklist

- [ ] I filtered the rules of the level my repository targets.
- [ ] I recorded each rule as compliant, not compliant or not applicable.
- [ ] I opened one issue per non-compliant rule (see the [migration playbook](../migration/playbook.md)).

---

*Generated from the rules in `docs/`. Last verified: see the footer of each page.*
