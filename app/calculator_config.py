"""Configuration management for the calculator application."""

import os
from pathlib import Path
from dotenv import load_dotenv
from app.exceptions import ConfigurationError


class CalculatorConfig:
    """Manages configuration settings from environment variables."""
    
    def __init__(self):
        """Initialize configuration by loading environment variables."""
        load_dotenv()
        self._load_config()
    
    def _load_config(self):
        """Load and validate configuration values."""
        # Base directories
        self.log_dir = Path(
            os.getenv('CALCULATOR_LOG_DIR', 'logs')
        )
        self.history_dir = Path(
            os.getenv('CALCULATOR_HISTORY_DIR', 'history')
        )
        
        # History settings
        try:
            self.max_history_size = int(
                os.getenv('CALCULATOR_MAX_HISTORY_SIZE', '100')
            )
        except ValueError:
            raise ConfigurationError(
                "CALCULATOR_MAX_HISTORY_SIZE must be an integer"
            )
        
        auto_save = os.getenv('CALCULATOR_AUTO_SAVE', 'true').lower()
        self.auto_save = auto_save in ('true', '1', 'yes')
        
        # Calculation settings
        try:
            self.precision = int(
                os.getenv('CALCULATOR_PRECISION', '10')
            )
        except ValueError:
            raise ConfigurationError(
                "CALCULATOR_PRECISION must be an integer"
            )
        
        try:
            self.max_input_value = float(
                os.getenv('CALCULATOR_MAX_INPUT_VALUE', '1e308')
            )
        except ValueError:
            raise ConfigurationError(
                "CALCULATOR_MAX_INPUT_VALUE must be a number"
            )
        
        self.default_encoding = os.getenv(
            'CALCULATOR_DEFAULT_ENCODING', 'utf-8'
        )
        
        # File paths
        self.log_dir.mkdir(exist_ok=True)
        self.history_dir.mkdir(exist_ok=True)
        
        self.log_file = self.log_dir / 'calculator.log'
        self.history_file = self.history_dir / 'history.csv'

