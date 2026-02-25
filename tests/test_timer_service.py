import pytest
from datetime import datetime
from app.services.timer_service import TimerService, UrgencyState
from app.repos.timer_repo import TimerRepository


@pytest.fixture
def timer_repo():
    """In-memory timer repository for testing."""
    return TimerRepository()


@pytest.fixture
def timer_service(timer_repo):
    """Timer service instance for testing."""
    return TimerService(timer_repo)


class TestTimerService:
    """Test suite for TimerService."""

    def test_create_timer(self, timer_service):
        """Create a new timer with specified duration."""
        timer = timer_service.create_timer(duration=60)
        assert timer.id is not None
        assert timer.initial_seconds == 60
        assert timer.remaining_seconds == 60
        assert timer.status == "active"

    def test_get_timer(self, timer_service):
        """Retrieve timer by ID."""
        created = timer_service.create_timer(duration=30)
        retrieved = timer_service.get_timer(created.id)
        assert retrieved.id == created.id
        assert retrieved.initial_seconds == 30

    def test_get_all_timers(self, timer_service):
        """Retrieve all active timers."""
        timer_service.create_timer(duration=60)
        timer_service.create_timer(duration=30)
        timers = timer_service.get_all_timers()
        assert len(timers) == 2

    def test_reset_timer(self, timer_service):
        """Reset timer to initial duration."""
        timer = timer_service.create_timer(duration=60)
        timer.remaining_seconds = 30
        timer_service.get_repo().update_timer(timer)
        reset_timer = timer_service.reset_timer(timer.id)
        assert reset_timer.remaining_seconds == 60

    def test_delete_timer(self, timer_service):
        """Delete a timer by ID."""
        timer = timer_service.create_timer(duration=60)
        timer_service.delete_timer(timer.id)
        retrieved = timer_service.get_timer(timer.id)
        assert retrieved is None

    def test_calculate_urgency_level_low(self, timer_service):
        """Calculate urgency level when time remaining is high (low urgency)."""
        urgency = timer_service.calculate_urgency_level(remaining=80, initial=100)
        assert urgency == UrgencyState.LOW

    def test_calculate_urgency_level_medium(self, timer_service):
        """Calculate urgency level when time remaining is medium (medium urgency)."""
        urgency = timer_service.calculate_urgency_level(remaining=50, initial=100)
        assert urgency == UrgencyState.MEDIUM

    def test_calculate_urgency_level_high(self, timer_service):
        """Calculate urgency level when time remaining is low (high urgency)."""
        urgency = timer_service.calculate_urgency_level(remaining=25, initial=100)
        assert urgency == UrgencyState.HIGH

    def test_calculate_urgency_level_critical(self, timer_service):
        """Calculate urgency level when time remaining is very low (critical urgency)."""
        urgency = timer_service.calculate_urgency_level(remaining=5, initial=100)
        assert urgency == UrgencyState.CRITICAL

    def test_get_colour_intensity_low(self, timer_service):
        """Get colour intensity for low urgency (green)."""
        colour = timer_service.get_colour_intensity(UrgencyState.LOW)
        assert colour["green"] > colour["red"]
        assert colour["green"] > colour["blue"]

    def test_get_colour_intensity_medium(self, timer_service):
        """Get colour intensity for medium urgency (yellow)."""
        colour = timer_service.get_colour_intensity(UrgencyState.MEDIUM)
        assert colour["red"] > 0
        assert colour["green"] > 0
        assert colour["blue"] == 0

    def test_get_colour_intensity_high(self, timer_service):
        """Get colour intensity for high urgency (orange)."""
        colour = timer_service.get_colour_intensity(UrgencyState.HIGH)
        assert colour["red"] > colour["green"]
        assert colour["blue"] == 0

    def test_get_colour_intensity_critical(self, timer_service):
        """Get colour intensity for critical urgency (red)."""
        colour = timer_service.get_colour_intensity(UrgencyState.CRITICAL)
        assert colour["red"] == 255
        assert colour["green"] == 0
        assert colour["blue"] == 0

    def test_get_facial_expression_low(self, timer_service):
        """Get facial expression for low urgency (neutral)."""
        expression = timer_service.get_facial_expression(UrgencyState.LOW)
        assert expression in ["neutral", "😐"]

    def test_get_facial_expression_medium(self, timer_service):
        """Get facial expression for medium urgency (concerned)."""
        expression = timer_service.get_facial_expression(UrgencyState.MEDIUM)
        assert expression in ["concerned", "😕"]

    def test_get_facial_expression_high(self, timer_service):
        """Get facial expression for high urgency (worried)."""
        expression = timer_service.get_facial_expression(UrgencyState.HIGH)
        assert expression in ["worried", "😟"]

    def test_get_facial_expression_critical(self, timer_service):
        """Get facial expression for critical urgency (alarm)."""
        expression = timer_service.get_facial_expression(UrgencyState.CRITICAL)
        assert expression in ["alarm", "😱"]

    def test_get_timer_state(self, timer_service):
        """Get complete timer state with colour and expression feedback."""
        timer = timer_service.create_timer(duration=100)
        timer.remaining_seconds = 25
        timer_service.get_repo().update_timer(timer)
        
        state = timer_service.get_timer_state(timer.id)
        assert state.id == timer.id
        assert state.remaining_time == 25
        assert state.remaining_percentage == 25.0
        assert state.urgency_level == UrgencyState.HIGH
        assert state.colour_intensity is not None
        assert state.facial_expression is not None

    def test_timer_not_found(self, timer_service):
        """Handle retrieval of non-existent timer."""
        retrieved = timer_service.get_timer("nonexistent-id")
        assert retrieved is None

    def test_reset_timer_not_found(self, timer_service):
        """Handle reset of non-existent timer."""
        reset = timer_service.reset_timer("nonexistent-id")
        assert reset is None
