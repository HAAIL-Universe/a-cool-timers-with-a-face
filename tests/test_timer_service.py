import pytest
from datetime import datetime
from uuid import uuid4
from app.services.timer_service import TimerService
from app.repos.timer_repo import TimerRepository
from app.models.timer import Timer, TimerStatus, UrgencyLevel


@pytest.fixture
def timer_repo():
    """Initialize in-memory timer repository."""
    return TimerRepository()


@pytest.fixture
def timer_service(timer_repo):
    """Initialize timer service with repository."""
    return TimerService(timer_repo)


class TestTimerServiceCreation:
    """Test timer creation and initialization."""

    def test_create_timer(self, timer_service):
        """Create a new timer with valid duration."""
        timer = timer_service.create_timer(duration=60)
        assert timer.id is not None
        assert timer.initial_seconds == 60
        assert timer.remaining_seconds == 60
        assert timer.status == TimerStatus.ACTIVE
        assert timer.urgency_level == UrgencyLevel.LOW

    def test_create_timer_invalid_duration(self, timer_service):
        """Reject timer creation with invalid duration."""
        with pytest.raises(ValueError):
            timer_service.create_timer(duration=0)
        with pytest.raises(ValueError):
            timer_service.create_timer(duration=-10)


class TestTimerServiceReset:
    """Test timer reset mechanics."""

    def test_reset_timer(self, timer_service):
        """Reset timer to initial duration."""
        timer = timer_service.create_timer(duration=60)
        timer.remaining_seconds = 30
        timer_service._repo.save(timer)
        
        reset_timer = timer_service.reset_timer(timer.id)
        assert reset_timer.remaining_seconds == 60
        assert reset_timer.status == TimerStatus.ACTIVE

    def test_reset_nonexistent_timer(self, timer_service):
        """Raise error when resetting non-existent timer."""
        with pytest.raises(ValueError):
            timer_service.reset_timer(str(uuid4()))

    def test_reset_expired_timer_raises_error(self, timer_service):
        """Prevent reset of expired timer."""
        timer = timer_service.create_timer(duration=60)
        timer.status = TimerStatus.EXPIRED
        timer_service._repo.save(timer)
        
        with pytest.raises(ValueError, match="Cannot reset expired timer"):
            timer_service.reset_timer(timer.id)


class TestTimerServiceUrgency:
    """Test urgency level calculation."""

    def test_urgency_low(self, timer_service):
        """Urgency is LOW when > 75% time remains."""
        timer = timer_service.create_timer(duration=100)
        timer.remaining_seconds = 80
        timer_service._repo.save(timer)
        
        urgency = timer_service.get_urgency_level(timer.id)
        assert urgency == UrgencyLevel.LOW

    def test_urgency_medium(self, timer_service):
        """Urgency is MEDIUM when 50-75% time remains."""
        timer = timer_service.create_timer(duration=100)
        timer.remaining_seconds = 60
        timer_service._repo.save(timer)
        
        urgency = timer_service.get_urgency_level(timer.id)
        assert urgency == UrgencyLevel.MEDIUM

    def test_urgency_high(self, timer_service):
        """Urgency is HIGH when 25-50% time remains."""
        timer = timer_service.create_timer(duration=100)
        timer.remaining_seconds = 35
        timer_service._repo.save(timer)
        
        urgency = timer_service.get_urgency_level(timer.id)
        assert urgency == UrgencyLevel.HIGH

    def test_urgency_critical(self, timer_service):
        """Urgency is CRITICAL when < 25% time remains."""
        timer = timer_service.create_timer(duration=100)
        timer.remaining_seconds = 20
        timer_service._repo.save(timer)
        
        urgency = timer_service.get_urgency_level(timer.id)
        assert urgency == UrgencyLevel.CRITICAL

    def test_urgency_at_zero(self, timer_service):
        """Urgency is CRITICAL at zero time."""
        timer = timer_service.create_timer(duration=100)
        timer.remaining_seconds = 0
        timer.status = TimerStatus.EXPIRED
        timer_service._repo.save(timer)
        
        urgency = timer_service.get_urgency_level(timer.id)
        assert urgency == UrgencyLevel.CRITICAL


class TestTimerServiceColourMapping:
    """Test colour intensity calculation."""

    def test_colour_low_urgency(self, timer_service):
        """Low urgency maps to green."""
        timer = timer_service.create_timer(duration=100)
        timer.remaining_seconds = 80
        timer_service._repo.save(timer)
        
        colour = timer_service.get_colour_intensity(timer.id)
        assert colour['red'] == 0
        assert colour['green'] == 255
        assert colour['blue'] == 0

    def test_colour_medium_urgency(self, timer_service):
        """Medium urgency maps to yellow."""
        timer = timer_service.create_timer(duration=100)
        timer.remaining_seconds = 60
        timer_service._repo.save(timer)
        
        colour = timer_service.get_colour_intensity(timer.id)
        assert colour['red'] == 255
        assert colour['green'] == 255
        assert colour['blue'] == 0

    def test_colour_high_urgency(self, timer_service):
        """High urgency maps to orange."""
        timer = timer_service.create_timer(duration=100)
        timer.remaining_seconds = 35
        timer_service._repo.save(timer)
        
        colour = timer_service.get_colour_intensity(timer.id)
        assert colour['red'] == 255
        assert colour['green'] < 255
        assert colour['blue'] == 0

    def test_colour_critical_urgency(self, timer_service):
        """Critical urgency maps to red."""
        timer = timer_service.create_timer(duration=100)
        timer.remaining_seconds = 10
        timer_service._repo.save(timer)
        
        colour = timer_service.get_colour_intensity(timer.id)
        assert colour['red'] == 255
        assert colour['green'] == 0
        assert colour['blue'] == 0


class TestTimerServiceState:
    """Test timer state retrieval."""

    def test_get_timer_state(self, timer_service):
        """Retrieve complete timer state."""
        timer = timer_service.create_timer(duration=100)
        timer.remaining_seconds = 50
        timer_service._repo.save(timer)
        
        state = timer_service.get_timer_state(timer.id)
        assert state['id'] == timer.id
        assert state['remaining_time'] == 50
        assert state['remaining_percentage'] == 50.0
        assert state['urgency_level'] == UrgencyLevel.MEDIUM
        assert state['colour_intensity']['red'] == 255
        assert state['colour_intensity']['green'] == 255

    def test_get_nonexistent_timer_state(self, timer_service):
        """Raise error for non-existent timer state."""
        with pytest.raises(ValueError):
            timer_service.get_timer_state(str(uuid4()))


class TestTimerServiceRetrieval:
    """Test timer retrieval operations."""

    def test_get_timer_by_id(self, timer_service):
        """Retrieve timer by ID."""
        timer = timer_service.create_timer(duration=60)
        retrieved = timer_service.get_timer(timer.id)
        assert retrieved.id == timer.id
        assert retrieved.initial_seconds == 60

    def test_get_all_timers(self, timer_service):
        """Retrieve all active timers."""
        timer1 = timer_service.create_timer(duration=60)
        timer2 = timer_service.create_timer(duration=120)
        
        all_timers = timer_service.get_all_timers()
        assert len(all_timers) == 2
        assert any(t.id == timer1.id for t in all_timers)
        assert any(t.id == timer2.id for t in all_timers)

    def test_get_nonexistent_timer(self, timer_service):
        """Raise error for non-existent timer."""
        with pytest.raises(ValueError):
            timer_service.get_timer(str(uuid4()))


class TestTimerServiceDeletion:
    """Test timer deletion."""

    def test_delete_timer(self, timer_service):
        """Delete a timer."""
        timer = timer_service.create_timer(duration=60)
        timer_service.delete_timer(timer.id)
        
        with pytest.raises(ValueError):
            timer_service.get_timer(timer.id)

    def test_delete_nonexistent_timer(self, timer_service):
        """Raise error when deleting non-existent timer."""
        with pytest.raises(ValueError):
            timer_service.delete_timer(str(uuid4()))
