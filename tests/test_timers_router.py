import uuid
from datetime import datetime
from fastapi.testclient import TestClient
from app.main import app
from app.models.timer import TimerStatus, UrgencyLevel


client = TestClient(app)


class TestTimersRouter:
    """Integration tests for timer endpoints."""

    def test_health_check(self) -> None:
        """Health check returns 200 with status ok."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_post_timers_creates_timer(self) -> None:
        """POST /timers with duration creates timer in active state."""
        response = client.post("/timers", json={"duration": 30})
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["initialDuration"] == 30
        assert data["remainingTime"] == 30
        assert data["status"] == "running"
        assert data["urgencyLevel"] == "low"

    def test_get_all_timers(self) -> None:
        """GET /timers returns list of all timers."""
        client.post("/timers", json={"duration": 20})
        client.post("/timers", json={"duration": 40})
        response = client.get("/timers")
        assert response.status_code == 200
        timers = response.json()
        assert len(timers) >= 2
        assert all("id" in t for t in timers)
        assert all("initialDuration" in t for t in timers)

    def test_get_timer_by_id(self) -> None:
        """GET /timers/{id} returns specific timer."""
        create_response = client.post("/timers", json={"duration": 25})
        timer_id = create_response.json()["id"]
        response = client.get(f"/timers/{timer_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == timer_id
        assert data["initialDuration"] == 25

    def test_get_timer_by_id_not_found(self) -> None:
        """GET /timers/{id} with nonexistent ID returns 404."""
        fake_id = str(uuid.uuid4())
        response = client.get(f"/timers/{fake_id}")
        assert response.status_code == 404

    def test_get_timer_state_fresh_timer(self) -> None:
        """GET /timers/{id}/state returns low urgency for fresh timer."""
        create_response = client.post("/timers", json={"duration": 100})
        timer_id = create_response.json()["id"]
        response = client.get(f"/timers/{timer_id}/state")
        assert response.status_code == 200
        state = response.json()
        assert state["id"] == timer_id
        assert state["remainingTime"] == 100
        assert state["remainingPercentage"] == 100.0
        assert state["urgencyLevel"] == "low"
        assert state["facialExpression"] == "calm"
        assert state["colourIntensity"]["red"] == 0
        assert state["colourIntensity"]["green"] == 255
        assert state["colourIntensity"]["blue"] == 0

    def test_get_timer_state_medium_urgency(self) -> None:
        """GET /timers/{id}/state returns medium urgency at 25-50% remaining."""
        create_response = client.post("/timers", json={"duration": 100})
        timer_id = create_response.json()["id"]
        client.post(f"/timers/{timer_id}/tick", json={"seconds_elapsed": 60})
        response = client.get(f"/timers/{timer_id}/state")
        assert response.status_code == 200
        state = response.json()
        assert state["urgencyLevel"] == "medium"
        assert state["facialExpression"] == "concerned"
        assert state["colourIntensity"]["red"] > 0
        assert state["colourIntensity"]["green"] > 0

    def test_get_timer_state_high_urgency(self) -> None:
        """GET /timers/{id}/state returns high urgency at 10-25% remaining."""
        create_response = client.post("/timers", json={"duration": 100})
        timer_id = create_response.json()["id"]
        client.post(f"/timers/{timer_id}/tick", json={"seconds_elapsed": 82})
        response = client.get(f"/timers/{timer_id}/state")
        assert response.status_code == 200
        state = response.json()
        assert state["urgencyLevel"] == "high"
        assert state["facialExpression"] == "stressed"
        assert state["colourIntensity"]["red"] > state["colourIntensity"]["green"]

    def test_get_timer_state_critical_urgency(self) -> None:
        """GET /timers/{id}/state returns critical at <10% remaining."""
        create_response = client.post("/timers", json={"duration": 100})
        timer_id = create_response.json()["id"]
        client.post(f"/timers/{timer_id}/tick", json={"seconds_elapsed": 95})
        response = client.get(f"/timers/{timer_id}/state")
        assert response.status_code == 200
        state = response.json()
        assert state["urgencyLevel"] == "critical"
        assert state["facialExpression"] == "critical"
        assert state["colourIntensity"]["red"] == 255
        assert state["colourIntensity"]["green"] == 0

    def test_post_tick_decrements_remaining_time(self) -> None:
        """POST /timers/{id}/tick reduces remaining_seconds."""
        create_response = client.post("/timers", json={"duration": 100})
        timer_id = create_response.json()["id"]
        response = client.post(f"/timers/{timer_id}/tick", json={"seconds_elapsed": 25})
        assert response.status_code == 200
        data = response.json()
        assert data["remainingTime"] == 75

    def test_post_tick_multiple_times(self) -> None:
        """POST /timers/{id}/tick can be called multiple times."""
        create_response = client.post("/timers", json={"duration": 100})
        timer_id = create_response.json()["id"]
        client.post(f"/timers/{timer_id}/tick", json={"seconds_elapsed": 30})
        response = client.post(f"/timers/{timer_id}/tick", json={"seconds_elapsed": 20})
        assert response.status_code == 200
        data = response.json()
        assert data["remainingTime"] == 50

    def test_post_reset_timer(self) -> None:
        """POST /timers/{id}/reset restores remaining_seconds to initial."""
        create_response = client.post("/timers", json={"duration": 60})
        timer_id = create_response.json()["id"]
        client.post(f"/timers/{timer_id}/tick", json={"seconds_elapsed": 40})
        response = client.post(f"/timers/{timer_id}/reset")
        assert response.status_code == 200
        data = response.json()
        assert data["remainingTime"] == 60

    def test_post_reset_updates_last_reset_at(self) -> None:
        """POST /timers/{id}/reset updates last_reset_at timestamp."""
        create_response = client.post("/timers", json={"duration": 50})
        timer_id = create_response.json()["id"]
        initial_reset = create_response.json()["lastResetAt"]
        client.post(f"/timers/{timer_id}/tick", json={"seconds_elapsed": 20})
        response = client.post(f"/timers/{timer_id}/reset")
        data = response.json()
        assert data["lastResetAt"] > initial_reset

    def test_delete_timer(self) -> None:
        """DELETE /timers/{id} removes timer from store."""
        create_response = client.post("/timers", json={"duration": 30})
        timer_id = create_response.json()["id"]
        response = client.delete(f"/timers/{timer_id}")
        assert response.status_code == 204
        get_response = client.get(f"/timers/{timer_id}")
        assert get_response.status_code == 404

    def test_delete_nonexistent_timer(self) -> None:
        """DELETE /timers/{id} with nonexistent ID returns 404."""
        fake_id = str(uuid.uuid4())
        response = client.delete(f"/timers/{fake_id}")
        assert response.status_code == 404

    def test_timer_response_schema(self) -> None:
        """Timer response includes all required fields."""
        response = client.post("/timers", json={"duration": 45})
        assert response.status_code == 201
        data = response.json()
        required_fields = [
            "id", "initialDuration", "remainingTime", "status",
            "urgencyLevel", "startedAt", "lastResetAt", "createdAt"
        ]
        for field in required_fields:
            assert field in data

    def test_timer_state_response_schema(self) -> None:
        """TimerState response includes all required fields."""
        create_response = client.post("/timers", json={"duration": 50})
        timer_id = create_response.json()["id"]
        response = client.get(f"/timers/{timer_id}/state")
        assert response.status_code == 200
        state = response.json()
        required_fields = [
            "id", "remainingTime", "remainingPercentage",
            "urgencyLevel", "colourIntensity", "facialExpression"
        ]
        for field in required_fields:
            assert field in state
        assert "red" in state["colourIntensity"]
        assert "green" in state["colourIntensity"]
        assert "blue" in state["colourIntensity"]

    def test_multiple_concurrent_timers(self) -> None:
        """Multiple timers can be created and tracked independently."""
        timer1 = client.post("/timers", json={"duration": 30}).json()
        timer2 = client.post("/timers", json={"duration": 60}).json()
        client.post(f"/timers/{timer1['id']}/tick", json={"seconds_elapsed": 10})
        response_1 = client.get(f"/timers/{timer1['id']}")
        response_2 = client.get(f"/timers/{timer2['id']}")
        assert response_1.json()["remainingTime"] == 20
        assert response_2.json()["remainingTime"] == 60

    def test_tick_on_nonexistent_timer(self) -> None:
        """POST /timers/{id}/tick with nonexistent ID returns 404."""
        fake_id = str(uuid.uuid4())
        response = client.post(f"/timers/{fake_id}/tick", json={"seconds_elapsed": 5})
        assert response.status_code == 404

    def test_reset_on_nonexistent_timer(self) -> None:
        """POST /timers/{id}/reset with nonexistent ID returns 404."""
        fake_id = str(uuid.uuid4())
        response = client.post(f"/timers/{fake_id}/reset")
        assert response.status_code == 404
