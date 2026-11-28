"""Contract test against a real provider. Never runs in CI (marker requires_api_key).

Run it by hand before changing the adapter:
    QA_LLM_BASE_URL=https://api.mistral.ai/v1 QA_LLM_API_KEY=... uv run pytest -m requires_api_key
"""

import os

import httpx
import pytest

from qa_service.domain.model import Document, Question
from qa_service.infrastructure.chat_completions import ChatCompletionsLanguageModel


@pytest.mark.requires_api_key
def test_real_provider_answers_from_the_documents() -> None:
    base_url = os.environ.get("QA_LLM_BASE_URL")
    api_key = os.environ.get("QA_LLM_API_KEY")
    if not base_url or not api_key:
        pytest.skip("QA_LLM_BASE_URL and QA_LLM_API_KEY are not set.")
    client = httpx.Client(
        base_url=base_url, headers={"Authorization": f"Bearer {api_key}"}, timeout=30
    )
    model = ChatCompletionsLanguageModel(
        client=client, model=os.environ.get("QA_LLM_MODEL", "mistral-small-latest")
    )

    answer = model.complete(
        Question("Which tool manages the dependencies?"),
        [Document("doc-1", "The project uses uv to manage its dependencies.")],
    )

    assert "uv" in answer
