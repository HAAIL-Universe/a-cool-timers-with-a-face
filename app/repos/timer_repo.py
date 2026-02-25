from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone


class Timer:
    """In-memory timer session representation."""
    
    def __init__(
        self,
        id: UUID,
        initial_seconds: int,
        remaining_seconds: int,
        status: str = "active",
        urgency_level: str = "low",
        started_at: Optional[datetime] = None,
        last_reset_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.initial_seconds = initial_seconds
        self.remaining_seconds = remaining_seconds
        self.status = status
        self.urgency_level = urgency_level
        self.started_at = started_at or datetime.now(timezone.utc)
        self.last_reset_at = last_reset_at or datetime.now(timezone.utc)
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)
    
    def to_dict(self) -> dict:
        """Convert timer to dictionary."""
        return {
            "id": str(self.id),
            "initial_seconds": self.initial_seconds,
            "remaining_seconds": self.remaining_seconds,
            "status": self.status,
            "urgency_level": self.urgency_level,
            "started_at": self.started_at.isoformat(),
            "last_reset_at": self.last_reset_at.isoformat(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class TimerRepository:
    """In-memory timer session store (no database persistence)."""
    
    def __init__(self):
        self._timers: dict[UUID, Timer] = {}
    
    def create(self, initial_seconds: int) -> Timer:
        """Create a new timer session."""
        timer_id = uuid4()
        timer = Timer(
            id=timer_id,
            initial_seconds=initial_seconds,
            remaining_seconds=initial_seconds,
            status="active",
            urgency_level="low",
        )
        self._timers[timer_id] = timer
        return timer
    
    def get_by_id(self, timer_id: UUID) -> Optional[Timer]:
        """Retrieve timer by ID."""
        return self._timers.get(timer_id)
    
    def update(self, timer_id: UUID, **kwargs) -> Optional[Timer]:
        """Update timer fields."""
        timer = self._timers.get(timer_id)
        if not timer:
            return None
        
        for key, value in kwargs.items():
            if hasattr(timer, key):
                setattr(timer, key, value)
        
        timer.updated_at = datetime.now(timezone.utc)
        return timer
    
    def list_all(self) -> list[Timer]:
        """Retrieve all active timers."""
        return list(self._timers.values())
    
    def delete(self, timer_id: UUID) -> bool:
        """Delete timer session."""
        if timer_id in self._timers:
            del self._timers[timer_id]
            return True
        return False
    
    def clear(self):
        """Clear all timers (for testing)."""
        self._timers.clear()
