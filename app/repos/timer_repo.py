from typing import Optional
from uuid import UUID
from app.models.timer import Timer, TimerStatus, UrgencyLevel


class TimerRepository:
    """In-memory repository for timer state."""

    def __init__(self) -> None:
        self._timers: dict[UUID, Timer] = {}

    def create(self, timer: Timer) -> Timer:
        """Create a new timer in session state."""
        self._timers[timer.id] = timer
        return timer

    def get_by_id(self, timer_id: UUID) -> Optional[Timer]:
        """Retrieve timer by ID."""
        return self._timers.get(timer_id)

    def update(self, timer: Timer) -> Timer:
        """Update timer state."""
        self._timers[timer.id] = timer
        return timer

    def delete(self, timer_id: UUID) -> bool:
        """Delete timer from session state."""
        if timer_id in self._timers:
            del self._timers[timer_id]
            return True
        return False

    def list_all(self) -> list[Timer]:
        """List all timers in session."""
        return list(self._timers.values())

    def clear(self) -> None:
        """Clear all timers (for testing/reset)."""
        self._timers.clear()


_timer_repo_instance: TimerRepository = TimerRepository()


def get_timer_repo() -> TimerRepository:
    """Get singleton timer repository instance."""
    return _timer_repo_instance
