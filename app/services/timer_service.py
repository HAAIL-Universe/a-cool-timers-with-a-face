import uuid
from datetime import datetime, timezone
from app.models.timer import (
    Timer,
    TimerStatus,
    UrgencyLevel,
    FacialExpression,
    ColourIntensity,
    TimerCreateRequest,
)
from app.repos.timer_repo import TimerRepo


class TimerService:
    """Business logic for timer countdown, urgency calculation, and state management."""

    def __init__(self, repo: TimerRepo) -> None:
        self.repo = repo

    def create_timer(self, request: TimerCreateRequest) -> Timer:
        """Create a new timer with given duration in seconds."""
        now = datetime.now(timezone.utc)
        timer = Timer(
            id=str(uuid.uuid4()),
            initial_seconds=request.duration,
            remaining_seconds=request.duration,
            status=TimerStatus.running,
            urgency_level=UrgencyLevel.low,
            started_at=now,
            last_reset_at=now,
            created_at=now,
        )
        return self.repo.create(timer)

    def get_timer(self, timer_id: str) -> Timer | None:
        """Retrieve timer by ID."""
        return self.repo.get(timer_id)

    def tick(self, timer_id: str) -> Timer | None:
        """Decrement remaining_seconds by 1; update urgency and status."""
        timer = self.repo.get(timer_id)
        if not timer:
            return None

        if timer.status != TimerStatus.running:
            return timer

        timer.remaining_seconds = max(0, timer.remaining_seconds - 1)

        if timer.remaining_seconds == 0:
            timer.status = TimerStatus.expired
        else:
            timer.urgency_level = self._calculate_urgency(timer)

        timer.updated_at = datetime.now(timezone.utc)
        return self.repo.update(timer)

    def reset_timer(self, timer_id: str) -> Timer | None:
        """Reset remaining_seconds to initial_seconds and update last_reset_at."""
        timer = self.repo.get(timer_id)
        if not timer:
            return None

        timer.remaining_seconds = timer.initial_seconds
        timer.status = TimerStatus.running
        timer.urgency_level = UrgencyLevel.low
        timer.last_reset_at = datetime.now(timezone.utc)
        timer.updated_at = datetime.now(timezone.utc)
        return self.repo.update(timer)

    def stop_timer(self, timer_id: str) -> Timer | None:
        """Pause the timer."""
        timer = self.repo.get(timer_id)
        if not timer:
            return None

        timer.status = TimerStatus.paused
        timer.updated_at = datetime.now(timezone.utc)
        return self.repo.update(timer)

    def resume_timer(self, timer_id: str) -> Timer | None:
        """Resume a paused timer."""
        timer = self.repo.get(timer_id)
        if not timer:
            return None

        if timer.status == TimerStatus.paused:
            timer.status = TimerStatus.running
            timer.updated_at = datetime.now(timezone.utc)
            return self.repo.update(timer)

        return timer

    def _calculate_urgency(self, timer: Timer) -> UrgencyLevel:
        """Map remaining time percentage to urgency level."""
        if timer.initial_seconds == 0:
            return UrgencyLevel.critical

        percentage = (timer.remaining_seconds / timer.initial_seconds) * 100

        if percentage > 50:
            return UrgencyLevel.low
        elif percentage > 25:
            return UrgencyLevel.medium
        elif percentage > 10:
            return UrgencyLevel.high
        else:
            return UrgencyLevel.critical

    def _map_colour(self, urgency: UrgencyLevel) -> ColourIntensity:
        """Map urgency level to RGB colour intensity."""
        colour_map = {
            UrgencyLevel.low: ColourIntensity(red=0, green=255, blue=0),
            UrgencyLevel.medium: ColourIntensity(red=255, green=255, blue=0),
            UrgencyLevel.high: ColourIntensity(red=255, green=165, blue=0),
            UrgencyLevel.critical: ColourIntensity(red=255, green=0, blue=0),
        }
        return colour_map[urgency]

    def _map_expression(self, urgency: UrgencyLevel) -> FacialExpression:
        """Map urgency level to facial expression."""
        expression_map = {
            UrgencyLevel.low: FacialExpression.calm,
            UrgencyLevel.medium: FacialExpression.concerned,
            UrgencyLevel.high: FacialExpression.stressed,
            UrgencyLevel.critical: FacialExpression.critical,
        }
        return expression_map[urgency]

    def get_timer_state(self, timer_id: str) -> dict | None:
        """Return TimerState for display; returns None if timer not found."""
        timer = self.repo.get(timer_id)
        if not timer:
            return None

        remaining_percentage = (
            (timer.remaining_seconds / timer.initial_seconds) * 100
            if timer.initial_seconds > 0
            else 0
        )

        colour = self._map_colour(timer.urgency_level)
        expression = self._map_expression(timer.urgency_level)

        return {
            "id": timer.id,
            "remaining_time": timer.remaining_seconds,
            "remaining_percentage": remaining_percentage,
            "urgency_level": timer.urgency_level,
            "colour_intensity": colour,
            "facial_expression": expression,
        }

    def delete_timer(self, timer_id: str) -> bool:
        """Delete a timer."""
        return self.repo.delete(timer_id)

    def list_timers(self) -> list[Timer]:
        """Return all timers."""
        return self.repo.list_all()
