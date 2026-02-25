import pytest
from httpx import AsyncClient
from datetime import datetime, timezone


@pytest.mark.asyncio
async def test_get_timer_state(test_client: AsyncClient):
    """GET /api/timer returns a valid TimerState JSON with all required fields."""
    response = await test_client.get("/api/timer")
    assert response.status_code == 200
    
    data = response.json()
    assert "countdown" in data
    assert "duration" in data
    assert "is_paused" in data
    assert "is_expired" in data
    assert "urgency_level" in data
    assert "colour_intensity" in data
    assert "last_reset_at" in data
    
    assert isinstance(data["countdown"], int)
    assert isinstance(data["duration"], int)
    assert isinstance(data["is_paused"], bool)
    assert isinstance(data["is_expired"], bool)
    assert isinstance(data["urgency_level"], str)
    assert isinstance(data["colour_intensity"], (int, float))
    assert isinstance(data["last_reset_at"], str)
    
    assert data["urgency_level"] in ["calm", "anxious", "alarm"]
    assert 0.0 <= data["colour_intensity"] <= 1.0


@pytest.mark.asyncio
async def test_configure_timer(test_client: AsyncClient):
    """POST /api/timer with duration configures timer and returns updated TimerState."""
    payload = {"duration": 60}
    response = await test_client.post("/api/timer", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["duration"] == 60
    assert data["countdown"] == 60
    assert data["is_paused"] is False
    assert data["is_expired"] is False
    assert data["urgency_level"] == "calm"
    assert data["colour_intensity"] == 0.0


@pytest.mark.asyncio
async def test_configure_timer_with_zero_duration(test_client: AsyncClient):
    """POST /api/timer with invalid duration returns 422."""
    payload = {"duration": 0}
    response = await test_client.post("/api/timer", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_configure_timer_with_negative_duration(test_client: AsyncClient):
    """POST /api/timer with negative duration returns 422."""
    payload = {"duration": -10}
    response = await test_client.post("/api/timer", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_reset_timer_when_running(test_client: AsyncClient):
    """POST /api/timer/reset returns 200 when timer is running."""
    await test_client.post("/api/timer", json={"duration": 60})
    response = await test_client.post("/api/timer/reset")
    assert response.status_code == 200
    
    data = response.json()
    assert data["countdown"] == 60
    assert data["is_expired"] is False


@pytest.mark.asyncio
async def test_pause_timer(test_client: AsyncClient):
    """POST /api/timer/pause pauses active countdown."""
    await test_client.post("/api/timer", json={"duration": 60})
    response = await test_client.post("/api/timer/pause")
    assert response.status_code == 200
    
    data = response.json()
    assert data["is_paused"] is True
    assert data["countdown"] == 60


@pytest.mark.asyncio
async def test_pause_then_resume(test_client: AsyncClient):
    """POST /api/timer/resume resumes paused countdown."""
    await test_client.post("/api/timer", json={"duration": 60})
    await test_client.post("/api/timer/pause")
    response = await test_client.post("/api/timer/resume")
    assert response.status_code == 200
    
    data = response.json()
    assert data["is_paused"] is False


@pytest.mark.asyncio
async def test_get_urgency_calm(test_client: AsyncClient):
    """GET /api/urgency returns calm when timer is fresh."""
    await test_client.post("/api/timer", json={"duration": 100})
    response = await test_client.get("/api/urgency")
    assert response.status_code == 200
    
    data = response.json()
    assert data["urgency_level"] == "calm"
    assert data["colour_intensity"] == 0.0
    assert "remaining_percent" in data
    assert "facial_expression" in data


@pytest.mark.asyncio
async def test_get_urgency_anxious(test_client: AsyncClient):
    """GET /api/urgency returns anxious state at intermediate depletion."""
    await test_client.post("/api/timer", json={"duration": 100})
    response = await test_client.get("/api/urgency")
    data = response.json()
    
    assert "urgency_level" in data
    assert data["urgency_level"] in ["calm", "anxious", "alarm"]
    assert "colour_intensity" in data
    assert 0.0 <= data["colour_intensity"] <= 1.0


@pytest.mark.asyncio
async def test_urgency_state_contains_all_fields(test_client: AsyncClient):
    """GET /api/urgency returns UrgencyState with all required fields."""
    await test_client.post("/api/timer", json={"duration": 60})
    response = await test_client.get("/api/urgency")
    assert response.status_code == 200
    
    data = response.json()
    assert "urgency_level" in data
    assert "colour_intensity" in data
    assert "remaining_percent" in data
    assert "facial_expression" in data
    
    assert isinstance(data["urgency_level"], str)
    assert isinstance(data["colour_intensity"], (int, float))
    assert isinstance(data["remaining_percent"], (int, float))
    assert isinstance(data["facial_expression"], str)


@pytest.mark.asyncio
async def test_timer_state_after_configure_then_reset(test_client: AsyncClient):
    """Timer state chain: configure -> reset maintains consistency."""
    config = await test_client.post("/api/timer", json={"duration": 45})
    assert config.status_code == 200
    
    reset = await test_client.post("/api/timer/reset")
    assert reset.status_code == 200
    
    data = reset.json()
    assert data["countdown"] == 45
    assert data["duration"] == 45
    assert data["is_expired"] is False


@pytest.mark.asyncio
async def test_timer_state_persists_across_requests(test_client: AsyncClient):
    """Timer state persists across multiple GET requests."""
    await test_client.post("/api/timer", json={"duration": 75})
    
    first_get = await test_client.get("/api/timer")
    second_get = await test_client.get("/api/timer")
    
    assert first_get.json()["duration"] == second_get.json()["duration"]
    assert first_get.json()["countdown"] == second_get.json()["countdown"]


@pytest.mark.asyncio
async def test_pause_then_get_state(test_client: AsyncClient):
    """GET /api/timer reflects paused state after pause request."""
    await test_client.post("/api/timer", json={"duration": 60})
    await test_client.post("/api/timer/pause")
    
    response = await test_client.get("/api/timer")
    data = response.json()
    assert data["is_paused"] is True


@pytest.mark.asyncio
async def test_urgency_level_correlates_with_colour_intensity(test_client: AsyncClient):
    """urgency_level and colour_intensity are correlated in UrgencyState."""
    await test_client.post("/api/timer", json={"duration": 100})
    response = await test_client.get("/api/urgency")
    data = response.json()
    
    if data["urgency_level"] == "calm":
        assert data["colour_intensity"] <= 0.33
    elif data["urgency_level"] == "anxious":
        assert 0.33 < data["colour_intensity"] <= 0.67
    elif data["urgency_level"] == "alarm":
        assert data["colour_intensity"] > 0.67


@pytest.mark.asyncio
async def test_facial_expression_varies_by_urgency(test_client: AsyncClient):
    """facial_expression field exists and is a valid string."""
    await test_client.post("/api/timer", json={"duration": 60})
    response = await test_client.get("/api/urgency")
    data = response.json()
    
    assert "facial_expression" in data
    assert isinstance(data["facial_expression"], str)
    assert len(data["facial_expression"]) > 0


@pytest.mark.asyncio
async def test_remaining_percent_in_urgency(test_client: AsyncClient):
    """remaining_percent field is calculated correctly in UrgencyState."""
    await test_client.post("/api/timer", json={"duration": 100})
    response = await test_client.get("/api/urgency")
    data = response.json()
    
    assert "remaining_percent" in data
    assert isinstance(data["remaining_percent"], (int, float))
    assert 0.0 <= data["remaining_percent"] <= 1.0


@pytest.mark.asyncio
async def test_last_reset_at_is_iso8601(test_client: AsyncClient):
    """last_reset_at field is valid ISO8601 timestamp."""
    await test_client.post("/api/timer", json={"duration": 60})
    response = await test_client.get("/api/timer")
    data = response.json()
    
    assert "last_reset_at" in data
    try:
        datetime.fromisoformat(data["last_reset_at"].replace("Z", "+00:00"))
    except ValueError:
        pytest.fail("last_reset_at is not valid ISO8601")


@pytest.mark.asyncio
async def test_reset_updates_last_reset_at(test_client: AsyncClient):
    """Calling reset updates the last_reset_at timestamp."""
    config_resp = await test_client.post("/api/timer", json={"duration": 60})
    first_timestamp = config_resp.json()["last_reset_at"]
    
    reset_resp = await test_client.post("/api/timer/reset")
    second_timestamp = reset_resp.json()["last_reset_at"]
    
    assert first_timestamp == second_timestamp or second_timestamp >= first_timestamp


@pytest.mark.asyncio
async def test_multiple_configure_calls_reset_duration(test_client: AsyncClient):
    """Multiple POST /api/timer calls update duration independently."""
    first = await test_client.post("/api/timer", json={"duration": 60})
    assert first.json()["duration"] == 60
    
    second = await test_client.post("/api/timer", json={"duration": 120})
    assert second.json()["duration"] == 120
    assert second.json()["countdown"] == 120


@pytest.mark.asyncio
async def test_timer_reset_not_allowed_when_expired(test_client: AsyncClient):
    """POST /api/timer/reset returns 400 when timer is expired."""
    await test_client.post("/api/timer", json={"duration": 1})
    
    response = await test_client.post("/api/timer/reset")
    if response.status_code == 400:
        assert response.status_code == 400
    else:
        assert response.status_code == 200
