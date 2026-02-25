import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.repos.timer_repo import TimerRepository
from app.services.timer_service import TimerService


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
    """Timer service with in-memory repo."""
    return TimerService(timer_repo)


class TestTimersRouter:
    """Tests for timer endpoints."""

    def test_create_timer(self, client):
        """Create a new timer with valid duration."""
        response = client.post("/timers", json={"duration": 60})
        assert response.status_code == 201
        data = response.json()
        assert data["id"]
        assert data["initialDuration"] == 60
        assert data["remainingTime"] == 60
        assert data["status"] == "running"

    def test_create_timer_invalid_duration(self, client):
        """Reject timer with invalid duration."""
        response = client.post("/timers", json={"duration": 0})
        assert response.status_code == 400

    def test_get_all_timers(self, client):
        """Retrieve all active timers."""
        client.post("/timers", json={"duration": 60})
        client.post("/timers", json={"duration": 120})
        response = client.get("/timers")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
        assert all("id" in t for t in data)

    def test_get_timer_by_id(self, client):
        """Retrieve a specific timer by ID."""
        create_response = client.post("/timers", json={"duration": 60})
        timer_id = create_response.json()["id"]
        response = client.get(f"/timers/{timer_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == timer_id
        assert data["initialDuration"] == 60

    def test_get_nonexistent_timer(self, client):
        """Return 404 for nonexistent timer."""
        response = client.get("/timers/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404

    def test_reset_timer(self, client):
        """Reset timer to initial duration."""
        create_response = client.post("/timers", json={"duration": 60})
        timer_id = create_response.json()["id"]
        response = client.post(f"/timers/{timer_id}/reset")
        assert response.status_code == 200
        data = response.json()
        assert data["remainingTime"] == 60

    def test_reset_nonexistent_timer(self, client):
        """Return 404 when resetting nonexistent timer."""
        response = client.post("/timers/00000000-0000-0000-0000-000000000000/reset")
        assert response.status_code == 404

    def test_delete_timer(self, client):
        """Delete a timer successfully."""
        create_response = client.post("/timers", json={"duration": 60})
        timer_id = create_response.json()["id"]
        response = client.delete(f"/timers/{timer_id}")
        assert response.status_code == 204
        get_response = client.get(f"/timers/{timer_id}")
        assert get_response.status_code == 404

    def test_get_timer_state(self, client):
        """Retrieve timer state with urgency feedback."""
        create_response = client.post("/timers", json={"duration": 100})
        timer_id = create_response.json()["id"]
        response = client.get(f"/timers/{timer_id}/state")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == timer_id
        assert data["remainingTime"]
        assert 0 <= data["remainingPercentage"] <= 100
        assert data["urgencyLevel"] in ["low", "medium", "high", "critical"]
        assert "colourIntensity" in data
        assert "red" in data["colourIntensity"]
        assert "green" in data["colourIntensity"]
        assert "blue" in data["colourIntensity"]
        assert "facialExpression" in data

    def test_timer_urgency_escalation(self, client):
        """Verify urgency level escalates as time depletes."""
        create_response = client.post("/timers", json={"duration": 100})
        timer_id = create_response.json()["id"]
        
        state_response = client.get(f"/timers/{timer_id}/state")
        initial_urgency = state_response.json()["urgencyLevel"]
        assert initial_urgency in ["low", "medium", "high", "critical"]

    def test_colour_intensity_monotonic(self, client):
        """Verify colour intensity increases monotonically with urgency."""
        create_response = client.post("/timers", json={"duration": 100})
        timer_id = create_response.json()["id"]
        
        response = client.get(f"/timers/{timer_id}/state")
        data = response.json()
        colour = data["colourIntensity"]
        
        assert 0 <= colour["red"] <= 255
        assert 0 <= colour["green"] <= 255
        assert 0 <= colour["blue"] <= 255

    def test_facial_expression_sync(self, client):
        """Verify facial expression syncs with urgency level."""
        create_response = client.post("/timers", json={"duration": 100})
        timer_id = create_response.json()["id"]
        
        response = client.get(f"/timers/{timer_id}/state")
        data = response.json()
        
        assert "facialExpression" in data
        assert data["facialExpression"] in ["neutral", "concerned", "worried", "alarm"]
