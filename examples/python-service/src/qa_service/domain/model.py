"""Domain model: plain Python objects, with no framework and no I/O.

The domain is the center of the architecture. It does not import any other layer.
"""

from __future__ import annotations

from dataclasses import dataclass

MAX_QUESTION_LENGTH = 500


class InvalidQuestionError(ValueError):
    """Raised when a question cannot be answered because its text is not valid."""


@dataclass(frozen=True, slots=True)
class Question:
    """A question asked by a user.

    Attributes:
        text: The question, without leading or trailing spaces.
    """

    text: str

    def __post_init__(self) -> None:
        """Validate the question text.

        Raises:
            InvalidQuestionError: If the text is empty or longer than MAX_QUESTION_LENGTH.
        """
        if not self.text.strip():
            msg = "The question is empty."
            raise InvalidQuestionError(msg)
        if len(self.text) > MAX_QUESTION_LENGTH:
            msg = f"The question is longer than {MAX_QUESTION_LENGTH} characters."
            raise InvalidQuestionError(msg)


@dataclass(frozen=True, slots=True)
class Document:
    """A piece of knowledge that can support an answer.

    Attributes:
        identifier: Stable identifier of the document, shown to the user as a source.
        content: Text of the document.
    """

    identifier: str
    content: str


@dataclass(frozen=True, slots=True)
class Answer:
    """An answer and the documents it is based on.

    Attributes:
        text: The answer given to the user.
        sources: Identifiers of the documents used to write the answer.
    """

    text: str
    sources: tuple[str, ...]

    @property
    def is_grounded(self) -> bool:
        """Whether the answer is based on at least one document."""
        return bool(self.sources)
