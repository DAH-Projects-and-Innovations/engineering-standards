# Testing

## TL;DR

- Many **unit tests** (fast, offline), fewer **integration tests** (real services in containers), very few **end-to-end tests**.
- Every `fix:` comes with a test that fails without the fix. Every `feat:` comes with tests of its behavior.
- Replace ports with **fakes** (small in-memory implementations), not with `mock.patch` on internal functions.
- Test adapters against **mocked HTTP** (`httpx.MockTransport`) or recorded responses. LLM and embedding APIs are never called in CI.
- A **flaky test** is quarantined the same day, with an issue. CI is never re-run until it happens to pass.
- Coverage on new code: at least **80 %** (SonarQube Cloud, Level 2).

Python specifics (pytest, markers, naming, coverage threshold) are in [Python](python.md#py-012-tests-live-outside-the-package-in-testsunit-testsintegration-and-testse2e). Frontend specifics are in [JavaScript and TypeScript](javascript.md). The [example service](../../examples/python-service/tests/) applies everything on this page.

## The test pyramid

| Kind | What it checks | Where | Speed | Runs |
|---|---|---|---|---|
| **Unit** | A function, a use case with fakes, an adapter with mocked HTTP, a route with `TestClient` and fake use cases | `tests/unit/` | milliseconds; whole suite < 1 minute | pre-push hook and every CI run |
| **Integration** | An adapter against the real service (Postgres, Redis, Qdrant) started in a container | `tests/integration/`, marker `integration` | seconds | separate CI job ([PY-025](python.md#py-025-integration-tests-that-need-services-run-in-their-own-ci-job)) |
| **Contract** | The real external API still behaves as our adapter expects | `tests/integration/`, marker `requires_api_key` | seconds, costs money | by hand, before changing the adapter |
| **End-to-end** | A user journey through the deployed stack (frontend + backend) | `tests/e2e/` or `frontend/e2e/` | minutes | separate CI job, Level 3 |

An `httpx.MockTransport` test or a FastAPI `TestClient` test is a **unit** test: it is in-process and needs no network.

## Rules

### TEST-001: Every bug fix comes with a regression test

**MUST** · Level 1 · Verified by: code review of `fix:` PRs (manual)

The test fails without the fix and passes with it. Write it first: it proves that you understood the bug. The PR template asks for it.

**Why:** a bug that comes back is twice as expensive, and destroys the trust of users.

### TEST-002: Every new feature includes tests of its behavior

**MUST** · Level 1 · Verified by: code review of `feat:` PRs (manual); SonarQube Cloud coverage on new code (automatic, Level 2)

Test the expected behavior and the main error cases (invalid input, empty result, failing dependency).

### TEST-003: Ports are replaced by fakes, not by patches of internal code

**SHOULD** · Level 2 · Verified by: code review (manual)

- A fake is a small class that implements the port in memory (`FakeRetriever` returns fixed documents and records its calls). Put shared fakes in `tests/conftest.py`.
- Use `unittest.mock` / `pytest-mock` only for what has no port (time, randomness), and prefer injecting a clock or a seed.
- Never `mock.patch("my_package.application.answer_question.httpx.post")`: the test breaks at every refactoring and checks how the code is written, not what it does.

```python
# ✅ Fake of the port, given to the use case
@dataclass
class FakeRetriever:
    documents: list[Document]

    def search(self, question: Question, limit: int) -> list[Document]:
        return self.documents[:limit]


def test_answer_question_returns_sources() -> None:
    use_case = AnswerQuestion(FakeRetriever([doc]), FakeLanguageModel(), max_documents=3)
    assert use_case(Question("Why?")).sources == (doc.identifier,)
```

### TEST-004: Adapters are tested against mocked or recorded HTTP responses

**SHOULD** · Level 2 · Verified by: code review (manual)

- For `httpx`, inject the client and use `httpx.MockTransport` (no extra dependency). Check the request (URL, body) and the handling of errors (HTTP 500, missing fields, empty answer).
- For SDKs that hide the HTTP client, record real responses once with `pytest-recording` (VCR.py) and replay them. Filter the `Authorization` header and every secret from the cassettes before commit (`filter_headers=["authorization"]`).
- LLM and embedding providers are **never** called in CI ([PY-016](python.md#py-016-calls-to-llm-and-embedding-providers-are-mocked-in-ci)).

### TEST-005: Integration tests use real services in containers

**SHOULD** · Level 2 · Verified by: CI job with `services:` or testcontainers (automatic)

- Use the same database or vector store as production, in a container (GitHub Actions `services:` or `testcontainers`), not SQLite instead of Postgres.
- Each test starts from a known state: a transaction rolled back after the test, or a new schema or collection.
- Mark them `@pytest.mark.integration`; they run in their own CI job.

### TEST-006: Tests are independent and leave nothing behind

**MUST** · Level 1 · Verified by: `pytest -p randomly` or `pytest-xdist` run (manual); code review (manual)

- A test does not depend on another test or on the order of execution.
- Files go in `tmp_path`; environment variables are set with `monkeypatch.setenv`; global state is reset by fixtures.
- No `time.sleep` to wait for something: wait for a condition with a timeout, or inject a clock.

### TEST-007: A flaky test is quarantined the same day, with an issue

**MUST** · Level 1 · Verified by: code review (manual); `flaky-test` label on issues (manual)

A test that fails sometimes, without a code change, is **flaky**. The person who sees it:

1. opens an issue with the label `flaky-test` and the link to the failed run;
2. marks the test `@pytest.mark.skip(reason="Flaky, see #123")` (or `test.skip` in Vitest) in a PR;
3. the owner fixes it in the next days, or deletes it.

Never re-run CI until the test happens to pass.

**Why:** when CI is red for no reason, people stop reading it, and real failures are missed.

### TEST-008: Test data is synthetic and built by factories

**SHOULD** · Level 2 · Verified by: code review (manual)

- No real personal data in tests or fixtures ([SEC-010](security.md#sec-010-no-real-personal-data-in-the-repository-tests-or-fixtures)). Use invented names, `example.test` domains and generated text.
- Build test objects with small factory functions or fixtures that set sensible defaults, so that each test shows only the values that matter for it.
- Big fixtures (documents, embeddings) live in `tests/data/` and stay small (less than 1 MB in total).

### TEST-009: Tests check behavior through the public API

**SHOULD** · Level 1 · Verified by: code review (manual)

- Test what a function or a component does (its result, its effect), not how it does it.
- Do not test private functions (`_helper`) directly; test the public function that uses them.
- Frontend: test components with Testing Library queries that a user would use (`getByRole`, `getByLabelText`), not CSS classes or internal state.

### TEST-010: One test checks one behavior, and its name says which

**SHOULD** · Level 1 · Verified by: code review (manual)

Name: `test_<unit>_<expected_behavior>` ([PY-014](python.md#py-014-tests-are-named-test_unit_expected_behavior-and-follow-arrange-act-assert)). Use `pytest.mark.parametrize` (with `ids=`) for the same behavior with several inputs.

### TEST-011: Coverage on new code is at least 80 %

**MUST** · Level 2 · Verified by: SonarQube Cloud quality gate (automatic)

See [SONAR-004](sonar.md#sonar-004-the-quality-gate-is-the-built-in-sonar-way-gate-and-blocks-the-merge). The global threshold of [PY-017](python.md#py-017-ci-measures-coverage-and-the-global-threshold-never-goes-down) protects old code at the same time. Coverage shows what is **not** tested; a high number does not prove that the tests are good. Review the assertions too.

### TEST-012: The main user journeys have end-to-end tests

**SHOULD** · Level 3 · Verified by: CI job with Playwright (automatic)

For an application with a frontend, a few Playwright tests cover the main journeys (for example: open the app, ask a question, see an answer with sources). They run against the stack started with `docker compose`, with fake providers (no paid API).

## Checklist

- [ ] Every `fix:` PR has a regression test; every `feat:` PR has behavior tests.
- [ ] Use cases are tested with fakes of their ports.
- [ ] Adapters are tested with mocked or recorded HTTP; no LLM call in CI.
- [ ] Integration tests use real services in containers and are marked `integration`.
- [ ] Tests pass in any order, and use `tmp_path` and `monkeypatch`.
- [ ] Flaky tests are skipped with an issue number.
- [ ] Test data is synthetic.

---

*Last verified: 2026-11-14.*
