from datetime import datetime, timezone
from app.schemas.timer import TimerConfig, TimerState, UrgencyState


class Timer:
    """Timer model representing a countdown timer instance."""
    
    def __init__(
        self,
        id: int,
        duration_seconds: int,
        remaining_seconds: int,
        status: str,
        started_at: datetime,
        paused_at: datetime | None,
        reset_count: int,
    ):
        self.id = id
        self.duration_seconds = duration_seconds
        self.remaining_seconds = remaining_seconds
        self.status = status
        self.started_at = started_at
        self.paused_at = paused_at
        self.reset_count = reset_count


class TimerRepo:
    """In-memory timer repository."""
    
    def __init__(self):
        self.timers = {}
        self.active_timer_id = None
    
    async def get_active_timer(self):
        """Get the currently active timer."""
        if self.active_timer_id is None:
            return None
        return self.timers.get(self.active_timer_id)
    
    async def create_timer(self, duration: int):
        """Create a new timer."""
        timer_id = len(self.timers) + 1
        timer = Timer(
            id=timer_id,
            duration_seconds=duration,
            remaining_seconds=duration,
            status="running",
            started_at=datetime.now(timezone.utc),
            paused_at=None,
            reset_count=0,
        )
        self.timers[timer_id] = timer
        self.active_timer_id = timer_id
        return timer
    
    async def update_timer(self, timer: Timer):
        """Update an existing timer."""
        self.timers[timer.id] = timer
        return timer


class TimerService:
    """Timer state machine: countdown logic, urgency calculation, transitions."""

    def __init__(self, repo: TimerRepo):
        self.repo = repo

    async def get_state(self) -> TimerState:
        """Fetch current timer state with live countdown calculation."""
        timer = await self.repo.get_active_timer()
        if not timer:
            return TimerState(
                countdown=0,
                duration=0,
                is_paused=False,
                is_expired=True,
                urgency_level="calm",
                colour_intensity=0.0,
                last_reset_at=None,
            )
        
        remaining = self._calc_remaining(timer)
        urgency_level, colour_intensity = self._calc_urgency(remaining, timer.duration_seconds)
        is_expired = remaining <= 0
        
        return TimerState(
            countdown=max(0, remaining),
            duration=timer.duration_seconds,
            is_paused=timer.status == "paused",
            is_expired=is_expired,
            urgency_level=urgency_level,
            colour_intensity=colour_intensity,
            last_reset_at=timer.started_at.isoformat() if timer.started_at else None,
        )

    async def configure(self, config: TimerConfig) -> TimerState:
        """Set timer duration and start countdown."""
        timer = await self.repo.create_timer(config.duration)
        urgency_level, colour_intensity = self._calc_urgency(config.duration, config.duration)
        
        return TimerState(
            countdown=config.duration,
            duration=config.duration,
            is_paused=False,
            is_expired=False,
            urgency_level=urgency_level,
            colour_intensity=colour_intensity,
            last_reset_at=timer.started_at.isoformat() if timer.started_at else None,
        )

    async def reset(self) -> TimerState:
        """Reset countdown to configured duration (fails if expired)."""
        timer = await self.repo.get_active_timer()
        if not timer:
            raise ValueError("No active timer found")
        
        remaining = self._calc_remaining(timer)
        if remaining <= 0:
            raise ValueError("Timer expired; reset not allowed until reconfigured")
        
        timer.remaining_seconds = timer.duration_seconds
        timer.paused_at = None
        timer.status = "running"
        timer.reset_count += 1
        timer.started_at = datetime.now(timezone.utc)
        
        updated = await self.repo.update_timer(timer)
        urgency_level, colour_intensity = self._calc_urgency(
            timer.duration_seconds, timer.duration_seconds
        )
        
        return TimerState(
            countdown=timer.duration_seconds,
            duration=timer.duration_seconds,
            is_paused=False,
            is_expired=False,
            urgency_level=urgency_level,
            colour_intensity=colour_intensity,
            last_reset_at=updated.started_at.isoformat() if updated.started_at else None,
        )

    async def pause(self) -> TimerState:
        """Pause active countdown."""
        timer = await self.repo.get_active_timer()
        if not timer:
            raise ValueError("No active timer found")
        
        remaining = self._calc_remaining(timer)
        timer.remaining_seconds = max(0, remaining)
        timer.paused_at = datetime.now(timezone.utc)
        timer.status = "paused"
        
        updated = await self.repo.update_timer(timer)
        urgency_level, colour_intensity = self._calc_urgency(timer.remaining_seconds, timer.duration_seconds)
        
        return TimerState(
            countdown=timer.remaining_seconds,
            duration=timer.duration_seconds,
            is_paused=True,
            is_expired=timer.remaining_seconds <= 0,
            urgency_level=urgency_level,
            colour_intensity=colour_intensity,
            last_reset_at=updated.started_at.isoformat() if updated.started_at else None,
        )

    async def resume(self) -> TimerState:
        """Resume paused countdown."""
        timer = await self.repo.get_active_timer()
        if not timer:
            raise ValueError("No active timer found")
        
        timer.paused_at = None
        timer.status = "running"
        timer.started_at = datetime.now(timezone.utc)
        
        updated = await self.repo.update_timer(timer)
        remaining = timer.remaining_seconds
        urgency_level, colour_intensity = self._calc_urgency(remaining, timer.duration_seconds)
        
        return TimerState(
            countdown=remaining,
            duration=timer.duration_seconds,
            is_paused=False,
            is_expired=remaining <= 0,
            urgency_level=urgency_level,
            colour_intensity=colour_intensity,
            last_reset_at=updated.started_at.isoformat() if updated.started_at else None,
        )

    async def get_urgency(self) -> UrgencyState:
        """Get real-time urgency state."""
        timer = await self.repo.get_active_timer()
        if not timer:
            return UrgencyState(
                urgency_level="calm",
                colour_intensity=0.0,
                remaining_percent=0.0,
                facial_expression="😐",
            )
        
        remaining = self._calc_remaining(timer)
        remaining = max(0, remaining)
        urgency_level, colour_intensity = self._calc_urgency(remaining, timer.duration_seconds)
        remaining_percent = remaining / timer.duration_seconds if timer.duration_seconds > 0 else 0.0
        remaining_percent = min(1.0, remaining_percent)
        
        facial_expr = "😐"
        if urgency_level == "calm":
            facial_expr = "😊"
        elif urgency_level == "anxious":
            facial_expr = "😰"
        elif urgency_level == "alarm":
            facial_expr = "😨"
        
        return UrgencyState(
            urgency_level=urgency_level,
            colour_intensity=colour_intensity,
            remaining_percent=remaining_percent,
            facial_expression=facial_expr,
        )

    @staticmethod
    def _calc_urgency(remaining: int, duration: int) -> tuple[str, float]:
        """Calculate urgency level and colour intensity from remaining/duration ratio."""
        if duration <= 0:
            return ("calm", 0.0)
        
        ratio = remaining / duration
        
        if ratio > 0.66:
            urgency = "calm"
            intensity = 0.2
        elif ratio > 0.33:
            urgency = "anxious"
            intensity = 0.65
        else:
            urgency = "alarm"
            intensity = 0.95
        
        return (urgency, intensity)

    @staticmethod
    def _calc_remaining(timer: Timer) -> int:
        """Compute live remaining_seconds accounting for elapsed wall-clock time."""
        if timer.status == "paused":
            return timer.remaining_seconds
        
        if not timer.started_at:
            return timer.remaining_seconds
        
        elapsed = (datetime.now(timezone.utc) - timer.started_at).total_seconds()
        remaining = timer.remaining_seconds - int(elapsed)
        
        return remaining
