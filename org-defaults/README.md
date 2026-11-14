# Organization defaults (the `.github` repository)

## TL;DR

- GitHub uses a public repository named **`.github`** in the organization for two things: the **organization profile** (`profile/README.md`, shown on the organization page) and **default community health files** for every repository that does not have its own.
- It also offers **workflow templates**: "Actions → New workflow" in any repository proposes the DAH Labs CI and release workflows.
- This folder contains the files that exist only there. The other files are copied from [`templates/`](../templates/README.md), so that there is one source for each.
- An organization owner creates the repository once and copies the files with the commands below.

Rules: [GitHub settings](../docs/standards/github-settings.md#the-organization-github-repository). Reference: [GitHub Docs: creating a default community health file](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file).

## What the `.github` repository contains

```text
.github/                         # the repository, named ".github"
├── profile/
│   └── README.md                # organization page (from org-defaults/profile/)
├── CODE_OF_CONDUCT.md           # default for every repository (from templates/docs/)
├── CONTRIBUTING.md              # short: links to the engineering standards
├── SECURITY.md                  # default security policy (from templates/docs/)
├── SUPPORT.md                   # where to ask questions
├── .github/
│   ├── pull_request_template.md # default PR template (from templates/github/)
│   └── ISSUE_TEMPLATE/          # default issue forms (from templates/github/ISSUE_TEMPLATE/)
└── workflow-templates/          # proposed in "Actions → New workflow" (from org-defaults/)
    ├── dah-ci.yml  dah-ci.properties.json
    └── dah-release.yml  dah-release.properties.json
```

Default files apply only to repositories that have **no** file of the same kind. A repository's own file always wins. Defaults are not copied into the repositories: a contributor who clones a repository does not get them, so Level 1 still requires the [required files](../docs/standards/required-files.md) in each repository.

## Create it (organization owner, once)

```bash
# 1. Create the public repository (it MUST be public for the defaults to work).
gh repo create DAH-Projects-and-Innovations/.github --public \
  --description "Default community health files and profile of DAH Labs"
git clone https://github.com/DAH-Projects-and-Innovations/.github.git dah-github
STD=/path/to/engineering-standards   # TODO: your clone of this repository
cd dah-github

# 2. Copy the files.
mkdir -p profile .github/ISSUE_TEMPLATE workflow-templates
cp "$STD/org-defaults/profile/README.md" profile/README.md
cp "$STD/templates/docs/CODE_OF_CONDUCT.md" CODE_OF_CONDUCT.md
cp "$STD/templates/docs/SECURITY.md" SECURITY.md
cp "$STD/templates/github/pull_request_template.md" .github/pull_request_template.md
cp "$STD"/templates/github/ISSUE_TEMPLATE/*.yml .github/ISSUE_TEMPLATE/
cp "$STD"/org-defaults/workflow-templates/* workflow-templates/

# 3. Write CONTRIBUTING.md and SUPPORT.md (see below), replace every TODO, then commit.
grep -rn TODO .
```

`CONTRIBUTING.md` of the `.github` repository can be three lines:

```markdown
# Contributing to DAH Labs

Every DAH Labs repository follows the [DAH Labs engineering standards](https://github.com/DAH-Projects-and-Innovations/engineering-standards).
Start with the [first day guide](https://github.com/DAH-Projects-and-Innovations/engineering-standards/blob/main/docs/getting-started/first-day.md), then read the CONTRIBUTING.md of the repository.
```

`SUPPORT.md` says where to ask questions: the **Question** issue form of the repository, or GitHub Discussions when the repository has them.

Then apply the same settings as any repository: a `main` ruleset, squash merge only, and `CODEOWNERS` with the `maintainers` team.

## Keep it up to date

The workflow templates in this folder are copies of [`templates/github/workflows/ci.yml`](../templates/github/workflows/ci.yml) and [`release.yml`](../templates/github/workflows/release.yml); a test of this repository checks that they stay identical. After a release of the engineering standards that changes a copied file, copy it again into the `.github` repository.

## Checklist

- [ ] The public repository `DAH-Projects-and-Innovations/.github` exists.
- [ ] `profile/README.md` lists public projects only, with no TODO left.
- [ ] Default `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CONTRIBUTING.md` and `SUPPORT.md` are at its root, with real contact addresses.
- [ ] The default PR template and issue forms are in its `.github/` folder.
- [ ] "Actions → New workflow" in a repository of the organization shows "DAH Labs CI" and "DAH Labs release".

---

*Last verified: 2026-11-14.*
