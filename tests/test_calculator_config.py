"""Tests for calculator configuration."""

import os
import pytest
from pathlib import Path
from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError


class TestCalculatorConfig:
    """Tests for CalculatorConfig class."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = CalculatorConfig()
        assert config.log_dir.exists()
        assert config.history_dir.exists()
        assert config.max_history_size == 100
        assert config.auto_save is True
        assert config.precision == 10
    
    def test_log_and_history_dirs_created(self):
        """Test that log and history directories are created."""
        config = CalculatorConfig()
        assert config.log_dir.is_dir()
        assert config.history_dir.is_dir()
    
    def test_file_paths(self):
        """Test that file paths are set correctly."""
        config = CalculatorConfig()
        assert config.log_file == config.log_dir / 'calculator.log'
        assert config.history_file == config.history_dir / 'history.csv'

    def test_config_invalid_max_history(self, monkeypatch):
        """Test invalid max history size raises error."""
        monkeypatch.setenv('CALCULATOR_MAX_HISTORY_SIZE', 'invalid')
        with pytest.raises(ConfigurationError):
            CalculatorConfig()

    def test_config_invalid_precision(self, monkeypatch):
        """Test invalid precision raises error."""
        monkeypatch.setenv('CALCULATOR_PRECISION', 'invalid')
        with pytest.raises(ConfigurationError):
            CalculatorConfig()

    def test_config_invalid_max_input(self, monkeypatch):
        """Test invalid max input value raises error."""
        monkeypatch.setenv('CALCULATOR_MAX_INPUT_VALUE', 'invalid')
        with pytest.raises(ConfigurationError):
            CalculatorConfig()
