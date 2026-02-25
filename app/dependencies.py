from typing import Generator
from app.repos.timer_repo import TimerRepository
from app.services.timer_service import TimerService


def get_timer_repo() -> TimerRepository:
    """Provide timer repository instance."""
    return TimerRepository()


def get_timer_service(repo: TimerRepository = None) -> TimerService:
    """Provide timer service instance."""
    if repo is None:
        repo = get_timer_repo()
    return TimerService(repo)
