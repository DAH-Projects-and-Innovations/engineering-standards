# Commits

## TL;DR

- Commit messages follow **[Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)**: `type(scope)!: description`.
- The description is in English, in the imperative mood, in lower case, without a final period, and the first line is at most 72 characters.
- Pull requests are **squash merged**. The PR title becomes the commit message on `main`, so **the PR title MUST follow the same format**. CI checks it.
- Commit types decide the next version number and the CHANGELOG sections (release-please).
- A `commit-msg` hook checks every local commit.

## Format

```text
type(scope)!: description          <- header, at most 72 characters

Body: why the change is needed and what it changes.  <- optional, wrap at 72 characters
Several paragraphs are allowed.

Refs #123                          <- footers, optional
BREAKING CHANGE: what breaks and how to migrate.
```

| Part | Required | Content |
|---|---|---|
| `type` | yes | One of the types of COM-002 |
| `(scope)` | no | The part of the code that changes: `api`, `frontend`, `llm`, `retrieval`, `ci`… |
| `!` | no | Marks a breaking change |
| `description` | yes | What the commit does, as an order: "add", "fix", "remove" |
| body | no | Why. The code already shows what |
| footers | no | `Refs #123`, `Closes #123`, `Co-authored-by: Name <email>`, `BREAKING CHANGE: …` |

## Rules

### COM-001: Commit messages follow Conventional Commits 1.0.0

**MUST** · Level 1 · Verified by: `conventional-pre-commit` commit-msg hook and PR title check in `pr-conventions.yml` (automatic)

**Why:** a fixed format makes the history readable and lets tools compute the next version and write the CHANGELOG.

**Examples:**

- ✅ `feat(retrieval): add hybrid retriever with reciprocal rank fusion`
- ✅ `fix(chunker): stop infinite loop when overlap is larger than chunk size`
- ✅ `docs: explain the free, hybrid and premium modes`
- ❌ `Ajout du module de recherche` (no type, not in English)
- ❌ `feat: changes` (says nothing)
- ❌ `TASKS 12-15` (no type, no description)

### COM-002: Only the standard types are used

**MUST** · Level 1 · Verified by: commit-msg hook and PR title check (automatic)

| Type | Meaning | SemVer effect | CHANGELOG section |
|---|---|---|---|
| `feat` | New feature for the user | **minor** (`1.2.0` → `1.3.0`) | Features |
| `fix` | Bug fix for the user | **patch** (`1.2.0` → `1.2.1`) | Bug Fixes |
| `perf` | Performance improvement | patch | Performance Improvements |
| `revert` | Reverts a previous commit | patch | Reverts |
| `docs` | Documentation only | none | Documentation |
| `refactor` | Code change that keeps the behavior | none | hidden |
| `style` | Formatting only (no logic change) | none | hidden |
| `test` | Tests only | none | hidden |
| `build` | Build system, packaging, Docker, dependencies | none | hidden |
| `ci` | CI configuration | none | hidden |
| `chore` | Other maintenance | none | hidden |
| any type with `!` or `BREAKING CHANGE:` | Breaking change | **major** (`1.2.0` → `2.0.0`) | ⚠ BREAKING CHANGES |

Before version `1.0.0`, a project MAY set the release-please option `bump-minor-pre-major: true`, so that a breaking change bumps `0.4.0` to `0.5.0` instead of `1.0.0` (see [Releases](releases.md)).

Dependabot uses `chore(deps):` and `build(deps):` titles, which follow this rule.

### COM-003: The description is short, English, imperative, lower case, without a final period

**MUST** · Level 1 · Verified by: PR title check (`subjectPattern`, automatic) and code review (manual)

- **English:** contributors come from francophone and anglophone countries; English is the shared language of the code.
- **Imperative:** "add", not "added" or "adds". Read it as "If applied, this commit will *add …*".
- **Lower case** first letter, **no final period**.

**Examples:**

- ✅ `fix(api): read CORS origins from the CORS_ORIGINS variable`
- ❌ `fix(api): Fixed CORS.` (past tense, capital letter, period, too vague)

### COM-004: The header is at most 72 characters

**MUST** · Level 1 · Verified by: PR title length check in `pr-conventions.yml` (automatic)

**Why:** GitHub, `git log --oneline` and most tools cut longer lines.

The check skips PRs opened by bots (Dependabot, release-please): they write their own titles, and their format is still checked ([COM-001](#com-001-commit-messages-follow-conventional-commits-100)).

### COM-005: The body explains why

**SHOULD** · Level 1 · Verified by: code review (manual)

When the reason is not obvious, write a body. Explain the problem, the reason for this solution and any side effect. Wrap lines at 72 characters.

```text
fix(retrieval): apply metadata filters in every vector store

The filters were passed to ChromaStore only. PineconeStore and
SimpleStore ignored them, so a query filtered on language could return
documents in any language.

Closes #11
```

### COM-006: Breaking changes are marked

**MUST** · Level 1 · Verified by: code review (manual); release-please reads the marker (automatic)

A change that forces users to change their code, their configuration or their data MUST have `!` after the type or scope **and** a `BREAKING CHANGE:` footer that explains how to migrate.

```text
feat(config)!: rename embedding.model to embedding.model_name

BREAKING CHANGE: configuration files must use `embedding.model_name`.
Run `scripts/migrate_config.py configs/` to update existing files.
```

### COM-007: Pull requests are squash merged and the PR title follows COM-001 to COM-004

**MUST** · Level 1 · Verified by: ruleset `allowed_merge_methods: [squash]` and `pr-conventions.yml` (automatic)

The repository allows only squash merging (see [GitHub settings](github-settings.md)). The squash commit takes the **PR title** as its header and the PR number is added at the end, for example `feat(api): add streaming answers (#64)`.

**Why:** one PR = one commit on `main`. The history stays linear and readable, and each commit on `main` passed CI and review. Contributors can make as many small commits as they want on their branch. See [ADR 0002](../adr/0002-squash-merge-only.md).

**Consequence:** commit messages on a branch matter less than the PR title. The commit-msg hook still checks them, to build good habits.

### COM-008: Commits on a branch are small and meaningful

**SHOULD** · Level 1 · Verified by: code review (manual)

Each commit does one thing and leaves the code working. Avoid messages that say nothing: `wip`, `fix`, `update`, `changes`, `misc`.

**Why:** small commits are easy to review one by one and easy to revert.

**Tip:** to fix the previous commit, use `git commit --fixup <sha>` then `git rebase -i --autosquash origin/main` before asking for review. The commit-msg hook rejects `fixup!` commits in `--strict` mode, so run the rebase before you push, or push with `--no-verify` only on your own branch (the PR title is what reaches `main`).

### COM-009: Scopes come from a list written in CONTRIBUTING.md

**SHOULD** · Level 1 · Verified by: code review (manual); `scopes` input of `pr-conventions.yml` (automatic, optional)

Each repository lists its scopes in `CONTRIBUTING.md`, usually one per component: `api`, `frontend`, `llm`, `retrieval`, `adapters`, `eval`, `deps`, `ci`, `docs`. A repository MAY pass this list to `pr-conventions.yml` to enforce it.

### COM-010: Commits are signed

**SHOULD** · Level 3 · Verified by: ruleset rule "Require signed commits" (automatic)

Sign commits with an SSH key or a GPG key ([GitHub Docs: signing commits](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits)). GitHub signs the squash commits it creates on `main`. The [tools installation guide](../getting-started/tools-installation.md#4-configure-git) shows the setup with an SSH key.

**Why:** a signature proves that the commit comes from the account that claims to have written it.

## Checklist

- [ ] `.pre-commit-config.yaml` has the `conventional-pre-commit` hook in the `commit-msg` stage.
- [ ] `pre-commit install` was run, so the `commit-msg` hook is active locally.
- [ ] CI calls `pr-conventions.yml` and its PR title check is a required status check.
- [ ] Only squash merge is allowed; the default squash message uses the PR title.
- [ ] `CONTRIBUTING.md` lists the allowed scopes.
- [ ] The last 20 commits on `main` follow Conventional Commits (`git log --oneline -20`).

---

*Last verified: 2026-11-13.*
