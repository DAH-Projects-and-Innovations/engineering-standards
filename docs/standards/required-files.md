# Required files

## TL;DR

- Every active repository has the files in the table below. Most of them are copied from [`templates/`](../../templates/) and personalized at the `TODO` markers.
- Code is licensed **Apache-2.0** by default; documentation and datasets **CC BY 4.0** when possible. Every exception is documented.
- The Code of Conduct is the **Contributor Covenant 3.0**.
- `CODEOWNERS` names the `maintainers` **team**, never individual people.
- Community health files (Code of Conduct, security policy, templates) MAY come from the organization `.github` repository, once it exists.

## Summary table

| File | Level | Template | Notes |
|---|---|---|---|
| `README.md` | 1 | [`templates/docs/README.md`](../../templates/docs/README.md) | FILE-001 |
| `LICENSE` | 1 | [Apache-2.0 text](https://www.apache.org/licenses/LICENSE-2.0.txt) | FILE-002, FILE-003 |
| `CONTRIBUTING.md` | 1 | [`templates/docs/CONTRIBUTING.md`](../../templates/docs/CONTRIBUTING.md) | FILE-004 |
| `CODE_OF_CONDUCT.md` | 1 | [`templates/docs/CODE_OF_CONDUCT.md`](../../templates/docs/CODE_OF_CONDUCT.md) | FILE-005 |
| `SECURITY.md` | 1 | [`templates/docs/SECURITY.md`](../../templates/docs/SECURITY.md) | FILE-006 |
| `CHANGELOG.md` | 1 | [`templates/docs/CHANGELOG.md`](../../templates/docs/CHANGELOG.md) | FILE-007 |
| `.github/CODEOWNERS` | 1 | [`templates/github/CODEOWNERS`](../../templates/github/CODEOWNERS) | FILE-008 |
| `.github/pull_request_template.md` | 1 | [`templates/github/pull_request_template.md`](../../templates/github/pull_request_template.md) | FILE-009 |
| `.github/ISSUE_TEMPLATE/*.yml` | 1 | [`templates/github/ISSUE_TEMPLATE/`](../../templates/github/ISSUE_TEMPLATE/) | FILE-010 |
| `.github/dependabot.yml` | 1 | [`templates/github/dependabot.yml`](../../templates/github/dependabot.yml) | FILE-011 |
| `.editorconfig` | 1 | [`templates/editor/editorconfig`](../../templates/editor/editorconfig) | FILE-012 |
| `.gitignore` | 1 | [`templates/git/gitignore`](../../templates/git/gitignore) | FILE-013 |
| `.gitattributes` | 1 | [`templates/git/gitattributes`](../../templates/git/gitattributes) | FILE-014 |
| `.env.example` | 1 | [`templates/env/env.example`](../../templates/env/env.example) | FILE-015 |
| `.pre-commit-config.yaml` | 1 | [`templates/pre-commit/`](../../templates/pre-commit/) | FILE-016 |
| `CITATION.cff` | 1 (research) | [`templates/docs/CITATION.cff`](../../templates/docs/CITATION.cff) | FILE-017 |
| `.git-blame-ignore-revs` | 1 (after a mass reformat) | [`templates/git/git-blame-ignore-revs`](../../templates/git/git-blame-ignore-revs) | FILE-018 |
| `sonar-project.properties` | 2 | see [SonarQube Cloud](sonar.md) | FILE-019 |

Templates file names have no leading dot (for example `gitignore`), so that they are visible in file browsers. Add the dot when you copy them.

## Rules

### FILE-001: `README.md` follows the DAH Labs template

**MUST** · Level 1 · Verified by: audit checklist (manual)

The README has, in this order:

1. Title and one-sentence description.
2. Badges: CI, SonarQube quality gate and coverage (Level 2), license, DAH Labs compliance level.
3. **Status** of the project: `experimental`, `active`, `maintained` or `archived`.
4. **Quick start**: the shortest path to see the project work (usually Docker Compose).
5. **Architecture**: one paragraph and one diagram (Mermaid), or a link to `docs/architecture.md`.
6. **Development**: install, run, test. Link to `CONTRIBUTING.md`.
7. **Contributing**, **License**, **Citation** (research repositories).
8. The line "A DAH Labs project — Data Afrique Hub".

The README is in English. Clone commands point to the organization repository, never to a personal fork.

- ✅ `git clone https://github.com/DAH-Projects-and-Innovations/baraza.git`
- ❌ `git clone https://github.com/<personal-account>/baraza.git`

### FILE-002: The repository has a `LICENSE` file that GitHub recognizes

**MUST** · Level 1 · Verified by: the license appears in the repository sidebar (`gh repo view --json licenseInfo`, automatic)

Copy the unmodified license text. GitHub detects the license only if the text is unchanged.

### FILE-003: Code is Apache-2.0 by default; documentation and data are CC BY 4.0; exceptions are documented

**MUST** · Level 1 · Verified by: `LICENSE` review and `license` field of `pyproject.toml` / `package.json` (manual)

| Content | Default license | Why |
|---|---|---|
| Source code | [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0) | Permissive, like MIT, **plus an explicit patent grant** and a patent retaliation clause that protect users and contributors |
| Documentation, reports | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | Free reuse with attribution |
| Datasets we create | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) when the data allows it | Free reuse with attribution |
| Model weights | Apache-2.0 or a license that is compatible with the training data | Depends on the data and base model licenses |

The open source policy of DAH Labs allows **exceptions**:

- personal or sensitive data;
- partner data covered by an agreement;
- commercial components of a product in incubation;
- risks of misuse (for example a model that could be used for surveillance).

Every exception is written in the README ("License" section) **and** in an ADR (`docs/adr/`) that says who decided, why and until when.

A dependency MUST have a license that is compatible with the license of the project. "Source-available" licenses (Business Source License, Server Side Public License, Elastic License 2.0) are not open source and need an ADR.

> ⚠️ **Team decision to validate:** the existing repositories mix MIT and Apache-2.0. Moving a repository from MIT to Apache-2.0 is allowed (MIT code can be included in an Apache-2.0 project), but the MIT notices of existing code MUST be kept. The team decides per repository; see [ADR 0007](../adr/0007-apache-2-0-default-license.md).

### FILE-004: `CONTRIBUTING.md` lets a newcomer set up the project in less than 10 minutes

**MUST** · Level 1 · Verified by: a new contributor follows it once per quarter and times it (manual)

It contains: prerequisites with versions, setup commands, how to run tests and linters, `pre-commit install`, the branch and commit conventions (with the list of scopes), how to open a PR, and where to ask questions. It links to these standards instead of copying them.

### FILE-005: `CODE_OF_CONDUCT.md` is the Contributor Covenant 3.0

**MUST** · Level 1 · Verified by: file present (automatic, GitHub community profile)

Use the [template](../../templates/docs/CODE_OF_CONDUCT.md), based on the [Contributor Covenant 3.0](https://www.contributor-covenant.org/version/3/0/code_of_conduct/). Replace the reporting contact marked `TODO`. Until the contact exists, the Code of Conduct is incomplete: people need a way to report a problem privately.

### FILE-006: `SECURITY.md` explains how to report a vulnerability privately

**MUST** · Level 1 · Verified by: file present and private vulnerability reporting enabled (automatic)

It says: do not open a public issue; use **Security → Report a vulnerability** (GitHub private vulnerability reporting); expected response time; supported versions. See [Security](security.md).

### FILE-007: `CHANGELOG.md` lists the notable changes of each version

**MUST** · Level 1 · Verified by: file present (manual)

At Level 1 the CHANGELOG MAY be written by hand in the [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format. At Level 2 it is generated by release-please from the commits (see [Releases](releases.md)) and nobody edits it by hand.

### FILE-008: `.github/CODEOWNERS` names a team, never a person

**MUST** · Level 1 · Verified by: CODEOWNERS errors are shown on the file page on GitHub (automatic); review (manual)

```text
# Default owners for everything in the repository.
*                       @DAH-Projects-and-Innovations/maintainers
```

- The team MUST have **write** access (or higher) to the repository; otherwise GitHub ignores the line.
- Never write individual user names. People change; teams stay.
- Sensitive paths (`.github/workflows/`, `SECURITY.md`) MAY have a second team, for example `@DAH-Projects-and-Innovations/security`, once it exists.

### FILE-009: `.github/pull_request_template.md` exists

**MUST** · Level 1 · Verified by: file present (automatic)

See [Pull requests](pull-requests.md#pr-001-every-pr-uses-the-template-and-fills-every-section).

### FILE-010: Issue forms exist for bugs, features and questions

**MUST** · Level 1 · Verified by: files present (automatic)

`.github/ISSUE_TEMPLATE/` contains `bug.yml`, `feature.yml`, `question.yml` and `config.yml` (which links to private vulnerability reporting and disables blank issues). `audit.yml` is used during [migration](../migration/playbook.md).

### FILE-011: `.github/dependabot.yml` covers every ecosystem of the repository

**MUST** · Level 1 · Verified by: Insights → Dependency graph → Dependabot (automatic)

See [Security](security.md#sec-002-dependabot-version-updates-run-weekly-and-are-grouped).

### FILE-012: `.editorconfig` sets the basic text style

**MUST** · Level 1 · Verified by: file present (manual)

UTF-8, LF line endings, final newline, 2 spaces by default, 4 spaces for Python.

### FILE-013: `.gitignore` covers Python, Node, ML outputs and secrets

**MUST** · Level 1 · Verified by: file present; `git status` is clean after a build and a test run (manual)

### FILE-014: `.gitattributes` normalizes line endings

**MUST** · Level 1 · Verified by: file present (manual)

`* text=auto eol=lf` avoids Windows line-ending changes in diffs. Lock files are marked `linguist-generated` so they are collapsed in PRs.

### FILE-015: `.env.example` lists every environment variable

**MUST** · Level 1 · Verified by: code review (manual)

Each variable has a comment and a safe example value. Never a real key. `.env` is in `.gitignore`.

### FILE-016: `.pre-commit-config.yaml` exists

**MUST** · Level 1 · Verified by: CI runs `pre-commit run --all-files` (automatic)

See [Git hooks](git-hooks.md).

### FILE-017: Research repositories have a `CITATION.cff` file

**MUST** · Level 1 · Verified by: "Cite this repository" button on GitHub (automatic)

GitHub reads [`CITATION.cff`](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files) and shows a citation in APA and BibTeX.

### FILE-018: A mass reformat commit is listed in `.git-blame-ignore-revs`

**SHOULD** · Level 1 · Verified by: code review (manual)

After a commit such as `style: apply ruff format`, add its full SHA to `.git-blame-ignore-revs`. GitHub's blame view then skips it, and so does local `git blame` after `git config blame.ignoreRevsFile .git-blame-ignore-revs`.

### FILE-019: `sonar-project.properties` configures the SonarQube Cloud analysis

**MUST** · Level 2 · Verified by: Sonar analysis in CI (automatic)

See [SonarQube Cloud](sonar.md).

## Checklist

- [ ] Every Level 1 file of the summary table exists.
- [ ] README has badges, status, quick start, architecture, development, license, and the DAH Labs line.
- [ ] Clone URLs point to the organization, not to a fork.
- [ ] `LICENSE` is recognized by GitHub; any exception is documented in the README and an ADR.
- [ ] The Code of Conduct reporting contact is filled.
- [ ] `CODEOWNERS` names a team that has write access.
- [ ] Research repositories have `CITATION.cff`.

---

*Last verified: 2026-11-13.*
