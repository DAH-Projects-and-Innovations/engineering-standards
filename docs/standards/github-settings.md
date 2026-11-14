# GitHub settings

## TL;DR

- **Repository:** default branch `main`, a **ruleset** that protects `main`, squash merge only, automatic deletion of merged branches, description and topics filled.
- **Bypass:** nobody bypasses the ruleset, or administrators bypass **in "pull request only" mode**, never "always".
- **Labels:** one standard set, defined in [`templates/github/labels.json`](../../templates/github/labels.json) and synchronized with a script.
- **Organization:** 2FA required (warn members first), base permission **Read**, teams instead of individuals, shared secrets at the organization level, read-only workflow token.
- The organization is on **GitHub Free**: rulesets work on public repositories only, and organization-wide rulesets are not available. Every rule below is applied **per repository**.

## Repository settings

### GH-001: The repository has a description, topics and a website

**MUST** · Level 1 · Verified by: `gh repo view --json description,repositoryTopics` (automatic)

```bash
gh repo edit DAH-Projects-and-Innovations/baraza \
  --description "Open source meeting minutes from transcripts, with the language model of your choice" \
  --add-topic dah-labs --add-topic llm --add-topic fastapi --add-topic nextjs
```

Every repository has the topic `dah-labs`, so the organization can list its projects.

### GH-002: A ruleset protects `main`

**MUST** · Level 1 · Verified by: Settings → Rules → Rulesets (automatic, `gh api repos/{owner}/{repo}/rulesets`)

The ruleset targets the default branch and enables:

| Rule | Value | Standard |
|---|---|---|
| Restrict deletions | on | GIT-002 |
| Block force pushes | on | GIT-002, GIT-008 |
| Require linear history | on | COM-007 |
| Require a pull request before merging | on | GIT-002 |
| ↳ Required approvals | **1** | PR-006 |
| ↳ Dismiss stale approvals when new commits are pushed | on | PR-010 |
| ↳ Require review from Code Owners | on | PR-006 |
| ↳ Require conversation resolution before merging | on | PR-009 |
| ↳ Allowed merge methods | **Squash** only | COM-007 |
| Require status checks to pass | on, with the CI checks | PR-008 |
| ↳ Require branches to be up to date before merging | off (squash merge and short branches make it unnecessary; turn it on if `main` breaks after merges) | |
| Require signed commits | Level 3 only | COM-010 |

**Apply it in one command** with the importable file [`templates/github/rulesets/main.json`](../../templates/github/rulesets/main.json):

```bash
# 1. Edit the "required_status_checks" list in main.json (see below).
# 2. Create the ruleset:
gh api --method POST repos/DAH-Projects-and-Innovations/<repo>/rulesets \
  --input templates/github/rulesets/main.json
```

You can also import the file in the web interface: **Settings → Rules → Rulesets → New ruleset → Import a ruleset**.

**Names of the required checks.** For a job that calls a reusable workflow, the check name is `<caller job id or name> / <job name in the reusable workflow>`, for example `backend / Python checks` or `conventions / PR title follows Conventional Commits`. Open a PR once, then copy the exact names from the "Checks" tab.

> ⚠️ To verify for each repository: the check names depend on the job names of your `ci.yml`. A wrong name blocks every PR, because the check never reports.

### GH-003: Nobody bypasses the ruleset, or administrators bypass in "pull request only" mode

**MUST** · Level 1 · Verified by: ruleset `bypass_actors` (automatic, `gh api repos/{owner}/{repo}/rulesets/{id} --jq .bypass_actors`)

- The safest choice is an **empty bypass list**.
- If an emergency path is needed, add the **Repository admin** role with bypass mode **"For pull requests only"** (`"bypass_mode": "pull_request"`). Admins can then merge a PR without approval in an emergency, but they can never push directly to `main`, force-push or delete it.
- Never use the mode **"Always"** (`"bypass_mode": "always"`): it turns every rule off for admins, including direct pushes.
- Every bypass is explained in the PR. GitHub records it in **Insights → Rule insights**.

### GH-004: Only squash merge is allowed, and the commit message comes from the PR

**MUST** · Level 1 · Verified by: `gh api repos/{owner}/{repo} --jq '{allow_squash_merge, allow_merge_commit, allow_rebase_merge, squash_merge_commit_title, squash_merge_commit_message}'` (automatic)

In **Settings → General → Pull Requests**:

- ✅ Allow squash merging, with **Default commit message: "Pull request title and description"**.
- ❌ Allow merge commits.
- ❌ Allow rebase merging.
- ✅ Always suggest updating pull request branches.

```bash
gh api --method PATCH repos/DAH-Projects-and-Innovations/<repo> \
  -F allow_squash_merge=true -F allow_merge_commit=false -F allow_rebase_merge=false \
  -f squash_merge_commit_title=PR_TITLE -f squash_merge_commit_message=PR_BODY \
  -F delete_branch_on_merge=true -F allow_update_branch=true
```

### GH-005: Merged branches are deleted automatically

**MUST** · Level 1 · Verified by: `delete_branch_on_merge` is `true` (automatic)

Set by the command of GH-004.

### GH-006: Issues are on, the wiki is off, Discussions are optional

**SHOULD** · Level 1 · Verified by: `gh repo view --json hasIssuesEnabled,hasWikiEnabled` (automatic)

- **Issues:** on. Issue forms guide the reporter (FILE-010).
- **Wiki:** off. Documentation lives in `docs/`, where it is reviewed and versioned.
- **Discussions:** MAY be turned on for questions and ideas, when somebody answers them.
- **Projects:** MAY be used for planning.

### GH-007: The repository uses the standard labels

**SHOULD** · Level 1 · Verified by: `gh label list` (automatic)

| Group | Labels |
|---|---|
| Type | `type: bug`, `type: feature`, `type: docs`, `type: refactor`, `type: test`, `type: chore`, `type: security`, `type: question`, `type: decision` |
| Priority | `priority: critical`, `priority: high`, `priority: medium`, `priority: low` |
| Status | `status: needs triage`, `status: blocked`, `status: in progress`, `status: needs info` |
| Size | `size: S`, `size: M`, `size: L` |
| Community | `good first issue`, `help wanted` |
| Review | `needs-2-reviews` |
| Process | `compliance-audit`, `dependencies` |

`good first issue` and `help wanted` keep their GitHub names, because GitHub and other sites use them to show issues to new contributors. Repositories MAY add `area: …` labels (for example `area: llm`, `area: frontend`).

**Synchronize** with the script of this repository (it needs `gh` and Python, and only creates or updates labels; it never deletes):

```bash
python scripts/sync_labels.py DAH-Projects-and-Innovations/<repo>
python scripts/sync_labels.py DAH-Projects-and-Innovations/<repo> --dry-run   # preview
```

## Organization settings

These settings are changed by an **organization owner**.

### GH-008: Two-factor authentication is required for every member

**MUST** · Level 1 · Verified by: `gh api orgs/DAH-Projects-and-Innovations --jq .two_factor_requirement_enabled` returns `true` (automatic)

**Warn members before you turn it on.** When an owner enables **Settings → Authentication security → Require two-factor authentication**, GitHub **removes from the organization every member and outside collaborator who does not use 2FA** ([GitHub Docs](https://docs.github.com/en/organizations/keeping-your-organization-secure/managing-two-factor-authentication-for-your-organization/requiring-two-factor-authentication-in-your-organization)). They lose access to private repositories and their forks of private repositories.

1. List members without 2FA: **People → filter "2FA: Disabled"** or `gh api "orgs/DAH-Projects-and-Innovations/members?filter=2fa_disabled" --jq '.[].login'`.
2. Send them a message with a deadline (for example 2 weeks) and the [GitHub guide to configure 2FA](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication). Recommend an authenticator app or a passkey.
3. Repeat the message a few days before the deadline.
4. Enable the requirement. Removed members can be invited again after they enable 2FA; GitHub keeps their access settings for 3 months.

### GH-009: The base permission is Read and access is given through teams

**MUST** · Level 1 · Verified by: `gh api orgs/DAH-Projects-and-Innovations --jq .default_repository_permission` returns `read` (automatic)

| Team | Repository role | Who |
|---|---|---|
| `maintainers` | **Maintain** (or Write) on the repositories they maintain | Core team that reviews and merges |
| `contributors` | **Triage** or Write | Regular volunteers |
| `security` (optional) | Write | People who handle vulnerability reports |

Occasional contributors work from a fork and need no role.

### GH-010: The CODEOWNERS team has write access

**MUST** · Level 1 · Verified by: no error shown on the CODEOWNERS file page (automatic)

GitHub ignores a CODEOWNERS line when the team does not have at least **Write** access. The team `@DAH-Projects-and-Innovations/maintainers` must be created and given Write (or Maintain) on each repository. Team visibility must be **visible**.

### GH-011: Shared secrets are organization secrets with selected repositories

**SHOULD** · Level 2 · Verified by: Settings → Secrets and variables → Actions (manual)

`SONAR_TOKEN` is created once at the organization level, with **Repository access: Selected repositories**.

### GH-012: The workflow token is read-only by default

**MUST** · Level 1 · Verified by: Settings → Actions → General → Workflow permissions (manual)

- **Workflow permissions:** "Read repository contents and packages permissions". Each workflow asks for more when it needs it (CI-004).
- **Allow GitHub Actions to create and approve pull requests:** off. Turn it on only for repositories that use release-please **without** the GitHub App (see [REL-005](releases.md#rel-005-the-release-pr-is-opened-with-a-github-app-token)).
- **Fork pull request workflows from outside collaborators:** "Require approval for first-time contributors" (or stricter).
- **Allowed actions:** "Allow all actions and reusable workflows" is acceptable while every workflow pins actions by SHA (CI-005). A stricter policy (GitHub, verified creators and a list of selected actions) is better.

> ⚠️ To verify: GitHub added options to the "Allowed actions" policy in 2025 (blocking actions, requiring SHA pinning). Check the current options in the organization settings before you choose.

## Private repositories and GitHub Free

On GitHub Free, rulesets and branch protection are **not available on private repositories**. For a private repository:

- prefer making it public if the content allows it;
- otherwise, give Write access only to the `maintainers` team, ask everyone else to work from forks, and rely on CI and review discipline;
- apply for the [GitHub Team plan for nonprofits](https://docs.github.com/en/nonprofit/nonprofit-teams-plan/getting-started-with-the-github-team-plan-for-nonprofits) (⚠️ eligibility to verify), which adds rulesets and protected branches for private repositories.

## The organization `.github` repository

A special public repository named `.github` provides default community health files (Code of Conduct, security policy, issue and PR templates) to every repository that does not have its own, and `profile/README.md` is shown on the organization page. It also holds **workflow templates**, proposed in "Actions → New workflow". The files and the setup commands are in [`org-defaults/`](../../org-defaults/README.md).

## Checklist

### Repository

- [ ] Description, topics (including `dah-labs`) and website are filled.
- [ ] A ruleset on `main` is active, imported from `templates/github/rulesets/main.json`, with the right check names.
- [ ] The bypass list is empty, or admins only in "pull request only" mode.
- [ ] Only squash merge is allowed; the default message is "Pull request title and description".
- [ ] Automatic deletion of head branches is on.
- [ ] Wiki is off; issues are on.
- [ ] Standard labels are synchronized.

### Organization

- [ ] Members were warned, then 2FA was required.
- [ ] Base permission is Read; teams `maintainers` (and `contributors`) exist.
- [ ] The `maintainers` team has Write or Maintain on every repository where it is a code owner.
- [ ] Workflow permissions are read-only by default.
- [ ] `SONAR_TOKEN` is an organization secret with selected repositories (Level 2).

---

*Last verified: 2026-11-13.*
