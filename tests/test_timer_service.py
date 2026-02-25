import pytest
import pytest_asyncio
from datetime import datetime, timezone
from app.services.timer_service import TimerService, TimerRepo, Timer
from app.schemas.timer import TimerConfig


@pytest_asyncio.fixture
async def timer_repo():
    """Create in-memory timer repository."""
    return TimerRepo()


@pytest_asyncio.fixture
async def timer_service(timer_repo):
    """Create TimerService instance."""
    return TimerService(timer_repo)


class TestTimerServiceConfigure:
    """Tests for timer configuration."""

    async def test_configure_creates_timer(self, timer_service):
        """Configure creates timer with correct duration."""
        config = TimerConfig(duration=60)
        state = await timer_service.configure(config)
        
        assert state.duration == 60
        assert state.countdown == 60
        assert state.is_paused is False
        assert state.is_expired is False
        assert state.urgency_level == "calm"
        assert state.colour_intensity == 0.2

    async def test_configure_sets_urgency_calm(self, timer_service):
        """Configure full duration shows calm urgency."""
        config = TimerConfig(duration=100)
        state = await timer_service.configure(config)
        
        assert state.urgency_level == "calm"
        assert state.colour_intensity == 0.2

    async def test_configure_overwrites_previous_timer(self, timer_service):
        """Configuring new timer overwrites previous one."""
        config1 = TimerConfig(duration=60)
        state1 = await timer_service.configure(config1)
        
        config2 = TimerConfig(duration=120)
        state2 = await timer_service.configure(config2)
        
        assert state2.duration == 120
        assert state2.countdown == 120

    async def test_configure_last_reset_at_is_set(self, timer_service):
        """Configure sets last_reset_at timestamp."""
        config = TimerConfig(duration=30)
        state = await timer_service.configure(config)
        
        assert state.last_reset_at is not None
        assert isinstance(state.last_reset_at, str)


class TestTimerServiceReset:
    """Tests for timer reset."""

    async def test_reset_resets_countdown(self, timer_service):
        """Reset sets countdown back to duration."""
        config = TimerConfig(duration=60)
        await timer_service.configure(config)
        
        state = await timer_service.reset()
        
        assert state.countdown == 60
        assert state.is_paused is False

    async def test_reset_increments_reset_count(self, timer_service):
        """Reset increments internal reset count."""
        config = TimerConfig(duration=60)
        await timer_service.configure(config)
        
        timer = await timer_service.repo.get_active_timer()
        assert timer.reset_count == 0
        
        await timer_service.reset()
        timer = await timer_service.repo.get_active_timer()
        assert timer.reset_count == 1

    async def test_reset_fails_when_no_timer(self, timer_service):
        """Reset raises error when no active timer."""
        with pytest.raises(ValueError, match="No active timer"):
            await timer_service.reset()

    async def test_reset_fails_when_expired(self, timer_service):
        """Reset raises error when timer has expired."""
        config = TimerConfig(duration=1)
        await timer_service.configure(config)
        
        timer = await timer_service.repo.get_active_timer()
        timer.remaining_seconds = 0
        await timer_service.repo.update_timer(timer)
        
        with pytest.raises(ValueError, match="Timer expired"):
            await timer_service.reset()

    async def test_reset_updates_started_at(self, timer_service):
        """Reset updates started_at timestamp."""
        config = TimerConfig(duration=60)
        state1 = await timer_service.configure(config)
        
        timer1 = await timer_service.repo.get_active_timer()
        initial_start = timer1.started_at
        
        state2 = await timer_service.reset()
        
        timer2 = await timer_service.repo.get_active_timer()
        assert timer2.started_at > initial_start


class TestTimerServicePause:
    """Tests for timer pause."""

    async def test_pause_sets_paused_status(self, timer_service):
        """Pause sets is_paused to True."""
        config = TimerConfig(duration=60)
        await timer_service.configure(config)
        
        state = await timer_service.pause()
        
        assert state.is_paused is True

    async def test_pause_preserves_countdown(self, timer_service):
        """Pause preserves remaining countdown."""
        config = TimerConfig(duration=60)
        await timer_service.configure(config)
        
        state = await timer_service.pause()
        
        assert state.countdown == 60

    async def test_pause_fails_when_no_timer(self, timer_service):
        """Pause raises error when no active timer."""
        with pytest.raises(ValueError, match="No active timer"):
            await timer_service.pause()

    async def test_pause_updates_paused_at(self, timer_service):
        """Pause sets paused_at timestamp."""
        config = TimerConfig(duration=60)
        await timer_service.configure(config)
        
        await timer_service.pause()
        
        timer = await timer_service.repo.get_active_timer()
        assert timer.paused_at is not None


class TestTimerServiceResume:
    """Tests for timer resume."""

    async def test_resume_unpauses_timer(self, timer_service):
        """Resume sets is_paused to False."""
        config = TimerConfig(duration=60)
        await timer_service.configure(config)
        await timer_service.pause()
        
        state = await timer_service.resume()
        
        assert state.is_paused is False

    async def test_resume_clears_paused_at(self, timer_service):
        """Resume clears paused_at timestamp."""
        config = TimerConfig(duration=60)
        await timer_service.configure(config)
        await timer_service.pause()
        
        await timer_service.resume()
        
        timer = await timer_service.repo.get_active_timer()
        assert timer.paused_at is None

    async def test_resume_fails_when_no_timer(self, timer_service):
        """Resume raises error when no active timer."""
        with pytest.raises(ValueError, match="No active timer"):
            await timer_service.resume()

    async def test_resume_preserves_countdown(self, timer_service):
        """Resume preserves remaining countdown."""
        config = TimerConfig(duration=60)
        await timer_service.configure(config)
        await timer_service.pause()
        
        state = await timer_service.resume()
        
        assert state.countdown == 60


class TestTimerServiceGetState:
    """Tests for getting timer state."""

    async def test_get_state_no_timer(self, timer_service):
        """Get state returns default expired state when no timer."""
        state = await timer_service.get_state()
        
        assert state.countdown == 0
        assert state.duration == 0
        assert state.is_expired is True
        assert state.urgency_level == "calm"
        assert state.colour_intensity == 0.0

    async def test_get_state_returns_current_state(self, timer_service):
        """Get state returns active timer state."""
        config = TimerConfig(duration=60)
        await timer_service.configure(config)
        
        state = await timer_service.get_state()
        
        assert state.duration == 60
        assert state.is_paused is False
        assert state.is_expired is False

    async def test_get_state_paused(self, timer_service):
        """Get state reflects paused status."""
        config = TimerConfig(duration=60)
        await timer_service.configure(config)
        await timer_service.pause()
        
        state = await timer_service.get_state()
        
        assert state.is_paused is True


class TestTimerServiceUrgencyCalculation:
    """Tests for urgency and colour intensity calculation."""

    async def test_urgency_calm_above_66_percent(self, timer_service):
        """Urgency is calm when remaining > 66% of duration."""
        config = TimerConfig(duration=100)
        await timer_service.configure(config)
        
        timer = await timer_service.repo.get_active_timer()
        timer.remaining_seconds = 70
        await timer_service.repo.update_timer(timer)
        
        state = await timer_service.get_state()
        
        assert state.urgency_level == "calm"
        assert state.colour_intensity == 0.2

    async def test_urgency_anxious_between_33_66_percent(self, timer_service):
        """Urgency is anxious when 33% < remaining <= 66%."""
        config = TimerConfig(duration=100)
        await timer_service.configure(config)
        
        timer = await timer_service.repo.get_active_timer()
        timer.remaining_seconds = 50
        await timer_service.repo.update_timer(timer)
        
        state = await timer_service.get_state()
        
        assert state.urgency_level == "anxious"
        assert state.colour_intensity == 0.65

    async def test_urgency_alarm_below_33_percent(self, timer_service):
        """Urgency is alarm when remaining <= 33% of duration."""
        config = TimerConfig(duration=100)
        await timer_service.configure(config)
        
        timer = await timer_service.repo.get_active_timer()
        timer.remaining_seconds = 20
        await timer_service.repo.update_timer(timer)
        
        state = await timer_service.get_state()
        
        assert state.urgency_level == "alarm"
        assert state.colour_intensity == 0.95

    async def test_urgency_zero_duration(self, timer_service):
        """Urgency defaults to calm with zero duration."""
        level, intensity = TimerService._calc_urgency(0, 0)
        
        assert level == "calm"
        assert intensity == 0.0


class TestTimerServiceGetUrgency:
    """Tests for get_urgency endpoint."""

    async def test_get_urgency_no_timer(self, timer_service):
        """Get urgency returns default state when no timer."""
        urgency = await timer_service.get_urgency()
        
        assert urgency.urgency_level == "calm"
        assert urgency.colour_intensity == 0.0
        assert urgency.remaining_percent == 0.0
        assert urgency.facial_expression == "😐"

    async def test_get_urgency_calm_expression(self, timer_service):
        """Get urgency returns calm expression for calm urgency."""
        config = TimerConfig(duration=100)
        await timer_service.configure(config)
        
        urgency = await timer_service.get_urgency()
        
        assert urgency.facial_expression == "😊"

    async def test_get_urgency_anxious_expression(self, timer_service):
        """Get urgency returns anxious expression for anxious urgency."""
        config = TimerConfig(duration=100)
        await timer_service.configure(config)
        
        timer = await timer_service.repo.get_active_timer()
        timer.remaining_seconds = 50
        await timer_service.repo.update_timer(timer)
        
        urgency = await timer_service.get_urgency()
        
        assert urgency.facial_expression == "😰"

    async def test_get_urgency_alarm_expression(self, timer_service):
        """Get urgency returns alarm expression for alarm urgency."""
        config = TimerConfig(duration=100)
        await timer_service.configure(config)
        
        timer = await timer_service.repo.get_active_timer()
        timer.remaining_seconds = 20
        await timer_service.repo.update_timer(timer)
        
        urgency = await timer_service.get_urgency()
        
        assert urgency.facial_expression == "😨"

    async def test_get_urgency_remaining_percent(self, timer_service):
        """Get urgency calculates remaining_percent correctly."""
        config = TimerConfig(duration=100)
        await timer_service.configure(config)
        
        timer = await timer_service.repo.get_active_timer()
        timer.remaining_seconds = 50
        await timer_service.repo.update_timer(timer)
        
        urgency = await timer_service.get_urgency()
        
        assert urgency.remaining_percent == 0.5


class TestTimerServiceElapsedCalculation:
    """Tests for elapsed time calculation in get_state."""

    async def test_paused_timer_preserves_remaining(self, timer_service):
        """Paused timer countdown does not decrease."""
        config = TimerConfig(duration=60)
        await timer_service.configure(config)
        
        timer = await timer_service.repo.get_active_timer()
        timer.remaining_seconds = 45
        timer.status = "paused"
        await timer_service.repo.update_timer(timer)
        
        state = await timer_service.get_state()
        
        assert state.countdown == 45

    async def test_no_start_time_returns_full_remaining(self, timer_service):
        """Timer without start_at returns full remaining_seconds."""
        config = TimerConfig(duration=60)
        await timer_service.configure(config)
        
        timer = await timer_service.repo.get_active_timer()
        timer.started_at = None
        timer.remaining_seconds = 30
        await timer_service.repo.update_timer(timer)
        
        state = await timer_service.get_state()
        
        assert state.countdown == 30
