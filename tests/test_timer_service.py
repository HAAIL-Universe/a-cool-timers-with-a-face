import pytest
from datetime import datetime, timedelta
from app.services.timer_service import TimerService
from app.schemas import TimerState


@pytest.fixture
def timer_service():
    """Initialize a fresh TimerService for each test."""
    return TimerService()


class TestTimerConfiguration:
    """Test timer configuration and initialization."""

    def test_configure_timer_sets_duration(self, timer_service):
        """Configure timer with valid duration."""
        result = timer_service.configure(duration_seconds=60)
        assert result.duration == 60
        assert result.countdown == 60
        assert result.is_paused is False
        assert result.is_expired is False

    def test_configure_timer_resets_state(self, timer_service):
        """Configuring timer resets any previous state."""
        timer_service.configure(duration_seconds=60)
        timer_service.countdown = 30
        timer_service.is_paused = True
        
        result = timer_service.configure(duration_seconds=45)
        assert result.countdown == 45
        assert result.duration == 45
        assert result.is_paused is False


class TestTimerCountdown:
    """Test countdown mechanics."""

    def test_tick_decrements_countdown(self, timer_service):
        """Each tick decrements countdown by one second."""
        timer_service.configure(duration_seconds=10)
        initial = timer_service.countdown
        
        timer_service.tick()
        assert timer_service.countdown == initial - 1

    def test_tick_when_paused_does_nothing(self, timer_service):
        """Tick does not decrement when paused."""
        timer_service.configure(duration_seconds=10)
        timer_service.pause()
        initial = timer_service.countdown
        
        timer_service.tick()
        assert timer_service.countdown == initial

    def test_tick_stops_at_zero(self, timer_service):
        """Countdown does not go below zero."""
        timer_service.configure(duration_seconds=1)
        timer_service.tick()
        timer_service.tick()
        
        assert timer_service.countdown == 0

    def test_countdown_sets_is_expired_flag(self, timer_service):
        """Timer marks is_expired when countdown reaches zero."""
        timer_service.configure(duration_seconds=1)
        timer_service.tick()
        
        assert timer_service.is_expired is True


class TestTimerReset:
    """Test reset mechanics."""

    def test_reset_restores_full_duration(self, timer_service):
        """Reset restores countdown to full duration."""
        timer_service.configure(duration_seconds=60)
        timer_service.countdown = 30
        
        result = timer_service.reset()
        assert result.countdown == 60
        assert result.is_paused is False

    def test_reset_when_expired_returns_error(self, timer_service):
        """Reset fails with 400 when timer status is expired."""
        timer_service.configure(duration_seconds=1)
        timer_service.tick()
        
        with pytest.raises(ValueError) as exc_info:
            timer_service.reset()
        assert "expired" in str(exc_info.value).lower()

    def test_reset_clears_expired_flag(self, timer_service):
        """Reset clears is_expired flag after reconfiguration."""
        timer_service.configure(duration_seconds=1)
        timer_service.tick()
        assert timer_service.is_expired is True
        
        timer_service.configure(duration_seconds=60)
        assert timer_service.is_expired is False
        assert timer_service.countdown == 60

    def test_reset_updates_timestamp(self, timer_service):
        """Reset updates last_reset_at timestamp."""
        timer_service.configure(duration_seconds=60)
        first_reset = timer_service.last_reset_at
        
        timer_service.countdown = 30
        timer_service.reset()
        
        assert timer_service.last_reset_at > first_reset


class TestTimerPauseResume:
    """Test pause and resume mechanics."""

    def test_pause_sets_flag(self, timer_service):
        """Pause sets is_paused flag."""
        timer_service.configure(duration_seconds=60)
        
        result = timer_service.pause()
        assert result.is_paused is True

    def test_resume_clears_flag(self, timer_service):
        """Resume clears is_paused flag."""
        timer_service.configure(duration_seconds=60)
        timer_service.pause()
        
        result = timer_service.resume()
        assert result.is_paused is False

    def test_resume_preserves_countdown(self, timer_service):
        """Resume preserves countdown value from pause."""
        timer_service.configure(duration_seconds=60)
        timer_service.countdown = 45
        timer_service.pause()
        
        result = timer_service.resume()
        assert result.countdown == 45

    def test_resume_when_expired_returns_error(self, timer_service):
        """Resume fails when timer is expired."""
        timer_service.configure(duration_seconds=1)
        timer_service.tick()
        
        with pytest.raises(ValueError) as exc_info:
            timer_service.resume()
        assert "expired" in str(exc_info.value).lower()


class TestUrgencyCalculation:
    """Test urgency level and colour intensity calculation."""

    def test_urgency_calm_when_high_remaining(self, timer_service):
        """Urgency is calm when >66% time remains."""
        timer_service.configure(duration_seconds=100)
        timer_service.countdown = 75
        
        result = timer_service.get_state()
        assert result.urgency_level == "calm"
        assert result.colour_intensity < 0.4

    def test_urgency_anxious_when_medium_remaining(self, timer_service):
        """Urgency is anxious when 33-66% time remains."""
        timer_service.configure(duration_seconds=100)
        timer_service.countdown = 50
        
        result = timer_service.get_state()
        assert result.urgency_level == "anxious"
        assert 0.4 <= result.colour_intensity <= 0.7

    def test_urgency_alarm_when_low_remaining(self, timer_service):
        """Urgency is alarm when <33% time remains."""
        timer_service.configure(duration_seconds=100)
        timer_service.countdown = 20
        
        result = timer_service.get_state()
        assert result.urgency_level == "alarm"
        assert result.colour_intensity > 0.7

    def test_urgency_alarm_at_zero(self, timer_service):
        """Urgency is alarm when countdown reaches zero."""
        timer_service.configure(duration_seconds=100)
        timer_service.countdown = 0
        timer_service.is_expired = True
        
        result = timer_service.get_state()
        assert result.urgency_level == "alarm"
        assert result.colour_intensity >= 0.9

    def test_colour_intensity_scales_linearly(self, timer_service):
        """Colour intensity scales proportionally with time depletion."""
        timer_service.configure(duration_seconds=100)
        
        intensities = []
        for remaining in [100, 75, 50, 25, 0]:
            timer_service.countdown = remaining
            state = timer_service.get_state()
            intensities.append(state.colour_intensity)
        
        for i in range(len(intensities) - 1):
            assert intensities[i] <= intensities[i + 1]


class TestTimerStateSnapshot:
    """Test complete state serialization."""

    def test_get_state_returns_complete_snapshot(self, timer_service):
        """get_state returns all required fields."""
        timer_service.configure(duration_seconds=60)
        timer_service.countdown = 45
        
        state = timer_service.get_state()
        assert state.countdown == 45
        assert state.duration == 60
        assert state.is_paused is False
        assert state.is_expired is False
        assert state.urgency_level in ["calm", "anxious", "alarm"]
        assert 0.0 <= state.colour_intensity <= 1.0
        assert state.last_reset_at is not None

    def test_state_after_pause(self, timer_service):
        """State reflects paused status."""
        timer_service.configure(duration_seconds=60)
        timer_service.countdown = 30
        timer_service.pause()
        
        state = timer_service.get_state()
        assert state.is_paused is True
        assert state.countdown == 30

    def test_state_after_expiry(self, timer_service):
        """State reflects expired status."""
        timer_service.configure(duration_seconds=1)
        timer_service.tick()
        
        state = timer_service.get_state()
        assert state.is_expired is True
        assert state.countdown == 0


class TestExpiryBoundaries:
    """Test edge cases around timer expiry."""

    def test_multiple_ticks_past_zero(self, timer_service):
        """Multiple ticks past zero keep countdown at zero."""
        timer_service.configure(duration_seconds=2)
        for _ in range(5):
            timer_service.tick()
        
        assert timer_service.countdown == 0
        assert timer_service.is_expired is True

    def test_configure_after_expiry_clears_state(self, timer_service):
        """Configuring after expiry resets expired flag."""
        timer_service.configure(duration_seconds=1)
        timer_service.tick()
        assert timer_service.is_expired is True
        
        timer_service.configure(duration_seconds=60)
        assert timer_service.is_expired is False
        assert timer_service.countdown == 60

    def test_expired_timer_prevents_resume(self, timer_service):
        """Cannot resume an expired timer."""
        timer_service.configure(duration_seconds=1)
        timer_service.tick()
        timer_service.pause()
        
        with pytest.raises(ValueError) as exc_info:
            timer_service.resume()
        assert "expired" in str(exc_info.value).lower()
