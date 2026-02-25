from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UUID, Index
from sqlalchemy.orm import relationship

from app.database import Base


class Timer(Base):
    __tablename__ = "timer"

    id = Column(UUID, primary_key=True, default=uuid4)
    name = Column(String(255), default="Workout")
    duration_seconds = Column(Integer, nullable=False)
    remaining_seconds = Column(Integer, nullable=False)
    started_at = Column(DateTime, nullable=True)
    paused_at = Column(DateTime, nullable=True)
    reset_count = Column(Integer, default=0)
    status = Column(String(50), default="stopped")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    events = relationship("TimerEvent", back_populates="timer", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_timer_status", "status"),
    )


class TimerEvent(Base):
    __tablename__ = "timer_event"

    id = Column(UUID, primary_key=True, default=uuid4)
    timer_id = Column(UUID, ForeignKey("timer.id", ondelete="CASCADE"), nullable=False)
    event_type = Column(String(50), nullable=False)
    urgency_level = Column(Integer, default=0)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    timer = relationship("Timer", back_populates="events")

    __table_args__ = (
        Index("idx_timer_event_timer_id", "timer_id"),
    )
