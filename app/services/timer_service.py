from uuid import UUID
from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel


class UrgencyState(BaseModel):
    """Urgency level with colour and expression mapping."""
    urgency_level: str
    colour_intensity: dict[str, int]
    facial_expression: str
    remaining_percentage: float


class TimerService:
    """Countdown timer logic: urgency calculation, colour/expression mapping."""

    URGENCY_THRESHOLDS = {
        "critical": 0.10,
        "high": 0.25,
        "medium": 0.50,
        "low": 1.00,
    }

    COLOUR_MAP = {
        "low": {"red": 0, "green": 255, "blue": 0},
        "medium": {"red": 255, "green": 255, "blue": 0},
        "high": {"red": 255, "green": 165, "blue": 0},
        "critical": {"red": 255, "green": 0, "blue": 0},
    }

    EXPRESSION_MAP = {
        "low": "neutral",
        "medium": "concerned",
        "high": "worried",
        "critical": "alarm",
    }

    @staticmethod
    def calculate_urgency(remaining_seconds: int, initial_seconds: int) -> UrgencyState:
        """Calculate urgency level, colour, and expression from remaining time."""
        if remaining_seconds <= 0:
            remaining_percentage = 0.0
        else:
            remaining_percentage = remaining_seconds / initial_seconds
        remaining_percentage = max(0.0, min(100.0, remaining_percentage * 100))

        urgency_level = TimerService._get_urgency_level(remaining_percentage / 100)
        colour = TimerService._blend_colour(remaining_percentage / 100, urgency_level)
        expression = TimerService.EXPRESSION_MAP[urgency_level]

        return UrgencyState(
            urgency_level=urgency_level,
            colour_intensity=colour,
            facial_expression=expression,
            remaining_percentage=remaining_percentage,
        )

    @staticmethod
    def _get_urgency_level(fraction: float) -> str:
        """Map fraction [0,1] to urgency level based on thresholds."""
        if fraction > TimerService.URGENCY_THRESHOLDS["medium"]:
            return "low"
        elif fraction > TimerService.URGENCY_THRESHOLDS["high"]:
            return "medium"
        elif fraction > TimerService.URGENCY_THRESHOLDS["critical"]:
            return "high"
        else:
            return "critical"

    @staticmethod
    def _blend_colour(fraction: float, urgency_level: str) -> dict[str, int]:
        """Blend base colour with intensity based on remaining fraction."""
        base_colour = TimerService.COLOUR_MAP[urgency_level]

        if urgency_level == "low":
            target = {"red": 0, "green": 255, "blue": 0}
        elif urgency_level == "medium":
            target = {"red": 255, "green": 255, "blue": 0}
        elif urgency_level == "high":
            target = {"red": 255, "green": 165, "blue": 0}
        else:
            target = {"red": 255, "green": 0, "blue": 0}

        if urgency_level == "critical":
            intensity = 1.0 - fraction
        elif urgency_level == "high":
            intensity = (1.0 - fraction) / 2
        elif urgency_level == "medium":
            intensity = (1.0 - fraction) / 4
        else:
            intensity = 0.0

        blended = {}
        for channel in ["red", "green", "blue"]:
            base = base_colour[channel]
            shift = int((target[channel] - base) * intensity)
            blended[channel] = max(0, min(255, base + shift))

        return blended

    @staticmethod
    def validate_reset(remaining_seconds: int) -> bool:
        """Validate timer can be reset (must have time remaining)."""
        return remaining_seconds > 0

    @staticmethod
    def calculate_remaining(
        initial_seconds: int,
        started_at: datetime,
        last_reset_at: Optional[datetime] = None,
    ) -> int:
        """Calculate remaining seconds from start/reset time."""
        reference_time = last_reset_at or started_at
        elapsed = (datetime.now(timezone.utc) - reference_time).total_seconds()
        remaining = max(0, initial_seconds - int(elapsed))
        return remaining
