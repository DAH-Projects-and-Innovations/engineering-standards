from tests.conftest import FakeLanguageModel, FakeRetriever

from qa_service.application.answer_question import NO_DOCUMENT_ANSWER, AnswerQuestion
from qa_service.domain.model import Question


def test_answer_question_returns_model_answer_with_sources(
    fake_retriever: FakeRetriever, fake_model: FakeLanguageModel
) -> None:
    # Arrange
    use_case = AnswerQuestion(fake_retriever, fake_model, max_documents=5)

    # Act
    answer = use_case(Question("How are dependencies managed?"))

    # Assert
    assert answer.text == "A fake answer."
    assert answer.sources == ("doc-1", "doc-2")


def test_answer_question_gives_at_most_max_documents_to_the_model(
    fake_retriever: FakeRetriever, fake_model: FakeLanguageModel
) -> None:
    use_case = AnswerQuestion(fake_retriever, fake_model, max_documents=1)

    use_case(Question("Where are secrets stored?"))

    assert fake_retriever.calls == [("Where are secrets stored?", 1)]
    assert [doc.identifier for doc in fake_model.received[0]] == ["doc-1"]


def test_answer_question_does_not_call_the_model_without_documents(
    fake_model: FakeLanguageModel,
) -> None:
    use_case = AnswerQuestion(FakeRetriever(documents=[]), fake_model, max_documents=3)

    answer = use_case(Question("What is the capital of Benin?"))

    assert answer.text == NO_DOCUMENT_ANSWER
    assert not answer.is_grounded
    assert fake_model.received == []
