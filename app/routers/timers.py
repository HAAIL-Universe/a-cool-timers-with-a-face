from fastapi import APIRouter, Depends, HTTPException, status
from app.models.timer import Timer, TimerState, TimerCreateRequest
from app.services.timer_service import TimerService
from app.dependencies import get_timer_service

router = APIRouter(prefix="/timers", tags=["timers"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Timer)
def create_timer(
    request: TimerCreateRequest,
    service: TimerService = Depends(get_timer_service),
) -> Timer:
    """Create a new timer with specified duration."""
    return service.create_timer(request.duration)


@router.get("/{timer_id}", response_model=Timer)
def get_timer(
    timer_id: str,
    service: TimerService = Depends(get_timer_service),
) -> Timer:
    """Fetch a timer by ID."""
    try:
        return service.get_timer(timer_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{timer_id}/state", response_model=TimerState)
def get_timer_state(
    timer_id: str,
    service: TimerService = Depends(get_timer_service),
) -> TimerState:
    """Get timer state including urgency, colour, and facial expression."""
    try:
        return service.get_timer_state(timer_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("", response_model=list[Timer])
def list_timers(
    service: TimerService = Depends(get_timer_service),
) -> list[Timer]:
    """List all timers."""
    return service.list_timers()


@router.post("/{timer_id}/reset", response_model=Timer)
def reset_timer(
    timer_id: str,
    service: TimerService = Depends(get_timer_service),
) -> Timer:
    """Reset timer to initial duration."""
    try:
        return service.reset_timer(timer_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{timer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_timer(
    timer_id: str,
    service: TimerService = Depends(get_timer_service),
) -> None:
    """Delete a timer."""
    try:
        service.delete_timer(timer_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
