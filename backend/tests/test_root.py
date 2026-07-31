from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/api/v1/")

    assert response.status_code == 200
    assert response.json()["name"] == "The Orchestrator API"
    assert response.json()["version"] == "0.1.0"
