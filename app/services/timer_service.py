from datetime import datetime, timedelta
from app.models.timer import (
    Timer,
    TimerState,
    TimerStatus,
    UrgencyLevel,
    FacialExpression,
    ColourIntensity,
    TimerCreateRequest,
)


class TimerRepo:
    """In-memory repository for Timer objects."""
    
    def __init__(self):
        self._timers: dict[str, Timer] = {}
    
    def create(self, timer: Timer) -> Timer:
        """Create a new timer."""
        self._timers[timer.id] = timer
        return timer
    
    def get(self, timer_id: str) -> Timer | None:
        """Fetch a timer by ID."""
        return self._timers.get(timer_id)
    
    def list_all(self) -> list[Timer]:
        """Fetch all timers."""
        return list(self._timers.values())
    
    def update(self, timer: Timer) -> Timer:
        """Update a timer."""
        self._timers[timer.id] = timer
        return timer
    
    def delete(self, timer_id: str) -> None:
        """Delete a timer."""
        if timer_id in self._timers:
            del self._timers[timer_id]


class TimerService:
    """Manages timer lifecycle, urgency calculation, and state mapping."""

    def __init__(self, repo: TimerRepo):
        self.repo = repo

    def create_timer(self, duration: int) -> Timer:
        """Create a new timer with given duration in seconds."""
        now = datetime.utcnow()
        timer = Timer(
            id=self._generate_id(),
            initial_seconds=duration,
            remaining_seconds=duration,
            status=TimerStatus.active,
            urgency_level=UrgencyLevel.low,
            started_at=now,
            last_reset_at=now,
            created_at=now,
        )
        return self.repo.create(timer)

    def get_timer(self, timer_id: str) -> Timer:
        """Fetch a timer by ID."""
        timer = self.repo.get(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")
        return timer

    def list_timers(self) -> list[Timer]:
        """Fetch all timers."""
        return self.repo.list_all()

    def reset_timer(self, timer_id: str) -> Timer:
        """Reset timer to initial duration."""
        timer = self.get_timer(timer_id)
        timer.remaining_seconds = timer.initial_seconds
        timer.last_reset_at = datetime.utcnow()
        timer.status = TimerStatus.active
        return self.repo.update(timer)

    def delete_timer(self, timer_id: str) -> None:
        """Delete a timer."""
        self.repo.delete(timer_id)

    def get_timer_state(self, timer_id: str) -> TimerState:
        """Compute full timer state including urgency, colour, and expression."""
        timer = self.get_timer(timer_id)
        remaining = self._compute_remaining_seconds(timer)
        remaining_pct = (remaining / timer.initial_seconds) * 100
        urgency = self._calculate_urgency(remaining_pct)
        colour = self._calculate_colour(urgency)
        expression = self._calculate_expression(urgency)

        return TimerState(
            id=timer.id,
            remaining_time=remaining,
            remaining_percentage=remaining_pct,
            urgency_level=urgency,
            colour_intensity=colour,
            facial_expression=expression,
        )

    def _calculate_urgency(self, remaining_pct: float) -> UrgencyLevel:
        """Map remaining percentage to urgency level."""
        if remaining_pct > 50:
            return UrgencyLevel.low
        elif remaining_pct >= 25:
            return UrgencyLevel.medium
        elif remaining_pct >= 10:
            return UrgencyLevel.high
        else:
            return UrgencyLevel.critical

    def _calculate_colour(self, urgency: UrgencyLevel) -> ColourIntensity:
        """Map urgency level to RGB colour."""
        if urgency == UrgencyLevel.low:
            return ColourIntensity(red=0, green=255, blue=0)
        elif urgency == UrgencyLevel.medium:
            return ColourIntensity(red=255, green=255, blue=0)
        elif urgency == UrgencyLevel.high:
            return ColourIntensity(red=255, green=165, blue=0)
        else:  # critical
            return ColourIntensity(red=255, green=0, blue=0)

    def _calculate_expression(self, urgency: UrgencyLevel) -> FacialExpression:
        """Map urgency level to facial expression."""
        if urgency == UrgencyLevel.low:
            return FacialExpression.calm
        elif urgency == UrgencyLevel.medium:
            return FacialExpression.concerned
        elif urgency == UrgencyLevel.high:
            return FacialExpression.stressed
        else:  # critical
            return FacialExpression.critical

    def _compute_remaining_seconds(self, timer: Timer) -> int:
        """Compute actual remaining time based on elapsed time since start."""
        elapsed = (datetime.utcnow() - timer.started_at).total_seconds()
        remaining = max(0, timer.initial_seconds - int(elapsed))
        return remaining

    def _generate_id(self) -> str:
        """Generate a unique timer ID."""
        import uuid
        return str(uuid.uuid4())
