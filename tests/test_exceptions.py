"""Tests for exceptions."""

import pytest
from app.exceptions import (
    CalculatorError,
    OperationError,
    ValidationError,
    HistoryError,
    ConfigurationError
)


class TestExceptions:
    """Tests for custom exceptions."""
    
    def test_calculator_error(self):
        """Test CalculatorError base exception."""
        with pytest.raises(CalculatorError):
            raise CalculatorError("Test error")
    
    def test_operation_error(self):
        """Test OperationError exception."""
        with pytest.raises(OperationError):
            raise OperationError("Operation failed")
    
    def test_validation_error(self):
        """Test ValidationError exception."""
        with pytest.raises(ValidationError):
            raise ValidationError("Validation failed")
    
    def test_history_error(self):
        """Test HistoryError exception."""
        with pytest.raises(HistoryError):
            raise HistoryError("History error")
    
    def test_configuration_error(self):
        """Test ConfigurationError exception."""
        with pytest.raises(ConfigurationError):
            raise ConfigurationError("Configuration error")

