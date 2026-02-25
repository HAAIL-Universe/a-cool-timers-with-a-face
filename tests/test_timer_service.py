import pytest
from datetime import datetime, timezone, timedelta
from app.services.timer_service import TimerService, UrgencyState
from app.repos.timer_repo import TimerRepo


class TestUrgencyCalculation:
    """Test urgency level assignment based on remaining percentage."""

    def test_low_urgency_above_50_percent(self):
        """Urgency is 'low' when > 50% remains."""
        result = TimerService.calculate_urgency(60, 100)
        assert result.urgency_level == "low"
        assert result.remaining_percentage == 60.0

    def test_medium_urgency_25_to_50_percent(self):
        """Urgency is 'medium' when 25–50% remains."""
        result = TimerService.calculate_urgency(40, 100)
        assert result.urgency_level == "medium"
        result = TimerService.calculate_urgency(25, 100)
        assert result.urgency_level == "medium"

    def test_high_urgency_10_to_25_percent(self):
        """Urgency is 'high' when 10–25% remains."""
        result = TimerService.calculate_urgency(20, 100)
        assert result.urgency_level == "high"
        result = TimerService.calculate_urgency(10, 100)
        assert result.urgency_level == "high"

    def test_critical_urgency_below_10_percent(self):
        """Urgency is 'critical' when < 10% remains."""
        result = TimerService.calculate_urgency(5, 100)
        assert result.urgency_level == "critical"
        result = TimerService.calculate_urgency(0, 100)
        assert result.urgency_level == "critical"

    def test_boundary_50_percent_is_low(self):
        """At exactly 50%, urgency transitions to 'low'."""
        result = TimerService.calculate_urgency(50, 100)
        assert result.urgency_level == "low"

    def test_boundary_25_percent_is_medium(self):
        """At exactly 25%, urgency transitions to 'medium'."""
        result = TimerService.calculate_urgency(25, 100)
        assert result.urgency_level == "medium"

    def test_boundary_10_percent_is_high(self):
        """At exactly 10%, urgency transitions to 'high'."""
        result = TimerService.calculate_urgency(10, 100)
        assert result.urgency_level == "high"

    def test_remaining_percentage_clamped_0_to_100(self):
        """Remaining percentage is clamped to [0, 100]."""
        result = TimerService.calculate_urgency(-10, 100)
        assert result.remaining_percentage == 0.0
        result = TimerService.calculate_urgency(150, 100)
        assert result.remaining_percentage == 100.0

    def test_zero_initial_duration_edge_case(self):
        """With zero initial duration, percentage defaults to 0."""
        result = TimerService.calculate_urgency(0, 1)
        assert result.remaining_percentage == 0.0


class TestColourMapping:
    """Test colour intensity mapping for urgency levels."""

    def test_low_urgency_green(self):
        """Low urgency is bright green."""
        result = TimerService.calculate_urgency(80, 100)
        assert result.urgency_level == "low"
        assert result.colour_intensity["green"] == 255
        assert result.colour_intensity["red"] == 0

    def test_medium_urgency_yellow(self):
        """Medium urgency is yellow (red + green)."""
        result = TimerService.calculate_urgency(35, 100)
        assert result.urgency_level == "medium"
        assert result.colour_intensity["red"] == 255
        assert result.colour_intensity["green"] == 255

    def test_high_urgency_orange(self):
        """High urgency is orange (red + orange)."""
        result = TimerService.calculate_urgency(15, 100)
        assert result.urgency_level == "high"
        assert result.colour_intensity["red"] == 255
        assert result.colour_intensity["green"] == 165

    def test_critical_urgency_red(self):
        """Critical urgency is red."""
        result = TimerService.calculate_urgency(5, 100)
        assert result.urgency_level == "critical"
        assert result.colour_intensity["red"] == 255
        assert result.colour_intensity["green"] == 0
        assert result.colour_intensity["blue"] == 0

    def test_colour_values_in_valid_range(self):
        """All colour channels are in [0, 255]."""
        for remaining in [5, 10, 20, 40, 60, 80, 99]:
            result = TimerService.calculate_urgency(remaining, 100)
            for channel in ["red", "green", "blue"]:
                assert 0 <= result.colour_intensity[channel] <= 255

    def test_colour_intensity_varies_within_urgency(self):
        """Colour intensity increases as urgency increases within a level."""
        result_high_in_critical = TimerService.calculate_urgency(9, 100)
        result_low_in_critical = TimerService.calculate_urgency(1, 100)
        assert result_high_in_critical.colour_intensity["red"] >= result_low_in_critical.colour_intensity["red"]


class TestFacialExpressionMapping:
    """Test facial expression assignment to urgency levels."""

    def test_low_urgency_neutral(self):
        """Low urgency maps to 'neutral' expression."""
        result = TimerService.calculate_urgency(80, 100)
        assert result.facial_expression == "neutral"

    def test_medium_urgency_concerned(self):
        """Medium urgency maps to 'concerned' expression."""
        result = TimerService.calculate_urgency(35, 100)
        assert result.facial_expression == "concerned"

    def test_high_urgency_worried(self):
        """High urgency maps to 'worried' expression."""
        result = TimerService.calculate_urgency(15, 100)
        assert result.facial_expression == "worried"

    def test_critical_urgency_alarm(self):
        """Critical urgency maps to 'alarm' expression."""
        result = TimerService.calculate_urgency(5, 100)
        assert result.facial_expression == "alarm"


class TestResetLogic:
    """Test timer reset validation and remaining-time calculation."""

    def test_validate_reset_with_positive_time(self):
        """Timer can be reset when time remains."""
        assert TimerService.validate_reset(10) is True
        assert TimerService.validate_reset(1) is True

    def test_validate_reset_with_zero_time(self):
        """Timer cannot be reset at zero."""
        assert TimerService.validate_reset(0) is False

    def test_validate_reset_with_negative_time(self):
        """Timer cannot be reset with negative time."""
        assert TimerService.validate_reset(-5) is False

    def test_calculate_remaining_from_start(self):
        """Remaining time decreases from start time."""
        now = datetime.now(timezone.utc)
        past = now - timedelta(seconds=30)
        remaining = TimerService.calculate_remaining(100, past)
        assert 25 <= remaining <= 31  # ~30 seconds elapsed, account for execution time

    def test_calculate_remaining_after_reset(self):
        """Reset time overrides start time."""
        now = datetime.now(timezone.utc)
        long_ago = now - timedelta(seconds=100)
        recent = now - timedelta(seconds=5)
        remaining = TimerService.calculate_remaining(100, long_ago, recent)
        assert 0 <= remaining <= 6  # ~5 seconds elapsed since reset

    def test_calculate_remaining_clamped_to_zero(self):
        """Remaining time cannot go below zero."""
        now = datetime.now(timezone.utc)
        far_past = now - timedelta(seconds=200)
        remaining = TimerService.calculate_remaining(100, far_past)
        assert remaining == 0

    def test_calculate_remaining_fresh_timer(self):
        """Fresh timer has full duration remaining."""
        now = datetime.now(timezone.utc)
        remaining = TimerService.calculate_remaining(100, now)
        assert 99 <= remaining <= 100


class TestExpiryDetection:
    """Test timer expiry state detection."""

    def test_is_expired_when_zero(self):
        """Timer is expired when remaining is zero."""
        assert TimerService.is_expired(0) is True

    def test_is_expired_when_negative(self):
        """Timer is expired when remaining is negative."""
        assert TimerService.is_expired(-5) is True

    def test_not_expired_when_positive(self):
        """Timer is not expired when remaining is positive."""
        assert TimerService.is_expired(10) is False
        assert TimerService.is_expired(1) is False

    def test_urgency_state_returned(self):
        """calculate_urgency returns a valid UrgencyState object."""
        result = TimerService.calculate_urgency(50, 100)
        assert isinstance(result, UrgencyState)
        assert hasattr(result, "urgency_level")
        assert hasattr(result, "colour_intensity")
        assert hasattr(result, "facial_expression")
        assert hasattr(result, "remaining_percentage")


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_very_long_duration(self):
        """Service handles very long durations (e.g., 24 hours)."""
        result = TimerService.calculate_urgency(43200, 86400)  # 12h / 24h
        assert result.urgency_level == "low"
        assert 49 <= result.remaining_percentage <= 51

    def test_very_short_duration(self):
        """Service handles very short durations (e.g., 1 second)."""
        result = TimerService.calculate_urgency(0, 1)
        assert result.urgency_level == "critical"
        assert result.remaining_percentage == 0.0

    def test_fractional_seconds_rounded(self):
        """Fractional seconds are handled without error."""
        result = TimerService.calculate_urgency(33, 100)
        assert 32 <= result.remaining_percentage <= 34

    def test_multiple_calls_independent(self):
        """Multiple calls to calculate_urgency are independent."""
        result1 = TimerService.calculate_urgency(80, 100)
        result2 = TimerService.calculate_urgency(20, 100)
        assert result1.urgency_level != result2.urgency_level
        assert result1.facial_expression != result2.facial_expression
