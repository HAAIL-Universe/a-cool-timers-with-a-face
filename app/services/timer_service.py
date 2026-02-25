from datetime import datetime, timezone
from uuid import UUID, uuid4
from enum import Enum
from typing import Optional

from app.services.urgency_calculator import UrgencyLevel


class TimerStatus(str, Enum):
    """Timer state enumeration."""
    ACTIVE = "active"
    PAUSED = "paused"
    EXPIRED = "expired"
    COMPLETED = "completed"


class Timer:
    """In-memory timer representation."""
    
    def __init__(
        self,
        initial_seconds: int,
        timer_id: Optional[UUID] = None,
        status: TimerStatus = TimerStatus.ACTIVE,
        remaining_seconds: Optional[int] = None,
        urgency_level: UrgencyLevel = UrgencyLevel.LOW,
        last_reset_at: Optional[datetime] = None,
        started_at: Optional[datetime] = None,
    ):
        self.id = timer_id or uuid4()
        self.status = status
        self.initial_seconds = initial_seconds
        self.remaining_seconds = remaining_seconds or initial_seconds
        self.urgency_level = urgency_level
        self.last_reset_at = last_reset_at or datetime.now(timezone.utc)
        self.started_at = started_at or datetime.now(timezone.utc)
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
        self.reset_count = 0
    
    def to_dict(self) -> dict:
        """Convert timer to dictionary."""
        return {
            "id": str(self.id),
            "status": self.status.value,
            "initial_seconds": self.initial_seconds,
            "remaining_seconds": self.remaining_seconds,
            "urgency_level": self.urgency_level.value,
            "last_reset_at": self.last_reset_at.isoformat(),
            "started_at": self.started_at.isoformat(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class TimerService:
    """Handles countdown logic, urgency state calculation, and reset validation."""
    
    URGENCY_THRESHOLDS = {
        UrgencyLevel.CRITICAL: 0.15,
        UrgencyLevel.HIGH: 0.40,
        UrgencyLevel.MEDIUM: 0.70,
        UrgencyLevel.LOW: 1.0,
    }
    
    def __init__(self):
        self.timers: dict[UUID, Timer] = {}
    
    def create_timer(self, initial_seconds: int) -> Timer:
        """Create a new timer with the given duration in seconds."""
        if initial_seconds <= 0:
            raise ValueError("Timer duration must be positive")
        
        timer = Timer(initial_seconds=initial_seconds)
        self.timers[timer.id] = timer
        return timer
    
    def get_timer(self, timer_id: UUID) -> Optional[Timer]:
        """Fetch timer by ID."""
        return self.timers.get(timer_id)
    
    def start_timer(self, timer_id: UUID) -> Timer:
        """Start the timer countdown."""
        timer = self.get_timer(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")
        
        if timer.status == TimerStatus.EXPIRED:
            raise ValueError("Cannot start an expired timer")
        
        timer.status = TimerStatus.ACTIVE
        timer.started_at = datetime.now(timezone.utc)
        timer.updated_at = datetime.now(timezone.utc)
        return timer
    
    def stop_timer(self, timer_id: UUID) -> Timer:
        """Pause the timer."""
        timer = self.get_timer(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")
        
        timer.status = TimerStatus.PAUSED
        timer.updated_at = datetime.now(timezone.utc)
        return timer
    
    def reset_timer(self, timer_id: UUID) -> Timer:
        """Reset timer to initial duration and enforce reset-before-expiry mechanic."""
        timer = self.get_timer(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")
        
        if timer.status == TimerStatus.EXPIRED:
            raise ValueError("Cannot reset an expired timer; start a new session")
        
        timer.remaining_seconds = timer.initial_seconds
        timer.urgency_level = UrgencyLevel.LOW
        timer.last_reset_at = datetime.now(timezone.utc)
        timer.reset_count += 1
        timer.status = TimerStatus.ACTIVE
        timer.updated_at = datetime.now(timezone.utc)
        return timer
    
    def update_timer_state(self, timer_id: UUID) -> Timer:
        """Update timer state based on elapsed time and calculate urgency."""
        timer = self.get_timer(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")
        
        if timer.status != TimerStatus.ACTIVE:
            return timer
        
        elapsed = (datetime.now(timezone.utc) - timer.started_at).total_seconds()
        timer.remaining_seconds = max(0, timer.initial_seconds - int(elapsed))
        
        if timer.remaining_seconds <= 0:
            timer.remaining_seconds = 0
            timer.status = TimerStatus.EXPIRED
            timer.urgency_level = UrgencyLevel.CRITICAL
        else:
            timer.urgency_level = self._calculate_urgency(timer.remaining_seconds, timer.initial_seconds)
        
        timer.updated_at = datetime.now(timezone.utc)
        return timer
    
    def _calculate_urgency(self, remaining_seconds: int, initial_seconds: int) -> UrgencyLevel:
        """Calculate urgency level based on remaining time as percentage of initial duration."""
        if initial_seconds == 0:
            return UrgencyLevel.LOW
        
        remaining_ratio = remaining_seconds / initial_seconds
        
        for level, threshold in sorted(self.URGENCY_THRESHOLDS.items(), key=lambda x: x[1]):
            if remaining_ratio <= threshold:
                return level
        
        return UrgencyLevel.LOW
    
    def delete_timer(self, timer_id: UUID) -> bool:
        """Delete a timer session."""
        if timer_id in self.timers:
            del self.timers[timer_id]
            return True
        return False
