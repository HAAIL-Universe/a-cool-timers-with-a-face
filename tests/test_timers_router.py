import pytest
from datetime import datetime
from uuid import uuid4
from fastapi.testclient import TestClient

from app.main import app
from app.models.timer import TimerStatus, UrgencyLevel


@pytest.fixture
def client():
    """Provide test client."""
    return TestClient(app)


@pytest.fixture
def timer_create_payload():
    """Provide timer creation payload."""
    return {"initial_seconds": 60}


class TestTimersRouter:
    """Tests for timer endpoints."""

    def test_create_timer(self, client, timer_create_payload):
        """Create a new timer."""
        response = client.post("/timers", json=timer_create_payload)
        assert response.status_code == 201
        data = response.json()
        assert data["initial_seconds"] == 60
        assert data["remaining_seconds"] == 60
        assert data["status"] == TimerStatus.active.value
        assert data["urgency_level"] == UrgencyLevel.low.value
        assert "id" in data
        assert "created_at" in data

    def test_get_all_timers(self, client, timer_create_payload):
        """Get all active timers."""
        client.post("/timers", json=timer_create_payload)
        client.post("/timers", json=timer_create_payload)
        
        response = client.get("/timers")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
        assert all("id" in timer for timer in data)

    def test_get_timer_by_id(self, client, timer_create_payload):
        """Get timer by ID."""
        create_response = client.post("/timers", json=timer_create_payload)
        timer_id = create_response.json()["id"]
        
        response = client.get(f"/timers/{timer_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == timer_id
        assert data["initial_seconds"] == 60

    def test_get_timer_by_id_not_found(self, client):
        """Get non-existent timer returns 404."""
        fake_id = str(uuid4())
        response = client.get(f"/timers/{fake_id}")
        assert response.status_code == 404

    def test_reset_timer(self, client, timer_create_payload):
        """Reset timer to initial duration."""
        create_response = client.post("/timers", json=timer_create_payload)
        timer_id = create_response.json()["id"]
        
        response = client.post(f"/timers/{timer_id}/reset")
        assert response.status_code == 200
        data = response.json()
        assert data["remaining_seconds"] == data["initial_seconds"]

    def test_delete_timer(self, client, timer_create_payload):
        """Delete a timer."""
        create_response = client.post("/timers", json=timer_create_payload)
        timer_id = create_response.json()["id"]
        
        response = client.delete(f"/timers/{timer_id}")
        assert response.status_code == 204
        
        get_response = client.get(f"/timers/{timer_id}")
        assert get_response.status_code == 404

    def test_get_timer_state(self, client, timer_create_payload):
        """Get timer state with urgency feedback."""
        create_response = client.post("/timers", json=timer_create_payload)
        timer_id = create_response.json()["id"]
        
        response = client.get(f"/timers/{timer_id}/state")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == timer_id
        assert "remaining_time" in data
        assert "remaining_percentage" in data
        assert "urgency_level" in data
        assert "colour_intensity" in data
        assert "facial_expression" in data

    def test_timer_invalid_duration(self, client):
        """Create timer with invalid duration."""
        response = client.post("/timers", json={"initial_seconds": 0})
        assert response.status_code == 422

    def test_timer_negative_duration(self, client):
        """Create timer with negative duration."""
        response = client.post("/timers", json={"initial_seconds": -10})
        assert response.status_code == 422
