"""Tests for calculation data model."""

from datetime import datetime
from app.calculation import Calculation


class TestCalculation:
    """Tests for Calculation class."""
    
    def test_calculation_creation(self):
        """Test creating a calculation."""
        calc = Calculation(
            operation='add',
            operand_a=5,
            operand_b=3,
            result=8
        )
        assert calc.operation == 'add'
        assert calc.operand_a == 5
        assert calc.operand_b == 3
        assert calc.result == 8
        assert isinstance(calc.timestamp, datetime)
    
    def test_calculation_str(self):
        """Test string representation."""
        calc = Calculation('add', 5, 3, 8)
        assert 'add(5, 3) = 8' in str(calc)
    
    def test_calculation_to_dict(self):
        """Test conversion to dictionary."""
        calc = Calculation('add', 5, 3, 8)
        data = calc.to_dict()
        assert data['operation'] == 'add'
        assert data['operand_a'] == 5
        assert data['operand_b'] == 3
        assert data['result'] == 8
        assert 'timestamp' in data
    
    def test_calculation_from_dict(self):
        """Test creation from dictionary."""
        timestamp = datetime.now()
        data = {
            'operation': 'add',
            'operand_a': 5,
            'operand_b': 3,
            'result': 8,
            'timestamp': timestamp.isoformat()
        }
        calc = Calculation.from_dict(data)
        assert calc.operation == 'add'
        assert calc.operand_a == 5
        assert calc.operand_b == 3
        assert calc.result == 8

