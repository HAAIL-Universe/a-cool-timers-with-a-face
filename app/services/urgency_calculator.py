from enum import Enum


class UrgencyLevel(Enum):
    """Urgency level enum mapping time remaining to visual intensity."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FacialExpression(Enum):
    """8-bit facial expressions mapped to urgency levels."""
    NEUTRAL = "neutral"
    CONCERNED = "concerned"
    WORRIED = "worried"
    ALARM = "alarm"


def calculate_urgency_level(remaining_seconds: int, initial_seconds: int) -> UrgencyLevel:
    """Calculate urgency level based on remaining time as percentage of initial duration."""
    if remaining_seconds <= 0:
        return UrgencyLevel.CRITICAL
    
    percentage_remaining = (remaining_seconds / initial_seconds) * 100 if initial_seconds > 0 else 0
    
    if percentage_remaining > 66:
        return UrgencyLevel.LOW
    elif percentage_remaining > 33:
        return UrgencyLevel.MEDIUM
    elif percentage_remaining > 0:
        return UrgencyLevel.HIGH
    else:
        return UrgencyLevel.CRITICAL


def calculate_facial_expression(urgency_level: UrgencyLevel) -> FacialExpression:
    """Map urgency level to corresponding 8-bit facial expression."""
    expression_map = {
        UrgencyLevel.LOW: FacialExpression.NEUTRAL,
        UrgencyLevel.MEDIUM: FacialExpression.CONCERNED,
        UrgencyLevel.HIGH: FacialExpression.WORRIED,
        UrgencyLevel.CRITICAL: FacialExpression.ALARM,
    }
    return expression_map.get(urgency_level, FacialExpression.NEUTRAL)


def calculate_colour_intensity(remaining_seconds: int, initial_seconds: int) -> dict:
    """Calculate RGB colour values based on time remaining; intensity increases as time depletes."""
    if remaining_seconds <= 0:
        return {"r": 255, "g": 0, "b": 0}
    
    percentage_remaining = (remaining_seconds / initial_seconds) * 100 if initial_seconds > 0 else 0
    
    if percentage_remaining > 66:
        r, g, b = 0, 255, 0
    elif percentage_remaining > 33:
        r, g, b = 255, 255, 0
    elif percentage_remaining > 0:
        r, g, b = 255, 165, 0
    else:
        r, g, b = 255, 0, 0
    
    return {"r": r, "g": g, "b": b}
