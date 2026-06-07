from fastapi.testclient import TestClient

from app import app


def test_health_endpoint():

    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200

    payload = response.json()

    assert payload["status"] == "ok"

    assert "model_file_present" in payload
    assert "preprocessor_file_present" in payload
