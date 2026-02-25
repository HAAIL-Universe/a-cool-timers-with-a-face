from app.repos.timer_repo import TimerRepository
from app.services.timer_service import TimerService


_timer_repo = TimerRepository()
_timer_service = TimerService(_timer_repo)


def get_timer_service() -> TimerService:
    """Get shared timer service instance for tests."""
    return _timer_service


def get_timer_repo() -> TimerRepository:
    """Get shared timer repository instance for tests."""
    return _timer_repo
