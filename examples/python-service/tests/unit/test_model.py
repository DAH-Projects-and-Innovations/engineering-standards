import pytest

from qa_service.domain.model import MAX_QUESTION_LENGTH, Answer, InvalidQuestionError, Question


def test_question_accepts_normal_text() -> None:
    question = Question("How are dependencies managed?")

    assert question.text == "How are dependencies managed?"


@pytest.mark.parametrize("text", ["", "   ", "x" * (MAX_QUESTION_LENGTH + 1)])
def test_question_rejects_empty_or_too_long_text(text: str) -> None:
    with pytest.raises(InvalidQuestionError):
        Question(text)


def test_answer_is_grounded_only_with_sources() -> None:
    assert Answer(text="Yes.", sources=("doc-1",)).is_grounded
    assert not Answer(text="I do not know.", sources=()).is_grounded
