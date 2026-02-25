import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from uuid import uuid4

from app.main import app
from app.services.timer_service import TimerService
from app.repos.timer_repo import TimerRepository


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def timer_repo():
    """In-memory timer repository."""
    return TimerRepository()


@pytest.fixture
def timer_service(timer_repo):
    """Timer service with injected repository."""
    return TimerService(timer_repo)


class TestTimersRouter:
    """Tests for /timers endpoints."""

    def test_create_timer(self, client):
        """Create a new timer session."""
        response = client.post("/timers", json={"duration": 60})
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["initialDuration"] == 60
        assert data["remainingTime"] == 60
        assert data["status"] == "running"

    def test_get_all_timers(self, client):
        """Get all active timers."""
        client.post("/timers", json={"duration": 60})
        client.post("/timers", json={"duration": 120})
        
        response = client.get("/timers")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2

    def test_get_timer_by_id(self, client):
        """Get timer by ID."""
        create_response = client.post("/timers", json={"duration": 60})
        timer_id = create_response.json()["id"]
        
        response = client.get(f"/timers/{timer_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == timer_id
        assert data["initialDuration"] == 60

    def test_get_timer_not_found(self, client):
        """Get non-existent timer returns 404."""
        response = client.get(f"/timers/{uuid4()}")
        assert response.status_code == 404

    def test_reset_timer(self, client):
        """Reset timer to initial duration."""
        create_response = client.post("/timers", json={"duration": 60})
        timer_id = create_response.json()["id"]
        
        response = client.post(f"/timers/{timer_id}/reset")
        assert response.status_code == 200
        data = response.json()
        assert data["remainingTime"] == 60
        assert data["status"] == "running"

    def test_reset_timer_not_found(self, client):
        """Reset non-existent timer returns 404."""
        response = client.post(f"/timers/{uuid4()}/reset")
        assert response.status_code == 404

    def test_delete_timer(self, client):
        """Delete a timer."""
        create_response = client.post("/timers", json={"duration": 60})
        timer_id = create_response.json()["id"]
        
        response = client.delete(f"/timers/{timer_id}")
        assert response.status_code == 204
        
        get_response = client.get(f"/timers/{timer_id}")
        assert get_response.status_code == 404

    def test_delete_timer_not_found(self, client):
        """Delete non-existent timer returns 404."""
        response = client.delete(f"/timers/{uuid4()}")
        assert response.status_code == 404

    def test_get_timer_state(self, client):
        """Get timer state with urgency feedback."""
        create_response = client.post("/timers", json={"duration": 60})
        timer_id = create_response.json()["id"]
        
        response = client.get(f"/timers/{timer_id}/state")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == timer_id
        assert "remainingTime" in data
        assert "remainingPercentage" in data
        assert "urgencyLevel" in data
        assert "colourIntensity" in data
        assert "facialExpression" in data

    def test_timer_state_urgency_low(self, client):
        """Timer with high remaining time has low urgency."""
        create_response = client.post("/timers", json={"duration": 100})
        timer_id = create_response.json()["id"]
        
        response = client.get(f"/timers/{timer_id}/state")
        data = response.json()
        assert data["urgencyLevel"] == "low"
        assert data["remainingPercentage"] > 75

    def test_timer_state_urgency_medium(self, client):
        """Timer with medium remaining time has medium urgency."""
        create_response = client.post("/timers", json={"duration": 100})
        timer_id = create_response.json()["id"]
        
        response = client.get(f"/timers/{timer_id}/state")
        data = response.json()
        assert "colourIntensity" in data
        assert isinstance(data["colourIntensity"]["red"], int)
        assert isinstance(data["colourIntensity"]["green"], int)
        assert isinstance(data["colourIntensity"]["blue"], int)

    def test_facial_expression_mapping(self, client):
        """Facial expressions map correctly to urgency levels."""
        create_response = client.post("/timers", json={"duration": 60})
        timer_id = create_response.json()["id"]
        
        response = client.get(f"/timers/{timer_id}/state")
        data = response.json()
        expression = data["facialExpression"]
        assert expression in ["neutral", "concerned", "worried", "alarm"]

    def test_colour_intensity_increases_with_urgency(self, client):
        """Colour intensity increases monotonically as time depletes."""
        create_response = client.post("/timers", json={"duration": 100})
        timer_id = create_response.json()["id"]
        
        response = client.get(f"/timers/{timer_id}/state")
        data = response.json()
        colour = data["colourIntensity"]
        
        assert colour["red"] >= 0
        assert colour["red"] <= 255
        assert colour["green"] >= 0
        assert colour["green"] <= 255
        assert colour["blue"] >= 0
        assert colour["blue"] <= 255

    def test_invalid_duration_negative(self, client):
        """Create timer with negative duration fails."""
        response = client.post("/timers", json={"duration": -10})
        assert response.status_code == 400

    def test_invalid_duration_zero(self, client):
        """Create timer with zero duration fails."""
        response = client.post("/timers", json={"duration": 0})
        assert response.status_code == 400

    def test_missing_duration_field(self, client):
        """Create timer without duration field fails."""
        response = client.post("/timers", json={})
        assert response.status_code == 422

    def test_timer_response_structure(self, client):
        """Timer response contains all required fields."""
        response = client.post("/timers", json={"duration": 60})
        data = response.json()
        
        required_fields = ["id", "initialDuration", "remainingTime", "status", "createdAt"]
        for field in required_fields:
            assert field in data

    def test_multiple_timers_independent(self, client):
        """Multiple timers maintain independent state."""
        timer1 = client.post("/timers", json={"duration": 60}).json()
        timer2 = client.post("/timers", json={"duration": 120}).json()
        
        assert timer1["id"] != timer2["id"]
        assert timer1["initialDuration"] == 60
        assert timer2["initialDuration"] == 120
        
        client.post(f"/timers/{timer1['id']}/reset")
        
        timer2_after = client.get(f"/timers/{timer2['id']}").json()
        assert timer2_after["initialDuration"] == 120
