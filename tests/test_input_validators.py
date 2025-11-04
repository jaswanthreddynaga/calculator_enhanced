"""Tests for input validation."""

import pytest
from app.input_validators import InputValidator
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError


class TestInputValidator:
    """Tests for InputValidator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = CalculatorConfig()
        self.validator = InputValidator(self.config)
    
    def test_validate_number_positive(self):
        """Test validating positive number."""
        assert self.validator.validate_number('5') == 5.0
    
    def test_validate_number_negative(self):
        """Test validating negative number."""
        assert self.validator.validate_number('-5') == -5.0
    
    def test_validate_number_decimal(self):
        """Test validating decimal number."""
        assert self.validator.validate_number('3.14') == 3.14
    
    def test_validate_number_invalid(self):
        """Test validating invalid number raises error."""
        with pytest.raises(ValidationError):
            self.validator.validate_number('abc')
    
    def test_validate_two_numbers(self):
        """Test validating two numbers."""
        a, b = self.validator.validate_two_numbers('5', '3')
        assert a == 5.0
        assert b == 3.0
    
    def test_validate_two_numbers_invalid_first(self):
        """Test validating two numbers with invalid first."""
        with pytest.raises(ValidationError):
            self.validator.validate_two_numbers('abc', '3')
    
    def test_validate_two_numbers_invalid_second(self):
        """Test validating two numbers with invalid second."""
        with pytest.raises(ValidationError):
            self.validator.validate_two_numbers('5', 'xyz')

