"""Additional integration tests."""

import pytest
from app.calculator import Calculator
from app.calculation import Calculation
from app.history import HistoryManager
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError


class TestIntegration:
    """Integration tests for calculator components."""
    
    def test_calculator_perform_calculation(self):
        """Test performing a calculation through calculator."""
        calculator = Calculator()
        result = calculator._perform_calculation('add', '5', '3')
        assert result == 8.0
    
    def test_calculator_perform_calculation_error(self):
        """Test calculation with error handling."""
        calculator = Calculator()
        with pytest.raises((OperationError, ValidationError)):
            calculator._perform_calculation('divide', '5', '0')
    
    def test_calculator_notify_observers(self):
        """Test observer notification."""
        calculator = Calculator()
        calc = Calculation('add', 5, 3, 8)
        # Should not raise any exceptions
        calculator._notify_observers(calc)
    
    def test_calculator_all_commands(self):
        """Test all calculator commands."""
        calculator = Calculator()
        
        # Test all operation commands
        operations = [
            'add', 'subtract', 'multiply', 'divide',
            'power', 'root', 'modulus', 'int_divide',
            'percent', 'abs_diff'
        ]
        
        for op in operations:
            if op == 'divide':
                result = calculator._process_command(f'{op} 10 2')
            elif op == 'root':
                result = calculator._process_command(f'{op} 16 2')
            elif op == 'modulus':
                result = calculator._process_command(f'{op} 10 3')
            elif op == 'percent':
                result = calculator._process_command(f'{op} 25 100')
            else:
                result = calculator._process_command(f'{op} 5 3')
            assert result is not None
