# Audit checklist

## TL;DR

- Use this checklist to audit a repository against the standards, once per quarter or before a migration.
- **Part A is automatic:** `python scripts/audit_repository.py <owner>/<repo>` prints a Markdown table (read-only, uses `gh`).
- **Part B is manual:** about 30 checks that need a human look.
- Record the results in an issue opened with the **Compliance audit** form ([`audit.yml`](../../templates/github/ISSUE_TEMPLATE/audit.yml)), one line per finding: rule, current state, action, effort, priority.
- **Security weaknesses never go in the public issue:** use a private security advisory.

## How to run the audit

```bash
git clone https://github.com/DAH-Projects-and-Innovations/engineering-standards.git
cd engineering-standards
gh auth login                       # once; an account with admin rights sees more settings
python scripts/audit_repository.py DAH-Projects-and-Innovations/<repo> --root backend > /tmp/audit.md
```

Then clone the audited repository **read-only** and go through Part B:

```bash
git clone https://github.com/DAH-Projects-and-Innovations/<repo>.git /tmp/<repo>
cd /tmp/<repo>
```

**Effort:** S = less than half a day, M = one to three days, L = more than three days (split it).
**Priority:** P1 = security or blocking for others, P2 = Level 1, P3 = Level 2 and 3.

## Part A — automatic checks

`scripts/audit_repository.py` checks:

- default branch, other long-lived branches (GIT-001);
- description, topics (GH-001); merge settings (GH-004, GH-005); wiki (GH-006);
- Dependabot security updates, secret scanning, push protection, private vulnerability reporting (SEC-001, SEC-003, SEC-008);
- ruleset on the default branch and its rules (GH-002, GH-003, PR-006, PR-009, PR-010, COM-007);
- presence of the required files (FILE-001 to FILE-016);
- `uv.lock`, other lock files, tests inside `src/`, model files (PY-002, JS-002, PY-012, REPO-006).

A ❔ result means that the token cannot read the value: check it by hand in the settings.

## Part B — manual checks

### Branches and commits

- [ ] **GIT-003** Recent branches follow the naming convention: `git branch -r --sort=-committerdate | head -20`.
- [ ] **GIT-005** No branch older than 2 weeks without a reason: `git for-each-ref --sort=committerdate refs/remotes --format='%(committerdate:short) %(refname:short)'`.
- [ ] **COM-001** The last 20 commits on the default branch follow Conventional Commits: `git log --format=%s -20`.
- [ ] **COM-009** `CONTRIBUTING.md` lists the scopes.

### Pull requests

- [ ] **PR-001** The PR template has the five sections (context, changes, how to test, screenshots, checklist).
- [ ] **PR-003** Recent merged PRs are mostly under 400 lines: `gh pr list --state merged --limit 20 --json number,additions,deletions`.
- [ ] **PR-008** The required checks of the ruleset match the CI job names.
- [ ] **PR-012** Open PRs older than 30 days: `gh pr list --json number,title,updatedAt`.

### Files

- [ ] **FILE-001** README: badges, status, quick start, architecture, development, license, DAH Labs line; English; clone URL points to the organization.
- [ ] **FILE-003** License is Apache-2.0, or the exception is documented (README + ADR).
- [ ] **FILE-004** A newcomer can follow `CONTRIBUTING.md` in less than 10 minutes (ask one to try).
- [ ] **FILE-005** The Code of Conduct is Contributor Covenant 3.0 and has a reporting contact.
- [ ] **FILE-008** `CODEOWNERS` names the `maintainers` team, not people, and shows no error on GitHub.
- [ ] **FILE-015** `.env.example` lists every variable read by the code: `grep -rhoE '[A-Z][A-Z0-9_]{3,}' $(grep -rl 'environ\|BaseSettings\|import.meta.env' --include=*.py --include=*.ts --include=*.tsx .) | sort -u`.

### Python

- [ ] **PY-001** `requires-python >= 3.12`, `.python-version` present.
- [ ] **PY-003** No `setup.py`, `setup.cfg`, `pytest.ini`, `mypy.ini`, hand-written `requirements.txt`.
- [ ] **PY-004/005** `uv run ruff check .` and `uv run ruff format --check .` pass; the Level 1 rule set is enabled.
- [ ] **PY-009** (Level 2) `uv run mypy` passes in strict mode; count the overrides.
- [ ] **PY-013** Markers are declared; `--strict-markers` is on.
- [ ] **PY-016** No test calls a real provider: `grep -rn "api_key\|OpenAI(\|Mistral(\|cohere.Client" tests/`.
- [ ] **PY-017** (Level 2) Current coverage: `uv run pytest --cov`; note it.
- [ ] **PY-019** No `print(` in the package: `uv run ruff check --select T20 src`.
- [ ] **PY-021** Settings use `pydantic-settings` and fail at startup when invalid.
- [ ] **PY-022** The package is in `src/<real_name>/` and is not imported as `src.…`.
- [ ] **PY-023** No test or lint tool in `[project] dependencies`.

### JavaScript / TypeScript

- [ ] **JS-001** `tsconfig.json` has `"strict": true`; count `.js`/`.jsx` source files.
- [ ] **JS-002** `packageManager: "pnpm@…"` is set; `pnpm-lock.yaml` is the only lock file.
- [ ] **JS-003** `.nvmrc` contains `24`; `engines.node` is set.
- [ ] **JS-007** Scripts `lint`, `format:check`, `typecheck`, `test`, `build` exist.
- [ ] **JS-009** No secret in `VITE_*` / `NEXT_PUBLIC_*` variables, in `.env.example` or Dockerfiles.

### Structure

- [ ] **REPO-001** No loose files at the root.
- [ ] **REPO-005** No `docs/` folder inside `src/`.
- [ ] **REPO-006** No data, model or PDF corpus committed: `git ls-files | grep -iE '\.(pdf|csv|zip|h5|pt|safetensors|parquet)$'`.
- [ ] **REPO-007** No `examples/` or notebooks inside the package.

### Hooks and CI

- [ ] **HOOK-001** `.pre-commit-config.yaml` installs `pre-commit`, `commit-msg` and `pre-push`.
- [ ] **HOOK-003/004/005** gitleaks, conventional-pre-commit and dah-branch-name are configured.
- [ ] **HOOK-006** Every `rev:` is a tag; Dependabot has a `pre-commit` entry.
- [ ] **CI-002** CI calls the reusable workflows with `@v1` or a SHA.
- [ ] **CI-004** Every workflow has `permissions:` at the top level.
- [ ] **CI-005** Every action is pinned by SHA: `grep -rn "uses:" .github/workflows | grep -v "@[0-9a-f]\{40\}"` prints only reusable workflows of the standards.
- [ ] **CI-006/007** Every workflow has `concurrency` and every job has `timeout-minutes`.
- [ ] **CI-009** No `pull_request_target` that checks out PR code: `grep -rn pull_request_target .github/workflows`.
- [ ] **CI-011** No `${{ github.event.` inside `run:` blocks.

### Security

- [ ] **SEC-002** `dependabot.yml` covers every ecosystem present (`uv`, `npm`, `docker`, `github-actions`, `pre-commit`).
- [ ] **SEC-004** gitleaks finds nothing in the history: `docker run --rm -v "$PWD:/repo" zricethezav/gitleaks:v8.30.1 git /repo --redact` (or the `security.yml` job). **Any finding is reported privately first.**
- [ ] **SEC-005** (Level 2) CodeQL default setup is on.
- [ ] **SEC-009** (Level 2) Dockerfiles: pinned base image with digest, `USER` not root, no `COPY . .` of secrets.
- [ ] **SEC-010** No real personal data in tests, fixtures, notebooks, screenshots, `data/`.

## Report template

Paste this in the audit issue, under the output of Part A:

```markdown
| Rule | Current state | Action | Effort | Priority |
|---|---|---|---|---|
| GIT-001 | Default branch is `development` | Follow default-branch-migration.md | M | P2 |
| FILE-008 | No CODEOWNERS | Add `.github/CODEOWNERS` with the maintainers team | S | P2 |
```

Then create one issue per line (or per group of small lines), with the labels `compliance-audit` and `size: S|M|L`, and link them from the audit issue.

## Checklist

- [ ] Part A was run and its output pasted in the audit issue.
- [ ] Part B was completed for the target level.
- [ ] Security findings were reported privately, not in the issue.
- [ ] Every finding became an issue with a size and a priority.

---

*Last verified: 2026-11-13.*
