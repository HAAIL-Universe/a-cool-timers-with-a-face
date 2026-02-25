from fastapi import APIRouter, HTTPException, status
from app.models.timer import TimerCreateRequest, Timer, TimerState
from app.services.timer import TimerService

router = APIRouter(prefix="/timers", tags=["timers"])
_timer_service = TimerService()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Timer)
async def create_timer(req: TimerCreateRequest) -> Timer:
    """Create a new timer."""
    return _timer_service.create_timer(req.duration)


@router.get("", response_model=list[Timer])
async def list_timers() -> list[Timer]:
    """List all timers."""
    return _timer_service.list_timers()


@router.get("/{timer_id}", response_model=Timer)
async def get_timer(timer_id: str) -> Timer:
    """Fetch timer by ID."""
    timer = _timer_service.get_timer(timer_id)
    if not timer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Timer not found")
    return timer


@router.delete("/{timer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_timer(timer_id: str) -> None:
    """Delete timer by ID."""
    _timer_service.delete_timer(timer_id)


@router.post("/{timer_id}/reset", response_model=Timer)
async def reset_timer(timer_id: str) -> Timer:
    """Reset timer to initial duration."""
    timer = _timer_service.reset_timer(timer_id)
    if not timer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Timer not found")
    return timer


@router.get("/{timer_id}/state", response_model=TimerState)
async def get_timer_state(timer_id: str) -> TimerState:
    """Fetch timer state (urgency, colour, expression)."""
    state = _timer_service.get_timer_state(timer_id)
    if not state:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Timer not found")
    return state
