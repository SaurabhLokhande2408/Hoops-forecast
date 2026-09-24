"""Health endpoint tests."""

from fastapi.testclient import TestClient

from app.main import app


def test_health() -> None:
    """The service reports a loaded model and dataset."""
    with TestClient(app) as client:
        response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["model_loaded"] is True
