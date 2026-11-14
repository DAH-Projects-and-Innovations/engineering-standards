# First contribution

## TL;DR

- **Fork** the repository if you are not a member of the organization; **clone** it directly if you are.
- Create a branch from `main` named `<type>/<issue>-<description>`.
- Make small commits with Conventional Commits messages; the hooks check them.
- Push, open a **draft** pull request, fill the template, wait for green CI, then click **Ready for review**.
- Answer the review, push fixes, and a maintainer squash merges.

## 1. Fork or clone?

| You are… | Do this |
|---|---|
| Not a member of DAH-Projects-and-Innovations | **Fork**: on the repository page, click **Fork**. You work in your copy and open PRs to the original. |
| A member with write access | **Clone** the organization repository directly. Never push to `main` (it is protected). |

```bash
# Fork (replace <your-account>):
gh repo fork DAH-Projects-and-Innovations/baraza --clone
cd baraza
# gh adds the original repository as the "upstream" remote.

# Or clone directly (members):
git clone git@github.com:DAH-Projects-and-Innovations/baraza.git
cd baraza
```

## 2. Install the project and the hooks

Follow the project's `CONTRIBUTING.md`. It usually looks like this:

```bash
cd backend && uv sync && uv run pytest && cd ..
cd frontend && pnpm install && pnpm test && cd ..
uvx pre-commit install
```

If a test fails **before** you change anything, tell the maintainers in the issue: it is not your fault.

## 3. Create a branch

```bash
git switch main
git pull --ff-only            # with a fork: git pull --ff-only upstream main
git switch -c fix/57-chunker-overlap
```

The name follows `<type>/<issue-number>-<short-description>` ([GIT-003](../standards/git-branching.md#git-003-branch-names-follow-typeissue-number-short-description)).

## 4. Change, test, commit

```bash
# edit the code, add a test
uv run pytest tests/unit/test_basic_chunker.py
git add -p                     # review each change before you stage it
git commit -m "fix(chunker): keep the overlap between consecutive chunks"
```

The hooks run on `git commit`. If a hook **modifies** files (formatting), run `git add -u` and commit again. If it **rejects** your message, read the error: usually the type is missing or the description starts with a capital letter.

## 5. Push and open a draft pull request

```bash
git push -u origin fix/57-chunker-overlap
gh pr create --draft --fill
```

Then, on GitHub:

1. Write the **title** in the Conventional Commits format: it becomes the commit message on `main`.
2. Fill **every section** of the template. Write `Closes #57`.
3. Wait for CI. If a check is red, open it, read the log, fix and push again.
4. Click **Ready for review**.

## 6. The review

- A maintainer answers within about 2 working days.
- Comments start with `blocking:`, `suggestion:`, `question:`, `nit:` or `praise:` ([Code review](../standards/code-review.md)). Only `blocking:` comments must be fixed.
- Answer every comment, even with "Done" or "I prefer to keep it because…".
- Push fixes as new commits: the PR is squash merged, so you do not need to rewrite history.

## 7. After the merge

```bash
git switch main
git pull --ff-only
git branch -d fix/57-chunker-overlap
```

Congratulations, and thank you! Choose your next issue.

## Checklist

- [ ] I forked or cloned the repository and installed it.
- [ ] `uvx pre-commit install` is done.
- [ ] My branch name follows the convention.
- [ ] My PR title follows Conventional Commits, and the template is filled.
- [ ] CI is green and I clicked **Ready for review**.
- [ ] I answered every review comment.

---

*Last verified: 2026-11-13.*
