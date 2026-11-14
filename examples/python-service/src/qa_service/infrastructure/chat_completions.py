"""Adapter: a language model behind an OpenAI-compatible chat completions API.

Many providers (Mistral, OpenAI, a local vLLM or Ollama server) expose this API. The HTTP
client is injected, so tests use `httpx.MockTransport` and never call the real API (PY-016).
"""

from __future__ import annotations

import logging

import httpx

from qa_service.domain.model import Document, Question

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "Answer the question using only the documents. "
    "If the documents do not contain the answer, say that you do not know."
)


class LanguageModelError(RuntimeError):
    """Raised when the provider does not return a usable answer."""


class ChatCompletionsLanguageModel:
    """Call `POST {base_url}/chat/completions` with the question and the documents."""

    def __init__(self, client: httpx.Client, model: str) -> None:
        """Create the adapter.

        Args:
            client: HTTP client configured with the base URL, the API key header and timeouts.
            model: Name of the model at the provider, for example `mistral-small-latest`.
        """
        self._client = client
        self._model = model

    def complete(self, question: Question, documents: list[Document]) -> str:
        """Ask the provider for an answer.

        Raises:
            LanguageModelError: If the request fails or the response has no answer.
        """
        context = "\n\n".join(f"[{doc.identifier}] {doc.content}" for doc in documents)
        payload = {
            "model": self._model,
            "temperature": 0,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Documents:\n{context}\n\nQuestion: {question.text}"},
            ],
        }
        try:
            response = self._client.post("/chat/completions", json=payload)
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
        except (httpx.HTTPError, KeyError, IndexError, TypeError, ValueError) as error:
            # Log the error type only: the response may contain the prompt (personal data).
            logger.warning("The language model call failed: %s", type(error).__name__)
            msg = "The language model did not return an answer."
            raise LanguageModelError(msg) from error

        if not isinstance(content, str) or not content.strip():
            msg = "The language model returned an empty answer."
            raise LanguageModelError(msg)
        return content.strip()
