"""Composition root: the only place that chooses the adapters (ARCH-004).

Every other module receives its dependencies as arguments. To use another vector store or
another provider, change this file only.
"""

from __future__ import annotations

import httpx

from qa_service.application.answer_question import AnswerQuestion
from qa_service.application.ports import LanguageModel
from qa_service.bootstrap.settings import Settings
from qa_service.domain.model import Document
from qa_service.infrastructure.chat_completions import ChatCompletionsLanguageModel
from qa_service.infrastructure.extractive_model import ExtractiveLanguageModel
from qa_service.infrastructure.keyword_retriever import KeywordRetriever

SAMPLE_DOCUMENTS = (
    Document(
        identifier="python-tooling",
        content="DAH Labs Python projects use uv to manage dependencies. "
        "The uv.lock file is committed so that everybody installs the same versions.",
    ),
    Document(
        identifier="branching",
        content="The main branch is the only long-lived branch. "
        "Every change goes through a short branch and a squash-merged pull request.",
    ),
    Document(
        identifier="security",
        content="Secrets never go into the repository. "
        "They are stored in GitHub secrets or in a local .env file that Git ignores.",
    ),
)


def build_language_model(settings: Settings) -> LanguageModel:
    """Return the remote model when it is configured, else the offline model."""
    base_url, api_key = settings.llm_base_url, settings.llm_api_key
    if base_url is None or api_key is None:
        return ExtractiveLanguageModel()
    client = httpx.Client(
        base_url=str(base_url),
        headers={"Authorization": f"Bearer {api_key.get_secret_value()}"},
        timeout=settings.llm_timeout_seconds,
    )
    return ChatCompletionsLanguageModel(client=client, model=settings.llm_model)


def build_answer_question(settings: Settings) -> AnswerQuestion:
    """Build the use case with the adapters chosen from the settings."""
    return AnswerQuestion(
        retriever=KeywordRetriever(SAMPLE_DOCUMENTS),
        model=build_language_model(settings),
        max_documents=settings.max_documents,
    )
