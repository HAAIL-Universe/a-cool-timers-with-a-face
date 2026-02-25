from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class TimerStatus(str, Enum):
    """Timer lifecycle states."""
    running = "running"
    paused = "paused"
    expired = "expired"
    completed = "completed"


class UrgencyLevel(str, Enum):
    """Urgency classification based on remaining time percentage."""
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class FacialExpression(str, Enum):
    """8-bit facial expression feedback states."""
    calm = "calm"
    concerned = "concerned"
    stressed = "stressed"
    critical = "critical"


class ColourIntensity(BaseModel):
    """RGB colour intensity (0-255 per channel)."""
    red: int
    green: int
    blue: int


class Timer(BaseModel):
    """Complete timer state for persistent storage."""
    id: str
    initial_seconds: int = Field(..., alias="initialDuration")
    remaining_seconds: int = Field(..., alias="remainingTime")
    status: TimerStatus
    urgency_level: UrgencyLevel
    started_at: datetime = Field(..., alias="startedAt")
    last_reset_at: datetime
    created_at: datetime = Field(..., alias="createdAt")

    model_config = {"populate_by_name": True}


class TimerState(BaseModel):
    """Timer state for client display."""
    id: str
    remaining_time: int
    remaining_percentage: float
    urgency_level: UrgencyLevel
    colour_intensity: ColourIntensity
    facial_expression: FacialExpression


class TimerCreateRequest(BaseModel):
    """Request payload for creating a new timer."""
    duration: int
