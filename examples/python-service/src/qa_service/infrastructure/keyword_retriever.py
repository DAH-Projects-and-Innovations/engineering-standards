"""Adapter: an in-memory retriever that ranks documents by shared words.

It is enough for an example and for tests. A real service would use a vector store; it would
implement the same `Retriever` port, and nothing else in the code would change.
"""

from __future__ import annotations

import re
from collections.abc import Iterable

from qa_service.domain.model import Document, Question

_WORD = re.compile(r"\w+", re.UNICODE)
_MIN_WORD_LENGTH = 4  # Ignores short words such as "the" or "are".


def _words(text: str) -> set[str]:
    return {word for word in _WORD.findall(text.casefold()) if len(word) >= _MIN_WORD_LENGTH}


class KeywordRetriever:
    """Rank documents by the number of words they share with the question."""

    def __init__(self, documents: Iterable[Document]) -> None:
        """Index the documents in memory.

        Args:
            documents: The documents that can be returned.
        """
        self._documents = [(document, _words(document.content)) for document in documents]

    def search(self, question: Question, limit: int) -> list[Document]:
        """Return the documents that share at least one word with the question."""
        question_words = _words(question.text)
        scored = [(len(question_words & words), document) for document, words in self._documents]
        relevant = [(score, document) for score, document in scored if score > 0]
        relevant.sort(key=lambda item: (-item[0], item[1].identifier))
        return [document for _, document in relevant[:limit]]
