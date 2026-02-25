import pytest
from datetime import datetime
from uuid import uuid4

from app.models.timer import (
    Timer,
    TimerCreate,
    TimerStatus,
    UrgencyLevel,
    TimerSession,
    TimerEvent,
)
from app.services.timer_service import TimerService
from app.repos.timer_repo import TimerRepository


@pytest.fixture
def timer_repo():
    """In-memory timer repository for testing."""
    return TimerRepository()


@pytest.fixture
def timer_service(timer_repo):
    """Timer service with in-memory repository."""
    return TimerService(repo=timer_repo)


class TestTimerServiceCreate:
    """Tests for timer creation."""

    def test_create_timer_success(self, timer_service: TimerService):
        """Create a timer with valid duration."""
        timer = timer_service.create_timer(initial_seconds=300)
        assert timer.id is not None
        assert timer.initial_seconds == 300
        assert timer.remaining_seconds == 300
        assert timer.status == TimerStatus.ACTIVE
        assert timer.urgency_level == UrgencyLevel.LOW

    def test_create_timer_invalid_duration(self, timer_service: TimerService):
        """Reject timer with zero or negative duration."""
        with pytest.raises(ValueError):
            timer_service.create_timer(initial_seconds=0)

        with pytest.raises(ValueError):
            timer_service.create_timer(initial_seconds=-10)


class TestTimerServiceGetTimer:
    """Tests for retrieving timer state."""

    def test_get_timer_by_id(self, timer_service: TimerService):
        """Retrieve timer by ID."""
        created = timer_service.create_timer(initial_seconds=300)
        retrieved = timer_service.get_timer(created.id)
        assert retrieved.id == created.id
        assert retrieved.remaining_seconds == 300

    def test_get_timer_not_found(self, timer_service: TimerService):
        """Return None for non-existent timer."""
        fake_id = uuid4()
        result = timer_service.get_timer(fake_id)
        assert result is None

    def test_get_all_timers(self, timer_service: TimerService):
        """Retrieve all active timers."""
        timer1 = timer_service.create_timer(initial_seconds=300)
        timer2 = timer_service.create_timer(initial_seconds=600)
        all_timers = timer_service.get_all_timers()
        assert len(all_timers) == 2
        assert any(t.id == timer1.id for t in all_timers)
        assert any(t.id == timer2.id for t in all_timers)


class TestTimerServiceUrgency:
    """Tests for urgency level calculation."""

    def test_urgency_low(self, timer_service: TimerService):
        """Low urgency when >75% time remaining."""
        timer = timer_service.create_timer(initial_seconds=100)
        timer.remaining_seconds = 80
        urgency = timer_service.calculate_urgency(timer)
        assert urgency == UrgencyLevel.LOW

    def test_urgency_medium(self, timer_service: TimerService):
        """Medium urgency when 50-75% time remaining."""
        timer = timer_service.create_timer(initial_seconds=100)
        timer.remaining_seconds = 60
        urgency = timer_service.calculate_urgency(timer)
        assert urgency == UrgencyLevel.MEDIUM

    def test_urgency_high(self, timer_service: TimerService):
        """High urgency when 25-50% time remaining."""
        timer = timer_service.create_timer(initial_seconds=100)
        timer.remaining_seconds = 40
        urgency = timer_service.calculate_urgency(timer)
        assert urgency == UrgencyLevel.HIGH

    def test_urgency_critical(self, timer_service: TimerService):
        """Critical urgency when <25% time remaining."""
        timer = timer_service.create_timer(initial_seconds=100)
        timer.remaining_seconds = 20
        urgency = timer_service.calculate_urgency(timer)
        assert urgency == UrgencyLevel.CRITICAL

    def test_urgency_expired(self, timer_service: TimerService):
        """Critical urgency when time reaches zero."""
        timer = timer_service.create_timer(initial_seconds=100)
        timer.remaining_seconds = 0
        urgency = timer_service.calculate_urgency(timer)
        assert urgency == UrgencyLevel.CRITICAL


class TestTimerServiceReset:
    """Tests for timer reset functionality."""

    def test_reset_timer_success(self, timer_service: TimerService):
        """Reset timer to initial duration."""
        timer = timer_service.create_timer(initial_seconds=300)
        timer.remaining_seconds = 150
        reset_timer = timer_service.reset_timer(timer.id)
        assert reset_timer.remaining_seconds == 300
        assert reset_timer.status == TimerStatus.ACTIVE

    def test_reset_nonexistent_timer(self, timer_service: TimerService):
        """Reject reset for non-existent timer."""
        with pytest.raises(ValueError):
            timer_service.reset_timer(uuid4())

    def test_reset_updates_last_reset_at(self, timer_service: TimerService):
        """Update last_reset_at timestamp on reset."""
        timer = timer_service.create_timer(initial_seconds=300)
        original_reset = timer.last_reset_at
        reset_timer = timer_service.reset_timer(timer.id)
        assert reset_timer.last_reset_at > original_reset


class TestTimerServiceDecrement:
    """Tests for timer countdown."""

    def test_decrement_active_timer(self, timer_service: TimerService):
        """Decrement remaining seconds on active timer."""
        timer = timer_service.create_timer(initial_seconds=300)
        decremented = timer_service.decrement_timer(timer.id, seconds=10)
        assert decremented.remaining_seconds == 290

    def test_decrement_paused_timer_raises(self, timer_service: TimerService):
        """Reject decrement on paused timer."""
        timer = timer_service.create_timer(initial_seconds=300)
        timer.status = TimerStatus.PAUSED
        with pytest.raises(ValueError):
            timer_service.decrement_timer(timer.id, seconds=10)

    def test_decrement_to_zero_expires_timer(self, timer_service: TimerService):
        """Mark timer as expired when countdown reaches zero."""
        timer = timer_service.create_timer(initial_seconds=300)
        decremented = timer_service.decrement_timer(timer.id, seconds=300)
        assert decremented.remaining_seconds == 0
        assert decremented.status == TimerStatus.EXPIRED

    def test_decrement_clamps_at_zero(self, timer_service: TimerService):
        """Never allow remaining seconds below zero."""
        timer = timer_service.create_timer(initial_seconds=300)
        decremented = timer_service.decrement_timer(timer.id, seconds=500)
        assert decremented.remaining_seconds == 0

    def test_decrement_nonexistent_timer(self, timer_service: TimerService):
        """Reject decrement for non-existent timer."""
        with pytest.raises(ValueError):
            timer_service.decrement_timer(uuid4(), seconds=10)


class TestTimerServicePauseResume:
    """Tests for pause/resume functionality."""

    def test_pause_active_timer(self, timer_service: TimerService):
        """Pause an active timer."""
        timer = timer_service.create_timer(initial_seconds=300)
        paused = timer_service.pause_timer(timer.id)
        assert paused.status == TimerStatus.PAUSED

    def test_resume_paused_timer(self, timer_service: TimerService):
        """Resume a paused timer."""
        timer = timer_service.create_timer(initial_seconds=300)
        paused = timer_service.pause_timer(timer.id)
        resumed = timer_service.resume_timer(timer.id)
        assert resumed.status == TimerStatus.ACTIVE

    def test_pause_expired_timer_raises(self, timer_service: TimerService):
        """Reject pause on expired timer."""
        timer = timer_service.create_timer(initial_seconds=300)
        timer.status = TimerStatus.EXPIRED
        with pytest.raises(ValueError):
            timer_service.pause_timer(timer.id)

    def test_resume_nonexistent_timer(self, timer_service: TimerService):
        """Reject resume for non-existent timer."""
        with pytest.raises(ValueError):
            timer_service.resume_timer(uuid4())


class TestTimerServiceDelete:
    """Tests for timer deletion."""

    def test_delete_timer_success(self, timer_service: TimerService):
        """Delete an existing timer."""
        timer = timer_service.create_timer(initial_seconds=300)
        result = timer_service.delete_timer(timer.id)
        assert result is True
        assert timer_service.get_timer(timer.id) is None

    def test_delete_nonexistent_timer(self, timer_service: TimerService):
        """Return False when deleting non-existent timer."""
        result = timer_service.delete_timer(uuid4())
        assert result is False


class TestTimerServiceColourMapping:
    """Tests for colour intensity calculation."""

    def test_colour_low_urgency(self, timer_service: TimerService):
        """Green colour for low urgency."""
        timer = timer_service.create_timer(initial_seconds=100)
        timer.remaining_seconds = 80
        colour = timer_service.calculate_colour(timer)
        assert colour["red"] == 0
        assert colour["green"] == 255
        assert colour["blue"] == 0

    def test_colour_medium_urgency(self, timer_service: TimerService):
        """Yellow colour for medium urgency."""
        timer = timer_service.create_timer(initial_seconds=100)
        timer.remaining_seconds = 60
        colour = timer_service.calculate_colour(timer)
        assert colour["red"] == 255
        assert colour["green"] == 255
        assert colour["blue"] == 0

    def test_colour_high_urgency(self, timer_service: TimerService):
        """Orange colour for high urgency."""
        timer = timer_service.create_timer(initial_seconds=100)
        timer.remaining_seconds = 40
        colour = timer_service.calculate_colour(timer)
        assert colour["red"] == 255
        assert colour["green"] > 0
        assert colour["green"] < 255
        assert colour["blue"] == 0

    def test_colour_critical_urgency(self, timer_service: TimerService):
        """Red colour for critical urgency."""
        timer = timer_service.create_timer(initial_seconds=100)
        timer.remaining_seconds = 10
        colour = timer_service.calculate_colour(timer)
        assert colour["red"] == 255
        assert colour["green"] == 0
        assert colour["blue"] == 0
