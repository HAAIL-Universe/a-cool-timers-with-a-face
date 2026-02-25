import pytest
from app.services.urgency_calculator import (
    calculate_urgency_level,
    calculate_colour_intensity,
    calculate_facial_expression,
    UrgencyLevel,
    FacialExpression,
)


class TestUrgencyLevel:
    """Test urgency level calculation based on remaining time percentage."""

    def test_low_urgency_above_75_percent(self):
        """Remaining time > 75% should be low urgency."""
        assert calculate_urgency_level(100, 80) == UrgencyLevel.LOW

    def test_medium_urgency_50_to_75_percent(self):
        """Remaining time 50-75% should be medium urgency."""
        assert calculate_urgency_level(100, 75) == UrgencyLevel.MEDIUM
        assert calculate_urgency_level(100, 60) == UrgencyLevel.MEDIUM

    def test_high_urgency_25_to_50_percent(self):
        """Remaining time 25-50% should be high urgency."""
        assert calculate_urgency_level(100, 50) == UrgencyLevel.HIGH
        assert calculate_urgency_level(100, 30) == UrgencyLevel.HIGH

    def test_critical_urgency_below_25_percent(self):
        """Remaining time < 25% should be critical urgency."""
        assert calculate_urgency_level(100, 24) == UrgencyLevel.CRITICAL
        assert calculate_urgency_level(100, 1) == UrgencyLevel.CRITICAL

    def test_zero_remaining_time(self):
        """Zero remaining time should be critical urgency."""
        assert calculate_urgency_level(100, 0) == UrgencyLevel.CRITICAL


class TestColourIntensity:
    """Test colour intensity calculation based on urgency level."""

    def test_low_urgency_green(self):
        """Low urgency should be bright green, minimal red/blue."""
        colour = calculate_colour_intensity(UrgencyLevel.LOW)
        assert colour["green"] == 255
        assert colour["red"] < 100
        assert colour["blue"] < 100

    def test_medium_urgency_yellow(self):
        """Medium urgency should transition to yellow (high green and red)."""
        colour = calculate_colour_intensity(UrgencyLevel.MEDIUM)
        assert colour["red"] > 150
        assert colour["green"] > 150
        assert colour["blue"] < 100

    def test_high_urgency_orange(self):
        """High urgency should be orange (high red and green, low blue)."""
        colour = calculate_colour_intensity(UrgencyLevel.HIGH)
        assert colour["red"] > 200
        assert colour["green"] > 100
        assert colour["blue"] < 100

    def test_critical_urgency_red(self):
        """Critical urgency should be bright red."""
        colour = calculate_colour_intensity(UrgencyLevel.CRITICAL)
        assert colour["red"] == 255
        assert colour["green"] < 100
        assert colour["blue"] < 100

    def test_colour_values_in_range(self):
        """All colour values should be in valid 0-255 range."""
        for urgency in UrgencyLevel:
            colour = calculate_colour_intensity(urgency)
            assert 0 <= colour["red"] <= 255
            assert 0 <= colour["green"] <= 255
            assert 0 <= colour["blue"] <= 255


class TestFacialExpression:
    """Test facial expression mapping to urgency levels."""

    def test_low_urgency_neutral_face(self):
        """Low urgency should show neutral 8-bit face."""
        expr = calculate_facial_expression(UrgencyLevel.LOW)
        assert expr == FacialExpression.NEUTRAL

    def test_medium_urgency_concerned_face(self):
        """Medium urgency should show concerned expression."""
        expr = calculate_facial_expression(UrgencyLevel.MEDIUM)
        assert expr == FacialExpression.CONCERNED

    def test_high_urgency_worried_face(self):
        """High urgency should show worried expression."""
        expr = calculate_facial_expression(UrgencyLevel.HIGH)
        assert expr == FacialExpression.WORRIED

    def test_critical_urgency_alarm_face(self):
        """Critical urgency should show alarm expression."""
        expr = calculate_facial_expression(UrgencyLevel.CRITICAL)
        assert expr == FacialExpression.ALARM


class TestIntegration:
    """Integration tests for urgency feedback system."""

    def test_full_urgency_feedback_chain_high_time(self):
        """Full chain: 100s remaining (90%) → green, neutral."""
        urgency = calculate_urgency_level(100, 90)
        colour = calculate_colour_intensity(urgency)
        expression = calculate_facial_expression(urgency)
        
        assert urgency == UrgencyLevel.LOW
        assert colour["green"] == 255
        assert expression == FacialExpression.NEUTRAL

    def test_full_urgency_feedback_chain_medium_time(self):
        """Full chain: 100s remaining (60%) → yellow, concerned."""
        urgency = calculate_urgency_level(100, 60)
        colour = calculate_colour_intensity(urgency)
        expression = calculate_facial_expression(urgency)
        
        assert urgency == UrgencyLevel.MEDIUM
        assert colour["red"] > 150
        assert colour["green"] > 150
        assert expression == FacialExpression.CONCERNED

    def test_full_urgency_feedback_chain_low_time(self):
        """Full chain: 100s remaining (10%) → red, alarm."""
        urgency = calculate_urgency_level(100, 10)
        colour = calculate_colour_intensity(urgency)
        expression = calculate_facial_expression(urgency)
        
        assert urgency == UrgencyLevel.CRITICAL
        assert colour["red"] == 255
        assert expression == FacialExpression.ALARM
    
    def test_percentage_calculation_accuracy(self):
        """Test that percentage thresholds are calculated correctly."""
        # Test boundary: 75% (100 * 0.75 = 75)
        assert calculate_urgency_level(100, 76) == UrgencyLevel.LOW
        assert calculate_urgency_level(100, 75) == UrgencyLevel.MEDIUM
        
        # Test boundary: 50% (100 * 0.50 = 50)
        assert calculate_urgency_level(100, 51) == UrgencyLevel.MEDIUM
        assert calculate_urgency_level(100, 50) == UrgencyLevel.HIGH
        
        # Test boundary: 25% (100 * 0.25 = 25)
        assert calculate_urgency_level(100, 26) == UrgencyLevel.HIGH
        assert calculate_urgency_level(100, 25) == UrgencyLevel.CRITICAL
