"""Tests for calculator main class."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from app.calculator import Calculator
from app.calculation import Calculation


class TestCalculator:
    """Tests for Calculator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        with patch('app.calculator.CalculatorConfig'):
            with patch('app.calculator.InputValidator'):
                with patch('app.calculator.HistoryManager'):
                    with patch('app.calculator.Logger'):
                        with patch('app.calculator.CalculatorOriginator'):
                            with patch('app.calculator.CalculatorCaretaker'):
                                with patch('app.calculator.LoggingObserver'):
                                    with patch('app.calculator.AutoSaveObserver'):
                                        self.calculator = Calculator()
    
    def test_process_command_add(self):
        """Test processing add command."""
        with patch.object(self.calculator, '_perform_calculation', return_value=8.0):
            result = self.calculator._process_command('add 5 3')
            assert 'Result: 8.0' in result or '8.0' in result
    
    def test_process_command_history(self):
        """Test processing history command."""
        mock_calc = Calculation('add', 5, 3, 8)
        with patch.object(
            self.calculator.history_manager,
            'get_history',
            return_value=[mock_calc]
        ):
            result = self.calculator._process_command('history')
            assert 'History' in result or 'add' in result
    
    def test_process_command_help(self):
        """Test processing help command."""
        result = self.calculator._process_command('help')
        assert 'Commands' in result or 'help' in result
    
    def test_process_command_unknown(self):
        """Test processing unknown command."""
        result = self.calculator._process_command('unknown_command')
        assert 'Unknown' in result or 'unknown' in result.lower()
    
    def test_process_command_exit(self):
        """Test processing exit command."""
        result = self.calculator._process_command('exit')
        assert result == "EXIT"

