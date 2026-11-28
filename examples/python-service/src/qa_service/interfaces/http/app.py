"""HTTP interface: translates HTTP requests into use case calls, and results into JSON.

This module knows FastAPI; the use case does not. The use case is received as an argument,
so tests give a use case built with fakes.
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from qa_service.application.answer_question import AnswerQuestion
from qa_service.domain.model import InvalidQuestionError, Question


class AnswerRequest(BaseModel):
    """Body of `POST /answers`."""

    question: str = Field(examples=["How are Python dependencies managed?"])


class AnswerResponse(BaseModel):
    """Response of `POST /answers`."""

    answer: str
    sources: list[str]


def build_app(answer_question: AnswerQuestion) -> FastAPI:
    """Create the FastAPI application around the use case."""
    app = FastAPI(title="QA service", version="0.1.0")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/answers")
    def create_answer(request: AnswerRequest) -> AnswerResponse:
        try:
            question = Question(request.question)
        except InvalidQuestionError as error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(error)
            ) from error
        answer = answer_question(question)
        return AnswerResponse(answer=answer.text, sources=list(answer.sources))

    return app
