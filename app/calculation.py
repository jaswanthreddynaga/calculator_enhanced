"""Calculation data model."""

from datetime import datetime
from typing import Optional


class Calculation:
    """Represents a single calculation operation."""
    
    def __init__(
        self,
        operation: str,
        operand_a: float,
        operand_b: float,
        result: float,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialize a calculation.
        
        Args:
            operation: Name of the operation
            operand_a: First operand
            operand_b: Second operand
            result: Calculation result
            timestamp: Timestamp of the calculation (defaults to now)
        """
        self.operation = operation
        self.operand_a = operand_a
        self.operand_b = operand_b
        self.result = result
        self.timestamp = timestamp or datetime.now()
    
    def __str__(self) -> str:
        """String representation of the calculation."""
        return (
            f"{self.operation}({self.operand_a}, {self.operand_b}) = "
            f"{self.result}"
        )
    
    def __repr__(self) -> str:
        """Detailed representation of the calculation."""
        return (
            f"Calculation(operation='{self.operation}', "
            f"operand_a={self.operand_a}, operand_b={self.operand_b}, "
            f"result={self.result}, timestamp={self.timestamp})"
        )
    
    def to_dict(self) -> dict:
        """Convert calculation to dictionary for CSV serialization."""
        return {
            'operation': self.operation,
            'operand_a': self.operand_a,
            'operand_b': self.operand_b,
            'result': self.result,
            'timestamp': self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Calculation':
        """Create Calculation from dictionary (CSV deserialization)."""
        timestamp = datetime.fromisoformat(
            data['timestamp']
        ) if 'timestamp' in data else datetime.now()
        
        return cls(
            operation=data['operation'],
            operand_a=float(data['operand_a']),
            operand_b=float(data['operand_b']),
            result=float(data['result']),
            timestamp=timestamp
        )

