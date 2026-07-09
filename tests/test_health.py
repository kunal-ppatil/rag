from fastapi.testclient import TestClient

from rag_enterprise.main import app


def test_health() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_returns_answer_and_source() -> None:
    client = TestClient(app)
    response = client.post("/v1/chat", json={"message": "What is the engineering release process?"})
    assert response.status_code == 200
    body = response.text
    assert "Answer:" in body
    assert "Engineering Release Notes" in body
