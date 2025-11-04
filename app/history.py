"""History management with pandas CSV serialization."""

import pandas as pd
from pathlib import Path
from typing import Optional
from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.exceptions import HistoryError


class HistoryManager:
    """Manages calculation history with CSV persistence."""
    
    def __init__(self, config: CalculatorConfig):
        """
        Initialize history manager.
        
        Args:
            config: Calculator configuration
        """
        self.config = config
        self._history: list[Calculation] = []
    
    def add_calculation(self, calculation: Calculation):
        """
        Add a calculation to history.
        
        Args:
            calculation: Calculation to add
        """
        self._history.append(calculation)
        
        # Limit history size
        if len(self._history) > self.config.max_history_size:
            self._history = self._history[-self.config.max_history_size:]
    
    def get_history(self) -> list[Calculation]:
        """Get calculation history."""
        return self._history.copy()
    
    def clear_history(self):
        """Clear calculation history."""
        self._history.clear()
    
    def set_history(self, history: list[Calculation]):
        """
        Set the history.
        
        Args:
            history: List of calculations
        """
        self._history = history.copy()
    
    def save_to_csv(self, file_path: Optional[Path] = None) -> bool:
        """
        Save history to CSV file using pandas.
        
        Args:
            file_path: Optional custom file path
            
        Returns:
            True if save was successful
            
        Raises:
            HistoryError: If save fails
        """
        if not self._history:
            return True  # Nothing to save
        
        file_path = file_path or self.config.history_file
        
        try:
            # Convert calculations to list of dictionaries
            data = [calc.to_dict() for calc in self._history]
            
            # Create DataFrame
            df = pd.DataFrame(data)
            
            # Save to CSV
            df.to_csv(
                file_path,
                index=False,
                encoding=self.config.default_encoding
            )
            return True
        except Exception as e:
            raise HistoryError(f"Failed to save history to CSV: {e}")
    
    def load_from_csv(self, file_path: Optional[Path] = None) -> bool:
        """
        Load history from CSV file using pandas.
        
        Args:
            file_path: Optional custom file path
            
        Returns:
            True if load was successful
            
        Raises:
            HistoryError: If load fails
        """
        file_path = file_path or self.config.history_file
        
        if not file_path.exists():
            return False  # File doesn't exist, not an error
        
        try:
            # Read CSV into DataFrame
            df = pd.read_csv(
                file_path,
                encoding=self.config.default_encoding
            )
            
            # Convert DataFrame rows to Calculation objects
            calculations = []
            for _, row in df.iterrows():
                try:
                    calc = Calculation.from_dict(row.to_dict())
                    calculations.append(calc)
                except Exception as e:
                    raise HistoryError(
                        f"Failed to parse calculation from CSV: {e}"
                    )
            
            self._history = calculations
            return True
        except pd.errors.EmptyDataError:
            # Empty file is okay
            self._history = []
            return True
        except Exception as e:
            raise HistoryError(f"Failed to load history from CSV: {e}")

