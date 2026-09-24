"""Prediction endpoint tests."""

from fastapi.testclient import TestClient

from app.main import app


def test_predict_known_player() -> None:
    """A known player returns a numeric next-season prediction."""
    with TestClient(app) as client:
        response = client.post("/api/predict", json={"player_name": "Stephen Curry"})
    assert response.status_code == 200
    assert isinstance(response.json()["predicted_pts"], float)
