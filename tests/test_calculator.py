"""Tests for calculator main class."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from app.calculator import Calculator
from app.calculation import Calculation
from app.exceptions import OperationError, ValidationError

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

    def test_process_command_add_error(self):
        """Test processing add command with an error."""
        with patch.object(self.calculator, '_perform_calculation', side_effect=ValidationError("Invalid number")):
            result = self.calculator._process_command('add a b')
            assert 'Error: Invalid number' in result

    
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
    
    def test_process_command_history_empty(self):
        """Test processing history command when history is empty."""
        with patch.object(self.calculator.history_manager, 'get_history', return_value=[]):
            result = self.calculator._process_command('history')
            assert 'No calculations' in result


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

    def test_process_command_no_command(self):
        """Test processing an empty command."""
        result = self.calculator._process_command('   ')
        assert result is None

    def test_process_command_clear(self):
        """Test the clear command."""
        self.calculator.originator.set_history.reset_mock()
        result = self.calculator._process_command('clear')
        assert "History cleared" in result
        self.calculator.history_manager.clear_history.assert_called_once()
        self.calculator.originator.set_history.assert_called_once_with([])

    def test_process_command_undo(self):
        """Test the undo command."""
        self.calculator.caretaker.undo.return_value = True
        mock_calc = Calculation('add', 1, 2, 3)
        self.calculator.originator.get_history.return_value = [mock_calc]
        result = self.calculator._process_command('undo')
        assert "Undone" in result

    def test_process_command_undo_empty(self):
        """Test undo when there is nothing to undo."""
        self.calculator.caretaker.undo.return_value = False
        result = self.calculator._process_command('undo')
        assert "Nothing to undo" in result

    def test_process_command_undo_to_clear(self):
        """Test undo that results in an empty history."""
        self.calculator.caretaker.undo.return_value = True
        self.calculator.originator.get_history.return_value = []
        result = self.calculator._process_command('undo')
        assert "History cleared" in result

    def test_process_command_redo(self):
        """Test the redo command."""
        self.calculator.caretaker.redo.return_value = True
        mock_calc = Calculation('add', 1, 2, 3)
        self.calculator.originator.get_history.return_value = [mock_calc]
        result = self.calculator._process_command('redo')
        assert "Redone" in result

    def test_process_command_redo_empty(self):
        """Test redo when there is nothing to redo."""
        self.calculator.caretaker.redo.return_value = False
        result = self.calculator._process_command('redo')
        assert "Nothing to redo" in result

    def test_process_command_redo_to_clear(self):
        """Test redo that results in an empty history."""
        self.calculator.caretaker.redo.return_value = True
        self.calculator.originator.get_history.return_value = []
        result = self.calculator._process_command('redo')
        assert "History cleared" in result

    def test_process_command_save(self):
        """Test the save command."""
        result = self.calculator._process_command('save')
        assert "History saved" in result

    def test_process_command_save_error(self):
        """Test the save command with an error."""
        self.calculator.history_manager.save_to_csv.side_effect = Exception("Disk full")
        result = self.calculator._process_command('save')
        assert "Error saving history" in result

    def test_process_command_load(self):
        """Test the load command."""
        self.calculator.history_manager.load_from_csv.return_value = True
        result = self.calculator._process_command('load')
        assert "History loaded" in result

    def test_process_command_load_no_file(self):
        """Test the load command when no file exists."""
        self.calculator.history_manager.load_from_csv.return_value = False
        result = self.calculator._process_command('load')
        assert "No history file found" in result

    def test_process_command_load_error(self):
        """Test the load command with an error."""
        self.calculator.history_manager.load_from_csv.side_effect = Exception("Permission denied")
        result = self.calculator._process_command('load')
        assert "Error loading history" in result

    @pytest.mark.parametrize("command", [
        'add', 'subtract', 'multiply', 'divide', 'power', 'root',
        'modulus', 'int_divide', 'percent', 'abs_diff'
    ])
    def test_operation_commands_wrong_arg_count(self, command):
        """Test operation commands with incorrect number of arguments."""
        result = self.calculator._process_command(f'{command} 5')
        assert "Error:" in result
        assert "requires 2 arguments" in result

    def test_init_load_history_error(self):
        """Test that an error during history loading on init is handled."""
        with patch('app.calculator.Logger') as mock_logger_class:
            mock_logger_instance = mock_logger_class.return_value
            with patch('app.calculator.HistoryManager') as mock_hm:
                mock_hm.return_value.load_from_csv.side_effect = Exception("Bad file")
                # This should not raise an exception, but log a warning
                calc = Calculator()
                mock_logger_instance.log_warning.assert_called_with("Could not load history: Bad file")
