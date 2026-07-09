from fastapi.testclient import TestClient

from rag_enterprise.main import app


def test_chat_uses_local_documents() -> None:
    client = TestClient(app)
    response = client.post("/v1/chat", json={"message": "What happens during engineering releases?"})
    assert response.status_code == 200
    body = response.text
    assert "Engineering Release Notes" in body
    assert "Sources:" in body
