"""Additional edge case tests."""

import pytest
from app.history import HistoryManager
from app.calculator_config import CalculatorConfig
from app.calculation import Calculation
from app.exceptions import HistoryError


class TestEdgeCases:
    """Edge case tests for better coverage."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = CalculatorConfig()
        self.history_manager = HistoryManager(self.config)
        self.history_manager.clear_history()
    
    def teardown_method(self):
        """Clean up test files."""
        if self.config.history_file.exists():
            self.config.history_file.unlink()
    
    def test_save_empty_history(self):
        """Test saving empty history."""
        assert self.history_manager.save_to_csv()
    
    def test_calculation_repr(self):
        """Test calculation representation."""
        calc = Calculation('add', 5, 3, 8)
        repr_str = repr(calc)
        assert 'Calculation' in repr_str
        assert 'add' in repr_str
    
    def test_calculation_from_dict_no_timestamp(self):
        """Test creating calculation from dict without timestamp."""
        data = {
            'operation': 'add',
            'operand_a': 5,
            'operand_b': 3,
            'result': 8
        }
        calc = Calculation.from_dict(data)
        assert calc.operation == 'add'
        assert isinstance(calc.timestamp, type(Calculation.from_dict(data).timestamp))

