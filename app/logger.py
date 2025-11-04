"""Logging functionality for the calculator."""

import logging
from pathlib import Path
from app.calculator_config import CalculatorConfig


class Logger:
    """Logger for calculator operations."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """Singleton pattern implementation."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize logger if not already initialized."""
        if Logger._initialized:  # pragma: no cover
            return
        
        self.config = CalculatorConfig()
        self._setup_logger()
        Logger._initialized = True
    
    def _setup_logger(self):
        """Configure the logger."""
        self.logger = logging.getLogger('calculator')
        self.logger.setLevel(logging.INFO)
        
        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()
        
        # File handler
        file_handler = logging.FileHandler(
            self.config.log_file,
            encoding=self.config.default_encoding
        )
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def log_calculation(self, operation: str, a: float, b: float, result: float):
        """Log a calculation operation."""
        self.logger.info(
            f"Calculation: {operation}({a}, {b}) = {result}"
        )
    
    def log_error(self, message: str):
        """Log an error."""
        self.logger.error(message)
    
    def log_warning(self, message: str):
        """Log a warning."""
        self.logger.warning(message)
    
    def log_info(self, message: str):
        """Log an info message."""
        self.logger.info(message)

