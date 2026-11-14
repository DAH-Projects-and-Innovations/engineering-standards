<!-- DAH Labs CONTRIBUTING template (rule FILE-004). Replace every TODO. Target: a newcomer
     installs the project in less than 10 minutes. -->

# Contributing to TODO project name

Thank you for your interest! All contributions are welcome: code, documentation, tests, evaluation data, translations and well-described issues.

By participating, you agree to follow our [Code of Conduct](CODE_OF_CONDUCT.md). This project follows the [DAH Labs engineering standards](https://github.com/DAH-Projects-and-Innovations/engineering-standards). Francophone contributors can start with the [French getting started page](https://github.com/DAH-Projects-and-Innovations/engineering-standards/blob/main/docs/getting-started/demarrage-fr.md).

## Before you start

- Look at the issues labeled `good first issue` for a first contribution.
- For a new feature or a large change, open an issue first, so that we can agree on the direction.
- Comment on an issue to say that you work on it, so that two people do not do the same work.
- Everything in the repository (code, comments, commits, issues, documentation) is written in English. Simple English is fine.

## Set up your environment (about 10 minutes)

Prerequisites (see the [tools installation guide](https://github.com/DAH-Projects-and-Innovations/engineering-standards/blob/main/docs/getting-started/tools-installation.md)):

| Tool | Version |
|---|---|
| Git | 2.40 or newer |
| uv | 0.13.8 or newer |
| Python | 3.12 (uv installs it for you) |
| Node.js | 24 LTS, with pnpm through corepack |
| Docker | with Docker Compose |

```bash
# 1. Fork the repository on GitHub (or clone it directly if you are a member), then:
git clone https://github.com/<your-account>/<repo>.git
cd <repo>

# 2. Back end
cd backend && uv sync && uv run pytest && cd ..

# 3. Front end
corepack enable
cd frontend && pnpm install && pnpm test && cd ..

# 4. Git hooks: checks run on commit and on push
uvx pre-commit install
```

## Run the project

TODO: the commands to start the API, the worker and the front end, and the URLs to open.

## Conventions

- **Branches:** `<type>/<issue-number>-<short-description>`, for example `feat/42-add-cohere-embedder`. See [Git branching](https://github.com/DAH-Projects-and-Innovations/engineering-standards/blob/main/docs/standards/git-branching.md).
- **Commits and PR titles:** [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/), for example `fix(api): read CORS origins from the environment`. See [Commits](https://github.com/DAH-Projects-and-Innovations/engineering-standards/blob/main/docs/standards/commits.md).
- **Scopes used in this repository:** TODO `api`, `core`, `llm`, `frontend`, `eval`, `docs`, `ci`, `deps`.
- **Code style:** Ruff (Python) and ESLint + Prettier (TypeScript) decide. Run `uv run ruff format .` and `pnpm format`.

## Tests and checks

```bash
cd backend
uv run ruff check . && uv run ruff format --check .
uv run mypy
uv run pytest

cd ../frontend
pnpm lint && pnpm typecheck && pnpm test && pnpm build
```

Tests never call a paid API or a real language model: use the fakes in `TODO: tests/fakes.py`.

## Open a pull request

1. Push your branch and open a **draft** pull request.
2. Fill in every section of the template.
3. When CI is green, click **Ready for review**.
4. A maintainer reviews within about 2 working days. Answer the comments, push fixes.
5. A maintainer (or you, if you have write access) squash merges the pull request.

## Mandatory rules

- **No secrets** in the code, the tests or the history. Use environment variables (`.env`, ignored by Git).
- **No real personal data** in the repository: test data is fictional.
- New dependencies must have a license compatible with TODO Apache-2.0.

## Questions

Open an issue with the "Question" form. TODO: other channel (forum, chat), if any.
