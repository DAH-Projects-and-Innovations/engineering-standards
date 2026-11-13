# DAH Labs engineering standards

The engineering rules, templates and reusable CI workflows of every repository of [DAH Labs](https://github.com/DAH-Projects-and-Innovations), the AI laboratory of Data Afrique Hub.

[![CI](https://github.com/DAH-Projects-and-Innovations/engineering-standards/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/DAH-Projects-and-Innovations/engineering-standards/actions/workflows/ci.yml)
[![Reusable workflows](https://github.com/DAH-Projects-and-Innovations/engineering-standards/actions/workflows/example-integration.yml/badge.svg?branch=main)](https://github.com/DAH-Projects-and-Innovations/engineering-standards/actions/workflows/example-integration.yml)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

> 🇫🇷 **Francophone contributors:** start with the [French getting started page (Démarrage)](docs/getting-started/demarrage-fr.md). The rest of the documentation is in simple English.

## Why these standards

DAH Labs wants to become, by 2036, an African AI laboratory of world reference. Our repositories are public: they must show clean code, a clear architecture, measured quality, reliable CI, reproducible research and good security. Most contributors are volunteers, in different countries and time zones, with different levels of experience. These standards give everybody the same simple rules, the tools that check them automatically, and files ready to copy.

Everything works **without infrastructure and without cost**: GitHub (Actions with hosted runners, Pages, Packages) and free services for public open source projects.

## How to use this repository

| You want to… | Go to |
|---|---|
| Contribute for the first time | [First day](docs/getting-started/first-day.md) · [Tools installation](docs/getting-started/tools-installation.md) · [First contribution](docs/getting-started/first-contribution.md) |
| Know the rules | [Standards](#standards) below, and the [rules matrix](docs/compliance/rules-matrix.md) |
| Start a new repository | [Repository structure](docs/standards/repository-structure.md), [Required files](docs/standards/required-files.md) and [`templates/`](templates/README.md) |
| Bring an existing repository up to the standards | [Migration playbook](docs/migration/playbook.md) and [audit checklist](docs/migration/audit-checklist.md) |
| Use the shared CI | [CI/CD](docs/standards/ci-cd.md) and [`templates/github/workflows/ci.yml`](templates/github/workflows/ci.yml) |
| Change a rule | [CONTRIBUTING.md](CONTRIBUTING.md) |

## Standards

Each rule has a stable ID, a requirement keyword ([RFC 2119](https://www.rfc-editor.org/rfc/rfc2119): MUST, SHOULD, MAY), a [compliance level](docs/compliance/levels.md), a reason, a verification method and examples.

| Topic | Page | Rule IDs |
|---|---|---|
| Branches | [Git branching](docs/standards/git-branching.md) | `GIT-*` |
| Commit messages | [Commits](docs/standards/commits.md) | `COM-*` |
| Pull requests | [Pull requests](docs/standards/pull-requests.md) | `PR-*` |
| Reviews | [Code review](docs/standards/code-review.md) | `REV-*` |
| Python | [Python](docs/standards/python.md) | `PY-*` |
| TypeScript | [JavaScript and TypeScript](docs/standards/javascript.md) | `JS-*` |
| Layout | [Repository structure](docs/standards/repository-structure.md) | `REPO-*` |
| Files | [Required files](docs/standards/required-files.md) | `FILE-*` |
| Hooks | [Git hooks](docs/standards/git-hooks.md) | `HOOK-*` |
| CI/CD | [CI/CD with GitHub Actions](docs/standards/ci-cd.md) | `CI-*` |
| Security | [Security](docs/standards/security.md) | `SEC-*` |
| GitHub | [GitHub settings](docs/standards/github-settings.md) | `GH-*` |
| Onboarding | [First day](docs/getting-started/first-day.md) | `ONB-*` |
| Levels | [Compliance levels](docs/compliance/levels.md) | `LVL-*` |

**Planned for the next version** (pages already exist with their scope): [Architecture](docs/standards/architecture.md), [Clean code](docs/standards/clean-code.md), [Testing](docs/standards/testing.md), [SonarQube Cloud](docs/standards/sonar.md), [Releases](docs/standards/releases.md), [ML and research](docs/standards/ml-research.md), [Documentation](docs/standards/documentation.md).

Other pages: [Glossary](docs/glossary.md) · [Architecture Decision Records](docs/adr/README.md) · [Documentation index](docs/README.md).

## Compliance levels

| Level | For | Badge |
|---|---|---|
| **1 · Foundation** | Every active repository (about 1 week of work) | [![Level 1](https://img.shields.io/badge/DAH%20Labs%20standards-Level%201%20Foundation-cd7f32)](docs/compliance/levels.md) |
| **2 · Standard** | Flagship projects | [![Level 2](https://img.shields.io/badge/DAH%20Labs%20standards-Level%202%20Standard-c0c0c0)](docs/compliance/levels.md) |
| **3 · Excellence** | Recommended | [![Level 3](https://img.shields.io/badge/DAH%20Labs%20standards-Level%203%20Excellence-ffd700)](docs/compliance/levels.md) |

### Flagship projects

The DAH Labs team decides which projects must reach Level 2 (rule LVL-002). Current list:

- TODO: list to be decided by the DAH Labs team.

## What is in this repository

```text
engineering-standards/
├── docs/
│   ├── getting-started/   # first day, tools, first contribution, French page
│   ├── standards/         # the rules, one page per topic
│   ├── compliance/        # levels and rules matrix
│   ├── migration/         # playbook, audit checklist, default branch migration
│   ├── adr/               # decisions about these standards
│   └── glossary.md
├── templates/             # files ready to copy into a project (TODO markers to personalize)
├── .github/workflows/     # reusable workflows (python-ci, node-ci, pr-conventions, pre-commit, security)
│                          # and the CI of this repository
├── .pre-commit-hooks.yaml # the dah-branch-name hook, usable from any repository
├── hooks/                 # code of the hooks
├── scripts/               # rules matrix generator, label sync, read-only audit
└── tests/                 # tests of the hooks and fixtures that test the reusable workflows
```

The documentation is plain Markdown with relative links: read it on GitHub. A documentation website can be added later without rewriting the pages.

## Use the reusable workflows

```yaml
jobs:
  backend:
    uses: DAH-Projects-and-Innovations/engineering-standards/.github/workflows/python-ci.yml@v1
    with:
      working-directory: backend
```

`@v1` follows the latest `1.x.y` release, which never contains breaking changes. See [CI/CD](docs/standards/ci-cd.md) for every workflow and its inputs. The workflows are tested on every change by [`example-integration.yml`](.github/workflows/example-integration.yml).

## Contributing

These standards change through pull requests, like code. Read [CONTRIBUTING.md](CONTRIBUTING.md): small fixes go through a normal PR; new or changed rules need a short proposal and an ADR.

Please follow the [Code of Conduct](CODE_OF_CONDUCT.md). Report security problems as explained in [SECURITY.md](SECURITY.md).

## License

Code (workflows, scripts, hooks, templates) is licensed under the [Apache License 2.0](LICENSE). Documentation in `docs/` is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

---

A [DAH Labs](https://github.com/DAH-Projects-and-Innovations) project — Data Afrique Hub.
