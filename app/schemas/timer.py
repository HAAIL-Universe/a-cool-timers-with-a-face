from pydantic import BaseModel, Field
from typing import Optional


class TimerConfig(BaseModel):
    """Timer configuration request."""
    duration: int = Field(..., description="Countdown duration in seconds (positive integer)", example=60)


class TimerState(BaseModel):
    """Complete timer state snapshot."""
    countdown: int = Field(..., description="Remaining seconds on countdown (0 if expired)", example=45)
    duration: int = Field(..., description="Configured timer duration in seconds", example=60)
    is_paused: bool = Field(..., description="Whether countdown is paused", example=False)
    is_expired: bool = Field(..., description="Whether countdown has reached zero", example=False)
    urgency_level: str = Field(..., description="Current urgency classification", example="anxious")
    colour_intensity: float = Field(..., description="Colour intensity 0.0 (cool/dim) to 1.0 (hot/bright red)", example=0.65)
    last_reset_at: Optional[str] = Field(None, description="ISO timestamp of last reset or configuration", example="2025-01-15T10:30:00Z")


class UrgencyState(BaseModel):
    """Real-time urgency and visual feedback state."""
    urgency_level: str = Field(..., description="Current urgency classification based on remaining time ratio", example="alarm")
    colour_intensity: float = Field(..., description="Colour intensity 0.0 (cool) to 1.0 (hot red); drives visual feedback", example=0.95)
    remaining_percent: float = Field(..., description="Percentage of countdown remaining (0.0 to 1.0)", example=0.15)
    facial_expression: str = Field(..., description="8-bit facial expression reflecting urgency", example="😨")
