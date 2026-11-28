"""Adapter: an offline language model that answers with the most relevant sentence.

It needs no API key, so the service runs on any laptop and in CI.
"""

from __future__ import annotations

import re

from qa_service.domain.model import Document, Question

_SENTENCE_END = re.compile(r"(?<=[.!?])\s+")


class ExtractiveLanguageModel:
    """Answer with the first sentence of the most relevant document."""

    def complete(self, question: Question, documents: list[Document]) -> str:
        """Return the first sentence of the first document."""
        first_sentence = _SENTENCE_END.split(documents[0].content.strip(), maxsplit=1)[0]
        return first_sentence
