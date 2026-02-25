from datetime import datetime, timedelta
from uuid import UUID
from enum import Enum
from typing import Optional


class TimerStatus(str, Enum):
    """Timer lifecycle status."""
    active = "active"
    paused = "paused"
    expired = "expired"
    completed = "completed"


class UrgencyLevel(str, Enum):
    """Urgency escalation levels based on remaining time."""
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class TimerState:
    """In-memory timer state container."""

    def __init__(
        self,
        timer_id: UUID,
        initial_seconds: int,
        remaining_seconds: int,
        status: TimerStatus = TimerStatus.active,
        urgency_level: UrgencyLevel = UrgencyLevel.low,
        started_at: Optional[datetime] = None,
        last_reset_at: Optional[datetime] = None,
    ):
        self.timer_id = timer_id
        self.initial_seconds = initial_seconds
        self.remaining_seconds = remaining_seconds
        self.status = status
        self.urgency_level = urgency_level
        self.started_at = started_at or datetime.utcnow()
        self.last_reset_at = last_reset_at or datetime.utcnow()

    def to_dict(self) -> dict:
        """Serialize timer state to dictionary."""
        return {
            "timer_id": str(self.timer_id),
            "initial_seconds": self.initial_seconds,
            "remaining_seconds": self.remaining_seconds,
            "status": self.status.value,
            "urgency_level": self.urgency_level.value,
            "started_at": self.started_at.isoformat(),
            "last_reset_at": self.last_reset_at.isoformat(),
        }


class TimerService:
    """Manages countdown logic, urgency state, and reset validation."""

    def __init__(self):
        self.timers: dict[UUID, TimerState] = {}

    def create_timer(self, initial_seconds: int) -> TimerState:
        """Create a new timer session."""
        from uuid import uuid4

        timer_id = uuid4()
        timer = TimerState(
            timer_id=timer_id,
            initial_seconds=initial_seconds,
            remaining_seconds=initial_seconds,
            status=TimerStatus.active,
            urgency_level=self._calculate_urgency(initial_seconds, initial_seconds),
        )
        self.timers[timer_id] = timer
        return timer

    def get_timer(self, timer_id: UUID) -> Optional[TimerState]:
        """Retrieve timer state by ID."""
        return self.timers.get(timer_id)

    def start_timer(self, timer_id: UUID) -> TimerState:
        """Start a timer countdown."""
        timer = self.get_timer(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")
        timer.status = TimerStatus.active
        timer.started_at = datetime.utcnow()
        return timer

    def pause_timer(self, timer_id: UUID) -> TimerState:
        """Pause a running timer."""
        timer = self.get_timer(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")
        timer.status = TimerStatus.paused
        return timer

    def stop_timer(self, timer_id: UUID) -> TimerState:
        """Stop and complete a timer."""
        timer = self.get_timer(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")
        timer.status = TimerStatus.completed
        return timer

    def reset_timer(self, timer_id: UUID) -> TimerState:
        """Reset timer to initial duration; enforce reset-before-expiry mechanic."""
        timer = self.get_timer(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")

        if timer.remaining_seconds <= 0:
            raise ValueError("Cannot reset expired timer; countdown reached zero")

        timer.remaining_seconds = timer.initial_seconds
        timer.last_reset_at = datetime.utcnow()
        timer.urgency_level = self._calculate_urgency(
            timer.initial_seconds, timer.remaining_seconds
        )
        return timer

    def tick(self, timer_id: UUID, elapsed_seconds: int = 1) -> TimerState:
        """Decrement remaining seconds and update urgency level."""
        timer = self.get_timer(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")

        if timer.status != TimerStatus.active:
            return timer

        timer.remaining_seconds = max(0, timer.remaining_seconds - elapsed_seconds)

        if timer.remaining_seconds <= 0:
            timer.status = TimerStatus.expired
            timer.urgency_level = UrgencyLevel.critical

        timer.urgency_level = self._calculate_urgency(
            timer.initial_seconds, timer.remaining_seconds
        )
        return timer

    def _calculate_urgency(
        self, initial_seconds: int, remaining_seconds: int
    ) -> UrgencyLevel:
        """Map remaining time to urgency level with monotonic intensity escalation."""
        if remaining_seconds <= 0:
            return UrgencyLevel.critical

        ratio = remaining_seconds / initial_seconds if initial_seconds > 0 else 1.0

        if ratio > 0.75:
            return UrgencyLevel.low
        elif ratio > 0.5:
            return UrgencyLevel.medium
        elif ratio > 0.25:
            return UrgencyLevel.high
        else:
            return UrgencyLevel.critical

    def clear_expired(self) -> None:
        """Clean up expired timer sessions from memory."""
        expired_ids = [
            tid for tid, t in self.timers.items() if t.status == TimerStatus.expired
        ]
        for tid in expired_ids:
            del self.timers[tid]
