from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Depends

from app.models.timer import TimerCreateRequest, Timer, TimerState
from app.services.timer_service import TimerService

router = APIRouter(prefix="/timers", tags=["timers"])


def get_timer_service() -> TimerService:
    return TimerService()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Timer)
async def create_timer(req: TimerCreateRequest, service: TimerService = Depends(get_timer_service)) -> Timer:
    """Create a new timer with initial duration."""
    timer = await service.create_timer(req.duration)
    return timer


@router.get("", response_model=list[Timer])
async def list_timers(service: TimerService = Depends(get_timer_service)) -> list[Timer]:
    """List all active timers."""
    timers = await service.list_timers()
    return timers


@router.get("/{timer_id}", response_model=Timer)
async def get_timer(timer_id: UUID, service: TimerService = Depends(get_timer_service)) -> Timer:
    """Get a timer by ID."""
    timer = await service.get_timer(timer_id)
    if not timer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Timer {timer_id} not found"
        )
    return timer


@router.delete("/{timer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_timer(timer_id: UUID, service: TimerService = Depends(get_timer_service)) -> None:
    """Delete a timer by ID."""
    success = await service.delete_timer(timer_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Timer {timer_id} not found"
        )


@router.post("/{timer_id}/reset", response_model=Timer)
async def reset_timer(timer_id: UUID, service: TimerService = Depends(get_timer_service)) -> Timer:
    """Reset timer to initial duration."""
    timer = await service.reset_timer(timer_id)
    if not timer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Timer {timer_id} not found"
        )
    return timer


@router.get("/{timer_id}/state", response_model=TimerState)
async def get_timer_state(timer_id: UUID, service: TimerService = Depends(get_timer_service)) -> TimerState:
    """Get timer state with urgency feedback (colour and facial expression). Returns 404 if timer not found."""
    state = await service.get_timer_state(timer_id)
    if not state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Timer {timer_id} not found"
        )
    return state
