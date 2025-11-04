"""Tests for history management."""

import os
import pandas as pd
import pytest
from pathlib import Path
from unittest.mock import patch
from app.history import HistoryManager
from app.calculator_config import CalculatorConfig
from app.calculation import Calculation
from app.exceptions import HistoryError


class TestHistoryManager:
    """Tests for HistoryManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = CalculatorConfig()
        self.history_manager = HistoryManager(self.config)
        self.history_manager.clear_history()
    
    def teardown_method(self):
        """Clean up test files."""
        if self.config.history_file.exists():
            self.config.history_file.unlink()
    
    def test_add_calculation(self):
        """Test adding a calculation."""
        calc = Calculation('add', 5, 3, 8)
        self.history_manager.add_calculation(calc)
        assert len(self.history_manager.get_history()) == 1
    
    def test_get_history(self):
        """Test getting history."""
        calc = Calculation('add', 5, 3, 8)
        self.history_manager.add_calculation(calc)
        history = self.history_manager.get_history()
        assert len(history) == 1
        assert history[0].operation == 'add'
    
    def test_clear_history(self):
        """Test clearing history."""
        calc = Calculation('add', 5, 3, 8)
        self.history_manager.add_calculation(calc)
        self.history_manager.clear_history()
        assert len(self.history_manager.get_history()) == 0
    
    def test_history_size_limit(self):
        """Test history size limit."""
        for i in range(150):
            calc = Calculation('add', i, i+1, 2*i+1)
            self.history_manager.add_calculation(calc)
        
        history = self.history_manager.get_history()
        assert len(history) == self.config.max_history_size
    
    def test_save_to_csv(self):
        """Test saving history to CSV."""
        calc1 = Calculation('add', 5, 3, 8)
        calc2 = Calculation('subtract', 10, 4, 6)
        self.history_manager.add_calculation(calc1)
        self.history_manager.add_calculation(calc2)
        
        self.history_manager.save_to_csv()
        assert self.config.history_file.exists()
        
        # Verify CSV content
        df = pd.read_csv(self.config.history_file)
        assert len(df) == 2
        assert df.iloc[0]['operation'] == 'add'
        assert df.iloc[1]['operation'] == 'subtract'
    
    def test_load_from_csv(self):
        """Test loading history from CSV."""
        calc1 = Calculation('add', 5, 3, 8)
        calc2 = Calculation('subtract', 10, 4, 6)
        self.history_manager.add_calculation(calc1)
        self.history_manager.add_calculation(calc2)
        self.history_manager.save_to_csv()
        
        # Clear and reload
        self.history_manager.clear_history()
        assert self.history_manager.load_from_csv()
        
        history = self.history_manager.get_history()
        assert len(history) == 2
        assert history[0].operation == 'add'
        assert history[1].operation == 'subtract'
    
    def test_load_from_csv_not_exists(self):
        """Test loading from non-existent CSV."""
        assert not self.history_manager.load_from_csv()
    
    def test_set_history(self):
        """Test setting history."""
        calcs = [
            Calculation('add', 1, 2, 3),
            Calculation('subtract', 5, 2, 3)
        ]
        self.history_manager.set_history(calcs)
        assert len(self.history_manager.get_history()) == 2

    def test_save_to_csv_fail(self):
        """Test that saving to CSV raises HistoryError on failure."""
        calc = Calculation('add', 5, 3, 8)
        self.history_manager.add_calculation(calc)
        with patch('pandas.DataFrame.to_csv', side_effect=IOError("Disk full")):
            with pytest.raises(HistoryError):
                self.history_manager.save_to_csv()

    def test_load_from_csv_fail(self):
        """Test that loading from CSV raises HistoryError on failure."""
        # Create a dummy file to load
        with open(self.config.history_file, 'w') as f:
            f.write("operation,operand_a,operand_b,result,timestamp\n")
            f.write("add,invalid,3,5,2023-01-01T00:00:00\n")
        
        with patch('app.history.Calculation.from_dict', side_effect=ValueError("Bad data")) as mock_from_dict:
            with pytest.raises(HistoryError):
                self.history_manager.load_from_csv()
