import pytest
from httpx import AsyncClient
from app.main import app
from app.dependencies import get_timer_repo, get_timer_service
from app.repos.timer_repo import TimerRepo
from app.services.timer_service import TimerService


@pytest.fixture
def timer_repo():
    """In-memory timer repository for testing."""
    return TimerRepo()


@pytest.fixture
def timer_service(timer_repo):
    """Timer service with injected repository."""
    return TimerService(timer_repo)


@pytest.fixture
def client(timer_repo, timer_service):
    """FastAPI test client with dependency overrides."""
    app.dependency_overrides[get_timer_repo] = lambda: timer_repo
    app.dependency_overrides[get_timer_service] = lambda: timer_service
    return AsyncClient(app=app, base_url="http://test")


@pytest.mark.asyncio
async def test_create_timer(client):
    """POST /timers with duration returns 201 with valid UUID and status=active."""
    response = await client.post("/timers", json={"duration": 30})
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["status"] == "active"
    assert data["initialDuration"] == 30
    assert data["remainingTime"] == 30
    assert len(data["id"]) == 36  # UUID format


@pytest.mark.asyncio
async def test_get_all_timers(client):
    """GET /timers returns list of timers."""
    await client.post("/timers", json={"duration": 20})
    await client.post("/timers", json={"duration": 40})
    
    response = await client.get("/timers")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


@pytest.mark.asyncio
async def test_get_timer_by_id(client):
    """GET /timers/{timerId} returns timer details."""
    create_response = await client.post("/timers", json={"duration": 25})
    timer_id = create_response.json()["id"]
    
    response = await client.get(f"/timers/{timer_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == timer_id
    assert data["initialDuration"] == 25


@pytest.mark.asyncio
async def test_get_timer_state(client):
    """GET /timers/{timerId}/state returns urgency, colour, and facial expression."""
    create_response = await client.post("/timers", json={"duration": 100})
    timer_id = create_response.json()["id"]
    
    response = await client.get(f"/timers/{timer_id}/state")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == timer_id
    assert "remainingTime" in data
    assert "remainingPercentage" in data
    assert "urgencyLevel" in data
    assert data["urgencyLevel"] in ["low", "medium", "high", "critical"]
    assert "colourIntensity" in data
    assert "red" in data["colourIntensity"]
    assert "green" in data["colourIntensity"]
    assert "blue" in data["colourIntensity"]
    assert "facialExpression" in data


@pytest.mark.asyncio
async def test_reset_timer(client):
    """POST /timers/{timerId}/reset resets remainingTime to initialDuration."""
    create_response = await client.post("/timers", json={"duration": 50})
    timer_id = create_response.json()["id"]
    
    reset_response = await client.post(f"/timers/{timer_id}/reset")
    assert reset_response.status_code == 200
    data = reset_response.json()
    assert data["remainingTime"] == data["initialDuration"]
    assert data["remainingTime"] == 50


@pytest.mark.asyncio
async def test_delete_timer(client):
    """DELETE /timers/{timerId} removes timer."""
    create_response = await client.post("/timers", json={"duration": 30})
    timer_id = create_response.json()["id"]
    
    delete_response = await client.delete(f"/timers/{timer_id}")
    assert delete_response.status_code == 204
    
    get_response = await client.get(f"/timers/{timer_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_get_nonexistent_timer(client):
    """GET /timers/{nonexistentId} returns 404."""
    response = await client.get("/timers/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_reset_nonexistent_timer(client):
    """POST /timers/{nonexistentId}/reset returns 404."""
    response = await client.post("/timers/00000000-0000-0000-0000-000000000000/reset")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_nonexistent_timer(client):
    """DELETE /timers/{nonexistentId} returns 404."""
    response = await client.delete("/timers/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_timer_urgency_thresholds(client):
    """Verify urgency levels match expected thresholds."""
    create_response = await client.post("/timers", json={"duration": 100})
    timer_id = create_response.json()["id"]
    
    state_response = await client.get(f"/timers/{timer_id}/state")
    data = state_response.json()
    
    percentage = data["remainingPercentage"]
    urgency = data["urgencyLevel"]
    
    if percentage > 50:
        assert urgency == "low"
    elif 25 < percentage <= 50:
        assert urgency == "medium"
    elif 10 < percentage <= 25:
        assert urgency == "high"
    elif percentage <= 10:
        assert urgency == "critical"


@pytest.mark.asyncio
async def test_colour_intensity_values(client):
    """Verify colour intensity RGB values are within valid range."""
    create_response = await client.post("/timers", json={"duration": 100})
    timer_id = create_response.json()["id"]
    
    state_response = await client.get(f"/timers/{timer_id}/state")
    data = state_response.json()
    
    colour = data["colourIntensity"]
    for channel in ["red", "green", "blue"]:
        assert 0 <= colour[channel] <= 255


@pytest.mark.asyncio
async def test_facial_expression_mapping(client):
    """Verify facial expression is a valid string."""
    create_response = await client.post("/timers", json={"duration": 100})
    timer_id = create_response.json()["id"]
    
    state_response = await client.get(f"/timers/{timer_id}/state")
    data = state_response.json()
    
    assert isinstance(data["facialExpression"], str)
    assert len(data["facialExpression"]) > 0


@pytest.mark.asyncio
async def test_multiple_timers_independent_state(client):
    """Verify multiple timers maintain independent state."""
    resp1 = await client.post("/timers", json={"duration": 30})
    resp2 = await client.post("/timers", json={"duration": 60})
    
    timer_id_1 = resp1.json()["id"]
    timer_id_2 = resp2.json()["id"]
    
    state1 = (await client.get(f"/timers/{timer_id_1}/state")).json()
    state2 = (await client.get(f"/timers/{timer_id_2}/state")).json()
    
    assert state1["remainingTime"] == 30
    assert state2["remainingTime"] == 60


@pytest.mark.asyncio
async def test_reset_does_not_affect_other_timers(client):
    """Verify reset on one timer does not affect others."""
    resp1 = await client.post("/timers", json={"duration": 50})
    resp2 = await client.post("/timers", json={"duration": 50})
    
    timer_id_1 = resp1.json()["id"]
    timer_id_2 = resp2.json()["id"]
    
    await client.post(f"/timers/{timer_id_1}/reset")
    
    state2 = (await client.get(f"/timers/{timer_id_2}/state")).json()
    assert state2["remainingTime"] == 50
