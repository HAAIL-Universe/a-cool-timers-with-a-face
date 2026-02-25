import pytest
from httpx import AsyncClient
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Timer, TimerEvent
from app.schemas import TimerState, TimerConfig, UrgencyState


@pytest.mark.asyncio
async def test_get_timer_state_initial(client: AsyncClient, test_db_session: AsyncSession):
    """Get timer state returns valid TimerState."""
    response = await client.get("/api/timer")
    assert response.status_code == 200
    data = response.json()
    assert "countdown" in data
    assert "duration" in data
    assert "is_paused" in data
    assert "is_expired" in data
    assert "urgency_level" in data
    assert "colour_intensity" in data


@pytest.mark.asyncio
async def test_configure_timer(client: AsyncClient, test_db_session: AsyncSession):
    """Configure timer with duration."""
    response = await client.post(
        "/api/timer",
        json={"duration": 60}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["duration"] == 60
    assert data["countdown"] == 60
    assert data["is_expired"] is False
    assert data["is_paused"] is True


@pytest.mark.asyncio
async def test_configure_timer_invalid_duration(client: AsyncClient):
    """Configure timer with invalid duration fails."""
    response = await client.post(
        "/api/timer",
        json={"duration": -5}
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_pause_timer(client: AsyncClient, test_db_session: AsyncSession):
    """Pause running timer."""
    await client.post("/api/timer", json={"duration": 60})
    response = await client.post("/api/timer/pause")
    assert response.status_code == 200
    data = response.json()
    assert data["is_paused"] is True


@pytest.mark.asyncio
async def test_resume_timer(client: AsyncClient, test_db_session: AsyncSession):
    """Resume paused timer."""
    await client.post("/api/timer", json={"duration": 60})
    await client.post("/api/timer/pause")
    response = await client.post("/api/timer/resume")
    assert response.status_code == 200
    data = response.json()
    assert data["is_paused"] is False


@pytest.mark.asyncio
async def test_reset_timer(client: AsyncClient, test_db_session: AsyncSession):
    """Reset timer before expiry."""
    await client.post("/api/timer", json={"duration": 60})
    response = await client.post("/api/timer/reset")
    assert response.status_code == 200
    data = response.json()
    assert data["countdown"] == 60
    assert data["is_expired"] is False


@pytest.mark.asyncio
async def test_reset_expired_timer_fails(client: AsyncClient, test_db_session: AsyncSession):
    """Reset expired timer returns 400."""
    timer = Timer(
        name="Test",
        duration_seconds=1,
        remaining_seconds=0,
        status="expired"
    )
    test_db_session.add(timer)
    await test_db_session.commit()

    response = await client.post("/api/timer/reset")
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_urgency_state(client: AsyncClient, test_db_session: AsyncSession):
    """Get current urgency state."""
    await client.post("/api/timer", json={"duration": 60})
    response = await client.get("/api/urgency")
    assert response.status_code == 200
    data = response.json()
    assert "urgency_level" in data
    assert data["urgency_level"] in ["calm", "anxious", "alarm"]
    assert "colour_intensity" in data
    assert 0.0 <= data["colour_intensity"] <= 1.0


@pytest.mark.asyncio
async def test_urgency_calm_high_time(client: AsyncClient, test_db_session: AsyncSession):
    """Urgency is calm when >66% time remains."""
    await client.post("/api/timer", json={"duration": 100})
    response = await client.get("/api/urgency")
    data = response.json()
    assert data["urgency_level"] == "calm"
    assert data["colour_intensity"] < 0.4


@pytest.mark.asyncio
async def test_urgency_anxious_medium_time(client: AsyncClient, test_db_session: AsyncSession):
    """Urgency is anxious when 33-66% time remains."""
    timer = Timer(
        name="Test",
        duration_seconds=100,
        remaining_seconds=50,
        status="running"
    )
    test_db_session.add(timer)
    await test_db_session.commit()

    response = await client.get("/api/urgency")
    data = response.json()
    assert data["urgency_level"] == "anxious"
    assert 0.4 <= data["colour_intensity"] <= 0.7


@pytest.mark.asyncio
async def test_urgency_alarm_low_time(client: AsyncClient, test_db_session: AsyncSession):
    """Urgency is alarm when <33% time remains."""
    timer = Timer(
        name="Test",
        duration_seconds=100,
        remaining_seconds=20,
        status="running"
    )
    test_db_session.add(timer)
    await test_db_session.commit()

    response = await client.get("/api/urgency")
    data = response.json()
    assert data["urgency_level"] == "alarm"
    assert data["colour_intensity"] > 0.7


@pytest.mark.asyncio
async def test_timer_state_structure(client: AsyncClient, test_db_session: AsyncSession):
    """TimerState response includes all required fields."""
    await client.post("/api/timer", json={"duration": 60})
    response = await client.get("/api/timer")
    data = response.json()
    
    required_fields = [
        "countdown",
        "duration",
        "is_paused",
        "is_expired",
        "urgency_level",
        "colour_intensity",
        "last_reset_at"
    ]
    for field in required_fields:
        assert field in data, f"Missing field: {field}"


@pytest.mark.asyncio
async def test_last_reset_at_timestamp(client: AsyncClient, test_db_session: AsyncSession):
    """last_reset_at is valid ISO8601 timestamp."""
    await client.post("/api/timer", json={"duration": 60})
    response = await client.get("/api/timer")
    data = response.json()
    
    last_reset_at = data["last_reset_at"]
    assert last_reset_at is not None
    datetime.fromisoformat(last_reset_at.replace("Z", "+00:00"))


@pytest.mark.asyncio
async def test_configure_overwrites_previous(client: AsyncClient, test_db_session: AsyncSession):
    """Configure timer overwrites previous duration."""
    await client.post("/api/timer", json={"duration": 60})
    response = await client.post("/api/timer", json={"duration": 120})
    data = response.json()
    assert data["duration"] == 120
    assert data["countdown"] == 120


@pytest.mark.asyncio
async def test_pause_then_reset_maintains_duration(client: AsyncClient, test_db_session: AsyncSession):
    """Reset after pause restores to configured duration."""
    await client.post("/api/timer", json={"duration": 60})
    await client.post("/api/timer/pause")
    response = await client.post("/api/timer/reset")
    data = response.json()
    assert data["countdown"] == 60
    assert data["is_paused"] is False
