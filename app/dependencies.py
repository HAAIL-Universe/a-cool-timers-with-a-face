from typing import Annotated

from fastapi import Depends

from app.repos.timer_repo import TimerRepo
from app.services.timer_service import TimerService


def get_timer_repo() -> TimerRepo:
    """Get timer repository instance."""
    return TimerRepo()


def get_timer_service(
    repo: Annotated[TimerRepo, Depends(get_timer_repo)]
) -> TimerService:
    """Get timer service instance."""
    return TimerService(repo)
