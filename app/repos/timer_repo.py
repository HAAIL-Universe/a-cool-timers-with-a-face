from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.timer import Timer, TimerEvent


class TimerRepository:
    """Database CRUD operations for timer and timer_event tables."""

    def __init__(self, session: AsyncSession):
        """Initialize repository with database session."""
        self.session = session

    async def get_or_create_timer(self, timer_id: Optional[UUID] = None) -> Timer:
        """Get existing timer or create default one if none exists."""
        if timer_id:
            stmt = select(Timer).where(Timer.id == timer_id)
            result = await self.session.execute(stmt)
            timer = result.scalar_one_or_none()
            if timer:
                return timer

        stmt = select(Timer).limit(1)
        result = await self.session.execute(stmt)
        timer = result.scalar_one_or_none()

        if not timer:
            timer = Timer(
                duration_seconds=60,
                remaining_seconds=60,
                status="stopped",
            )
            self.session.add(timer)
            await self.session.flush()

        return timer

    async def get_timer(self, timer_id: UUID) -> Optional[Timer]:
        """Fetch timer by ID."""
        stmt = select(Timer).where(Timer.id == timer_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_timer(
        self,
        timer_id: UUID,
        duration_seconds: Optional[int] = None,
        remaining_seconds: Optional[int] = None,
        status: Optional[str] = None,
        started_at: Optional[datetime] = None,
        paused_at: Optional[datetime] = None,
        reset_count: Optional[int] = None,
        name: Optional[str] = None,
    ) -> Timer:
        """Update timer fields."""
        timer = await self.get_timer(timer_id)
        if not timer:
            raise ValueError(f"Timer {timer_id} not found")

        if duration_seconds is not None:
            timer.duration_seconds = duration_seconds
        if remaining_seconds is not None:
            timer.remaining_seconds = remaining_seconds
        if status is not None:
            timer.status = status
        if started_at is not None:
            timer.started_at = started_at
        if paused_at is not None:
            timer.paused_at = paused_at
        if reset_count is not None:
            timer.reset_count = reset_count
        if name is not None:
            timer.name = name

        timer.updated_at = datetime.utcnow()
        await self.session.flush()
        return timer

    async def create_timer_event(
        self,
        timer_id: UUID,
        event_type: str,
        urgency_level: int = 0,
    ) -> TimerEvent:
        """Create a timer event log entry."""
        event = TimerEvent(
            timer_id=timer_id,
            event_type=event_type,
            urgency_level=urgency_level,
        )
        self.session.add(event)
        await self.session.flush()
        return event

    async def get_timer_events(self, timer_id: UUID) -> list[TimerEvent]:
        """Fetch all events for a timer."""
        stmt = select(TimerEvent).where(TimerEvent.timer_id == timer_id).order_by(TimerEvent.recorded_at)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def commit(self) -> None:
        """Commit pending transaction."""
        await self.session.commit()

    async def rollback(self) -> None:
        """Rollback pending transaction."""
        await self.session.rollback()
