# Example: a Python service with a layered architecture

A small question answering HTTP service that follows the DAH Labs engineering standards. Use it as a reference when you read [Architecture](../../docs/standards/architecture.md), [Clean code](../../docs/standards/clean-code.md) and [Testing](../../docs/standards/testing.md). It is tested on every change by the [integration workflow](../../.github/workflows/example-integration.yml).

## Layers

```text
src/qa_service/
├── domain/          # Question, Document, Answer: plain Python, no framework, no I/O
├── application/     # use case AnswerQuestion + ports (Retriever, LanguageModel)
├── infrastructure/  # adapters: keyword retriever, offline model, chat completions API client
├── interfaces/http/ # FastAPI routes: HTTP <-> use case
└── bootstrap/       # composition root: settings and choice of the adapters
```

Imports go inward only: `bootstrap` → `interfaces` / `infrastructure` → `application` → `domain`. `uv run lint-imports` checks it (contracts in `pyproject.toml`).

## Run

```bash
uv sync
uv run uvicorn --factory qa_service.bootstrap.main:create_app --reload
curl -s localhost:8000/answers -H 'content-type: application/json' \
  -d '{"question": "Which tool manages Python dependencies?"}'
```

Without configuration the service uses an offline model that answers with a sentence of the best document. To use a provider with an OpenAI-compatible API, copy `.env.example` to `.env` and fill `QA_LLM_BASE_URL` and `QA_LLM_API_KEY`.

With Docker:

```bash
docker build -t qa-service .
docker run --rm -p 8000:8000 qa-service
```

## Checks

```bash
uv run ruff check . && uv run ruff format --check .
uv run mypy
uv run lint-imports
uv run pytest --cov
```
