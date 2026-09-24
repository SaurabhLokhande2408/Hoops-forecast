"""Player endpoint tests."""

from fastapi.testclient import TestClient

from app.main import app


def test_missing_player_returns_404() -> None:
    """Unknown exact player names return a proper not-found response."""
    with TestClient(app) as client:
        response = client.get("/api/players/Definitely%20Not%20An%20NBA%20Player")
    assert response.status_code == 404
