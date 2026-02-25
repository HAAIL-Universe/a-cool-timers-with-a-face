from fastapi import APIRouter, HTTPException
from app.services.timer_service import TimerService, TimerRepo
from app.schemas.timer import TimerConfig, TimerState, UrgencyState

router = APIRouter(prefix="/api", tags=["timer"])

# In-memory repo for Phase 0 (replaced by DB-backed repo later)
timer_repo = TimerRepo()
timer_service = TimerService(timer_repo)


@router.get("/timer", response_model=TimerState)
async def get_timer() -> TimerState:
    """Get current timer state."""
    return await timer_service.get_state()


@router.post("/timer", response_model=TimerState)
async def configure_timer(config: TimerConfig) -> TimerState:
    """Configure timer duration and start countdown."""
    return await timer_service.configure(config)


@router.post("/timer/reset", response_model=TimerState)
async def reset_timer() -> TimerState:
    """Reset countdown to configured duration (fails if expired)."""
    try:
        return await timer_service.reset()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/timer/pause", response_model=TimerState)
async def pause_timer() -> TimerState:
    """Pause active countdown without reset."""
    try:
        return await timer_service.pause()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/timer/resume", response_model=TimerState)
async def resume_timer() -> TimerState:
    """Resume paused countdown."""
    try:
        return await timer_service.resume()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/urgency", response_model=UrgencyState)
async def get_urgency() -> UrgencyState:
    """Get current urgency level and visual feedback state."""
    return await timer_service.get_urgency()
