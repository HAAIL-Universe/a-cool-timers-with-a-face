from enum import Enum
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class TimerStatus(str, Enum):
    """Timer state enumeration."""
    ACTIVE = "active"
    PAUSED = "paused"
    EXPIRED = "expired"
    COMPLETED = "completed"


class UrgencyLevel(str, Enum):
    """Urgency state enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Timer(BaseModel):
    """Timer session model."""
    id: UUID = Field(default_factory=uuid4)
    status: TimerStatus = TimerStatus.ACTIVE
    initial_seconds: int
    remaining_seconds: int
    urgency_level: UrgencyLevel = UrgencyLevel.LOW
    last_reset_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        use_enum_values = False


class TimerSession(BaseModel):
    """Timer session history model."""
    id: UUID = Field(default_factory=uuid4)
    timer_id: UUID
    total_duration_seconds: int
    resets_count: int = 0
    completed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        use_enum_values = False


class TimerEvent(BaseModel):
    """Timer event log model."""
    id: UUID = Field(default_factory=uuid4)
    timer_id: UUID
    event_type: str
    urgency_level: Optional[UrgencyLevel] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        use_enum_values = False
