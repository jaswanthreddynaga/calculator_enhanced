"""Operations module implementing Factory Pattern for calculator operations."""

from abc import ABC, abstractmethod
from app.exceptions import OperationError


class Operation(ABC):
    """Abstract base class for calculator operations."""
    
    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        """
        Execute the operation.
        
        Args:
            a: First operand
            b: Second operand
            
        Returns:
            Result of the operation
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get the name of the operation."""
        pass


class AddOperation(Operation):
    """Addition operation."""
    
    def execute(self, a: float, b: float) -> float:
        """Add two numbers."""
        return a + b
    
    def get_name(self) -> str:
        """Get operation name."""
        return "add"


class SubtractOperation(Operation):
    """Subtraction operation."""
    
    def execute(self, a: float, b: float) -> float:
        """Subtract b from a."""
        return a - b
    
    def get_name(self) -> str:
        """Get operation name."""
        return "subtract"


class MultiplyOperation(Operation):
    """Multiplication operation."""
    
    def execute(self, a: float, b: float) -> float:
        """Multiply two numbers."""
        return a * b
    
    def get_name(self) -> str:
        """Get operation name."""
        return "multiply"


class DivideOperation(Operation):
    """Division operation."""
    
    def execute(self, a: float, b: float) -> float:
        """Divide a by b."""
        if b == 0:
            raise OperationError("Division by zero is not allowed")
        return a / b
    
    def get_name(self) -> str:
        """Get operation name."""
        return "divide"


class PowerOperation(Operation):
    """Power operation."""
    
    def execute(self, a: float, b: float) -> float:
        """Raise a to the power of b."""
        try:
            result = a ** b
            # Check if result is complex (has imaginary part)
            if isinstance(result, complex):
                if result.imag != 0:
                    raise OperationError(
                        f"Invalid result for power operation: {a} ** {b}"
                    )
                result = result.real
            # Check for invalid types
            if not isinstance(result, (int, float)):
                raise OperationError(
                    f"Invalid result for power operation: {a} ** {b}"
                )
            return float(result)
        except (ValueError, OverflowError) as e:
            raise OperationError(
                f"Error computing power: {e}"
            )
    
    def get_name(self) -> str:
        """Get operation name."""
        return "power"


class RootOperation(Operation):
    """Root operation."""
    
    def execute(self, a: float, b: float) -> float:
        """Calculate the bth root of a."""
        if b == 0:
            raise OperationError("Cannot calculate 0th root")
        if a < 0 and b % 2 == 0:
            raise OperationError(
                "Cannot calculate even root of negative number"
            )
        try:
            if a < 0:
                # For odd roots of negative numbers
                result = -((-a) ** (1 / b))
            else:
                result = a ** (1 / b)
            return float(result)
        except (ValueError, OverflowError, ZeroDivisionError) as e:
            raise OperationError(f"Error computing root: {e}")
    
    def get_name(self) -> str:
        """Get operation name."""
        return "root"


class ModulusOperation(Operation):
    """Modulus operation."""
    
    def execute(self, a: float, b: float) -> float:
        """Compute a modulo b."""
        if b == 0:
            raise OperationError("Modulus by zero is not allowed")
        return float(a % b)
    
    def get_name(self) -> str:
        """Get operation name."""
        return "modulus"


class IntDivideOperation(Operation):
    """Integer division operation."""
    
    def execute(self, a: float, b: float) -> float:
        """Perform integer division of a by b."""
        if b == 0:
            raise OperationError("Integer division by zero is not allowed")
        return float(a // b)
    
    def get_name(self) -> str:
        """Get operation name."""
        return "int_divide"


class PercentOperation(Operation):
    """Percentage calculation operation."""
    
    def execute(self, a: float, b: float) -> float:
        """Calculate (a / b) * 100."""
        if b == 0:
            raise OperationError("Cannot calculate percentage with zero denominator")
        return (a / b) * 100
    
    def get_name(self) -> str:
        """Get operation name."""
        return "percent"


class AbsDiffOperation(Operation):
    """Absolute difference operation."""
    
    def execute(self, a: float, b: float) -> float:
        """Calculate absolute difference between a and b."""
        return abs(a - b)
    
    def get_name(self) -> str:
        """Get operation name."""
        return "abs_diff"


class OperationFactory:
    """Factory for creating operation instances."""
    
    _operations = {
        'add': AddOperation,
        'subtract': SubtractOperation,
        'multiply': MultiplyOperation,
        'divide': DivideOperation,
        'power': PowerOperation,
        'root': RootOperation,
        'modulus': ModulusOperation,
        'int_divide': IntDivideOperation,
        'percent': PercentOperation,
        'abs_diff': AbsDiffOperation,
    }
    
    @classmethod
    def create_operation(cls, operation_name: str) -> Operation:
        """
        Create an operation instance by name.
        
        Args:
            operation_name: Name of the operation
            
        Returns:
            Operation instance
            
        Raises:
            OperationError: If operation name is invalid
        """
        operation_name = operation_name.lower()
        if operation_name not in cls._operations:
            raise OperationError(
                f"Unknown operation: {operation_name}. "
                f"Available operations: {', '.join(cls._operations.keys())}"
            )
        return cls._operations[operation_name]()
    
    @classmethod
    def get_available_operations(cls) -> list[str]:
        """Get list of available operation names."""
        return list(cls._operations.keys())

