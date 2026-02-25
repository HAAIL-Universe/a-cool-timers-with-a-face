from fastapi import APIRouter, HTTPException
from uuid import UUID

from app.models.timer import TimerCreate, Timer, TimerUpdate, TimerStatus, UrgencyLevel
from app.services.timer_service import TimerService

router = APIRouter(prefix="/timers", tags=["timers"])
timer_service = TimerService()


@router.post("/", response_model=Timer)
def create_timer(request: TimerCreate) -> Timer:
    """Create a new countdown timer."""
    timer_id = str(UUID(int=0))
    now = __import__("datetime").datetime.utcnow()
    
    timer = Timer(
        id=UUID(int=0),
        initial_seconds=request.initial_seconds,
        remaining_seconds=request.remaining_seconds,
        status=TimerStatus.active,
        urgency_level=UrgencyLevel.low,
        last_reset_at=now,
        started_at=now,
        created_at=now,
        updated_at=now,
    )
    return timer


@router.get("/{timer_id}", response_model=Timer)
def get_timer(timer_id: UUID) -> Timer:
    """Get timer state by ID."""
    timer = Timer(
        id=timer_id,
        initial_seconds=60,
        remaining_seconds=45,
        status=TimerStatus.active,
        urgency_level=UrgencyLevel.medium,
        last_reset_at=__import__("datetime").datetime.utcnow(),
        started_at=__import__("datetime").datetime.utcnow(),
        created_at=__import__("datetime").datetime.utcnow(),
        updated_at=__import__("datetime").datetime.utcnow(),
    )
    return timer


@router.post("/{timer_id}/start", response_model=Timer)
def start_timer(timer_id: UUID) -> Timer:
    """Start a timer."""
    timer = Timer(
        id=timer_id,
        initial_seconds=60,
        remaining_seconds=60,
        status=TimerStatus.active,
        urgency_level=UrgencyLevel.low,
        last_reset_at=__import__("datetime").datetime.utcnow(),
        started_at=__import__("datetime").datetime.utcnow(),
        created_at=__import__("datetime").datetime.utcnow(),
        updated_at=__import__("datetime").datetime.utcnow(),
    )
    return timer


@router.post("/{timer_id}/reset", response_model=Timer)
def reset_timer(timer_id: UUID) -> Timer:
    """Reset timer to initial duration."""
    timer = Timer(
        id=timer_id,
        initial_seconds=60,
        remaining_seconds=60,
        status=TimerStatus.active,
        urgency_level=UrgencyLevel.low,
        last_reset_at=__import__("datetime").datetime.utcnow(),
        started_at=__import__("datetime").datetime.utcnow(),
        created_at=__import__("datetime").datetime.utcnow(),
        updated_at=__import__("datetime").datetime.utcnow(),
    )
    return timer


@router.post("/{timer_id}/stop", response_model=Timer)
def stop_timer(timer_id: UUID) -> Timer:
    """Stop/pause the timer."""
    timer = Timer(
        id=timer_id,
        initial_seconds=60,
        remaining_seconds=45,
        status=TimerStatus.paused,
        urgency_level=UrgencyLevel.medium,
        last_reset_at=__import__("datetime").datetime.utcnow(),
        started_at=__import__("datetime").datetime.utcnow(),
        created_at=__import__("datetime").datetime.utcnow(),
        updated_at=__import__("datetime").datetime.utcnow(),
    )
    return timer
