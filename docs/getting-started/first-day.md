# First day

## TL;DR

- This is the path for a new contributor, from zero to a first merged pull request.
- **Morning:** install the tools and configure Git and GitHub (about 1 hour).
- **Afternoon:** read the essential standards (about 1 hour), set up one project and make a first small contribution.
- You do not need to know everything. Ask questions: there are no stupid questions.
- Francophone contributors: see also the [French getting started page](demarrage-fr.md).

## Your first day, step by step

| # | Step | Time | Link |
|---|---|---|---|
| 1 | Install Git, uv, Node.js + pnpm, Docker, `gh` | 30–45 min | [Tools installation](tools-installation.md) |
| 2 | Configure Git (name, e-mail, SSH key, commit signing) and enable 2FA on GitHub | 15 min | [Configure Git](tools-installation.md#4-configure-git) |
| 3 | Read the five essential pages | 1 h | below |
| 4 | Choose a project and a `good first issue` | 15 min | [Organization repositories](https://github.com/orgs/DAH-Projects-and-Innovations/repositories) |
| 5 | Fork or clone, install, run the tests | 15–30 min | the project's `CONTRIBUTING.md` |
| 6 | Make your first pull request | 1–2 h | [First contribution](first-contribution.md) |

### The five essential pages

1. [Git branching](../standards/git-branching.md): one branch `main`, short branches named `feat/42-…`.
2. [Commits](../standards/commits.md): `type(scope): description`.
3. [Pull requests](../standards/pull-requests.md): small, with the template filled.
4. [Code review](../standards/code-review.md): how to give and receive comments.
5. [Git hooks](../standards/git-hooks.md): `uvx pre-commit install`, then the tools check your work automatically.

Keep the [glossary](../glossary.md) open: it explains words like *ruleset*, *linter* or *quality gate*.

## Rules for maintainers

These rules help maintainers welcome new contributors.

### ONB-001: Each repository keeps a few well-described `good first issue` issues

**SHOULD** · Level 1 · Verified by: `gh issue list --label "good first issue"` returns at least 3 open issues (manual)

A good first issue says: the context, what to change, which files are concerned, how to test, and who can help. It takes less than one day.

**Example:**

- ✅ "Add a test for `BasicChunker` when the text is shorter than `chunk_size`. File: `tests/unit/test_basic_chunker.py`. Expected: one chunk with the whole text. Run `uv run pytest tests/unit/test_basic_chunker.py`."
- ❌ "Improve the tests."

### ONB-002: First-time contributors get an answer within 2 working days

**SHOULD** · Level 1 · Verified by: monthly review of open issues and PRs from first-time contributors (manual)

Thank them, answer their question, and point them to the right page of these standards. GitHub shows a "First-time contributor" label on their PRs.

### ONB-003: Contributors use a configured Git identity and two-factor authentication

**MUST** · Level 1 · Verified by: commits show a GitHub account (manual); organization 2FA requirement (automatic, GH-008)

Commits are linked to a GitHub account through the e-mail address (a noreply address is fine). Every member of the organization uses two-factor authentication.

### ONB-004: Contributor setup is tested by a newcomer every quarter

**SHOULD** · Level 2 · Verified by: audit issue mentions the test (manual)

Once per quarter, a new or occasional contributor follows `CONTRIBUTING.md` from zero and reports the time it took and the problems found. Goal: less than 10 minutes (FILE-004).

## Checklist

- [ ] My tools pass the [check commands](tools-installation.md#7-check-everything).
- [ ] Git is configured; my SSH key is on GitHub; 2FA is enabled.
- [ ] I read the five essential pages.
- [ ] I chose a `good first issue` and said in a comment that I work on it.
- [ ] `uvx pre-commit install` is done in my clone.
- [ ] My first pull request is open.

---

*Last verified: 2026-11-13.*
