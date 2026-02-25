from typing import Annotated

from fastapi import Depends

from app.repos.timer_repo import TimerRepo
from app.services.timer_service import TimerService

_timer_repo: TimerRepo | None = None
_timer_service: TimerService | None = None


def get_timer_repo() -> TimerRepo:
    """Provide singleton TimerRepo instance."""
    global _timer_repo
    if _timer_repo is None:
        _timer_repo = TimerRepo()
    return _timer_repo


def get_timer_service(repo: Annotated[TimerRepo, Depends(get_timer_repo)]) -> TimerService:
    """Provide singleton TimerService instance."""
    global _timer_service
    if _timer_service is None:
        _timer_service = TimerService(repo)
    return _timer_service


TimerRepoDep = Annotated[TimerRepo, Depends(get_timer_repo)]
TimerServiceDep = Annotated[TimerService, Depends(get_timer_service)]
