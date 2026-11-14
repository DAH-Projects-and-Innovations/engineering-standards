# Code review

## TL;DR

- Code review is how we share knowledge and catch problems early. It is a conversation between colleagues, not an exam.
- Review within **2 working days**. Volunteers have other jobs: say so if you cannot.
- Check correctness, tests, security and readability first; style is the job of the tools.
- Prefix every comment: `blocking:`, `suggestion:`, `question:`, `nit:` or `praise:`.
- The author is responsible for every line, including code written with an AI assistant.

## What to check, in order

1. **Purpose:** does the PR do what the issue asks? Is there a simpler way?
2. **Correctness:** edge cases, error handling, concurrency, empty inputs, encodings (French accents, non-Latin scripts).
3. **Tests:** is new behavior tested? Do the tests fail without the change? Are LLM and embedding calls mocked?
4. **Security and privacy:** no secret, no real personal data, input validation, no new permission without reason.
5. **Architecture:** does the code respect the layers (see [Architecture](architecture.md))? Does a new dependency make sense, and is its license compatible?
6. **Readability:** names, function size, comments that explain *why*.
7. **Documentation:** README, docstrings, ADR for a structuring decision, CHANGELOG through the PR title.

Formatting, import order and simple bugs are checked by Ruff, ESLint and Prettier. Do not comment on them by hand: if the tools do not catch something you care about, propose a rule change instead.

## Rules

### REV-001: A first review happens within 2 working days

**SHOULD** · Level 1 · Verified by: monthly review of open PRs (manual)

When a PR is marked **Ready for review**, a code owner gives a first review within 2 working days. If you cannot, write "I will look at this on Friday" or ask another maintainer.

**Why:** a contributor who waits a week for feedback often does not come back.

### REV-002: The reviewer follows the review order above

**MUST** · Level 1 · Verified by: code review (manual)

A review that only says "LGTM" on a 300-line PR is not a review. If you approve, you share the responsibility for the change.

### REV-003: Every comment has a prefix

**SHOULD** · Level 1 · Verified by: code review (manual)

| Prefix | Meaning | Must the author act? |
|---|---|---|
| `blocking:` | Must change before merge (bug, security, broken rule) | Yes |
| `suggestion:` | A better way; the author decides | No, but answer |
| `question:` | The reviewer wants to understand | Answer |
| `nit:` | Small detail (naming, wording) | No |
| `praise:` | Something done well | No |

**Why:** without a prefix, a new contributor cannot tell an order from an idea, and treats every comment as blocking.

**Examples:**

- ✅ `blocking: this logs the full request, which contains the API key. Please log only the provider name.`
- ✅ `question: why a list here and not a set? Order does not seem to matter.`
- ✅ `nit: "docs" would read better than "documents_list".`
- ✅ `praise: the contract test for every IVectorStore implementation is great.`
- ❌ `This is wrong.`
- ❌ `Why would you do that??`

### REV-004: Comments are kind and about the code

**MUST** · Level 1 · Verified by: Code of Conduct (manual)

- Talk about the code, not the person: "this function" rather than "you".
- Explain **why**, and propose a solution when you can.
- Use the GitHub **Add a suggestion** button for small changes: the author applies it in one click.
- Assume good intent. Many contributors write in their second or third language.
- Thank the author. Say what is good, not only what is wrong.

**Why:** DAH Labs depends on volunteers. A harsh review costs us a contributor; a kind review creates a maintainer.

### REV-005: "Request changes" is only for blocking problems

**SHOULD** · Level 1 · Verified by: code review (manual)

Use **Comment** for questions and suggestions, **Request changes** only when at least one `blocking:` comment exists, and **Approve** when only `nit:` or `suggestion:` comments remain.

### REV-006: The person who opens a conversation resolves it

**SHOULD** · Level 1 · Verified by: code review (manual)

The author answers or pushes a fix, then the reviewer marks the conversation as resolved. The author MAY resolve `nit:` and `praise:` comments.

### REV-007: The author understands every line, including AI-generated code

**MUST** · Level 1 · Verified by: code review (manual)

AI assistants are allowed. The author MUST be able to explain every line of the PR, and MUST check that generated code respects these standards, does not copy code under an incompatible license and does not invent APIs. Say in the PR description when a large part was generated.

**Why:** the reviewer reviews the author's work. Responsibility cannot be delegated to a tool.

### REV-008: Reviewers run the code for non-trivial changes

**MAY** · Level 2 · Verified by: code review (manual)

For a behavior change, check out the branch (`gh pr checkout 64`) and follow the "How to test" section of the PR.

## Checklist

- [ ] Every open PR marked "Ready for review" had a first review within 2 working days.
- [ ] Review comments use the prefixes.
- [ ] "Request changes" was used only with at least one `blocking:` comment.
- [ ] The author answered every comment before merge.

---

*Last verified: 2026-11-13.*
