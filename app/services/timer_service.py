from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4
from typing import Optional


class UrgencyState(str, Enum):
    """Urgency state enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TimerState:
    """In-memory timer state container."""

    def __init__(
        self,
        timer_id: UUID,
        initial_seconds: int,
        remaining_seconds: int,
        status: str = "active",
        urgency_level: UrgencyState = UrgencyState.LOW,
        started_at: Optional[datetime] = None,
        last_reset_at: Optional[datetime] = None,
    ):
        self.timer_id = timer_id
        self.initial_seconds = initial_seconds
        self.remaining_seconds = remaining_seconds
        self.status = status
        self.urgency_level = urgency_level
        self.started_at = started_at or datetime.now(timezone.utc)
        self.last_reset_at = last_reset_at or datetime.now(timezone.utc)
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self) -> dict:
        """Convert state to dictionary."""
        return {
            "timer_id": str(self.timer_id),
            "initial_seconds": self.initial_seconds,
            "remaining_seconds": self.remaining_seconds,
            "status": self.status,
            "urgency_level": self.urgency_level.value,
            "started_at": self.started_at.isoformat(),
            "last_reset_at": self.last_reset_at.isoformat(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class TimerService:
    """Service for timer countdown logic, urgency state calculation, and reset validation."""

    def __init__(self):
        self._timers: dict[UUID, TimerState] = {}

    def create_timer(self, initial_seconds: int) -> TimerState:
        """Create a new timer session."""
        timer_id = uuid4()
        timer = TimerState(
            timer_id=timer_id,
            initial_seconds=initial_seconds,
            remaining_seconds=initial_seconds,
            status="active",
            urgency_level=UrgencyState.LOW,
        )
        self._timers[timer_id] = timer
        return timer

    def get_timer(self, timer_id: UUID) -> Optional[TimerState]:
        """Retrieve timer state by ID."""
        return self._timers.get(timer_id)

    def calculate_urgency_level(self, remaining_seconds: int, initial_seconds: int) -> UrgencyState:
        """Calculate urgency level based on remaining time percentage."""
        if remaining_seconds <= 0:
            return UrgencyState.CRITICAL
        
        percentage = (remaining_seconds / initial_seconds) * 100
        
        if percentage > 75:
            return UrgencyState.LOW
        elif percentage > 50:
            return UrgencyState.MEDIUM
        elif percentage > 25:
            return UrgencyState.HIGH
        else:
            return UrgencyState.CRITICAL

    def tick(self, timer_id: UUID, elapsed_seconds: int) -> Optional[TimerState]:
        """Update timer with elapsed time and recalculate urgency."""
        timer = self.get_timer(timer_id)
        if not timer:
            return None
        
        timer.remaining_seconds = max(0, timer.initial_seconds - elapsed_seconds)
        timer.urgency_level = self.calculate_urgency_level(timer.remaining_seconds, timer.initial_seconds)
        timer.updated_at = datetime.now(timezone.utc)
        
        if timer.remaining_seconds == 0:
            timer.status = "expired"
        
        return timer

    def reset(self, timer_id: UUID) -> Optional[TimerState]:
        """Reset timer to initial duration."""
        timer = self.get_timer(timer_id)
        if not timer:
            return None
        
        if timer.status == "expired":
            raise ValueError("Cannot reset an expired timer")
        
        timer.remaining_seconds = timer.initial_seconds
        timer.urgency_level = UrgencyState.LOW
        timer.last_reset_at = datetime.now(timezone.utc)
        timer.started_at = datetime.now(timezone.utc)
        timer.updated_at = datetime.now(timezone.utc)
        timer.status = "active"
        
        return timer

    def stop(self, timer_id: UUID) -> Optional[TimerState]:
        """Stop the timer."""
        timer = self.get_timer(timer_id)
        if not timer:
            return None
        
        timer.status = "paused"
        timer.updated_at = datetime.now(timezone.utc)
        
        return timer

    def start(self, timer_id: UUID) -> Optional[TimerState]:
        """Start or resume the timer."""
        timer = self.get_timer(timer_id)
        if not timer:
            return None
        
        timer.status = "active"
        timer.updated_at = datetime.now(timezone.utc)
        
        return timer

    def clear_all(self) -> None:
        """Clear all timer sessions (for testing)."""
        self._timers.clear()
