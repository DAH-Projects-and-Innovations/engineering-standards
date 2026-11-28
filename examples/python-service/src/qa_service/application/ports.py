"""Ports: the interfaces that the application needs from the outside world.

Adapters in `qa_service.infrastructure` implement these protocols. Tests replace them with
fakes, so the use cases are tested without network, database or API key (TEST-003).
"""

from __future__ import annotations

from typing import Protocol

from qa_service.domain.model import Document, Question


class Retriever(Protocol):
    """Finds the documents that are relevant to a question."""

    def search(self, question: Question, limit: int) -> list[Document]:
        """Return at most `limit` documents, the most relevant first."""
        ...


class LanguageModel(Protocol):
    """Writes an answer from a question and supporting documents."""

    def complete(self, question: Question, documents: list[Document]) -> str:
        """Return the text of the answer."""
        ...
