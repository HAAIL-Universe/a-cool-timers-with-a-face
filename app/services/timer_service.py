from datetime import datetime
from typing import Optional
from uuid import UUID

from app.models.timer import Timer
from app.repos.timer_repo import TimerRepo
from app.schemas.timer import UrgencyLevel, TimerStatus


class TimerService:
    """Timer state machine and urgency calculation logic."""

    def __init__(self, repo: TimerRepo):
        """Initialize service with repository."""
        self.repo = repo

    def create_timer(self, duration_seconds: int, name: str = "Workout") -> Timer:
        """Create a new timer."""
        return self.repo.create_timer(duration_seconds, name)

    def get_timer(self, timer_id: UUID) -> Optional[Timer]:
        """Fetch timer by ID."""
        return self.repo.get_timer(timer_id)

    def start_timer(self, timer_id: UUID) -> Optional[Timer]:
        """Start countdown from current remaining seconds."""
        timer = self.repo.get_timer(timer_id)
        if not timer:
            return None

        timer = self.repo.update_timer(
            timer_id,
            remaining_seconds=timer.remaining_seconds,
            status=TimerStatus.running,
            started_at=datetime.utcnow(),
            paused_at=None,
        )
        if timer:
            self.repo.record_event(timer_id, "started", self._calculate_urgency(timer))
        return timer

    def pause_timer(self, timer_id: UUID) -> Optional[Timer]:
        """Pause countdown."""
        timer = self.repo.get_timer(timer_id)
        if not timer:
            return None

        timer = self.repo.update_timer(
            timer_id,
            remaining_seconds=timer.remaining_seconds,
            status=TimerStatus.paused,
            paused_at=datetime.utcnow(),
        )
        if timer:
            self.repo.record_event(timer_id, "paused", self._calculate_urgency(timer))
        return timer

    def reset_timer(
        self, timer_id: UUID, duration_seconds: Optional[int] = None
    ) -> Optional[Timer]:
        """Reset timer to initial or new duration."""
        timer = self.repo.get_timer(timer_id)
        if not timer:
            return None

        new_duration = duration_seconds if duration_seconds else timer.duration_seconds
        timer = self.repo.update_timer(
            timer_id,
            remaining_seconds=new_duration,
            status=TimerStatus.stopped,
            started_at=None,
            paused_at=None,
            reset_count=timer.reset_count + 1,
        )
        if timer:
            self.repo.record_event(timer_id, "reset", self._calculate_urgency(timer))
        return timer

    def tick_timer(self, timer_id: UUID, delta_seconds: int = 1) -> Optional[Timer]:
        """Decrement remaining seconds and check for expiry."""
        timer = self.repo.get_timer(timer_id)
        if not timer or timer.status != TimerStatus.running:
            return timer

        remaining = max(0, timer.remaining_seconds - delta_seconds)
        new_status = TimerStatus.expired if remaining == 0 else TimerStatus.running

        timer = self.repo.update_timer(
            timer_id,
            remaining_seconds=remaining,
            status=new_status,
        )
        if timer and new_status == TimerStatus.expired:
            self.repo.record_event(timer_id, "expired", self._calculate_urgency(timer))
        return timer

    def _calculate_urgency(self, timer: Timer) -> int:
        """Calculate urgency level based on remaining time ratio."""
        if timer.duration_seconds == 0:
            return UrgencyLevel.calm

        ratio = timer.remaining_seconds / timer.duration_seconds

        if ratio > 0.5:
            return UrgencyLevel.calm
        elif ratio > 0.25:
            return UrgencyLevel.elevated
        elif ratio > 0.0:
            return UrgencyLevel.anxious
        else:
            return UrgencyLevel.alarm

    def calculate_urgency_response(self, timer: Timer) -> dict:
        """Calculate visual urgency state for frontend."""
        urgency_level = self._calculate_urgency(timer)

        colour_intensity = 1.0 - (timer.remaining_seconds / timer.duration_seconds)

        facial_expressions = {
            UrgencyLevel.calm: "calm",
            UrgencyLevel.elevated: "slightly_concerned",
            UrgencyLevel.anxious: "anxious",
            UrgencyLevel.alarm: "alarm",
        }

        return {
            "level": urgency_level,
            "colour_intensity": colour_intensity,
            "facial_expression": facial_expressions[urgency_level],
        }
