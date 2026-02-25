from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class TimerStatus(str, Enum):
    """Timer operational status."""
    ACTIVE = "active"
    PAUSED = "paused"
    EXPIRED = "expired"
    COMPLETED = "completed"


class UrgencyLevel(str, Enum):
    """Urgency state for visual feedback."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Timer:
    """In-memory timer model."""

    def __init__(
        self,
        id: Optional[UUID] = None,
        status: TimerStatus = TimerStatus.ACTIVE,
        initial_seconds: int = 60,
        remaining_seconds: Optional[int] = None,
        urgency_level: UrgencyLevel = UrgencyLevel.LOW,
        last_reset_at: Optional[datetime] = None,
        started_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = id or uuid4()
        self.status = status
        self.initial_seconds = initial_seconds
        self.remaining_seconds = remaining_seconds if remaining_seconds is not None else initial_seconds
        self.urgency_level = urgency_level
        self.last_reset_at = last_reset_at or datetime.utcnow()
        self.started_at = started_at or datetime.utcnow()
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def to_dict(self) -> dict:
        """Convert timer to dictionary representation."""
        return {
            "id": str(self.id),
            "status": self.status.value,
            "initial_seconds": self.initial_seconds,
            "remaining_seconds": self.remaining_seconds,
            "urgency_level": self.urgency_level.value,
            "last_reset_at": self.last_reset_at.isoformat(),
            "started_at": self.started_at.isoformat(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self) -> str:
        return (
            f"Timer(id={self.id}, status={self.status.value}, "
            f"remaining={self.remaining_seconds}s, urgency={self.urgency_level.value})"
        )
