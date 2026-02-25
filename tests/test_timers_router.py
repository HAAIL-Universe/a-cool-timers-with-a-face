import pytest
from uuid import uuid4
from datetime import datetime
from fastapi.testclient import TestClient

from app.main import app
from app.models.timer import Timer, TimerStatus, UrgencyLevel
from app.services.timer_service import TimerService
from app.repos.timer_repo import TimerRepository


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def timer_repo():
    """Timer repository instance."""
    return TimerRepository()


@pytest.fixture
def timer_service(timer_repo):
    """Timer service instance."""
    return TimerService(timer_repo)


@pytest.fixture
def sample_timer():
    """Sample timer for testing."""
    return Timer(
        id=uuid4(),
        initial_seconds=60,
        remaining_seconds=60,
        status=TimerStatus.ACTIVE,
        urgency_level=UrgencyLevel.LOW,
        started_at=datetime.utcnow(),
        last_reset_at=datetime.utcnow(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


class TestTimerRouter:
    """Tests for timer router endpoints."""

    def test_create_timer(self, client):
        """Test creating a new timer."""
        response = client.post("/api/timer/timers", json={"initial_seconds": 60})
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["initial_seconds"] == 60
        assert data["remaining_seconds"] == 60
        assert data["status"] == TimerStatus.ACTIVE

    def test_get_all_timers(self, client):
        """Test retrieving all timers."""
        client.post("/api/timer/timers", json={"initial_seconds": 60})
        client.post("/api/timer/timers", json={"initial_seconds": 120})
        
        response = client.get("/api/timer/timers")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2

    def test_get_timer_by_id(self, client):
        """Test retrieving a specific timer."""
        create_response = client.post("/api/timer/timers", json={"initial_seconds": 60})
        timer_id = create_response.json()["id"]
        
        response = client.get(f"/api/timer/timers/{timer_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == timer_id
        assert data["initial_seconds"] == 60

    def test_get_nonexistent_timer(self, client):
        """Test retrieving a non-existent timer."""
        fake_id = str(uuid4())
        response = client.get(f"/api/timer/timers/{fake_id}")
        assert response.status_code == 404

    def test_reset_timer(self, client):
        """Test resetting a timer."""
        create_response = client.post("/api/timer/timers", json={"initial_seconds": 60})
        timer_id = create_response.json()["id"]
        
        response = client.post(f"/api/timer/timers/{timer_id}/reset")
        assert response.status_code == 200
        data = response.json()
        assert data["remaining_seconds"] == data["initial_seconds"]
        assert data["urgency_level"] == UrgencyLevel.LOW

    def test_reset_nonexistent_timer(self, client):
        """Test resetting a non-existent timer."""
        fake_id = str(uuid4())
        response = client.post(f"/api/timer/timers/{fake_id}/reset")
        assert response.status_code == 404

    def test_get_timer_state(self, client):
        """Test retrieving timer state with urgency feedback."""
        create_response = client.post("/api/timer/timers", json={"initial_seconds": 60})
        timer_id = create_response.json()["id"]
        
        response = client.get(f"/api/timer/timers/{timer_id}/state")
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "remaining_time" in data
        assert "remaining_percentage" in data
        assert "urgency_level" in data
        assert "colour_intensity" in data
        assert "facial_expression" in data

    def test_delete_timer(self, client):
        """Test deleting a timer."""
        create_response = client.post("/api/timer/timers", json={"initial_seconds": 60})
        timer_id = create_response.json()["id"]
        
        response = client.delete(f"/api/timer/timers/{timer_id}")
        assert response.status_code == 204
        
        get_response = client.get(f"/api/timer/timers/{timer_id}")
        assert get_response.status_code == 404

    def test_timer_urgency_escalation(self, client, timer_service):
        """Test that urgency level escalates correctly as time depletes."""
        timer = Timer(
            id=uuid4(),
            initial_seconds=100,
            remaining_seconds=100,
            status=TimerStatus.ACTIVE,
            urgency_level=UrgencyLevel.LOW,
            started_at=datetime.utcnow(),
            last_reset_at=datetime.utcnow(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        
        low_urgency = timer_service.calculate_urgency_level(timer.remaining_seconds, timer.initial_seconds)
        assert low_urgency == UrgencyLevel.LOW
        
        timer.remaining_seconds = 50
        medium_urgency = timer_service.calculate_urgency_level(timer.remaining_seconds, timer.initial_seconds)
        assert medium_urgency == UrgencyLevel.MEDIUM
        
        timer.remaining_seconds = 25
        high_urgency = timer_service.calculate_urgency_level(timer.remaining_seconds, timer.initial_seconds)
        assert high_urgency == UrgencyLevel.HIGH
        
        timer.remaining_seconds = 5
        critical_urgency = timer_service.calculate_urgency_level(timer.remaining_seconds, timer.initial_seconds)
        assert critical_urgency == UrgencyLevel.CRITICAL

    def test_colour_intensity_increases_monotonically(self, client, timer_service):
        """Test that colour intensity increases as time depletes."""
        initial_seconds = 100
        
        colour_100 = timer_service.calculate_colour_intensity(100, initial_seconds)
        colour_75 = timer_service.calculate_colour_intensity(75, initial_seconds)
        colour_50 = timer_service.calculate_colour_intensity(50, initial_seconds)
        colour_25 = timer_service.calculate_colour_intensity(25, initial_seconds)
        colour_0 = timer_service.calculate_colour_intensity(0, initial_seconds)
        
        red_values = [colour_100["red"], colour_75["red"], colour_50["red"], colour_25["red"], colour_0["red"]]
        assert red_values == sorted(red_values)
        
        green_values = [colour_100["green"], colour_75["green"], colour_50["green"], colour_25["green"], colour_0["green"]]
        assert green_values == sorted(green_values, reverse=True)

    def test_facial_expression_maps_to_urgency(self, client, timer_service):
        """Test that facial expressions map correctly to urgency levels."""
        low_expr = timer_service.get_facial_expression(UrgencyLevel.LOW)
        assert low_expr is not None
        
        medium_expr = timer_service.get_facial_expression(UrgencyLevel.MEDIUM)
        assert medium_expr is not None
        
        high_expr = timer_service.get_facial_expression(UrgencyLevel.HIGH)
        assert high_expr is not None
        
        critical_expr = timer_service.get_facial_expression(UrgencyLevel.CRITICAL)
        assert critical_expr is not None
        
        assert low_expr != critical_expr
