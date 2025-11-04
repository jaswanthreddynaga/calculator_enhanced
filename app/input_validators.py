"""Input validation utilities for the calculator."""

from app.exceptions import ValidationError
from app.calculator_config import CalculatorConfig


class InputValidator:
    """Validates user inputs for calculator operations."""
    
    def __init__(self, config: CalculatorConfig):
        """Initialize validator with configuration."""
        self.config = config
    
    def validate_number(self, value: str) -> float:
        """
        Validate and convert a string to a number.
        
        Args:
            value: String representation of a number
            
        Returns:
            Validated float value
            
        Raises:
            ValidationError: If value is not a valid number or exceeds limits
        """
        try:
            num = float(value)
        except ValueError:
            raise ValidationError(f"'{value}' is not a valid number")
        
        if abs(num) > self.config.max_input_value:
            raise ValidationError(
                f"Input value {num} exceeds maximum allowed value "
                f"{self.config.max_input_value}"
            )
        
        return num
    
    def validate_two_numbers(self, a_str: str, b_str: str) -> tuple[float, float]:
        """
        Validate two input numbers.
        
        Args:
            a_str: First number as string
            b_str: Second number as string
            
        Returns:
            Tuple of validated float values
            
        Raises:
            ValidationError: If either value is invalid
        """
        a = self.validate_number(a_str)
        b = self.validate_number(b_str)
        return a, b

