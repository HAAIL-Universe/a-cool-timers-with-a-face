from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class TimerStatus(str, Enum):
    """Timer operational state."""
    stopped = "stopped"
    running = "running"
    paused = "paused"
    expired = "expired"


class UrgencyLevel(int, Enum):
    """Visual feedback urgency escalation (0-3)."""
    calm = 0
    alert = 1
    caution = 2
    alarm = 3


class TimerEventType(str, Enum):
    """Timer state transition events."""
    reset = "reset"
    started = "started"
    paused = "paused"
    expired = "expired"


class TimerEventCreate(BaseModel):
    """Create a timer event log entry."""
    timer_id: str
    event_type: TimerEventType
    urgency_level: UrgencyLevel = UrgencyLevel.calm


class TimerEventResponse(BaseModel):
    """Timer event retrieved from storage."""
    id: str
    timer_id: str
    event_type: TimerEventType
    urgency_level: UrgencyLevel
    recorded_at: datetime

    class Config:
        from_attributes = True


class TimerCreate(BaseModel):
    """Configure a new timer."""
    name: str = Field(default="Workout", min_length=1, max_length=255)
    duration_seconds: int = Field(ge=1, le=3600)


class TimerUpdate(BaseModel):
    """Update timer state (pause/reset)."""
    status: Optional[TimerStatus] = None
    remaining_seconds: Optional[int] = None


class TimerResponse(BaseModel):
    """Timer state for API response."""
    id: str
    name: str
    duration_seconds: int
    remaining_seconds: int
    status: TimerStatus
    reset_count: int
    started_at: Optional[datetime] = None
    paused_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UrgencyResponse(BaseModel):
    """Current urgency level with intensity metadata."""
    urgency_level: UrgencyLevel
    remaining_seconds: int
    duration_seconds: int
    intensity_percent: float = Field(ge=0, le=100)
