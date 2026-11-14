import pytest
from fastapi.testclient import TestClient
from tests.conftest import FakeLanguageModel, FakeRetriever

from qa_service.application.answer_question import AnswerQuestion
from qa_service.interfaces.http.app import build_app


@pytest.fixture
def client(fake_retriever: FakeRetriever, fake_model: FakeLanguageModel) -> TestClient:
    return TestClient(build_app(AnswerQuestion(fake_retriever, fake_model, max_documents=2)))


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_post_answers_returns_the_answer_and_its_sources(client: TestClient) -> None:
    response = client.post("/answers", json={"question": "How are dependencies managed?"})

    assert response.status_code == 200
    assert response.json() == {"answer": "A fake answer.", "sources": ["doc-1", "doc-2"]}


def test_post_answers_rejects_an_empty_question(client: TestClient) -> None:
    response = client.post("/answers", json={"question": "  "})

    assert response.status_code == 422
    assert response.json() == {"detail": "The question is empty."}
