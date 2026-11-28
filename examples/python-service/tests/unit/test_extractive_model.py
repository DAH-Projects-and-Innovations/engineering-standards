from qa_service.domain.model import Document, Question
from qa_service.infrastructure.extractive_model import ExtractiveLanguageModel


def test_complete_returns_the_first_sentence_of_the_first_document(
    documents: list[Document],
) -> None:
    answer = ExtractiveLanguageModel().complete(Question("How?"), documents)

    assert answer == "uv manages the dependencies."
