from typing import Dict, Optional
from datetime import datetime
from app.models.timer import Timer, TimerStatus, UrgencyLevel


class TimerRepo:
    """In-memory store for Timer objects."""

    def __init__(self) -> None:
        self._timers: Dict[str, Timer] = {}

    def create(self, timer: Timer) -> Timer:
        """Store a new timer and return it."""
        self._timers[timer.id] = timer
        return timer

    def get(self, timer_id: str) -> Optional[Timer]:
        """Retrieve timer by ID; returns None if not found."""
        return self._timers.get(timer_id)

    def update(self, timer: Timer) -> Timer:
        """Update an existing timer and return it."""
        self._timers[timer.id] = timer
        return timer

    def delete(self, timer_id: str) -> bool:
        """Delete timer by ID; returns True if found and deleted."""
        if timer_id in self._timers:
            del self._timers[timer_id]
            return True
        return False

    def list_all(self) -> list[Timer]:
        """Return all timers as a list."""
        return list(self._timers.values())

    def clear(self) -> None:
        """Clear all timers from the store."""
        self._timers.clear()
