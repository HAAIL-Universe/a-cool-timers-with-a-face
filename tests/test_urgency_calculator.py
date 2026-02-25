"""Parametrized tests for urgency calculation and RGB colour interpolation."""

import pytest
from app.services.urgency_calculator import (
    calculate_urgency_level,
    interpolate_rgb,
    URGENCY_THRESHOLDS,
    COLOUR_MAP,
)


class TestCalculateUrgencyLevel:
    """Tests for calculate_urgency_level() boundary conditions."""

    @pytest.mark.parametrize(
        "elapsed,total,expected",
        [
            (0, 100, "low"),
            (10, 100, "low"),
            (24, 100, "low"),
            (26, 100, "medium"),
            (50, 100, "medium"),
            (74, 100, "medium"),
            (76, 100, "high"),
            (100, 100, "high"),
            (124, 100, "critical"),
            (150, 100, "critical"),
        ],
        ids=[
            "0% elapsed → low",
            "10% elapsed → low",
            "24% elapsed → low (edge)",
            "26% elapsed → medium (cross 25% threshold)",
            "50% elapsed → medium",
            "74% elapsed → medium (edge)",
            "76% elapsed → high (cross 50% threshold)",
            "100% elapsed → high",
            "124% elapsed → critical (cross 75% threshold)",
            "150% elapsed → critical (overspent)",
        ],
    )
    def test_urgency_by_elapsed_percentage(self, elapsed, total, expected):
        """Verify urgency level matches remaining time percentage thresholds."""
        result = calculate_urgency_level(elapsed, total)
        assert result == expected

    @pytest.mark.parametrize(
        "elapsed,total,expected",
        [
            (0, 30, "low"),
            (7, 30, "low"),
            (8, 30, "medium"),
            (15, 30, "medium"),
            (22, 30, "high"),
            (29, 30, "critical"),
            (30, 30, "critical"),
        ],
        ids=[
            "30s timer: 30s remaining → low",
            "30s timer: 23s remaining → low",
            "30s timer: 22s remaining → medium (75% threshold)",
            "30s timer: 15s remaining → medium",
            "30s timer: 8s remaining → high (50% threshold)",
            "30s timer: 1s remaining → critical (25% threshold)",
            "30s timer: 0s remaining → critical",
        ],
    )
    def test_urgency_30s_countdown(self, elapsed, total, expected):
        """Realistic 30-second countdown scenarios."""
        result = calculate_urgency_level(elapsed, total)
        assert result == expected

    @pytest.mark.parametrize(
        "remaining,total,expected",
        [
            (100, 100, "low"),
            (76, 100, "low"),
            (75, 100, "low"),
            (74, 100, "medium"),
            (51, 100, "medium"),
            (50, 100, "medium"),
            (49, 100, "high"),
            (26, 100, "high"),
            (25, 100, "high"),
            (24, 100, "critical"),
            (1, 100, "critical"),
            (0, 100, "critical"),
        ],
        ids=[
            "100% remaining → low",
            "76% remaining → low",
            "75% remaining → low (on boundary)",
            "74% remaining → medium",
            "51% remaining → medium",
            "50% remaining → medium (on boundary)",
            "49% remaining → high",
            "26% remaining → high",
            "25% remaining → high (on boundary)",
            "24% remaining → critical",
            "1% remaining → critical",
            "0% remaining → critical",
        ],
    )
    def test_urgency_boundary_values(self, remaining, total, expected):
        """Test exact boundary thresholds for all transitions."""
        elapsed = total - remaining
        result = calculate_urgency_level(elapsed, total)
        assert result == expected

    @pytest.mark.parametrize(
        "elapsed,total",
        [
            (0, 0),
            (5, 0),
            (100, 0),
        ],
        ids=[
            "zero duration, zero elapsed",
            "zero duration, positive elapsed",
            "zero duration, large elapsed",
        ],
    )
    def test_zero_duration_always_critical(self, elapsed, total):
        """Edge case: zero or negative total duration always returns critical."""
        result = calculate_urgency_level(elapsed, total)
        assert result == "critical"

    @pytest.mark.parametrize(
        "elapsed,total",
        [
            (0, 1),
            (0, 60),
            (0, 120),
        ],
        ids=[
            "1-second timer, just started",
            "60-second timer, just started",
            "120-second timer, just started",
        ],
    )
    def test_timer_just_started(self, elapsed, total):
        """At elapsed=0, all timers are in low urgency."""
        result = calculate_urgency_level(elapsed, total)
        assert result == "low"

    @pytest.mark.parametrize(
        "elapsed,total",
        [
            (1, 1),
            (60, 60),
            (120, 120),
        ],
        ids=[
            "1-second timer expired",
            "60-second timer expired",
            "120-second timer expired",
        ],
    )
    def test_timer_fully_expired(self, elapsed, total):
        """When elapsed >= total, urgency is critical."""
        result = calculate_urgency_level(elapsed, total)
        assert result == "critical"

    @pytest.mark.parametrize(
        "elapsed,total",
        [
            (-5, 100),
            (0, -50),
            (-10, -50),
        ],
        ids=[
            "negative elapsed (before start)",
            "negative total (invalid)",
            "both negative",
        ],
    )
    def test_negative_values(self, elapsed, total):
        """Negative elapsed is clamped to 0; negative total returns critical."""
        result = calculate_urgency_level(elapsed, total)
        if total <= 0:
            assert result == "critical"
        else:
            assert result == "low"


class TestInterpolateRgb:
    """Tests for interpolate_rgb() colour output."""

    @pytest.mark.parametrize(
        "urgency_level,expected_hex",
        [
            ("low", "#00ff00"),
            ("medium", "#ffff00"),
            ("high", "#ffa500"),
            ("critical", "#ff0000"),
        ],
        ids=[
            "low → green",
            "medium → yellow",
            "high → orange",
            "critical → red",
        ],
    )
    def test_urgency_to_hex_colour(self, urgency_level, expected_hex):
        """Verify each urgency level maps to correct hex colour."""
        result = interpolate_rgb(urgency_level)
        assert result == expected_hex

    @pytest.mark.parametrize(
        "urgency_level",
        ["low", "medium", "high", "critical"],
        ids=["low", "medium", "high", "critical"],
    )
    def test_hex_format_valid(self, urgency_level):
        """All urgency levels produce valid #RRGGBB hex format."""
        result = interpolate_rgb(urgency_level)
        assert result.startswith("#")
        assert len(result) == 7
        assert all(c in "0123456789abcdef" for c in result[1:])

    @pytest.mark.parametrize(
        "invalid_level",
        ["unknown", "CRITICAL", "LOW", "", "urgency", None],
        ids=[
            "unknown level",
            "uppercase critical",
            "uppercase low",
            "empty string",
            "partial match",
            "None",
        ],
    )
    def test_invalid_urgency_level_fallback_to_green(self, invalid_level):
        """Invalid urgency levels default to green (low)."""
        result = interpolate_rgb(invalid_level)
        assert result == "#00ff00"

    @pytest.mark.parametrize(
        "urgency_level,rgb_tuple",
        [
            ("low", (0, 255, 0)),
            ("medium", (255, 255, 0)),
            ("high", (255, 165, 0)),
            ("critical", (255, 0, 0)),
        ],
        ids=["low", "medium", "high", "critical"],
    )
    def test_rgb_values_from_colour_map(self, urgency_level, rgb_tuple):
        """Verify interpolate_rgb matches COLOUR_MAP values."""
        expected_hex = f"#{rgb_tuple[0]:02x}{rgb_tuple[1]:02x}{rgb_tuple[2]:02x}"
        result = interpolate_rgb(urgency_level)
        assert result == expected_hex
        assert result == interpolate_rgb(urgency_level)


class TestColourMapIntegrity:
    """Tests for COLOUR_MAP and URGENCY_THRESHOLDS constants."""

    def test_all_urgency_levels_have_colours(self):
        """Every urgency level in URGENCY_THRESHOLDS has a colour."""
        for level in URGENCY_THRESHOLDS:
            assert level in COLOUR_MAP, f"No colour defined for '{level}'"

    def test_all_colours_have_urgency_levels(self):
        """Every colour in COLOUR_MAP has a threshold."""
        for level in COLOUR_MAP:
            assert level in URGENCY_THRESHOLDS, f"No threshold defined for '{level}'"

    def test_thresholds_ordered_descending(self):
        """Thresholds are ordered from critical to low (0.25 → 1.0)."""
        thresholds = [
            URGENCY_THRESHOLDS["critical"],
            URGENCY_THRESHOLDS["high"],
            URGENCY_THRESHOLDS["medium"],
            URGENCY_THRESHOLDS["low"],
        ]
        assert thresholds == sorted(thresholds)

    @pytest.mark.parametrize(
        "level,threshold",
        [
            ("critical", 0.25),
            ("high", 0.50),
            ("medium", 0.75),
            ("low", 1.00),
        ],
        ids=["critical=25%", "high=50%", "medium=75%", "low=100%"],
    )
    def test_threshold_values(self, level, threshold):
        """Verify exact threshold percentages."""
        assert URGENCY_THRESHOLDS[level] == threshold

    @pytest.mark.parametrize(
        "level,rgb",
        [
            ("low", (0, 255, 0)),
            ("medium", (255, 255, 0)),
            ("high", (255, 165, 0)),
            ("critical", (255, 0, 0)),
        ],
        ids=["low=green", "medium=yellow", "high=orange", "critical=red"],
    )
    def test_colour_rgb_values(self, level, rgb):
        """Verify exact RGB tuples."""
        assert COLOUR_MAP[level] == rgb


class TestEndToEndUrgency:
    """Integration tests: urgency level → colour output."""

    @pytest.mark.parametrize(
        "elapsed,total,expected_level,expected_hex",
        [
            (0, 100, "low", "#00ff00"),
            (50, 100, "medium", "#ffff00"),
            (76, 100, "high", "#ffa500"),
            (125, 100, "critical", "#ff0000"),
        ],
        ids=[
            "low → green",
            "medium → yellow",
            "high → orange",
            "critical → red",
        ],
    )
    def test_elapsed_to_colour_pipeline(
        self, elapsed, total, expected_level, expected_hex
    ):
        """Full pipeline: elapsed time → urgency level → hex colour."""
        level = calculate_urgency_level(elapsed, total)
        colour = interpolate_rgb(level)
        assert level == expected_level
        assert colour == expected_hex

    @pytest.mark.parametrize(
        "timer_duration,remaining_seconds,expected_level",
        [
            (30, 30, "low"),
            (30, 23, "low"),
            (30, 22, "medium"),
            (30, 15, "medium"),
            (30, 8, "high"),
            (30, 3, "critical"),
            (60, 60, "low"),
            (60, 45, "low"),
            (60, 44, "medium"),
            (60, 31, "medium"),
            (60, 30, "high"),
            (60, 15, "high"),
            (60, 6, "critical"),
        ],
        ids=[
            "30s: 100% remaining",
            "30s: 77% remaining (low)",
            "30s: 73% remaining (medium)",
            "30s: 50% remaining (medium)",
            "30s: 27% remaining (high)",
            "30s: 10% remaining (critical)",
            "60s: 100% remaining",
            "60s: 75% remaining (low)",
            "60s: 73% remaining (medium)",
            "60s: 52% remaining (medium)",
            "60s: 50% remaining (high)",
            "60s: 25% remaining (high)",
            "60s: 10% remaining (critical)",
        ],
    )
    def test_realistic_countdown_scenarios(
        self, timer_duration, remaining_seconds, expected_level
    ):
        """Realistic timer countdown scenarios for 30s and 60s presets."""
        elapsed = timer_duration - remaining_seconds
        result = calculate_urgency_level(elapsed, timer_duration)
        assert result == expected_level
