from pydantic import SecretStr

from qa_service.bootstrap.container import build_answer_question, build_language_model
from qa_service.bootstrap.main import create_app
from qa_service.bootstrap.settings import Settings
from qa_service.domain.model import Question
from qa_service.infrastructure.chat_completions import ChatCompletionsLanguageModel
from qa_service.infrastructure.extractive_model import ExtractiveLanguageModel


def test_build_language_model_is_offline_without_url_and_key() -> None:
    settings = Settings(llm_base_url=None, llm_api_key=None)

    assert isinstance(build_language_model(settings), ExtractiveLanguageModel)


def test_build_language_model_is_remote_with_url_and_key() -> None:
    settings = Settings(
        llm_base_url="https://llm.example.test/v1",
        llm_api_key=SecretStr("test-only-key"),
    )

    assert isinstance(build_language_model(settings), ChatCompletionsLanguageModel)


def test_build_answer_question_answers_from_the_sample_documents() -> None:
    use_case = build_answer_question(Settings(llm_base_url=None, llm_api_key=None))

    answer = use_case(Question("Which tool manages Python dependencies?"))

    assert answer.sources[0] == "python-tooling"


def test_create_app_exposes_the_health_route() -> None:
    routes = {getattr(route, "path", "") for route in create_app().routes}

    assert "/health" in routes
