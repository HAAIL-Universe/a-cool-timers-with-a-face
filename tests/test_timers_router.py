import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
import uuid

from app.main import app
from app.services.timer_service import TimerService, UrgencyState


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def mock_timer_service():
    """Mock TimerService for testing."""
    return Mock(spec=TimerService)


@pytest.fixture
def sample_timer_id():
    """Sample timer ID for testing."""
    return str(uuid.uuid4())


@pytest.fixture
def sample_timer_response():
    """Sample timer response object."""
    return {
        "id": str(uuid.uuid4()),
        "initialDuration": 300,
        "remainingTime": 250,
        "status": "running",
        "createdAt": datetime.utcnow().isoformat(),
        "startedAt": datetime.utcnow().isoformat(),
    }


@pytest.fixture
def sample_timer_state():
    """Sample timer state response."""
    return {
        "id": str(uuid.uuid4()),
        "remainingTime": 250,
        "remainingPercentage": 83.33,
        "urgencyLevel": "low",
        "colourIntensity": {"red": 0, "green": 255, "blue": 0},
        "facialExpression": "neutral",
    }


class TestTimerRoutes:
    """Test suite for timer API routes."""

    def test_create_timer_success(self, client, sample_timer_response):
        """Test creating a new timer with valid duration."""
        response = client.post(
            "/timers",
            json={"duration": 300},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["initialDuration"] == 300
        assert data["status"] == "running"
        assert "id" in data
        assert "createdAt" in data

    def test_create_timer_invalid_duration(self, client):
        """Test creating a timer with invalid duration."""
        response = client.post(
            "/timers",
            json={"duration": 0},
        )
        assert response.status_code == 400

    def test_create_timer_negative_duration(self, client):
        """Test creating a timer with negative duration."""
        response = client.post(
            "/timers",
            json={"duration": -100},
        )
        assert response.status_code == 400

    def test_get_all_timers(self, client):
        """Test retrieving all active timers."""
        client.post("/timers", json={"duration": 300})
        client.post("/timers", json={"duration": 600})

        response = client.get("/timers")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2

    def test_get_timer_by_id(self, client, sample_timer_id):
        """Test retrieving a timer by ID."""
        create_response = client.post("/timers", json={"duration": 300})
        timer_id = create_response.json()["id"]

        response = client.get(f"/timers/{timer_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == timer_id
        assert data["initialDuration"] == 300

    def test_get_timer_not_found(self, client):
        """Test retrieving a non-existent timer."""
        fake_id = str(uuid.uuid4())
        response = client.get(f"/timers/{fake_id}")
        assert response.status_code == 404

    def test_reset_timer(self, client):
        """Test resetting a timer to initial duration."""
        create_response = client.post("/timers", json={"duration": 300})
        timer_id = create_response.json()["id"]

        response = client.post(f"/timers/{timer_id}/reset")
        assert response.status_code == 200
        data = response.json()
        assert data["remainingTime"] == 300
        assert data["id"] == timer_id

    def test_reset_timer_not_found(self, client):
        """Test resetting a non-existent timer."""
        fake_id = str(uuid.uuid4())
        response = client.post(f"/timers/{fake_id}/reset")
        assert response.status_code == 404

    def test_get_timer_state(self, client):
        """Test retrieving timer state with urgency feedback."""
        create_response = client.post("/timers", json={"duration": 300})
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

    def test_timer_state_urgency_levels(self, client):
        """Test that urgency levels map correctly to remaining time."""
        create_response = client.post("/timers", json={"duration": 100})
        timer_id = create_response.json()["id"]

        response = client.get(f"/timers/{timer_id}/state")
        assert response.status_code == 200
        data = response.json()
        assert data["urgencyLevel"] in ["low", "medium", "high", "critical"]

    def test_get_timer_state_not_found(self, client):
        """Test getting state of non-existent timer."""
        fake_id = str(uuid.uuid4())
        response = client.get(f"/timers/{fake_id}/state")
        assert response.status_code == 404

    def test_delete_timer(self, client):
        """Test deleting a timer."""
        create_response = client.post("/timers", json={"duration": 300})
        timer_id = create_response.json()["id"]

        response = client.delete(f"/timers/{timer_id}")
        assert response.status_code == 204

        get_response = client.get(f"/timers/{timer_id}")
        assert get_response.status_code == 404

    def test_delete_timer_not_found(self, client):
        """Test deleting a non-existent timer."""
        fake_id = str(uuid.uuid4())
        response = client.delete(f"/timers/{fake_id}")
        assert response.status_code == 404

    def test_timer_colour_intensity_increases_with_urgency(self, client):
        """Test that colour intensity increases as urgency increases."""
        create_response = client.post("/timers", json={"duration": 100})
        timer_id = create_response.json()["id"]

        response = client.get(f"/timers/{timer_id}/state")
        assert response.status_code == 200
        data = response.json()
        colour = data["colourIntensity"]
        assert "red" in colour
        assert "green" in colour
        assert "blue" in colour
        assert all(0 <= c <= 255 for c in colour.values())

    def test_facial_expression_maps_to_urgency(self, client):
        """Test that facial expressions map to urgency levels."""
        create_response = client.post("/timers", json={"duration": 100})
        timer_id = create_response.json()["id"]

        response = client.get(f"/timers/{timer_id}/state")
        assert response.status_code == 200
        data = response.json()
        assert "facialExpression" in data
        assert data["facialExpression"] in ["neutral", "concerned", "worried", "alarm"]

    def test_create_timer_missing_duration(self, client):
        """Test creating a timer without duration field."""
        response = client.post("/timers", json={})
        assert response.status_code == 422

    def test_timer_remaining_percentage(self, client):
        """Test that remaining percentage is calculated correctly."""
        create_response = client.post("/timers", json={"duration": 100})
        timer_id = create_response.json()["id"]

        response = client.get(f"/timers/{timer_id}/state")
        assert response.status_code == 200
        data = response.json()
        assert 0 <= data["remainingPercentage"] <= 100

    def test_multiple_timers_independent_state(self, client):
        """Test that multiple timers maintain independent state."""
        resp1 = client.post("/timers", json={"duration": 300})
        resp2 = client.post("/timers", json={"duration": 600})

        timer1_id = resp1.json()["id"]
        timer2_id = resp2.json()["id"]

        state1 = client.get(f"/timers/{timer1_id}/state").json()
        state2 = client.get(f"/timers/{timer2_id}/state").json()

        assert state1["id"] == timer1_id
        assert state2["id"] == timer2_id
        assert state1["remainingTime"] <= 300
        assert state2["remainingTime"] <= 600
