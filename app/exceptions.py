"""Custom exceptions for the calculator application."""


class CalculatorError(Exception):
    """Base exception for calculator errors."""
    pass


class OperationError(CalculatorError):
    """Exception raised for operation-related errors."""
    pass


class ValidationError(CalculatorError):
    """Exception raised for input validation errors."""
    pass


class HistoryError(CalculatorError):
    """Exception raised for history-related errors."""
    pass


class ConfigurationError(CalculatorError):
    """Exception raised for configuration-related errors."""
    pass

