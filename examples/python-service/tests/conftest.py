"""Shared fakes for the ports (TEST-003): tests never use the network or an API key."""

from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from qa_service.domain.model import Document, Question


@dataclass
class FakeRetriever:
    """Return fixed documents and remember the calls."""

    documents: list[Document] = field(default_factory=list)
    calls: list[tuple[str, int]] = field(default_factory=list)

    def search(self, question: Question, limit: int) -> list[Document]:
        self.calls.append((question.text, limit))
        return self.documents[:limit]


@dataclass
class FakeLanguageModel:
    """Return a fixed answer and remember the documents it received."""

    answer: str = "A fake answer."
    received: list[list[Document]] = field(default_factory=list)

    def complete(self, question: Question, documents: list[Document]) -> str:
        self.received.append(documents)
        return self.answer


@pytest.fixture
def documents() -> list[Document]:
    return [
        Document(identifier="doc-1", content="uv manages the dependencies. It is fast."),
        Document(identifier="doc-2", content="Secrets are stored in GitHub secrets."),
    ]


@pytest.fixture
def fake_retriever(documents: list[Document]) -> FakeRetriever:
    return FakeRetriever(documents=documents)


@pytest.fixture
def fake_model() -> FakeLanguageModel:
    return FakeLanguageModel()
