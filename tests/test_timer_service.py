from datetime import datetime, timedelta
import pytest
from app.services.timer_service import TimerService, TimerRepo
from app.models.timer import (
    Timer,
    TimerStatus,
    UrgencyLevel,
    FacialExpression,
    ColourIntensity,
    TimerCreateRequest,
)


@pytest.fixture
def timer_repo():
    return TimerRepo()


@pytest.fixture
def timer_service(timer_repo):
    return TimerService(timer_repo)


class TestTimerService:
    def test_create_timer_returns_active_status(self, timer_service):
        """POST /timers creates a timer with status=active."""
        timer = timer_service.create_timer(30)
        assert timer.status == TimerStatus.active
        assert timer.initial_seconds == 30
        assert timer.id is not None

    def test_urgency_low_above_50_pct(self, timer_service):
        """Urgency is 'low' when remaining > 50% of duration."""
        timer = timer_service.create_timer(100)
        timer.remaining_seconds = 60
        state = timer_service.get_timer_state(timer.id)
        assert state.urgency_level == UrgencyLevel.low

    def test_urgency_medium_25_to_50_pct(self, timer_service):
        """Urgency is 'medium' when remaining is 25-50% of duration."""
        timer = timer_service.create_timer(100)
        timer.remaining_seconds = 40
        state = timer_service.get_timer_state(timer.id)
        assert state.urgency_level == UrgencyLevel.medium

    def test_urgency_high_10_to_25_pct(self, timer_service):
        """Urgency is 'high' when remaining is 10-25% of duration."""
        timer = timer_service.create_timer(100)
        timer.remaining_seconds = 20
        state = timer_service.get_timer_state(timer.id)
        assert state.urgency_level == UrgencyLevel.high

    def test_urgency_critical_below_10_pct(self, timer_service):
        """Urgency is 'critical' when remaining < 10% of duration."""
        timer = timer_service.create_timer(100)
        timer.remaining_seconds = 5
        state = timer_service.get_timer_state(timer.id)
        assert state.urgency_level == UrgencyLevel.critical

    def test_reset_timer_restores_initial_seconds(self, timer_service):
        """POST /timers/{id}/reset restores remaining_seconds to initial_seconds."""
        timer = timer_service.create_timer(30)
        original_remaining = timer.remaining_seconds
        timer.remaining_seconds = 10
        timer_service.repo.update(timer)
        
        reset_timer = timer_service.reset_timer(timer.id)
        assert reset_timer.remaining_seconds == original_remaining

    def test_colour_green_at_low_urgency(self, timer_service):
        """Colour is green-dominant at low urgency."""
        timer = timer_service.create_timer(100)
        timer.remaining_seconds = 60
        state = timer_service.get_timer_state(timer.id)
        assert state.colour_intensity.green > state.colour_intensity.red
        assert state.colour_intensity.green > state.colour_intensity.blue

    def test_colour_red_at_critical_urgency(self, timer_service):
        """Colour is red-dominant at critical urgency."""
        timer = timer_service.create_timer(100)
        timer.remaining_seconds = 5
        state = timer_service.get_timer_state(timer.id)
        assert state.colour_intensity.red > state.colour_intensity.green
        assert state.colour_intensity.red > state.colour_intensity.blue

    def test_expression_calm_at_low_urgency(self, timer_service):
        """Facial expression is 'calm' at low urgency."""
        timer = timer_service.create_timer(100)
        timer.remaining_seconds = 60
        state = timer_service.get_timer_state(timer.id)
        assert state.facial_expression == FacialExpression.calm

    def test_expression_critical_at_critical_urgency(self, timer_service):
        """Facial expression is 'critical' at critical urgency."""
        timer = timer_service.create_timer(100)
        timer.remaining_seconds = 5
        state = timer_service.get_timer_state(timer.id)
        assert state.facial_expression == FacialExpression.critical

    def test_get_timer_by_id(self, timer_service):
        """GET /timers/{id} retrieves timer by ID."""
        timer = timer_service.create_timer(30)
        retrieved = timer_service.get_timer(timer.id)
        assert retrieved.id == timer.id
        assert retrieved.initial_seconds == 30

    def test_list_timers(self, timer_service):
        """GET /timers returns list of all timers."""
        timer1 = timer_service.create_timer(30)
        timer2 = timer_service.create_timer(60)
        timers = timer_service.list_timers()
        assert len(timers) >= 2
        ids = {t.id for t in timers}
        assert timer1.id in ids
        assert timer2.id in ids

    def test_delete_timer(self, timer_service):
        """DELETE /timers/{id} removes timer."""
        timer = timer_service.create_timer(30)
        timer_service.delete_timer(timer.id)
        retrieved = timer_service.get_timer(timer.id)
        assert retrieved is None
