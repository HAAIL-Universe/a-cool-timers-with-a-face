from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from app.models.timer import TimerCreateRequest, Timer, TimerState
from app.services.timer_service import TimerService
from app.dependencies import get_timer_service

router = APIRouter(prefix="/timers", tags=["timers"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Timer)
async def create_timer(
    request: TimerCreateRequest,
    timer_service: TimerService = Depends(get_timer_service),
) -> Timer:
    """Create a new timer."""
    timer = timer_service.create_timer(request.duration)
    return timer


@router.get("", response_model=list[Timer])
async def list_timers(
    timer_service: TimerService = Depends(get_timer_service),
) -> list[Timer]:
    """List all timers."""
    timers = timer_service.list_timers()
    return timers


@router.get("/{timer_id}", response_model=Timer)
async def get_timer(
    timer_id: UUID,
    timer_service: TimerService = Depends(get_timer_service),
) -> Timer:
    """Get a timer by ID."""
    timer = timer_service.get_timer(timer_id)
    if not timer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timer not found",
        )
    return timer


@router.post("/{timer_id}/reset", response_model=Timer)
async def reset_timer(
    timer_id: UUID,
    timer_service: TimerService = Depends(get_timer_service),
) -> Timer:
    """Reset a timer to its initial duration."""
    timer = timer_service.get_timer(timer_id)
    if not timer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timer not found",
        )
    reset_timer_result = timer_service.reset_timer(timer_id)
    return reset_timer_result


@router.get("/{timer_id}/state", response_model=TimerState)
async def get_timer_state(
    timer_id: UUID,
    timer_service: TimerService = Depends(get_timer_service),
) -> TimerState:
    """Get the current state of a timer including urgency and colour."""
    timer = timer_service.get_timer(timer_id)
    if not timer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timer not found",
        )
    state = timer_service.get_timer_state(timer_id)
    return state


@router.delete("/{timer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_timer(
    timer_id: UUID,
    timer_service: TimerService = Depends(get_timer_service),
) -> None:
    """Delete a timer."""
    timer = timer_service.get_timer(timer_id)
    if not timer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timer not found",
        )
    timer_service.delete_timer(timer_id)
