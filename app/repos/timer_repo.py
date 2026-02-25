from datetime import datetime
from typing import Optional
from uuid import uuid4

from app.models.timer import Timer, TimerStatus, UrgencyLevel


class TimerRepository:
    """In-memory store for Timer objects."""

    def __init__(self) -> None:
        self._timers: dict[str, Timer] = {}

    def create(self, initial_seconds: int) -> Timer:
        """Create and store a new timer."""
        now = datetime.utcnow()
        timer = Timer(
            id=str(uuid4()),
            initial_seconds=initial_seconds,
            remaining_seconds=initial_seconds,
            status=TimerStatus.active,
            urgency_level=UrgencyLevel.low,
            started_at=now,
            last_reset_at=now,
            created_at=now,
        )
        self._timers[timer.id] = timer
        return timer

    def get(self, timer_id: str) -> Optional[Timer]:
        """Retrieve a timer by ID."""
        return self._timers.get(timer_id)

    def update(self, timer: Timer) -> Timer:
        """Update an existing timer."""
        self._timers[timer.id] = timer
        return timer

    def delete(self, timer_id: str) -> bool:
        """Delete a timer by ID; return True if deleted, False if not found."""
        if timer_id in self._timers:
            del self._timers[timer_id]
            return True
        return False

    def list_all(self) -> list[Timer]:
        """Return all stored timers."""
        return list(self._timers.values())

    def clear(self) -> None:
        """Clear all timers (for testing)."""
        self._timers.clear()
