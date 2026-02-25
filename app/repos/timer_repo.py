from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Optional, Dict, List

class Timer:
    """In-memory timer record."""
    def __init__(
        self,
        id: UUID,
        initial_seconds: int,
        remaining_seconds: int,
        status: str,
        created_at: datetime,
        started_at: datetime,
        last_reset_at: datetime,
    ):
        self.id = id
        self.initial_seconds = initial_seconds
        self.remaining_seconds = remaining_seconds
        self.status = status
        self.created_at = created_at
        self.started_at = started_at
        self.last_reset_at = last_reset_at
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self) -> Dict:
        """Serialize timer to dict."""
        return {
            "id": str(self.id),
            "initialDuration": self.initial_seconds,
            "remainingTime": self.remaining_seconds,
            "status": self.status,
            "createdAt": self.created_at.isoformat(),
            "startedAt": self.started_at.isoformat(),
        }


class TimerRepo:
    """In-memory repository for timer records."""

    _timers: Dict[UUID, Timer] = {}

    @classmethod
    def create(cls, duration_seconds: int) -> Timer:
        """Create a new timer record."""
        now = datetime.now(timezone.utc)
        timer_id = uuid4()
        timer = Timer(
            id=timer_id,
            initial_seconds=duration_seconds,
            remaining_seconds=duration_seconds,
            status="active",
            created_at=now,
            started_at=now,
            last_reset_at=now,
        )
        cls._timers[timer_id] = timer
        return timer

    @classmethod
    def get_by_id(cls, timer_id: UUID) -> Optional[Timer]:
        """Fetch timer by ID."""
        return cls._timers.get(timer_id)

    @classmethod
    def list_all(cls) -> List[Timer]:
        """Get all timers."""
        return list(cls._timers.values())

    @classmethod
    def update(cls, timer_id: UUID, **kwargs) -> Optional[Timer]:
        """Update timer fields."""
        timer = cls._timers.get(timer_id)
        if not timer:
            return None
        for key, value in kwargs.items():
            if hasattr(timer, key):
                setattr(timer, key, value)
        timer.updated_at = datetime.now(timezone.utc)
        return timer

    @classmethod
    def delete(cls, timer_id: UUID) -> bool:
        """Delete timer by ID."""
        if timer_id in cls._timers:
            del cls._timers[timer_id]
            return True
        return False

    @classmethod
    def reset_time(cls, timer_id: UUID) -> Optional[Timer]:
        """Reset timer to initial duration."""
        timer = cls._timers.get(timer_id)
        if not timer:
            return None
        timer.remaining_seconds = timer.initial_seconds
        timer.last_reset_at = datetime.now(timezone.utc)
        timer.updated_at = datetime.now(timezone.utc)
        return timer

    @classmethod
    def clear_all(cls) -> None:
        """Clear all timers (for testing)."""
        cls._timers.clear()
