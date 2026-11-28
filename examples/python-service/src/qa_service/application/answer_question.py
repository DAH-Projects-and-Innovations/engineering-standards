"""Use case: answer a question from the documents found by the retriever."""

from __future__ import annotations

import logging

from qa_service.application.ports import LanguageModel, Retriever
from qa_service.domain.model import Answer, Question

logger = logging.getLogger(__name__)

NO_DOCUMENT_ANSWER = "I do not know: no document answers this question."


class AnswerQuestion:
    """Answer a question with a retriever and a language model.

    The use case depends only on ports. The composition root (`qa_service.bootstrap`) decides
    which adapters are used.
    """

    def __init__(self, retriever: Retriever, model: LanguageModel, max_documents: int) -> None:
        """Create the use case.

        Args:
            retriever: Port that finds the relevant documents.
            model: Port that writes the answer.
            max_documents: Maximum number of documents given to the model.
        """
        self._retriever = retriever
        self._model = model
        self._max_documents = max_documents

    def __call__(self, question: Question) -> Answer:
        """Answer the question.

        The model is not called when no document is found: an answer without a source is
        not reliable, and calling a paid API for it costs money for nothing.

        Args:
            question: The validated question.

        Returns:
            The answer and the identifiers of its sources.
        """
        documents = self._retriever.search(question, limit=self._max_documents)
        if not documents:
            logger.info("No document found; the model is not called.")
            return Answer(text=NO_DOCUMENT_ANSWER, sources=())

        text = self._model.complete(question, documents)
        logger.info("Answered with %d documents.", len(documents))
        return Answer(text=text, sources=tuple(document.identifier for document in documents))
