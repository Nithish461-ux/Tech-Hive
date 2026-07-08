from unittest.mock import patch

from fastapi.testclient import TestClient

import Backend.rag_engine as rag_engine
from Backend.main import app


def test_embed_fallback_returns_plain_lists():
    class DummyEmbedder:
        def encode(self, texts, show_progress_bar=False):
            return [[0.0, 1.0] for _ in texts]

    rag_engine._embedder = DummyEmbedder()

    result = rag_engine.embed(["hello"])

    assert result == [[0.0, 1.0]]


def test_query_falls_back_to_keyword_matching_for_uploaded_documents():
    rag_engine._collection = rag_engine._MockCollection()
    rag_engine.add_document(
        source="attendance.txt",
        category="Exams",
        raw_text="Students must maintain 75% attendance to be eligible for exams.",
    )

    hits = rag_engine.query("What attendance is needed for exams?")

    assert hits
    assert "75%" in hits[0]["text"] or "attendance" in hits[0]["text"].lower()


def test_chat_response_includes_source_category():
    with patch("Backend.main.rag_engine.query", return_value=[{
        "text": "Attendance required is 75%.",
        "source": "attendance.txt",
        "category": "Exams",
    }]):
        with TestClient(app) as client:
            response = client.post("/api/chat", json={"query": "attendance"})

    assert response.status_code == 200
    assert response.json()["sources"][0]["category"] == "Exams"


def test_startup_seeds_knowledge_base_when_empty():
    with patch("Backend.main.rag_engine.is_empty", return_value=True), patch(
        "Backend.main.seed_knowledge_base.run"
    ) as seed_run:
        with TestClient(app) as client:
            client.get("/api/health")

        seed_run.assert_called_once()
