from typing import Optional
from uuid import UUID
from app.models.timer import Timer, TimerStatus, UrgencyLevel


class TimerRepository:
    """In-memory session store for timer state."""

    def __init__(self) -> None:
        self._timers: dict[UUID, Timer] = {}

    def create(self, timer: Timer) -> Timer:
        """Store a new timer in session."""
        self._timers[timer.id] = timer
        return timer

    def get_by_id(self, timer_id: UUID) -> Optional[Timer]:
        """Retrieve timer by ID from session store."""
        return self._timers.get(timer_id)

    def update(self, timer: Timer) -> Timer:
        """Update an existing timer in session store."""
        self._timers[timer.id] = timer
        return timer

    def list_all(self) -> list[Timer]:
        """Return all timers in session store."""
        return list(self._timers.values())

    def delete(self, timer_id: UUID) -> bool:
        """Remove timer from session store."""
        if timer_id in self._timers:
            del self._timers[timer_id]
            return True
        return False

    def clear(self) -> None:
        """Clear all timers from session store (for testing/reset)."""
        self._timers.clear()


_timer_repo: Optional[TimerRepository] = None


def get_timer_repo() -> TimerRepository:
    """Dependency injection getter for timer repository."""
    global _timer_repo
    if _timer_repo is None:
        _timer_repo = TimerRepository()
    return _timer_repo
