import pytest
from datetime import datetime
from uuid import uuid4
from unittest.mock import Mock, MagicMock

from app.models.timer import Timer
from app.services.timer_service import TimerService
from app.schemas.timer import UrgencyLevel, TimerStatus


@pytest.fixture
def mock_repo():
    """Create a mock TimerRepo."""
    return Mock()


@pytest.fixture
def timer_service(mock_repo):
    """Create TimerService with mocked repo."""
    return TimerService(mock_repo)


@pytest.fixture
def sample_timer():
    """Create a sample timer for testing."""
    return Timer(
        id=uuid4(),
        name="Test Timer",
        duration_seconds=60,
        remaining_seconds=60,
        started_at=None,
        paused_at=None,
        reset_count=0,
        status=TimerStatus.stopped,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


class TestTimerServiceCreate:
    """Tests for timer creation."""

    def test_create_timer(self, timer_service, mock_repo, sample_timer):
        """Test creating a new timer."""
        mock_repo.create_timer.return_value = sample_timer

        result = timer_service.create_timer(60, "Workout")

        assert result.id == sample_timer.id
        assert result.duration_seconds == 60
        assert result.remaining_seconds == 60
        mock_repo.create_timer.assert_called_once_with(60, "Workout")

    def test_create_timer_default_name(self, timer_service, mock_repo, sample_timer):
        """Test creating timer with default name."""
        mock_repo.create_timer.return_value = sample_timer

        timer_service.create_timer(45)

        mock_repo.create_timer.assert_called_once_with(45, "Workout")


class TestTimerServiceGet:
    """Tests for fetching timers."""

    def test_get_timer_exists(self, timer_service, mock_repo, sample_timer):
        """Test fetching existing timer."""
        mock_repo.get_timer.return_value = sample_timer

        result = timer_service.get_timer(sample_timer.id)

        assert result.id == sample_timer.id
        mock_repo.get_timer.assert_called_once_with(sample_timer.id)

    def test_get_timer_not_found(self, timer_service, mock_repo):
        """Test fetching non-existent timer."""
        timer_id = uuid4()
        mock_repo.get_timer.return_value = None

        result = timer_service.get_timer(timer_id)

        assert result is None


class TestTimerServiceStart:
    """Tests for starting timers."""

    def test_start_timer(self, timer_service, mock_repo, sample_timer):
        """Test starting a timer."""
        mock_repo.get_timer.return_value = sample_timer
        started_timer = Timer(
            id=sample_timer.id,
            name=sample_timer.name,
            duration_seconds=60,
            remaining_seconds=60,
            started_at=datetime.utcnow(),
            paused_at=None,
            reset_count=0,
            status=TimerStatus.running,
            created_at=sample_timer.created_at,
            updated_at=datetime.utcnow(),
        )
        mock_repo.update_timer.return_value = started_timer

        result = timer_service.start_timer(sample_timer.id)

        assert result.status == TimerStatus.running
        assert result.started_at is not None
        assert result.paused_at is None
        mock_repo.record_event.assert_called_once()

    def test_start_nonexistent_timer(self, timer_service, mock_repo):
        """Test starting non-existent timer."""
        timer_id = uuid4()
        mock_repo.get_timer.return_value = None

        result = timer_service.start_timer(timer_id)

        assert result is None
        mock_repo.update_timer.assert_not_called()


class TestTimerServicePause:
    """Tests for pausing timers."""

    def test_pause_timer(self, timer_service, mock_repo, sample_timer):
        """Test pausing a running timer."""
        running_timer = Timer(
            id=sample_timer.id,
            name=sample_timer.name,
            duration_seconds=60,
            remaining_seconds=45,
            started_at=datetime.utcnow(),
            paused_at=None,
            reset_count=0,
            status=TimerStatus.running,
            created_at=sample_timer.created_at,
            updated_at=datetime.utcnow(),
        )
        mock_repo.get_timer.return_value = running_timer
        paused_timer = Timer(
            id=running_timer.id,
            name=running_timer.name,
            duration_seconds=60,
            remaining_seconds=45,
            started_at=running_timer.started_at,
            paused_at=datetime.utcnow(),
            reset_count=0,
            status=TimerStatus.paused,
            created_at=running_timer.created_at,
            updated_at=datetime.utcnow(),
        )
        mock_repo.update_timer.return_value = paused_timer

        result = timer_service.pause_timer(running_timer.id)

        assert result.status == TimerStatus.paused
        assert result.paused_at is not None
        mock_repo.record_event.assert_called_once()


class TestTimerServiceReset:
    """Tests for resetting timers."""

    def test_reset_timer_to_original_duration(self, timer_service, mock_repo, sample_timer):
        """Test resetting timer to original duration."""
        running_timer = Timer(
            id=sample_timer.id,
            name=sample_timer.name,
            duration_seconds=60,
            remaining_seconds=30,
            started_at=datetime.utcnow(),
            paused_at=None,
            reset_count=0,
            status=TimerStatus.running,
            created_at=sample_timer.created_at,
            updated_at=datetime.utcnow(),
        )
        mock_repo.get_timer.return_value = running_timer
        reset_timer = Timer(
            id=running_timer.id,
            name=running_timer.name,
            duration_seconds=60,
            remaining_seconds=60,
            started_at=None,
            paused_at=None,
            reset_count=1,
            status=TimerStatus.stopped,
            created_at=running_timer.created_at,
            updated_at=datetime.utcnow(),
        )
        mock_repo.update_timer.return_value = reset_timer

        result = timer_service.reset_timer(running_timer.id)

        assert result.remaining_seconds == 60
        assert result.status == TimerStatus.stopped
        assert result.reset_count == 1
        mock_repo.record_event.assert_called_once()

    def test_reset_timer_to_new_duration(self, timer_service, mock_repo, sample_timer):
        """Test resetting timer to new duration."""
        mock_repo.get_timer.return_value = sample_timer
        reset_timer = Timer(
            id=sample_timer.id,
            name=sample_timer.name,
            duration_seconds=90,
            remaining_seconds=90,
            started_at=None,
            paused_at=None,
            reset_count=1,
            status=TimerStatus.stopped,
            created_at=sample_timer.created_at,
            updated_at=datetime.utcnow(),
        )
        mock_repo.update_timer.return_value = reset_timer

        result = timer_service.reset_timer(sample_timer.id, 90)

        assert result.remaining_seconds == 90
        assert result.duration_seconds == 90


class TestTimerServiceTick:
    """Tests for timer countdown ticks."""

    def test_tick_timer_running(self, timer_service, mock_repo, sample_timer):
        """Test ticking a running timer."""
        running_timer = Timer(
            id=sample_timer.id,
            name=sample_timer.name,
            duration_seconds=60,
            remaining_seconds=30,
            started_at=datetime.utcnow(),
            paused_at=None,
            reset_count=0,
            status=TimerStatus.running,
            created_at=sample_timer.created_at,
            updated_at=datetime.utcnow(),
        )
        mock_repo.get_timer.return_value = running_timer
        ticked_timer = Timer(
            id=running_timer.id,
            name=running_timer.name,
            duration_seconds=60,
            remaining_seconds=29,
            started_at=running_timer.started_at,
            paused_at=None,
            reset_count=0,
            status=TimerStatus.running,
            created_at=running_timer.created_at,
            updated_at=datetime.utcnow(),
        )
        mock_repo.update_timer.return_value = ticked_timer

        result = timer_service.tick_timer(running_timer.id)

        assert result.remaining_seconds == 29
        assert result.status == TimerStatus.running
        mock_repo.record_event.assert_not_called()

    def test_tick_timer_to_expiry(self, timer_service, mock_repo, sample_timer):
        """Test ticking timer to zero."""
        running_timer = Timer(
            id=sample_timer.id,
            name=sample_timer.name,
            duration_seconds=60,
            remaining_seconds=1,
            started_at=datetime.utcnow(),
            paused_at=None,
            reset_count=0,
            status=TimerStatus.running,
            created_at=sample_timer.created_at,
            updated_at=datetime.utcnow(),
        )
        mock_repo.get_timer.return_value = running_timer
        expired_timer = Timer(
            id=running_timer.id,
            name=running_timer.name,
            duration_seconds=60,
            remaining_seconds=0,
            started_at=running_timer.started_at,
            paused_at=None,
            reset_count=0,
            status=TimerStatus.expired,
            created_at=running_timer.created_at,
            updated_at=datetime.utcnow(),
        )
        mock_repo.update_timer.return_value = expired_timer

        result = timer_service.tick_timer(running_timer.id)

        assert result.remaining_seconds == 0
        assert result.status == TimerStatus.expired
        mock_repo.record_event.assert_called_once()

    def test_tick_paused_timer_no_change(self, timer_service, mock_repo, sample_timer):
        """Test ticking paused timer does nothing."""
        paused_timer = Timer(
            id=sample_timer.id,
            name=sample_timer.name,
            duration_seconds=60,
            remaining_seconds=30,
            started_at=None,
            paused_at=datetime.utcnow(),
            reset_count=0,
            status=TimerStatus.paused,
            created_at=sample_timer.created_at,
            updated_at=datetime.utcnow(),
        )
        mock_repo.get_timer.return_value = paused_timer

        result = timer_service.tick_timer(paused_timer.id)

        assert result == paused_timer
        mock_repo.update_timer.assert_not_called()


class TestTimerServiceUrgency:
    """Tests for urgency calculation."""

    def test_urgency_calm(self, timer_service):
        """Test calm urgency when >50% time remains."""
        timer = Timer(
            id=uuid4(),
            name="Test",
            duration_seconds=100,
            remaining_seconds=60,
            started_at=None,
            paused_at=None,
            reset_count=0,
            status=TimerStatus.running,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        urgency = timer_service._calculate_urgency(timer)

        assert urgency == UrgencyLevel.calm

    def test_urgency_elevated(self, timer_service):
        """Test elevated urgency when 25-50% time remains."""
        timer = Timer(
            id=uuid4(),
            name="Test",
            duration_seconds=100,
            remaining_seconds=40,
            started_at=None,
            paused_at=None,
            reset_count=0,
            status=TimerStatus.running,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        urgency = timer_service._calculate_urgency(timer)

        assert urgency == UrgencyLevel.elevated

    def test_urgency_anxious(self, timer_service):
        """Test anxious urgency when 0-25% time remains."""
        timer = Timer(
            id=uuid4(),
            name="Test",
            duration_seconds=100,
            remaining_seconds=15,
            started_at=None,
            paused_at=None,
            reset_count=0,
            status=TimerStatus.running,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        urgency = timer_service._calculate_urgency(timer)

        assert urgency == UrgencyLevel.anxious

    def test_urgency_alarm(self, timer_service):
        """Test alarm urgency when expired."""
        timer = Timer(
            id=uuid4(),
            name="Test",
            duration_seconds=100,
            remaining_seconds=0,
            started_at=None,
            paused_at=None,
            reset_count=0,
            status=TimerStatus.expired,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        urgency = timer_service._calculate_urgency(timer)

        assert urgency == UrgencyLevel.alarm

    def test_calculate_urgency_response(self, timer_service):
        """Test visual urgency response calculation."""
        timer = Timer(
            id=uuid4(),
            name="Test",
            duration_seconds=100,
            remaining_seconds=30,
            started_at=None,
            paused_at=None,
            reset_count=0,
            status=TimerStatus.running,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        response = timer_service.calculate_urgency_response(timer)

        assert "level" in response
        assert "colour_intensity" in response
        assert "facial_expression" in response
        assert response["colour_intensity"] == 0.7
        assert isinstance(response["facial_expression"], str)
