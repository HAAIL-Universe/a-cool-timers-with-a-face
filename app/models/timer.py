from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


class TimerState(str, Enum):
    """Timer operational state."""
    ACTIVE = "active"
    PAUSED = "paused"
    EXPIRED = "expired"
    COMPLETED = "completed"


class UrgencyLevel(str, Enum):
    """Urgency level based on time remaining."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Timer:
    """In-memory timer session model."""
    id: str
    status: TimerState
    initial_seconds: int
    remaining_seconds: int
    urgency_level: UrgencyLevel
    last_reset_at: datetime
    started_at: datetime
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        timer_id: str,
        initial_seconds: int,
        remaining_seconds: int,
    ) -> "Timer":
        """Create a new timer instance."""
        now = datetime.utcnow()
        return cls(
            id=timer_id,
            status=TimerState.ACTIVE,
            initial_seconds=initial_seconds,
            remaining_seconds=remaining_seconds,
            urgency_level=UrgencyLevel.LOW,
            last_reset_at=now,
            started_at=now,
            created_at=now,
            updated_at=now,
        )

    def to_dict(self) -> dict:
        """Convert timer to dictionary."""
        return {
            "id": self.id,
            "status": self.status.value,
            "initial_seconds": self.initial_seconds,
            "remaining_seconds": self.remaining_seconds,
            "urgency_level": self.urgency_level.value,
            "last_reset_at": self.last_reset_at.isoformat(),
            "started_at": self.started_at.isoformat(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
