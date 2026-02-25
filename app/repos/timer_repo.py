from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.timer import Timer, TimerEvent


class TimerRepo:
    """Repository for timer data access."""

    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db

    def create_timer(
        self,
        duration_seconds: int,
        name: str = "Workout",
    ) -> Timer:
        """Create a new timer."""
        timer = Timer(
            name=name,
            duration_seconds=duration_seconds,
            remaining_seconds=duration_seconds,
            status="stopped",
        )
        self.db.add(timer)
        self.db.commit()
        self.db.refresh(timer)
        return timer

    def get_timer(self, timer_id: UUID) -> Optional[Timer]:
        """Fetch timer by ID."""
        return self.db.query(Timer).filter(Timer.id == timer_id).first()

    def list_timers(self) -> List[Timer]:
        """Fetch all timers."""
        return self.db.query(Timer).all()

    def update_timer(
        self,
        timer_id: UUID,
        remaining_seconds: int,
        status: str,
        started_at=None,
        paused_at=None,
        reset_count: Optional[int] = None,
    ) -> Optional[Timer]:
        """Update timer state."""
        timer = self.get_timer(timer_id)
        if not timer:
            return None

        timer.remaining_seconds = remaining_seconds
        timer.status = status
        if started_at is not None:
            timer.started_at = started_at
        if paused_at is not None:
            timer.paused_at = paused_at
        if reset_count is not None:
            timer.reset_count = reset_count

        self.db.commit()
        self.db.refresh(timer)
        return timer

    def delete_timer(self, timer_id: UUID) -> bool:
        """Delete timer by ID."""
        timer = self.get_timer(timer_id)
        if not timer:
            return False

        self.db.delete(timer)
        self.db.commit()
        return True

    def record_event(
        self,
        timer_id: UUID,
        event_type: str,
        urgency_level: int = 0,
    ) -> TimerEvent:
        """Record timer event."""
        event = TimerEvent(
            timer_id=timer_id,
            event_type=event_type,
            urgency_level=urgency_level,
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def get_timer_events(self, timer_id: UUID) -> List[TimerEvent]:
        """Fetch all events for a timer."""
        return self.db.query(TimerEvent).filter(TimerEvent.timer_id == timer_id).all()
