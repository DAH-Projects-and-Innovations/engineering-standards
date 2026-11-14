# Default branch migration: from `development` to `main`

## TL;DR

- Some repositories use `development` as default branch and `main` for releases. The standard is **one branch, `main`** ([GIT-001](../standards/git-branching.md#git-001-main-is-the-only-long-lived-branch-and-the-default-branch)).
- The migration renames `development` to `main`, with GitHub's **rename branch** feature, which retargets open PRs automatically.
- It takes about **30 minutes** of work and a **short freeze**, plus communication before and after.
- ⚠️ **Team decision:** this migration changes the daily work of every contributor. The team confirms it (in an issue or an ADR) before it starts.

## Before you start

**Prerequisites:**

- You are a repository **admin**.
- The team agreed, and the date is announced at least **one week** before, in a pinned issue and on every open PR.
- There is no release in progress.

**Check the relation between the two branches:**

```bash
git fetch origin
git log --oneline origin/development..origin/main   # commits only on main
git log --oneline origin/main..origin/development   # commits only on development
```

- If the first command prints **nothing**, `main` is behind `development`: go on.
- If it prints commits (for example hotfixes made directly on `main`), merge `main` into `development` first, with a normal PR from a branch (`chore/merge-main-into-development`), and wait for CI.

## Procedure

### 1. Save the old `main` (5 minutes)

```bash
git tag archive/main-before-migration origin/main
git push origin archive/main-before-migration
```

The tag keeps the old release history reachable forever.

### 2. Freeze merges

Comment in the pinned issue: "Merge freeze: default branch migration in progress".

### 3. Disable the ruleset during the operation

Rulesets may block the deletion or renaming of protected branches. In **Settings → Rules → Rulesets**, set the enforcement of the rulesets that target `main` or `development` to **Disabled** (do not delete them).

> ⚠️ To verify: whether a ruleset blocks a branch rename for admins depends on its rules. Disabling it for a few minutes is the safe option.

### 4. Delete the old `main`

Run:

```bash
git push origin --delete main
```

`main` is not the default branch, so GitHub allows it. Open PRs that targeted the old `main` (rare) are closed by GitHub: note their numbers first with `gh pr list --base main`, and reopen them on the new `main` later.

### 5. Rename `development` to `main`

On GitHub: **Code → Branches → `development` → ⋯ → Rename branch → `main`**.

GitHub then ([GitHub Docs: renaming a branch](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-branches-in-your-repository/renaming-a-branch)):

- retargets the open pull requests from `development` to `main`;
- updates branch protection rules that named the branch explicitly;
- keeps `main` as the default branch, because `development` was the default;
- redirects web links that contain the old branch name.

GitHub does **not** update: workflow files, Dependabot configuration, documentation, badges, local clones and rulesets that use an explicit `refs/heads/development` condition.

### 6. Fix and re-enable the ruleset

Edit the ruleset conditions: target `~DEFAULT_BRANCH` (or `refs/heads/main`) only, remove `development`. Follow [GH-002](../standards/github-settings.md#gh-002-a-ruleset-protects-main) and [GH-003](../standards/github-settings.md#gh-003-nobody-bypasses-the-ruleset-or-administrators-bypass-in-pull-request-only-mode). Set the enforcement back to **Active**.

### 7. Update the repository files (one PR)

```bash
git switch -c chore/use-main-as-only-branch origin/main
grep -rn "development" .github/ docs/ README.md CONTRIBUTING.md
```

Typical changes:

- `.github/workflows/*.yml`: `branches: [main, development]` → `branches: [main]`.
- `.github/dependabot.yml`: remove `target-branch: development` if present.
- `CONTRIBUTING.md`: "Branch off `development`" → "Branch off `main`"; remove the description of the two-branch model.
- README badges and links that contain `development`.

Title: `chore: use main as the only long-lived branch`.

### 8. End the freeze and tell everybody

Post this message in the pinned issue and on each open PR:

```markdown
The default branch is now `main`; `development` no longer exists.
Your open pull request was retargeted to `main` automatically.

Update your local clone once:

    git fetch origin --prune
    git switch development
    git branch -m development main
    git branch -u origin/main main
    git remote set-head origin -a
    git pull --ff-only

New branches start from `main`: git switch -c feat/42-my-change origin/main
```

## Rollback

If something goes wrong before step 7:

1. Rename `main` back to `development` (Code → Branches).
2. Recreate the old `main` from the tag: `git push origin archive/main-before-migration:refs/heads/main`.
3. Re-enable the original ruleset.

## Checklist

- [ ] The team confirmed the migration; the date was announced one week before.
- [ ] `main` had no commits missing from `development` (or they were merged first).
- [ ] The tag `archive/main-before-migration` exists on GitHub.
- [ ] `development` was renamed to `main`; open PRs now target `main`.
- [ ] The ruleset targets `~DEFAULT_BRANCH` only and is active again.
- [ ] Workflows, Dependabot, CONTRIBUTING and README no longer mention `development`.
- [ ] Contributors received the update commands.

---

*Last verified: 2026-11-13.*
