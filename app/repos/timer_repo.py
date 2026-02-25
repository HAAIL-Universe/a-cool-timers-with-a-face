from typing import Dict, Optional
from uuid import UUID

from app.models.timer import Timer, TimerStatus, UrgencyLevel


class TimerRepository:
    """In-memory timer repository for session-based state management."""

    def __init__(self) -> None:
        """Initialize in-memory timer store."""
        self._timers: Dict[UUID, Timer] = {}

    def create(self, timer: Timer) -> Timer:
        """Create and store a new timer."""
        self._timers[timer.id] = timer
        return timer

    def get_by_id(self, timer_id: UUID) -> Optional[Timer]:
        """Retrieve timer by ID."""
        return self._timers.get(timer_id)

    def update(self, timer_id: UUID, timer: Timer) -> Optional[Timer]:
        """Update an existing timer."""
        if timer_id in self._timers:
            self._timers[timer_id] = timer
            return timer
        return None

    def delete(self, timer_id: UUID) -> bool:
        """Delete a timer by ID."""
        if timer_id in self._timers:
            del self._timers[timer_id]
            return True
        return False

    def list_all(self) -> list[Timer]:
        """Retrieve all timers."""
        return list(self._timers.values())

    def clear(self) -> None:
        """Clear all timers from session store."""
        self._timers.clear()
