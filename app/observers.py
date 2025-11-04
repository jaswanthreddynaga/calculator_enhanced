"""Observer Pattern implementation for calculator events."""

from abc import ABC, abstractmethod
from app.calculation import Calculation


class CalculatorObserver(ABC):
    """Abstract observer for calculator events."""
    
    @abstractmethod
    def on_calculation(self, calculation: Calculation):
        """
        Called when a new calculation is performed.
        
        Args:
            calculation: The calculation that was performed
        """
        pass


class LoggingObserver(CalculatorObserver):
    """Observer that logs calculations."""
    
    def __init__(self):
        """Initialize logging observer."""
        from app.logger import Logger
        self.logger = Logger()
    
    def on_calculation(self, calculation: Calculation):
        """Log the calculation."""
        self.logger.log_calculation(
            calculation.operation,
            calculation.operand_a,
            calculation.operand_b,
            calculation.result
        )


class AutoSaveObserver(CalculatorObserver):
    """Observer that auto-saves calculation history."""
    
    def __init__(self, history_manager):
        """
        Initialize auto-save observer.
        
        Args:
            history_manager: HistoryManager instance to use for saving
        """
        self.history_manager = history_manager
    
    def on_calculation(self, calculation: Calculation):
        """Auto-save the calculation history."""
        try:
            self.history_manager.save_to_csv()
        except Exception as e:
            from app.logger import Logger
            logger = Logger()
            logger.log_error(f"Auto-save failed: {e}")

