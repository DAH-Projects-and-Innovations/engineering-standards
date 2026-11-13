# Git hooks (pre-commit)

## TL;DR

- Every repository uses the **[pre-commit](https://pre-commit.com/)** framework with three hook stages: `pre-commit`, `commit-msg` and `pre-push`.
- **pre-commit** (each commit, less than 10 s): file hygiene, secrets (gitleaks), Ruff, Prettier, hadolint, nbstripout, `uv.lock` check.
- **commit-msg**: Conventional Commits.
- **pre-push**: branch name, no push to `main`, mypy, fast unit tests.
- Hooks can be skipped on a laptop, so **CI runs them again**: CI is the source of truth.

Templates: [`templates/pre-commit/python.yaml`](../../templates/pre-commit/python.yaml) and [`templates/pre-commit/fullstack.yaml`](../../templates/pre-commit/fullstack.yaml).

## What runs when

| Stage | When | Hooks | Time budget |
|---|---|---|---|
| `pre-commit` | `git commit` | trailing-whitespace, end-of-file-fixer, mixed-line-ending, check-yaml/toml/json, check-added-large-files (500 KB), check-merge-conflict, check-case-conflict, detect-private-key, no-commit-to-branch, **gitleaks**, **ruff check --fix**, **ruff format**, **uv-lock --check**, Prettier (front end), hadolint (Dockerfiles), nbstripout (notebooks) | < 10 s |
| `commit-msg` | `git commit` | conventional-pre-commit `--strict` | < 1 s |
| `pre-push` | `git push` | **dah-branch-name** (name + no push to `main`), mypy, `pytest -m "not slow and not integration …"`, ESLint, `tsc` | < 2 min |

## Install, step by step

You need `git` and `uv` (see [Tools installation](../getting-started/tools-installation.md)). pre-commit itself runs through `uvx`, so you do not install it globally.

### Linux and macOS

```bash
cd my-repository
uvx pre-commit install            # installs the three hook types listed in the config
uvx pre-commit run --all-files    # first run: downloads the hook tools, then checks everything
```

### Windows

Use **WSL 2** (Windows Subsystem for Linux) with Ubuntu, and follow the Linux steps inside WSL. Clone the repository inside the WSL file system (`~/code/…`), not in `/mnt/c/…`: it is much faster and avoids line-ending problems.

Native Windows (PowerShell or Git Bash) MAY work, but it is not tested by DAH Labs. Some hooks are scripts with a `#!/usr/bin/env python3` line, which needs `python3` on the `PATH`.

### Check that it works

```bash
git switch -c docs/test-hooks
echo "trailing space " >> README.md
git commit -am "test"           # rejected: "test" is not a Conventional Commit
git commit -am "docs: test hooks"   # trailing-whitespace fixes the file; add it and commit again
git switch main && git branch -D docs/test-hooks && git checkout README.md
```

## Rules

### HOOK-001: The repository uses pre-commit with the three hook stages

**MUST** · Level 1 · Verified by: `.pre-commit-config.yaml` review (manual); `pre-commit.yml` in CI (automatic)

`.pre-commit-config.yaml` sets:

```yaml
default_install_hook_types: [pre-commit, commit-msg, pre-push]
```

so a single `pre-commit install` installs all hooks.

### HOOK-002: The pre-commit stage is fast and fixes what it can

**MUST** · Level 1 · Verified by: `pre-commit.yml` in CI (automatic)

The pre-commit stage contains the hygiene hooks, Ruff (lint with `--fix`, then format) and, depending on the repository, Prettier, hadolint and nbstripout. It runs in less than 10 seconds on a normal commit. Slow checks go to the pre-push stage.

**Why:** if commits are slow, people skip the hooks.

### HOOK-003: gitleaks scans every commit for secrets

**MUST** · Level 1 · Verified by: `gitleaks` hook (automatic); `security.yml` scans the history in CI (automatic)

A false positive (for example a fake key in documentation) goes in `.gitleaksignore`, with a comment. Never add a real key to `.gitleaksignore`: revoke it (see [Security](security.md#sec-004-no-secret-is-ever-committed-and-a-leaked-secret-is-revoked-first)).

### HOOK-004: The commit-msg stage checks Conventional Commits

**MUST** · Level 1 · Verified by: `conventional-pre-commit` hook (automatic)

### HOOK-005: The pre-push stage checks the branch name, types and fast tests

**SHOULD** · Level 1 · Verified by: `.pre-commit-config.yaml` review (manual)

The `dah-branch-name` hook comes from this repository, so no script is copied into projects:

```yaml
- repo: https://github.com/DAH-Projects-and-Innovations/engineering-standards
  rev: v1.0.0
  hooks:
    - id: dah-branch-name
```

It rejects a push to `main` and a branch name that does not follow [GIT-003](git-branching.md#git-003-branch-names-follow-typeissue-number-short-description). The mypy and pytest hooks are local hooks that use the project environment (`uv run --frozen …`).

### HOOK-006: Hook versions are pinned and updated by Dependabot

**MUST** · Level 1 · Verified by: `rev:` values are tags, not branches (manual); Dependabot `pre-commit` ecosystem (automatic)

Each `rev:` is a release tag (`v0.17.5`), never `main` or `master`. Dependabot reads `.pre-commit-config.yaml` and opens PRs to update the tags ([GitHub changelog, 2026-03-10](https://github.blog/changelog/2026-03-10-dependabot-now-supports-pre-commit-hooks/)):

```yaml
- package-ecosystem: pre-commit
  directory: /
  schedule:
    interval: weekly
```

You MAY also run `uvx pre-commit autoupdate` by hand.

Keep the Ruff version of the hook equal to the Ruff version in the dev dependency group, so that the hook and CI give the same results.

### HOOK-007: CI runs every pre-commit hook again on all files

**MUST** · Level 1 · Verified by: `pre-commit.yml` reusable workflow is a required check (automatic)

```bash
git commit --no-verify     # skips every local hook
```

Anybody can skip local hooks, or forget to install them. CI calls [`pre-commit.yml`](../../.github/workflows/pre-commit.yml), which runs `pre-commit run --all-files`. A PR that skipped a hook fails in CI.

Local hooks that need installed project tools (for example `prettier` with `language: system`) are skipped in that job with the `skip` input, because `node-ci.yml` already runs them.

### HOOK-008: Hooks are not skipped without a reason

**SHOULD** · Level 1 · Verified by: CI (automatic)

`--no-verify` is acceptable on your own branch (for example to push a work-in-progress commit for a draft PR). CI will still check everything before merge.

### HOOK-009: Notebook outputs are stripped before commit

**MUST** · Level 1 · Verified by: `nbstripout` hook (automatic)

Every repository with `.ipynb` files enables the `nbstripout` hook (see [ML and research](ml-research.md)).

**Why:** outputs make diffs unreadable, make the repository heavy, and can contain personal data or secrets.

### HOOK-010: Dockerfiles are checked by hadolint

**SHOULD** · Level 1 · Verified by: `hadolint` hook (automatic)

## Troubleshooting

| Problem | Solution |
|---|---|
| `files were modified by this hook` | The hook fixed the files. Run `git add -u` and commit again. |
| `[INFO] Initializing environment` takes minutes | Normal the first time: pre-commit downloads the tools. Later runs are fast. |
| A hook fails only on your machine | `uvx pre-commit clean`, then `uvx pre-commit run --all-files`. |
| `uv: command not found` in a local hook | Install uv and open a new terminal (see [Tools installation](../getting-started/tools-installation.md)). |
| `pnpm` hooks fail | Run `pnpm --dir frontend install` first. |
| The pre-push hook says the branch name is wrong | `git branch -m <type>/<issue>-<description>`, then push again. |

## Checklist

- [ ] `.pre-commit-config.yaml` sets `default_install_hook_types: [pre-commit, commit-msg, pre-push]`.
- [ ] gitleaks, Ruff, `uv-lock`, `conventional-pre-commit` and `dah-branch-name` are configured.
- [ ] nbstripout (notebooks) and hadolint (Dockerfiles) are configured when needed.
- [ ] Every `rev:` is a tag; Dependabot has a `pre-commit` entry.
- [ ] CI calls `pre-commit.yml` and it is a required check.
- [ ] `CONTRIBUTING.md` says to run `uvx pre-commit install`.

---

*Last verified: 2026-11-13.*
