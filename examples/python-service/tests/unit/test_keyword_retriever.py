from qa_service.domain.model import Document, Question
from qa_service.infrastructure.keyword_retriever import KeywordRetriever


def test_search_ranks_documents_by_shared_words(documents: list[Document]) -> None:
    retriever = KeywordRetriever(documents)

    found = retriever.search(Question("Where are the secrets stored?"), limit=5)

    assert [doc.identifier for doc in found] == ["doc-2"]


def test_search_respects_the_limit() -> None:
    documents = [Document(f"doc-{index}", "python packaging") for index in range(5)]
    retriever = KeywordRetriever(documents)

    found = retriever.search(Question("python packaging"), limit=2)

    assert [doc.identifier for doc in found] == ["doc-0", "doc-1"]


def test_search_returns_nothing_without_shared_words(documents: list[Document]) -> None:
    retriever = KeywordRetriever(documents)

    assert retriever.search(Question("Bonjour"), limit=5) == []
