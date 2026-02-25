from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class TimerStatus(str, Enum):
    """Timer state enumeration."""
    active = "active"
    paused = "paused"
    expired = "expired"
    completed = "completed"


class UrgencyLevel(str, Enum):
    """Urgency level enumeration."""
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class TimerBase(BaseModel):
    """Base timer model."""
    initial_seconds: int = Field(..., gt=0)
    remaining_seconds: int = Field(..., ge=0)
    status: TimerStatus = TimerStatus.active
    urgency_level: UrgencyLevel = UrgencyLevel.low


class Timer(TimerBase):
    """Timer domain model."""
    id: UUID = Field(default_factory=uuid4)
    last_reset_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class TimerCreate(BaseModel):
    """Request model for creating a timer."""
    initial_seconds: int = Field(..., gt=0)


class TimerResponse(BaseModel):
    """Response model for timer."""
    id: UUID
    initial_seconds: int
    remaining_seconds: int
    status: TimerStatus
    urgency_level: UrgencyLevel
    last_reset_at: datetime
    started_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TimerStateUpdate(BaseModel):
    """Internal model for timer state updates."""
    remaining_seconds: Optional[int] = None
    status: Optional[TimerStatus] = None
    urgency_level: Optional[UrgencyLevel] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)
