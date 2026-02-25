from app.services.timer_service import TimerRepo, TimerService

_timer_repo_instance: TimerRepo | None = None
_timer_service_instance: TimerService | None = None


def get_timer_repo() -> TimerRepo:
    """Return singleton TimerRepo instance."""
    global _timer_repo_instance
    if _timer_repo_instance is None:
        _timer_repo_instance = TimerRepo()
    return _timer_repo_instance


def get_timer_service() -> TimerService:
    """Return singleton TimerService instance."""
    global _timer_service_instance
    if _timer_service_instance is None:
        repo = get_timer_repo()
        _timer_service_instance = TimerService(repo)
    return _timer_service_instance
