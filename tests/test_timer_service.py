import pytest
from uuid import UUID
from datetime import datetime

from app.models.timer import Timer, TimerCreate, TimerStatus, UrgencyLevel
from app.repos.timer_repo import TimerRepository
from app.services.timer_service import TimerService


@pytest.fixture
def timer_repo() -> TimerRepository:
    """Provide a fresh timer repository for each test."""
    return TimerRepository()


@pytest.fixture
def timer_service(timer_repo: TimerRepository) -> TimerService:
    """Provide a timer service with an in-memory repository."""
    return TimerService(timer_repo)


class TestTimerServiceCreate:
    """Tests for timer creation."""

    def test_create_timer(self, timer_service: TimerService) -> None:
        """Create a timer with initial duration."""
        timer_create = TimerCreate(initial_seconds=60)
        timer = timer_service.create_timer(timer_create)
        
        assert timer.id is not None
        assert timer.initial_seconds == 60
        assert timer.remaining_seconds == 60
        assert timer.status == TimerStatus.active
        assert timer.urgency_level == UrgencyLevel.low

    def test_create_timer_sets_timestamps(self, timer_service: TimerService) -> None:
        """Verify timestamps are set on creation."""
        timer_create = TimerCreate(initial_seconds=30)
        timer = timer_service.create_timer(timer_create)
        
        assert timer.created_at is not None
        assert timer.updated_at is not None
        assert timer.started_at is not None


class TestTimerServiceRetrieval:
    """Tests for timer retrieval."""

    def test_get_timer_by_id(self, timer_service: TimerService) -> None:
        """Retrieve an existing timer."""
        timer_create = TimerCreate(initial_seconds=45)
        created = timer_service.create_timer(timer_create)
        
        retrieved = timer_service.get_timer(created.id)
        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.initial_seconds == 45

    def test_get_nonexistent_timer(self, timer_service: TimerService) -> None:
        """Attempting to get nonexistent timer returns None."""
        fake_id = UUID('00000000-0000-0000-0000-000000000000')
        timer = timer_service.get_timer(fake_id)
        assert timer is None

    def test_list_all_timers(self, timer_service: TimerService) -> None:
        """List all created timers."""
        timer_service.create_timer(TimerCreate(initial_seconds=60))
        timer_service.create_timer(TimerCreate(initial_seconds=30))
        timer_service.create_timer(TimerCreate(initial_seconds=120))
        
        timers = timer_service.list_all_timers()
        assert len(timers) == 3


class TestTimerServiceReset:
    """Tests for timer reset functionality."""

    def test_reset_timer(self, timer_service: TimerService) -> None:
        """Reset timer restores initial duration."""
        timer_create = TimerCreate(initial_seconds=60)
        timer = timer_service.create_timer(timer_create)
        
        timer.remaining_seconds = 10
        timer_service.repo.update(timer.id, timer)
        
        reset_timer = timer_service.reset_timer(timer.id)
        assert reset_timer is not None
        assert reset_timer.remaining_seconds == 60
        assert reset_timer.status == TimerStatus.active
        assert reset_timer.urgency_level == UrgencyLevel.low

    def test_reset_timer_updates_timestamp(self, timer_service: TimerService) -> None:
        """Reset updates last_reset_at timestamp."""
        timer = timer_service.create_timer(TimerCreate(initial_seconds=60))
        original_reset = timer.last_reset_at
        
        reset_timer = timer_service.reset_timer(timer.id)
        assert reset_timer is not None
        assert reset_timer.last_reset_at >= original_reset

    def test_reset_nonexistent_timer(self, timer_service: TimerService) -> None:
        """Resetting nonexistent timer returns None."""
        fake_id = UUID('00000000-0000-0000-0000-000000000000')
        result = timer_service.reset_timer(fake_id)
        assert result is None


class TestTimerServiceTick:
    """Tests for timer countdown."""

    def test_tick_decrements_remaining_time(self, timer_service: TimerService) -> None:
        """Tick decrements remaining seconds by 1."""
        timer = timer_service.create_timer(TimerCreate(initial_seconds=60))
        
        ticked = timer_service.tick_timer(timer.id)
        assert ticked is not None
        assert ticked.remaining_seconds == 59

    def test_tick_multiple_times(self, timer_service: TimerService) -> None:
        """Multiple ticks accumulate."""
        timer = timer_service.create_timer(TimerCreate(initial_seconds=60))
        
        for _ in range(5):
            timer_service.tick_timer(timer.id)
        
        result = timer_service.get_timer(timer.id)
        assert result is not None
        assert result.remaining_seconds == 55

    def test_tick_sets_expired_at_zero(self, timer_service: TimerService) -> None:
        """Timer expires when remaining reaches zero."""
        timer = timer_service.create_timer(TimerCreate(initial_seconds=1))
        
        ticked = timer_service.tick_timer(timer.id)
        assert ticked is not None
        assert ticked.remaining_seconds == 0
        assert ticked.status == TimerStatus.expired

    def test_tick_expired_timer_does_nothing(self, timer_service: TimerService) -> None:
        """Ticking expired timer has no effect."""
        timer = timer_service.create_timer(TimerCreate(initial_seconds=1))
        timer_service.tick_timer(timer.id)
        
        result = timer_service.tick_timer(timer.id)
        assert result is None

    def test_tick_paused_timer_does_nothing(self, timer_service: TimerService) -> None:
        """Ticking paused timer has no effect."""
        timer = timer_service.create_timer(TimerCreate(initial_seconds=60))
        timer_service.stop_timer(timer.id)
        
        result = timer_service.tick_timer(timer.id)
        assert result is None


class TestTimerServiceUrgency:
    """Tests for urgency level calculation."""

    def test_urgency_low_above_50_percent(self, timer_service: TimerService) -> None:
        """Urgency is low when remaining > 50%."""
        timer = timer_service.create_timer(TimerCreate(initial_seconds=100))
        
        urgency = timer_service._calculate_urgency(100, 51)
        assert urgency == UrgencyLevel.low

    def test_urgency_medium_25_to_50_percent(self, timer_service: TimerService) -> None:
        """Urgency is medium when 25% < remaining <= 50%."""
        urgency = timer_service._calculate_urgency(100, 40)
        assert urgency == UrgencyLevel.medium

    def test_urgency_high_10_to_25_percent(self, timer_service: TimerService) -> None:
        """Urgency is high when 10% < remaining <= 25%."""
        urgency = timer_service._calculate_urgency(100, 20)
        assert urgency == UrgencyLevel.high

    def test_urgency_critical_below_10_percent(self, timer_service: TimerService) -> None:
        """Urgency is critical when remaining <= 10%."""
        urgency = timer_service._calculate_urgency(100, 5)
        assert urgency == UrgencyLevel.critical

    def test_urgency_critical_at_zero(self, timer_service: TimerService) -> None:
        """Urgency is critical when remaining is zero."""
        urgency = timer_service._calculate_urgency(100, 0)
        assert urgency == UrgencyLevel.critical

    def test_urgency_low_for_zero_initial(self, timer_service: TimerService) -> None:
        """Urgency defaults to low for zero initial duration."""
        urgency = timer_service._calculate_urgency(0, 0)
        assert urgency == UrgencyLevel.low


class TestTimerServiceControl:
    """Tests for timer start/stop control."""

    def test_start_paused_timer(self, timer_service: TimerService) -> None:
        """Start resumes a paused timer."""
        timer = timer_service.create_timer(TimerCreate(initial_seconds=60))
        timer_service.stop_timer(timer.id)
        
        started = timer_service.start_timer(timer.id)
        assert started is not None
        assert started.status == TimerStatus.active

    def test_stop_active_timer(self, timer_service: TimerService) -> None:
        """Stop pauses an active timer."""
        timer = timer_service.create_timer(TimerCreate(initial_seconds=60))
        
        stopped = timer_service.stop_timer(timer.id)
        assert stopped is not None
        assert stopped.status == TimerStatus.paused

    def test_start_nonexistent_timer(self, timer_service: TimerService) -> None:
        """Starting nonexistent timer returns None."""
        fake_id = UUID('00000000-0000-0000-0000-000000000000')
        result = timer_service.start_timer(fake_id)
        assert result is None

    def test_stop_nonexistent_timer(self, timer_service: TimerService) -> None:
        """Stopping nonexistent timer returns None."""
        fake_id = UUID('00000000-0000-0000-0000-000000000000')
        result = timer_service.stop_timer(fake_id)
        assert result is None


class TestTimerServiceDelete:
    """Tests for timer deletion."""

    def test_delete_timer(self, timer_service: TimerService) -> None:
        """Delete removes a timer."""
        timer = timer_service.create_timer(TimerCreate(initial_seconds=60))
        
        result = timer_service.delete_timer(timer.id)
        assert result is True
        assert timer_service.get_timer(timer.id) is None

    def test_delete_nonexistent_timer(self, timer_service: TimerService) -> None:
        """Deleting nonexistent timer returns False."""
        fake_id = UUID('00000000-0000-0000-0000-000000000000')
        result = timer_service.delete_timer(fake_id)
        assert result is False
