# Contributing to the DAH Labs engineering standards

Thank you for helping us improve these standards. They belong to everybody who works on DAH Labs repositories: if a rule is unclear, wrong or too hard to follow, please tell us.

By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Kinds of changes

| Change | Example | Process |
|---|---|---|
| **Fix** | Typo, broken link, clearer example, outdated version number | Normal pull request |
| **Template or workflow improvement** without new rule | New input in `python-ci.yml`, better comment in a template | Pull request with tests (fixtures) |
| **New rule, changed rule, removed rule** | "Require Vitest at Level 1" | **Proposal** (below) |
| **Structuring decision** | Change of tool, of license, of branch model | Proposal **and** ADR |

## The proposal process (lightweight RFC)

1. **Open an issue** with the "Rule change proposal" form. Explain the problem, the proposed rule, its level, how it is verified, and its cost for existing repositories.
2. **Discuss** for at least **5 working days**, so that volunteers in every time zone can answer.
3. **Open a pull request** that:
   - changes the standards page (rule with ID, keyword, level, verification, examples);
   - adds an ADR in `docs/adr/` when the decision is structuring (start from [`0000-template.md`](docs/adr/0000-template.md), status `proposed`);
   - updates the templates and reusable workflows if needed;
   - regenerates the rules matrix (`python scripts/generate_rules_matrix.py`; the pre-commit hook does it for you).
4. **Approval:** 2 maintainers approve. The ADR status becomes `accepted` in the same PR.
5. **Release:** the change is published in the next version of the standards (see "Versions" below).

### Rule IDs

- An ID is **never reused**. A removed rule keeps its ID in the CHANGELOG; new rules get the next free number.
- A rule moves between levels by a proposal, never silently.

## Versions

The standards use Semantic Versioning and the history is in [CHANGELOG.md](CHANGELOG.md).

| Change | Version |
|---|---|
| Fix, clarification, new MAY rule, new Level 3 rule, new optional input of a workflow | patch or minor |
| New SHOULD rule, new reusable workflow | minor |
| New MUST rule at Level 1 or 2, removed workflow input, breaking change in a reusable workflow | **major** (`v2`), with a migration note |

Projects call the reusable workflows with the moving major tag (`@v1`), so a breaking change never reaches them without their decision.

## Set up this repository

```bash
git clone https://github.com/DAH-Projects-and-Innovations/engineering-standards.git
cd engineering-standards
uvx pre-commit install
uvx pre-commit run --all-files       # markdownlint, yamllint, actionlint, lychee (offline), ruff, ...
uv run --no-project --with pytest pytest tests/hooks
```

Requirements: Git, [uv](https://docs.astral.sh/uv/), and Node.js (used by the markdownlint hook). To test the fixtures:

```bash
cd tests/fixtures/python-minimal && uv sync && uv run pytest && cd -
cd tests/fixtures/node-minimal && pnpm install && pnpm test && cd -
```

## Writing style

- **Plain English:** short sentences, simple words, no idioms, the same word for the same thing. Many readers use English as a second or third language.
- RFC 2119 keywords in capital letters: **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, **MAY**.
- Each page starts with a **TL;DR** (3 to 6 lines) and ends with a **checklist** and the line `*Last verified: YYYY-MM-DD.*`.
- Each rule uses exactly this format, so that the matrix generator can read it:

  ```markdown
  ### PY-019: Code uses `logging`, never `print`

  **MUST** · Level 1 · Verified by: Ruff `T20` (automatic)

  Text of the rule.

  **Why:** the reason, in one or two sentences.

  **Examples:**

  - ✅ good example
  - ❌ bad example
  ```

- Prefer examples from DAH Labs repositories (RAG-DataAfriqueHub, baraza) to generic ones. Never publish an example that reveals an unfixed security weakness.
- Anything you could not verify in an official source is marked `> ⚠️ To verify: …`.
- Only one page is in French: `docs/getting-started/demarrage-fr.md`.

## Branches, commits, pull requests

This repository follows its own standards: [branch names](docs/standards/git-branching.md), [Conventional Commits](docs/standards/commits.md), squash merge, [pull request template](.github/pull_request_template.md). Scopes used here: `standards`, `templates`, `workflows`, `hooks`, `scripts`, `migration`, `adr`, `getting-started`, `deps`.
