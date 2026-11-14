# Security

## TL;DR

- Turn on the free GitHub security features: **Dependabot** alerts, security updates and version updates; **secret scanning** with **push protection**; **CodeQL** default setup; **private vulnerability reporting**.
- No secret in the code or the Git history, ever. If a secret leaks: **revoke it first**, then clean up.
- Audit dependencies (`pip-audit`, `pnpm audit`, dependency review on PRs).
- Docker images run as a **non-root** user, from a pinned base image.
- **Never** put real personal data in the repository, the tests or the fixtures. Data protection laws apply (GDPR and African national laws).

Most features below are **free for public repositories**. For private repositories on GitHub Free, secret scanning, push protection, CodeQL and dependency review need paid GitHub security products: see [Private repositories](#private-repositories-on-github-free).

## Rules

### SEC-001: Dependabot alerts and security updates are enabled

**MUST** · Level 1 · Verified by: Settings → Advanced Security (automatic, `gh api repos/{owner}/{repo} --jq .security_and_analysis`)

- **Dependabot alerts:** GitHub warns when a dependency has a known vulnerability.
- **Dependabot security updates:** GitHub opens a PR that upgrades the vulnerable dependency.

### SEC-002: Dependabot version updates run weekly and are grouped

**MUST** · Level 1 · Verified by: `.github/dependabot.yml` review (manual)

The [template](../../templates/github/dependabot.yml) covers every ecosystem of a DAH Labs repository: `uv`, `npm` (also used for pnpm), `github-actions`, `docker` and `pre-commit`. Minor and patch updates are grouped into one PR per ecosystem and per week; major updates come one by one, because they can break the code.

```yaml
- package-ecosystem: uv
  directory: /backend
  schedule:
    interval: weekly
    day: monday
  commit-message:
    prefix: chore
    include: scope    # gives "chore(deps): bump ..."
  groups:
    minor-and-patch:
      update-types: [minor, patch]
```

Dependabot PRs follow Conventional Commits (`chore(deps): …`), so `pr-conventions.yml` accepts them, and their branch names (`dependabot/…`) are exempt from the branch name check.

**Why:** small, regular updates are easy. A year of updates at once is a project.

Review Dependabot PRs every week. Merge them when CI is green; for a major update, read the release notes first.

### SEC-003: Secret scanning and push protection are enabled

**MUST** · Level 1 · Verified by: Settings → Advanced Security (automatic); `security.yml` gitleaks job (automatic)

- **Secret scanning** finds known secret formats (API keys of OpenAI, AWS, Hugging Face…) in the whole history. It is free and automatic for public repositories ([GitHub Docs](https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning)).
- **Push protection** blocks a push that contains a secret.
- **gitleaks** runs in the pre-commit hook (staged changes) and in CI (full history), and also finds generic secrets.

### SEC-004: No secret is ever committed, and a leaked secret is revoked first

**MUST** · Level 1 · Verified by: gitleaks and secret scanning (automatic); code review (manual)

Secrets live in environment variables (`.env`, ignored by Git) on your machine and in GitHub secrets in CI. `.env.example` contains only fake values.

**If a secret is committed or pushed, even for one minute:**

1. **Revoke the secret immediately** in the provider's dashboard (OpenAI, Mistral, Hugging Face, database…), then create a new one. Do this **first**: bots scan GitHub for keys within minutes, and removing the commit does not remove copies that already exist (forks, clones, caches).
2. **Tell the maintainers** privately (not in a public issue): what leaked, when, and that it is revoked.
3. **Check the usage** logs of the provider for unknown activity.
4. **Clean the history** only if needed (for example personal data, or a secret that cannot be revoked): use [`git filter-repo`](https://github.com/newren/git-filter-repo) on a fresh clone, force-push after coordination with every contributor, and ask GitHub Support to remove cached views. For a revoked key, a cleaning commit that removes the key from the current files is usually enough.
5. **Add the fingerprint** of the revoked secret to `.gitleaksignore` with a comment, so that the history scan stays green.
6. **Write a short post-mortem** in the security tracking issue: how did it happen, and what prevents it next time.

### SEC-005: CodeQL code scanning uses the default setup

**MUST** · Level 2 · Verified by: Security → Code scanning shows CodeQL results (automatic)

Enable it in **Settings → Advanced Security → Code scanning → CodeQL analysis → Set up → Default**. GitHub detects Python and JavaScript/TypeScript, and runs the analysis on PRs, on `main` and every week.

**Why the default setup and not a workflow:** GitHub maintains the configuration and the CodeQL versions. There is no workflow file to update. A custom workflow is only needed for special build steps, which DAH Labs projects do not have.

### SEC-006: Pull requests are checked for vulnerable new dependencies

**MUST** · Level 2 · Verified by: `dependency-review` job of `security.yml` (automatic)

The job fails if a PR adds a dependency with a known vulnerability of severity `high` or more (input `fail-on-severity`).

### SEC-007: Locked dependencies are audited

**SHOULD** · Level 2 · Verified by: `python-audit` and `node-audit` jobs of `security.yml` (automatic)

Enable them with the inputs `python-working-directory` and `node-working-directory`. Locally:

```bash
uv export --frozen --no-emit-project --format requirements-txt > /tmp/req.txt
uvx pip-audit --strict --disable-pip -r /tmp/req.txt
pnpm audit --prod --audit-level high
```

`pnpm audit` was checked with pnpm 12.18.0 on 2026-11-13. It depends on the audit service of the npm registry; if the job fails because of that service (and not because of a vulnerability), rely on Dependabot alerts and dependency review, and open an issue in this repository.

### SEC-008: Private vulnerability reporting is enabled and `SECURITY.md` explains it

**MUST** · Level 1 · Verified by: `gh api repos/{owner}/{repo}/private-vulnerability-reporting` returns `"enabled": true` (automatic)

Enable it in **Settings → Advanced Security → Private vulnerability reporting**. The [`SECURITY.md` template](../../templates/docs/SECURITY.md) explains how to use it.

### SEC-009: Docker images run as non-root from a pinned base image

**MUST** · Level 2 · Verified by: hadolint (automatic); Dockerfile review (manual)

- Pin the base image by tag **and digest**: `FROM python:3.12-slim@sha256:…`. Dependabot (`docker` ecosystem) updates the digest.
- Use a multi-stage build: build tools stay in the build stage.
- Create and use an unprivileged user: `USER app`.
- Copy only what is needed (`.dockerignore`); never copy `.env`.
- The Dockerfile template is planned for the next version of these standards.

### SEC-010: No real personal data in the repository, tests or fixtures

**MUST** · Level 1 · Verified by: code review (manual)

DAH Labs projects handle meetings, health and nutrition questions, documents and voices. Personal data in a public repository is a data breach.

- Test data is **fictional**: invented names, invented meetings, generated texts. Say so in the fixture (`"fictional": true` or a header comment).
- Never commit exports of production databases, real transcripts, real recordings, screenshots with real names, or logs from real users.
- Datasets of real people are stored outside Git, with access control, and described in a dataset card (see [ML and research](ml-research.md)).
- Collect only the data you need, say why you collect it, and delete it when it is no longer needed.

Personal data of people in the European Union is covered by the **GDPR**. Many African countries also have data protection laws and authorities, for example (non-exhaustive):

| Country | Law |
|---|---|
| Benin | Law No. 2017-20 on the Digital Code (Book V, personal data) |
| Côte d'Ivoire | Law No. 2013-450 on the protection of personal data |
| Senegal | Law No. 2008-12 on the protection of personal data |
| Ghana | Data Protection Act, 2012 (Act 843) |
| Nigeria | Nigeria Data Protection Act, 2023 |
| Kenya | Data Protection Act, 2019 |

The African Union also adopted the **Malabo Convention** on cyber security and personal data protection (2014).

> ⚠️ To verify: this table is a starting point, not legal advice. Laws change. Before a project collects personal data, check the laws of the countries concerned with a qualified person, and record the decision in an ADR.

### SEC-011: Security fixes are merged quickly

**SHOULD** · Level 2 · Verified by: Security → Dependabot alerts age (manual)

| Severity | Fix within |
|---|---|
| Critical | 7 days |
| High | 30 days |
| Moderate and low | next planned update |

### SEC-012: Dependencies have licenses that are compatible with the project

**SHOULD** · Level 2 · Verified by: dependency review (automatic, with a license policy); code review (manual)

See [FILE-003](required-files.md#file-003-code-is-apache-20-by-default-documentation-and-data-are-cc-by-40-exceptions-are-documented). Watch out for "source-available" licenses.

### SEC-013: OpenSSF Scorecard measures the security practices

**SHOULD** · Level 3 · Verified by: Scorecard workflow results (automatic)

[OpenSSF Scorecard](https://github.com/ossf/scorecard) checks branch protection, pinned dependencies, token permissions, dangerous workflows and more. Copy [`templates/github/workflows/scorecard.yml`](../../templates/github/workflows/scorecard.yml). It is a standalone workflow, not a reusable one, because Scorecard rejects published results from workflows that do not follow [its restrictions](https://github.com/ossf/scorecard-action#workflow-restrictions).

## Private repositories on GitHub Free

The organization uses GitHub Free. For **private** repositories:

| Feature | Public repository | Private repository on GitHub Free |
|---|---|---|
| Dependabot alerts and updates | ✅ free | ✅ free |
| Secret scanning, push protection | ✅ free | ❌ needs GitHub Secret Protection (paid, Team or Enterprise) |
| CodeQL code scanning | ✅ free | ❌ needs GitHub Code Security (paid) |
| Dependency review | ✅ free | ❌ needs GitHub Code Security (paid) |
| Rulesets and branch protection | ✅ free | ❌ needs GitHub Team or higher |

Minimum for a private repository: Dependabot, **gitleaks** in pre-commit and in CI (`security.yml` with `scan-secrets: true`), `pip-audit` / `pnpm audit`, and code review. Prefer public repositories when the content allows it.

> ⚠️ To verify: the [GitHub for Nonprofits](https://docs.github.com/en/nonprofit) program offers a free GitHub Team plan to eligible nonprofit organizations. Check the eligibility of Data Afrique Hub and which security features the Team plan includes before relying on it.

## Checklist

- [ ] Dependabot alerts and security updates are enabled.
- [ ] `.github/dependabot.yml` covers `uv`, `npm`, `github-actions`, `docker` and `pre-commit` with weekly grouped updates.
- [ ] Secret scanning and push protection are enabled (public repositories).
- [ ] gitleaks runs in pre-commit and in CI; `.gitleaksignore` contains only revoked or fake values.
- [ ] Private vulnerability reporting is enabled and `SECURITY.md` explains it.
- [ ] CodeQL default setup is enabled (Level 2).
- [ ] `security.yml` runs dependency review on PRs (Level 2).
- [ ] Docker images use a pinned base image and a non-root user (Level 2).
- [ ] No real personal data in the repository, tests, fixtures, screenshots or notebooks.

---

*Last verified: 2026-11-13.*
