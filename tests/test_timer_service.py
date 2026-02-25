import pytest
from datetime import datetime
from uuid import uuid4
from app.models.timer import (
    Timer, TimerState, TimerCreateRequest, TimerStatus,
    UrgencyLevel, ColourIntensity, FacialExpression
)


class TimerService:
    """Service for managing timers."""
    
    def __init__(self, timer_repo):
        self.timer_repo = timer_repo
    
    def create_timer(self, seconds):
        """Create a new timer."""
        timer_id = str(uuid4())
        timer = Timer(
            id=timer_id,
            initial_seconds=seconds,
            remaining_seconds=seconds,
            status=TimerStatus.running,
            urgency_level=UrgencyLevel.low,
            started_at=datetime.now(),
            last_reset_at=datetime.now(),
            created_at=datetime.now()
        )
        self.timer_repo.save(timer)
        return timer
    
    def get_timer(self, timer_id):
        """Get a timer by ID."""
        return self.timer_repo.get(timer_id)
    
    def list_timers(self):
        """List all timers."""
        return self.timer_repo.list()
    
    def update_timer(self, timer):
        """Update a timer."""
        self.timer_repo.save(timer)
    
    def reset_timer(self, timer_id):
        """Reset a timer to initial seconds."""
        timer = self.timer_repo.get(timer_id)
        if timer:
            timer.remaining_seconds = timer.initial_seconds
            timer.last_reset_at = datetime.now()
            self.timer_repo.save(timer)
    
    def delete_timer(self, timer_id):
        """Delete a timer."""
        self.timer_repo.delete(timer_id)
    
    def get_timer_state(self, timer_id):
        """Get the current state of a timer."""
        timer = self.timer_repo.get(timer_id)
        if not timer:
            return None
        
        remaining_percentage = (timer.remaining_seconds / timer.initial_seconds) * 100.0
        urgency = self._calculate_urgency(timer.remaining_seconds / timer.initial_seconds)
        colour = self._calculate_colour(urgency)
        expression = self._calculate_expression(urgency)
        
        return TimerState(
            id=timer.id,
            remaining_time=timer.remaining_seconds,
            remaining_percentage=remaining_percentage,
            urgency_level=urgency,
            colour_intensity=colour,
            facial_expression=expression
        )
    
    def _calculate_urgency(self, ratio):
        """Calculate urgency level based on remaining time ratio."""
        if ratio > 0.5:
            return UrgencyLevel.low
        elif ratio > 0.25:
            return UrgencyLevel.medium
        elif ratio > 0.1:
            return UrgencyLevel.high
        else:
            return UrgencyLevel.critical
    
    def _calculate_colour(self, urgency_level):
        """Calculate colour intensity based on urgency level."""
        if urgency_level == UrgencyLevel.low:
            return ColourIntensity(red=0, green=255, blue=0)
        elif urgency_level == UrgencyLevel.medium:
            return ColourIntensity(red=255, green=255, blue=0)
        elif urgency_level == UrgencyLevel.high:
            return ColourIntensity(red=255, green=165, blue=0)
        else:  # critical
            return ColourIntensity(red=255, green=0, blue=0)
    
    def _calculate_expression(self, urgency_level):
        """Calculate facial expression based on urgency level."""
        if urgency_level == UrgencyLevel.low:
            return FacialExpression.calm
        elif urgency_level == UrgencyLevel.medium:
            return FacialExpression.concerned
        elif urgency_level == UrgencyLevel.high:
            return FacialExpression.stressed
        else:  # critical
            return FacialExpression.critical


class TimerRepo:
    """In-memory timer repository."""
    
    def __init__(self):
        self.timers = {}
    
    def save(self, timer):
        """Save or update a timer."""
        self.timers[timer.id] = timer
    
    def get(self, timer_id):
        """Get a timer by ID."""
        return self.timers.get(timer_id)
    
    def list(self):
        """List all timers."""
        return list(self.timers.values())
    
    def delete(self, timer_id):
        """Delete a timer."""
        if timer_id in self.timers:
            del self.timers[timer_id]


@pytest.fixture
def timer_repo():
    """Provide an in-memory timer repository."""
    return TimerRepo()


@pytest.fixture
def timer_service(timer_repo):
    """Provide a TimerService instance with a repo."""
    return TimerService(timer_repo)


class TestTimerServiceCreate:
    """Tests for timer creation."""
    
    def test_create_timer_returns_active_status(self, timer_service):
        """POST creates timer with status 'running'."""
        result = timer_service.create_timer(30)
        assert isinstance(result, Timer)
        assert result.status == TimerStatus.running
        assert result.initial_seconds == 30
        assert result.remaining_seconds == 30
        assert result.id is not None
        assert result.urgency_level == UrgencyLevel.low


class TestTimerServiceReset:
    """Tests for timer reset functionality."""
    
    def test_reset_timer_restores_initial_seconds(self, timer_service):
        """POST /reset restores remaining_seconds to initial_seconds."""
        timer = timer_service.create_timer(60)
        timer.remaining_seconds = 15
        timer_service.reset_timer(timer.id)
        
        reset_timer = timer_service.get_timer(timer.id)
        assert reset_timer.remaining_seconds == 60
        assert reset_timer.initial_seconds == 60


class TestUrgencyThresholds:
    """Tests for urgency level calculation."""
    
    def test_urgency_low_above_50_pct(self, timer_service):
        """Urgency is 'low' when remaining > 50% of initial."""
        timer = timer_service.create_timer(100)
        timer.remaining_seconds = 51
        timer_service.update_timer(timer)
        
        urgency = timer_service._calculate_urgency(51 / 100)
        assert urgency == UrgencyLevel.low
    
    def test_urgency_medium_25_to_50_pct(self, timer_service):
        """Urgency is 'medium' when remaining is 25-50% of initial."""
        timer = timer_service.create_timer(100)
        timer.remaining_seconds = 40
        timer_service.update_timer(timer)
        
        urgency = timer_service._calculate_urgency(40 / 100)
        assert urgency == UrgencyLevel.medium
    
    def test_urgency_high_10_to_25_pct(self, timer_service):
        """Urgency is 'high' when remaining is 10-25% of initial."""
        timer = timer_service.create_timer(100)
        timer.remaining_seconds = 20
        timer_service.update_timer(timer)
        
        urgency = timer_service._calculate_urgency(20 / 100)
        assert urgency == UrgencyLevel.high
    
    def test_urgency_critical_below_10_pct(self, timer_service):
        """Urgency is 'critical' when remaining < 10% of initial."""
        timer = timer_service.create_timer(100)
        timer.remaining_seconds = 5
        timer_service.update_timer(timer)
        
        urgency = timer_service._calculate_urgency(5 / 100)
        assert urgency == UrgencyLevel.critical


class TestColourMapping:
    """Tests for colour intensity calculation."""
    
    def test_colour_green_at_low_urgency(self, timer_service):
        """Colour is green-dominant at low urgency."""
        colour = timer_service._calculate_colour(UrgencyLevel.low)
        assert isinstance(colour, ColourIntensity)
        assert colour.green > colour.red
        assert colour.green > colour.blue
    
    def test_colour_yellow_at_medium_urgency(self, timer_service):
        """Colour is yellow-dominant at medium urgency."""
        colour = timer_service._calculate_colour(UrgencyLevel.medium)
        assert isinstance(colour, ColourIntensity)
        assert colour.red > colour.blue
        assert colour.green > colour.blue
    
    def test_colour_orange_at_high_urgency(self, timer_service):
        """Colour is orange-dominant at high urgency."""
        colour = timer_service._calculate_colour(UrgencyLevel.high)
        assert isinstance(colour, ColourIntensity)
        assert colour.red > colour.blue
        assert colour.green < colour.red
    
    def test_colour_red_at_critical_urgency(self, timer_service):
        """Colour is red-dominant at critical urgency."""
        colour = timer_service._calculate_colour(UrgencyLevel.critical)
        assert isinstance(colour, ColourIntensity)
        assert colour.red > colour.green
        assert colour.red > colour.blue


class TestExpressionMapping:
    """Tests for facial expression calculation."""
    
    def test_expression_calm_at_low_urgency(self, timer_service):
        """Expression is 'calm' at low urgency."""
        expr = timer_service._calculate_expression(UrgencyLevel.low)
        assert expr == FacialExpression.calm
    
    def test_expression_concerned_at_medium_urgency(self, timer_service):
        """Expression is 'concerned' at medium urgency."""
        expr = timer_service._calculate_expression(UrgencyLevel.medium)
        assert expr == FacialExpression.concerned
    
    def test_expression_stressed_at_high_urgency(self, timer_service):
        """Expression is 'stressed' at high urgency."""
        expr = timer_service._calculate_expression(UrgencyLevel.high)
        assert expr == FacialExpression.stressed
    
    def test_expression_critical_at_critical_urgency(self, timer_service):
        """Expression is 'critical' at critical urgency."""
        expr = timer_service._calculate_expression(UrgencyLevel.critical)
        assert expr == FacialExpression.critical


class TestTimerServiceGetAndList:
    """Tests for timer retrieval."""
    
    def test_get_timer_by_id(self, timer_service):
        """GET retrieves a timer by ID."""
        created = timer_service.create_timer(45)
        retrieved = timer_service.get_timer(created.id)
        assert retrieved.id == created.id
        assert retrieved.initial_seconds == 45
    
    def test_list_timers_returns_all(self, timer_service):
        """GET /timers returns all created timers."""
        timer1 = timer_service.create_timer(30)
        timer2 = timer_service.create_timer(60)
        timers = timer_service.list_timers()
        assert len(timers) == 2
        assert timer1.id in [t.id for t in timers]
        assert timer2.id in [t.id for t in timers]


class TestTimerStateComputation:
    """Tests for TimerState computation."""
    
    def test_get_timer_state_fresh_timer(self, timer_service):
        """GET /state on fresh timer returns low urgency and green colour."""
        timer = timer_service.create_timer(100)
        state = timer_service.get_timer_state(timer.id)
        
        assert isinstance(state, TimerState)
        assert state.id == timer.id
        assert state.remaining_time == 100
        assert state.remaining_percentage == 100.0
        assert state.urgency_level == UrgencyLevel.low
        assert state.facial_expression == FacialExpression.calm
        assert state.colour_intensity.green > state.colour_intensity.red
    
    def test_get_timer_state_remaining_percentage(self, timer_service):
        """GET /state computes remaining_percentage correctly."""
        timer = timer_service.create_timer(100)
        timer.remaining_seconds = 25
        timer_service.update_timer(timer)
        
        state = timer_service.get_timer_state(timer.id)
        assert state.remaining_percentage == 25.0
        assert state.urgency_level == UrgencyLevel.high


class TestTimerDeletion:
    """Tests for timer deletion."""
    
    def test_delete_timer_removes_from_store(self, timer_service):
        """DELETE removes timer from storage."""
        timer = timer_service.create_timer(30)
        timer_id = timer.id
        timer_service.delete_timer(timer_id)
        
        retrieved = timer_service.get_timer(timer_id)
        assert retrieved is None
