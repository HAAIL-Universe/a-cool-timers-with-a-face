from fastapi import APIRouter, HTTPException, Depends, status
from uuid import UUID
from app.models.timer import TimerCreateRequest, Timer, TimerState
from app.services.timer_service import TimerService
from app.repos.timer_repo import TimerRepo

router = APIRouter(prefix="/timers", tags=["timers"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Timer)
async def create_timer(
    request: TimerCreateRequest,
    timer_service: TimerService = Depends(lambda: TimerService(TimerRepo())),
) -> Timer:
    """Create a new timer session."""
    return timer_service.create_timer(request.duration)


@router.get("", response_model=list[Timer])
async def list_timers(
    timer_service: TimerService = Depends(lambda: TimerService(TimerRepo())),
) -> list[Timer]:
    """List all active timers."""
    return timer_service.list_timers()


@router.get("/{timer_id}", response_model=Timer)
async def get_timer(
    timer_id: UUID,
    timer_service: TimerService = Depends(lambda: TimerService(TimerRepo())),
) -> Timer:
    """Fetch a timer by ID."""
    timer = timer_service.get_timer(timer_id)
    if not timer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Timer not found")
    return timer


@router.get("/{timer_id}/state", response_model=TimerState)
async def get_timer_state(
    timer_id: UUID,
    timer_service: TimerService = Depends(lambda: TimerService(TimerRepo())),
) -> TimerState:
    """Get timer state including urgency level, expression, and colour."""
    timer = timer_service.get_timer(timer_id)
    if not timer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Timer not found")
    return timer_service.get_timer_state(timer)


@router.post("/{timer_id}/reset", response_model=Timer)
async def reset_timer(
    timer_id: UUID,
    timer_service: TimerService = Depends(lambda: TimerService(TimerRepo())),
) -> Timer:
    """Reset timer to initial duration."""
    timer = timer_service.get_timer(timer_id)
    if not timer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Timer not found")
    return timer_service.reset_timer(timer_id)


@router.delete("/{timer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_timer(
    timer_id: UUID,
    timer_service: TimerService = Depends(lambda: TimerService(TimerRepo())),
) -> None:
    """Delete a timer."""
    timer = timer_service.get_timer(timer_id)
    if not timer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Timer not found")
    timer_service.delete_timer(timer_id)
