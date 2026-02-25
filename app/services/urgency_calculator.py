"""Pure functions for urgency level calculation and RGB colour interpolation."""

URGENCY_THRESHOLDS = {
    "critical": 0.25,
    "high": 0.50,
    "medium": 0.75,
    "low": 1.00,
}

COLOUR_MAP = {
    "low": (0, 255, 0),
    "medium": (255, 255, 0),
    "high": (255, 165, 0),
    "critical": (255, 0, 0),
}


def calculate_urgency_level(elapsed: float, total: float) -> str:
    """Determine urgency level based on remaining time percentage.
    
    Args:
        elapsed: Seconds elapsed since timer started.
        total: Total duration in seconds.
    
    Returns:
        Urgency level: 'low', 'medium', 'high', or 'critical'.
    """
    if total <= 0:
        return "critical"
    
    remaining = max(0, total - elapsed)
    percentage = remaining / total
    
    if percentage <= URGENCY_THRESHOLDS["critical"]:
        return "critical"
    elif percentage <= URGENCY_THRESHOLDS["high"]:
        return "high"
    elif percentage <= URGENCY_THRESHOLDS["medium"]:
        return "medium"
    else:
        return "low"


def interpolate_rgb(urgency_level: str) -> str:
    """Get hex RGB colour for urgency level.
    
    Args:
        urgency_level: One of 'low', 'medium', 'high', 'critical'.
    
    Returns:
        Hex colour string (e.g., '#00ff00').
    """
    rgb = COLOUR_MAP.get(urgency_level, (0, 255, 0))
    r, g, b = rgb
    return f"#{r:02x}{g:02x}{b:02x}"
