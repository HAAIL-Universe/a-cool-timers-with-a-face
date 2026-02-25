from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, UUID, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from app.database import Base


class Timer(Base):
    """Countdown timer state for workout sessions."""
    __tablename__ = "timer"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
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

    def to_dict(self) -> dict:
        """Convert timer to dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "duration_seconds": self.duration_seconds,
            "remaining_seconds": self.remaining_seconds,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "paused_at": self.paused_at.isoformat() if self.paused_at else None,
            "reset_count": self.reset_count,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class TimerEvent(Base):
    """Log of reset and state transitions for tracking workout cadence."""
    __tablename__ = "timer_event"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timer_id = Column(UUID(as_uuid=True), ForeignKey("timer.id", ondelete="CASCADE"), nullable=False)
    event_type = Column(String(50), nullable=False)
    urgency_level = Column(Integer, default=0)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    timer = relationship("Timer", back_populates="events")

    def to_dict(self) -> dict:
        """Convert timer event to dictionary."""
        return {
            "id": str(self.id),
            "timer_id": str(self.timer_id),
            "event_type": self.event_type,
            "urgency_level": self.urgency_level,
            "recorded_at": self.recorded_at.isoformat(),
        }
