from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


class ColourIntensity(BaseModel):
    """RGB colour intensity for timer state feedback."""
    red: int = Field(..., ge=0, le=255)
    green: int = Field(..., ge=0, le=255)
    blue: int = Field(..., ge=0, le=255)


class TimerCreateRequest(BaseModel):
    """Request schema for creating a new timer."""
    duration: int = Field(..., gt=0, description="Timer duration in seconds")


class Timer(BaseModel):
    """Timer resource schema."""
    id: UUID
    initialDuration: int = Field(..., alias="initial_duration")
    remainingTime: int = Field(..., alias="remaining_time")
    createdAt: datetime = Field(..., alias="created_at")
    startedAt: datetime = Field(..., alias="started_at")
    status: str

    class Config:
        from_attributes = True
        populate_by_name = True


class TimerState(BaseModel):
    """Timer state with urgency feedback (colour and facial expression)."""
    id: UUID
    remainingTime: int = Field(..., alias="remaining_time")
    remainingPercentage: float = Field(..., alias="remaining_percentage", ge=0, le=100)
    urgencyLevel: str = Field(..., alias="urgency_level")
    colourIntensity: ColourIntensity = Field(..., alias="colour_intensity")
    facialExpression: str = Field(..., alias="facial_expression")

    class Config:
        from_attributes = True
        populate_by_name = True
