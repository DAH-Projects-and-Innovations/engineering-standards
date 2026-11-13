# Templates

## TL;DR

- Files ready to copy into a DAH Labs repository. Each one says where it goes and which rules it implements.
- Replace every `TODO` marker. Search for them with `grep -rn TODO <file>`.
- File names have no leading dot here (`gitignore`, `editorconfig`) so that they are visible; add the dot when you copy.
- The `fixtures` in `tests/fixtures/` show filled versions of the Python and front-end templates that pass CI.

## Where each template goes

| Template | Copy to | Rules |
|---|---|---|
| [`python/pyproject.toml`](python/pyproject.toml) | `backend/pyproject.toml` (or root of a library) | PY-* |
| [`js/eslint.config.js`](js/eslint.config.js) | `frontend/eslint.config.js` | JS-004, JS-011, JS-012 |
| [`js/prettier.config.js`](js/prettier.config.js), [`js/prettierignore`](js/prettierignore) | `frontend/prettier.config.js`, `frontend/.prettierignore` | JS-004 |
| [`js/tsconfig.json`](js/tsconfig.json) | `frontend/tsconfig.json` (Vite or library) | JS-001 |
| [`js/vitest.config.ts`](js/vitest.config.ts) | `frontend/vitest.config.ts` | JS-006 |
| [`js/nvmrc`](js/nvmrc) | `frontend/.nvmrc` | JS-003 |
| [`pre-commit/python.yaml`](pre-commit/python.yaml) | `.pre-commit-config.yaml` (Python only) | HOOK-* |
| [`pre-commit/fullstack.yaml`](pre-commit/fullstack.yaml) | `.pre-commit-config.yaml` (backend + frontend) | HOOK-* |
| [`editor/editorconfig`](editor/editorconfig) | `.editorconfig` | FILE-012 |
| [`git/gitignore`](git/gitignore) | `.gitignore` | FILE-013, REPO-006 |
| [`git/gitattributes`](git/gitattributes) | `.gitattributes` | FILE-014 |
| [`git/git-blame-ignore-revs`](git/git-blame-ignore-revs) | `.git-blame-ignore-revs` | FILE-018 |
| [`env/env.example`](env/env.example) | `.env.example` | FILE-015, PY-021 |
| [`github/workflows/ci.yml`](github/workflows/ci.yml) | `.github/workflows/ci.yml` | CI-* |
| [`github/workflows/scorecard.yml`](github/workflows/scorecard.yml) | `.github/workflows/scorecard.yml` | SEC-013 |
| [`github/dependabot.yml`](github/dependabot.yml) | `.github/dependabot.yml` | SEC-002, HOOK-006 |
| [`github/CODEOWNERS`](github/CODEOWNERS) | `.github/CODEOWNERS` | FILE-008 |
| [`github/pull_request_template.md`](github/pull_request_template.md) | `.github/pull_request_template.md` | PR-001 |
| [`github/ISSUE_TEMPLATE/`](github/ISSUE_TEMPLATE/) | `.github/ISSUE_TEMPLATE/` | FILE-010 |
| [`github/rulesets/main.json`](github/rulesets/main.json) | imported with `gh api` (not copied) | GH-002, GH-003 |
| [`github/labels.json`](github/labels.json) | used by `scripts/sync_labels.py` (not copied) | GH-007 |
| [`docs/README.md`](docs/README.md) | `README.md` | FILE-001 |
| [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) | `CONTRIBUTING.md` | FILE-004 |
| [`docs/CODE_OF_CONDUCT.md`](docs/CODE_OF_CONDUCT.md) | `CODE_OF_CONDUCT.md` | FILE-005 |
| [`docs/SECURITY.md`](docs/SECURITY.md) | `SECURITY.md` | FILE-006 |
| [`docs/CHANGELOG.md`](docs/CHANGELOG.md) | `CHANGELOG.md` | FILE-007 |
| [`docs/CITATION.cff`](docs/CITATION.cff) | `CITATION.cff` (research repositories) | FILE-017 |
| [`docs/adr.md`](docs/adr.md) | `docs/adr/NNNN-title.md` | DOC-* (next version) |

Planned for the next version: `sonar-project.properties`, release-please configuration, a Python Dockerfile (multi-stage, non-root, uv), model card and dataset card.

## Checklist

- [ ] Every copied file is at the right place, with the leading dot when needed.
- [ ] `grep -rn TODO` on the copied files returns nothing (or only items with an issue).
- [ ] `uvx pre-commit run --all-files` and CI pass after the copy.

---

*Last verified: 2026-11-13.*
