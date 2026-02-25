from datetime import datetime
from enum import Enum
from typing import Optional
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


class TimerBase(BaseModel):
    """Base timer schema."""
    initial_seconds: int = Field(..., gt=0)
    remaining_seconds: int = Field(..., ge=0)
    status: TimerStatus = TimerStatus.ACTIVE
    urgency_level: UrgencyLevel = UrgencyLevel.LOW


class TimerCreate(BaseModel):
    """Timer creation schema."""
    initial_seconds: int = Field(..., gt=0)


class TimerUpdate(BaseModel):
    """Timer update schema."""
    remaining_seconds: Optional[int] = None
    status: Optional[TimerStatus] = None
    urgency_level: Optional[UrgencyLevel] = None


class Timer(TimerBase):
    """Timer model with metadata."""
    id: UUID = Field(default_factory=uuid4)
    started_at: datetime = Field(default_factory=datetime.utcnow)
    last_reset_at: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class TimerSessionBase(BaseModel):
    """Base timer session schema."""
    total_duration_seconds: int = Field(..., ge=0)
    resets_count: int = Field(default=0, ge=0)


class TimerSessionCreate(TimerSessionBase):
    """Timer session creation schema."""
    timer_id: UUID


class TimerSession(TimerSessionBase):
    """Timer session model with metadata."""
    id: UUID = Field(default_factory=uuid4)
    timer_id: UUID
    completed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class TimerEventBase(BaseModel):
    """Base timer event schema."""
    event_type: str
    urgency_level: Optional[UrgencyLevel] = None


class TimerEventCreate(TimerEventBase):
    """Timer event creation schema."""
    timer_id: UUID


class TimerEvent(TimerEventBase):
    """Timer event model with metadata."""
    id: UUID = Field(default_factory=uuid4)
    timer_id: UUID
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
