from datetime import datetime
from uuid import UUID

from app.models.timer import Timer, TimerCreate, TimerResponse, TimerStatus, UrgencyLevel
from app.repos.timer_repo import TimerRepository


class TimerService:
    """Service layer for timer operations and urgency state management."""

    def __init__(self, repo: TimerRepository) -> None:
        """Initialize TimerService with repository."""
        self.repo = repo

    def create_timer(self, timer_create: TimerCreate) -> Timer:
        """Create a new timer with initial countdown."""
        timer = Timer(
            initial_seconds=timer_create.initial_seconds,
            remaining_seconds=timer_create.initial_seconds,
            status=TimerStatus.active,
            urgency_level=self._calculate_urgency(timer_create.initial_seconds, timer_create.initial_seconds),
        )
        return self.repo.create(timer)

    def get_timer(self, timer_id: UUID) -> Timer | None:
        """Retrieve timer by ID."""
        return self.repo.get_by_id(timer_id)

    def start_timer(self, timer_id: UUID) -> Timer | None:
        """Start a paused timer."""
        timer = self.repo.get_by_id(timer_id)
        if not timer:
            return None
        timer.status = TimerStatus.active
        timer.updated_at = datetime.utcnow()
        return self.repo.update(timer_id, timer)

    def stop_timer(self, timer_id: UUID) -> Timer | None:
        """Pause an active timer."""
        timer = self.repo.get_by_id(timer_id)
        if not timer:
            return None
        timer.status = TimerStatus.paused
        timer.updated_at = datetime.utcnow()
        return self.repo.update(timer_id, timer)

    def reset_timer(self, timer_id: UUID) -> Timer | None:
        """Reset timer to initial duration."""
        timer = self.repo.get_by_id(timer_id)
        if not timer:
            return None
        timer.remaining_seconds = timer.initial_seconds
        timer.status = TimerStatus.active
        timer.urgency_level = self._calculate_urgency(timer.initial_seconds, timer.initial_seconds)
        timer.last_reset_at = datetime.utcnow()
        timer.updated_at = datetime.utcnow()
        return self.repo.update(timer_id, timer)

    def tick_timer(self, timer_id: UUID) -> Timer | None:
        """Decrement timer by 1 second and update urgency."""
        timer = self.repo.get_by_id(timer_id)
        if not timer or timer.status != TimerStatus.active:
            return None
        
        if timer.remaining_seconds > 0:
            timer.remaining_seconds -= 1
        
        if timer.remaining_seconds <= 0:
            timer.status = TimerStatus.expired
            timer.remaining_seconds = 0
        
        timer.urgency_level = self._calculate_urgency(timer.initial_seconds, timer.remaining_seconds)
        timer.updated_at = datetime.utcnow()
        return self.repo.update(timer_id, timer)

    def _calculate_urgency(self, initial_seconds: int, remaining_seconds: int) -> UrgencyLevel:
        """Calculate urgency level based on remaining time percentage."""
        if remaining_seconds <= 0:
            return UrgencyLevel.critical
        
        if initial_seconds == 0:
            return UrgencyLevel.low
        
        percentage = remaining_seconds / initial_seconds
        
        if percentage > 0.5:
            return UrgencyLevel.low
        elif percentage > 0.25:
            return UrgencyLevel.medium
        elif percentage > 0.1:
            return UrgencyLevel.high
        else:
            return UrgencyLevel.critical

    def list_all_timers(self) -> list[Timer]:
        """Retrieve all active timers."""
        return self.repo.list_all()

    def delete_timer(self, timer_id: UUID) -> bool:
        """Delete a timer session."""
        return self.repo.delete(timer_id)
