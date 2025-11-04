"""Tests for observers."""

from unittest.mock import Mock, patch
from app.observers import LoggingObserver, AutoSaveObserver
from app.calculation import Calculation


class TestLoggingObserver:
    """Tests for LoggingObserver class."""
    
    def test_on_calculation(self):
        """Test logging observer on calculation."""
        with patch('app.observers.Logger') as mock_logger_class:
            mock_logger = Mock()
            mock_logger_class.return_value = mock_logger
            
            observer = LoggingObserver()
            calc = Calculation('add', 5, 3, 8)
            observer.on_calculation(calc)
            
            mock_logger.log_calculation.assert_called_once_with(
                'add', 5, 3, 8
            )


class TestAutoSaveObserver:
    """Tests for AutoSaveObserver class."""
    
    def test_on_calculation(self):
        """Test auto-save observer on calculation."""
        mock_history_manager = Mock()
        observer = AutoSaveObserver(mock_history_manager)
        
        calc = Calculation('add', 5, 3, 8)
        observer.on_calculation(calc)
        
        mock_history_manager.save_to_csv.assert_called_once()
    
    def test_on_calculation_save_error(self):
        """Test auto-save observer handles save errors."""
        mock_history_manager = Mock()
        mock_history_manager.save_to_csv.side_effect = Exception("Save error")
        
        observer = AutoSaveObserver(mock_history_manager)
        
        with patch('app.observers.Logger') as mock_logger_class:
            mock_logger = Mock()
            mock_logger_class.return_value = mock_logger
            
            calc = Calculation('add', 5, 3, 8)
            observer.on_calculation(calc)
            
            mock_logger.log_error.assert_called_once()

