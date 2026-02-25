import pytest
from fastapi.testclient import TestClient
from app.routers.timers import app
from app.models.timer import Timer, TimerState, TimerStatus, UrgencyLevel, FacialExpression


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


class TestTimersRouter:
    def test_post_timers_creates_timer(self, client):
        """POST /timers with {duration: 30} returns 201 with Timer object."""
        response = client.post("/timers", json={"duration": 30})
        assert response.status_code == 201
        data = response.json()
        assert data["id"] is not None
        assert data["status"] == "active"
        assert data["initial_seconds"] == 30
        assert data["remaining_seconds"] == 30

    def test_get_timers_returns_list(self, client):
        """GET /timers returns list of all timers."""
        client.post("/timers", json={"duration": 30})
        client.post("/timers", json={"duration": 60})
        response = client.get("/timers")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2

    def test_get_timer_by_id(self, client):
        """GET /timers/{id} retrieves timer by ID."""
        create_response = client.post("/timers", json={"duration": 30})
        timer_id = create_response.json()["id"]
        response = client.get(f"/timers/{timer_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == timer_id
        assert data["initial_seconds"] == 30

    def test_get_timer_by_id_not_found(self, client):
        """GET /timers/{id} returns 404 for nonexistent timer."""
        response = client.get("/timers/nonexistent-id")
        assert response.status_code == 404

    def test_delete_timer(self, client):
        """DELETE /timers/{id} removes timer."""
        create_response = client.post("/timers", json={"duration": 30})
        timer_id = create_response.json()["id"]
        response = client.delete(f"/timers/{timer_id}")
        assert response.status_code == 204
        get_response = client.get(f"/timers/{timer_id}")
        assert get_response.status_code == 404

    def test_post_reset_timer(self, client):
        """POST /timers/{id}/reset restores remaining_seconds to initial_seconds."""
        create_response = client.post("/timers", json={"duration": 30})
        timer_id = create_response.json()["id"]
        reset_response = client.post(f"/timers/{timer_id}/reset")
        assert reset_response.status_code == 200
        data = reset_response.json()
        assert data["remaining_seconds"] == data["initial_seconds"]

    def test_get_timer_state_fields(self, client):
        """GET /timers/{id}/state returns urgency_level, colour_intensity, facial_expression."""
        create_response = client.post("/timers", json={"duration": 30})
        timer_id = create_response.json()["id"]
        response = client.get(f"/timers/{timer_id}/state")
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "remaining_time" in data
        assert "remaining_percentage" in data
        assert data["urgency_level"] == "low"
        assert data["facial_expression"] == "calm"
        assert "colour_intensity" in data
        assert "red" in data["colour_intensity"]
        assert "green" in data["colour_intensity"]
        assert "blue" in data["colour_intensity"]
        assert data["colour_intensity"]["green"] > data["colour_intensity"]["red"]
        assert data["colour_intensity"]["green"] > data["colour_intensity"]["blue"]

    def test_post_timers_invalid_duration(self, client):
        """POST /timers with invalid duration returns 422."""
        response = client.post("/timers", json={"duration": -5})
        assert response.status_code == 422

    def test_post_timers_missing_duration(self, client):
        """POST /timers without duration returns 422."""
        response = client.post("/timers", json={})
        assert response.status_code == 422
