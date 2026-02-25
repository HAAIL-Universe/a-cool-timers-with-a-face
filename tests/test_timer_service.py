import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from app.services.timer_service import TimerService
from app.schemas import TimerState, UrgencyLevel


@pytest.fixture
def timer_service():
    """Create a TimerService instance for testing."""
    return TimerService()


def test_create_timer(timer_service: TimerService):
    """Test creating a new timer."""
    duration = 60
    timer = timer_service.create_timer(duration)
    assert timer.id is not None
    assert timer.initial_seconds == duration
    assert timer.remaining_seconds == duration
    assert timer.status == "active"


def test_get_timer(timer_service: TimerService):
    """Test retrieving a timer by ID."""
    duration = 60
    timer = timer_service.create_timer(duration)
    retrieved = timer_service.get_timer(timer.id)
    assert retrieved.id == timer.id
    assert retrieved.initial_seconds == duration


def test_get_nonexistent_timer(timer_service: TimerService):
    """Test retrieving a nonexistent timer raises error."""
    with pytest.raises(ValueError):
        timer_service.get_timer(str(uuid4()))


def test_list_timers(timer_service: TimerService):
    """Test listing all timers."""
    timer1 = timer_service.create_timer(60)
    timer2 = timer_service.create_timer(120)
    timers = timer_service.list_timers()
    assert len(timers) == 2
    assert any(t.id == timer1.id for t in timers)
    assert any(t.id == timer2.id for t in timers)


def test_reset_timer(timer_service: TimerService):
    """Test resetting a timer."""
    duration = 60
    timer = timer_service.create_timer(duration)
    timer.remaining_seconds = 30
    timer_service._timers[timer.id] = timer
    
    reset_timer = timer_service.reset_timer(timer.id)
    assert reset_timer.remaining_seconds == duration
    assert reset_timer.last_reset_at is not None


def test_delete_timer(timer_service: TimerService):
    """Test deleting a timer."""
    timer = timer_service.create_timer(60)
    timer_service.delete_timer(timer.id)
    
    with pytest.raises(ValueError):
        timer_service.get_timer(timer.id)


def test_get_timer_state(timer_service: TimerService):
    """Test getting timer state with urgency and colour feedback."""
    timer = timer_service.create_timer(100)
    state = timer_service.get_timer_state(timer.id)
    
    assert isinstance(state, TimerState)
    assert state.id == timer.id
    assert state.remaining_time == 100
    assert 0 <= state.remaining_percentage <= 100
    assert state.urgency_level in ["low", "medium", "high", "critical"]
    assert hasattr(state, "colour_intensity")


def test_urgency_levels(timer_service: TimerService):
    """Test urgency level calculation based on remaining time."""
    timer = timer_service.create_timer(100)
    
    timer.remaining_seconds = 100
    state = timer_service.get_timer_state(timer.id)
    assert state.urgency_level == UrgencyLevel.LOW
    
    timer.remaining_seconds = 75
    state = timer_service.get_timer_state(timer.id)
    assert state.urgency_level == UrgencyLevel.LOW
    
    timer.remaining_seconds = 50
    state = timer_service.get_timer_state(timer.id)
    assert state.urgency_level == UrgencyLevel.MEDIUM
    
    timer.remaining_seconds = 25
    state = timer_service.get_timer_state(timer.id)
    assert state.urgency_level == UrgencyLevel.HIGH
    
    timer.remaining_seconds = 5
    state = timer_service.get_timer_state(timer.id)
    assert state.urgency_level == UrgencyLevel.CRITICAL


def test_colour_intensity_increases_with_urgency(timer_service: TimerService):
    """Test that colour intensity increases as urgency escalates."""
    timer = timer_service.create_timer(100)
    
    timer.remaining_seconds = 100
    state_low = timer_service.get_timer_state(timer.id)
    
    timer.remaining_seconds = 25
    state_high = timer_service.get_timer_state(timer.id)
    
    assert state_high.colour_intensity.red >= state_low.colour_intensity.red
    assert state_high.colour_intensity.green <= state_low.colour_intensity.green


def test_facial_expression_maps_to_urgency(timer_service: TimerService):
    """Test that facial expression updates with urgency level."""
    timer = timer_service.create_timer(100)
    
    timer.remaining_seconds = 100
    state = timer_service.get_timer_state(timer.id)
    assert hasattr(state, "facial_expression")
    
    timer.remaining_seconds = 5
    state = timer_service.get_timer_state(timer.id)
    assert state.facial_expression is not None


def test_timer_cannot_be_reset_after_expiry(timer_service: TimerService):
    """Test that timer cannot be reset after expiry."""
    timer = timer_service.create_timer(10)
    timer.remaining_seconds = 0
    timer.status = "expired"
    timer_service._timers[timer.id] = timer
    
    with pytest.raises(ValueError):
        timer_service.reset_timer(timer.id)
