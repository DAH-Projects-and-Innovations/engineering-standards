import json

import httpx
import pytest

from qa_service.domain.model import Document, Question
from qa_service.infrastructure.chat_completions import (
    ChatCompletionsLanguageModel,
    LanguageModelError,
)


def _model(handler: httpx.MockTransport) -> ChatCompletionsLanguageModel:
    client = httpx.Client(base_url="https://llm.example.test/v1", transport=handler)
    return ChatCompletionsLanguageModel(client=client, model="test-model")


def _reply(content: object) -> httpx.Response:
    return httpx.Response(200, json={"choices": [{"message": {"content": content}}]})


def test_complete_sends_the_documents_and_returns_the_answer(documents: list[Document]) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return _reply("  uv manages them.  ")

    answer = _model(httpx.MockTransport(handler)).complete(Question("Dependencies?"), documents)

    assert answer == "uv manages them."
    body = json.loads(requests[0].content)
    assert requests[0].url.path == "/v1/chat/completions"
    assert body["model"] == "test-model"
    assert "[doc-1]" in body["messages"][1]["content"]


@pytest.mark.parametrize(
    "response",
    [
        httpx.Response(500, json={"error": "server error"}),
        httpx.Response(200, json={"choices": []}),
        _reply(""),
        _reply(None),
    ],
    ids=["http-error", "no-choice", "empty-answer", "not-a-string"],
)
def test_complete_raises_language_model_error_on_bad_responses(
    documents: list[Document], response: httpx.Response
) -> None:
    model = _model(httpx.MockTransport(lambda _request: response))

    with pytest.raises(LanguageModelError):
        model.complete(Question("Dependencies?"), documents)
