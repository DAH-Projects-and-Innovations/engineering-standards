# Glossary

## TL;DR

- Short definitions of the words used in these standards, for beginners.
- Words are in alphabetical order.
- French translations are in the [French getting started page](getting-started/demarrage-fr.md#glossaire-français--anglais).

## Terms

- **Adapter**: A class in `infrastructure/` that implements a port with a real technology (a database, an API, a vector store). See [Architecture](standards/architecture.md).
- **ADR (Architecture Decision Record)**: A short document that records one important decision: the context, the options, the choice and its consequences. Stored in `docs/adr/`.
- **Approval**: A review that says "this can be merged". The ruleset requires at least one.
- **Artifact**: A file produced by a workflow (for example a coverage report or a Docker image) and kept after the run.
- **Branch**: A line of work in Git. `main` is the only long-lived branch; other branches are short and merged by pull request.
- **Breaking change**: A change that forces users to change their code, configuration or data. Marked with `!` and `BREAKING CHANGE:`; it creates a new major version.
- **CD (Continuous Delivery)**: Automatic publication of versioned artifacts (images, packages, models) when a release is made.
- **CHANGELOG**: The file that lists the notable changes of each version.
- **CI (Continuous Integration)**: Automatic checks (lint, tests, build) that run on every push and pull request, on GitHub Actions.
- **Code scanning / CodeQL**: Static analysis by GitHub that looks for security problems in the code.
- **CODEOWNERS**: A file that says which team must review changes to which files.
- **Composition root**: The one place (`bootstrap/container.py`) that creates the adapters from the settings and gives them to the use cases.
- **Conventional Commits**: A format for commit messages: `type(scope): description`.
- **Coverage**: The percentage of code lines (or branches) executed by the tests.
- **Dataset card**: A document that describes a dataset: content, sources, license, personal data, languages and limits.
- **Dependabot**: A GitHub service that warns about vulnerable dependencies and opens pull requests to update them.
- **Draft pull request**: A pull request that is not ready for review yet.
- **Fake**: A small in-memory implementation of a port, used in tests instead of the real adapter.
- **Fixture**: Test data or a test helper prepared before a test runs.
- **Flaky test**: A test that sometimes fails without any code change. It is quarantined with an issue (TEST-007).
- **Fork**: Your own copy of a repository on GitHub. You change the copy and propose changes to the original with a pull request.
- **Formatter**: A tool that rewrites the code layout automatically (Ruff format, Prettier).
- **GitHub Actions**: GitHub's CI/CD service. Workflows are YAML files in `.github/workflows/`.
- **Hook (Git hook)**: A script that Git runs automatically at a given moment (before a commit, before a push).
- **Linter**: A tool that finds probable bugs and bad practices without running the code (Ruff check, ESLint).
- **Lock file**: A file that records the exact version of every dependency (`uv.lock`, `pnpm-lock.yaml`), so everybody installs the same versions.
- **Merge (squash merge)**: Combining a branch into `main`. A squash merge turns all commits of the branch into one commit.
- **Mock / fake**: A replacement for a real component in tests. A fake is a small working implementation (for example `FakeLLM`); a mock records calls and returns prepared answers.
- **Model card**: A document that describes a model: intended use, training data, evaluation, limitations.
- **New code**: In SonarQube Cloud, the code changed by a pull request, or changed on `main` during the last 30 days. The quality gate checks it.
- **Port and adapter**: A port is an interface that the application needs (for example `IEmbedder`). An adapter is a concrete implementation of a port (for example `OpenAIEmbedder`).
- **Port**: An interface (`typing.Protocol`) that a use case needs from the outside world, for example `Retriever`.
- **pre-commit**: The framework that installs and runs Git hooks from a `.pre-commit-config.yaml` file.
- **Pull request (PR)**: A request to merge a branch, with a description, a review and CI checks.
- **Push protection**: A GitHub feature that blocks a push containing a secret.
- **Quality gate**: A set of conditions (coverage, duplication, bugs, vulnerabilities on new code) that a project must meet in SonarQube Cloud.
- **Release PR**: The pull request that release-please keeps open with the next version and its CHANGELOG. Merging it creates the release.
- **Release**: A published version of a project, with a tag (`v1.2.0`) and notes.
- **Repository (repo)**: A project stored in Git, with its history.
- **Reusable workflow**: A GitHub Actions workflow that other workflows call with `uses:`. The DAH Labs reusable workflows live in this repository.
- **Ruleset**: A set of GitHub rules that protect a branch: require pull requests, approvals, CI checks; block force pushes and deletion.
- **Scope**: In a commit message, the part of the code that changes: `feat(api): …`.
- **Secret scanning**: A GitHub feature that finds secrets in a repository.
- **Secret**: A value that gives access to something: API key, password, token. Never in Git.
- **Semantic Versioning (SemVer)**: Version numbers `MAJOR.MINOR.PATCH`: major for breaking changes, minor for features, patch for fixes.
- **SHA**: The unique identifier of a Git commit, for example `3d3c42e5aac5ba805825da76410c181273ba90b1`.
- **Status check**: The result (success or failure) of a CI job on a pull request.
- **Tag**: A name attached to one commit, for example `v1.2.0`.
- **Trunk-based development / GitHub Flow**: A way of working with one main branch (`main`) and short branches merged often.
- **Type checker**: A tool that checks the types of the code without running it (mypy, `tsc`).
- **Use case**: A class or function in `application/` that does one action of the system, for example "answer a question".
- **Workflow**: An automated process in GitHub Actions, defined in a YAML file.

---

*Last verified: 2026-11-14.*
