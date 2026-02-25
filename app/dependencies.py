from fastapi import Depends
from app.repos.timer_repo import TimerRepo
from app.services.timer_service import TimerService

_timer_repo_instance: TimerRepo | None = None
_timer_service_instance: TimerService | None = None


def get_timer_repo() -> TimerRepo:
    """Provide singleton TimerRepo instance."""
    global _timer_repo_instance
    if _timer_repo_instance is None:
        _timer_repo_instance = TimerRepo()
    return _timer_repo_instance


def get_timer_service(repo: TimerRepo = Depends(get_timer_repo)) -> TimerService:
    """Provide singleton TimerService instance."""
    global _timer_service_instance
    if _timer_service_instance is None:
        _timer_service_instance = TimerService(repo)
    return _timer_service_instance
