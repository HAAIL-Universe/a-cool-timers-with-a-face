from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class TimerStatus(str, Enum):
    active = "active"
    paused = "paused"
    expired = "expired"
    completed = "completed"


class UrgencyLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class FacialExpression(str, Enum):
    calm = "calm"
    concerned = "concerned"
    stressed = "stressed"
    critical = "critical"


class ColourIntensity(BaseModel):
    red: int = Field(..., ge=0, le=255)
    green: int = Field(..., ge=0, le=255)
    blue: int = Field(..., ge=0, le=255)


class Timer(BaseModel):
    id: str
    initial_seconds: int
    remaining_seconds: int
    status: TimerStatus
    urgency_level: UrgencyLevel
    started_at: datetime
    last_reset_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class TimerState(BaseModel):
    id: str
    remaining_time: int
    remaining_percentage: float
    urgency_level: UrgencyLevel
    colour_intensity: ColourIntensity
    facial_expression: FacialExpression

    class Config:
        from_attributes = True


class TimerCreateRequest(BaseModel):
    duration: int = Field(..., gt=0)
