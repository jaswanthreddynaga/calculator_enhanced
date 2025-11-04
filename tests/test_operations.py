"""Tests for calculator operations."""

import pytest
from app.operations import (
    OperationFactory,
    AddOperation,
    SubtractOperation,
    MultiplyOperation,
    DivideOperation,
    PowerOperation,
    RootOperation,
    ModulusOperation,
    IntDivideOperation,
    PercentOperation,
    AbsDiffOperation,
    OperationError
)


class TestAddOperation:
    """Tests for addition operation."""
    
    def test_add_positive_numbers(self):
        """Test adding positive numbers."""
        op = AddOperation()
        assert op.execute(5, 3) == 8
    
    def test_add_negative_numbers(self):
        """Test adding negative numbers."""
        op = AddOperation()
        assert op.execute(-5, -3) == -8
    
    def test_add_mixed_numbers(self):
        """Test adding positive and negative numbers."""
        op = AddOperation()
        assert op.execute(5, -3) == 2


class TestSubtractOperation:
    """Tests for subtraction operation."""
    
    def test_subtract_positive_numbers(self):
        """Test subtracting positive numbers."""
        op = SubtractOperation()
        assert op.execute(5, 3) == 2
    
    def test_subtract_negative_numbers(self):
        """Test subtracting negative numbers."""
        op = SubtractOperation()
        assert op.execute(-5, -3) == -2


class TestMultiplyOperation:
    """Tests for multiplication operation."""
    
    def test_multiply_positive_numbers(self):
        """Test multiplying positive numbers."""
        op = MultiplyOperation()
        assert op.execute(5, 3) == 15
    
    def test_multiply_by_zero(self):
        """Test multiplying by zero."""
        op = MultiplyOperation()
        assert op.execute(5, 0) == 0


class TestDivideOperation:
    """Tests for division operation."""
    
    def test_divide_positive_numbers(self):
        """Test dividing positive numbers."""
        op = DivideOperation()
        assert op.execute(10, 2) == 5.0
    
    def test_divide_by_zero(self):
        """Test dividing by zero raises error."""
        op = DivideOperation()
        with pytest.raises(OperationError):
            op.execute(10, 0)
    
    def test_divide_decimal_result(self):
        """Test division resulting in decimal."""
        op = DivideOperation()
        assert op.execute(7, 2) == 3.5


class TestPowerOperation:
    """Tests for power operation."""
    
    def test_power_positive_base_positive_exponent(self):
        """Test power with positive base and exponent."""
        op = PowerOperation()
        assert op.execute(2, 3) == 8.0
    
    def test_power_zero_exponent(self):
        """Test power with zero exponent."""
        op = PowerOperation()
        assert op.execute(5, 0) == 1.0
    
    def test_power_negative_exponent(self):
        """Test power with negative exponent."""
        op = PowerOperation()
        assert op.execute(2, -2) == 0.25
    
    def test_power_zero_base(self):
        """Test power with zero base."""
        op = PowerOperation()
        assert op.execute(0, 5) == 0.0


class TestRootOperation:
    """Tests for root operation."""
    
    def test_square_root(self):
        """Test square root."""
        op = RootOperation()
        assert abs(op.execute(16, 2) - 4.0) < 0.001
    
    def test_cube_root(self):
        """Test cube root."""
        op = RootOperation()
        assert abs(op.execute(27, 3) - 3.0) < 0.001
    
    def test_root_zero_base(self):
        """Test root of zero."""
        op = RootOperation()
        assert op.execute(0, 5) == 0.0
    
    def test_root_zero_degree(self):
        """Test root with zero degree raises error."""
        op = RootOperation()
        with pytest.raises(OperationError):
            op.execute(16, 0)
    
    def test_even_root_negative_number(self):
        """Test even root of negative number raises error."""
        op = RootOperation()
        with pytest.raises(OperationError):
            op.execute(-16, 2)


class TestModulusOperation:
    """Tests for modulus operation."""
    
    def test_modulus_positive_numbers(self):
        """Test modulus with positive numbers."""
        op = ModulusOperation()
        assert op.execute(10, 3) == 1.0
    
    def test_modulus_zero_remainder(self):
        """Test modulus with zero remainder."""
        op = ModulusOperation()
        assert op.execute(10, 5) == 0.0
    
    def test_modulus_by_zero(self):
        """Test modulus by zero raises error."""
        op = ModulusOperation()
        with pytest.raises(OperationError):
            op.execute(10, 0)


class TestIntDivideOperation:
    """Tests for integer division operation."""
    
    def test_int_divide_positive_numbers(self):
        """Test integer division with positive numbers."""
        op = IntDivideOperation()
        assert op.execute(10, 3) == 3.0
    
    def test_int_divide_exact_division(self):
        """Test integer division with exact division."""
        op = IntDivideOperation()
        assert op.execute(10, 5) == 2.0
    
    def test_int_divide_by_zero(self):
        """Test integer division by zero raises error."""
        op = IntDivideOperation()
        with pytest.raises(OperationError):
            op.execute(10, 0)


class TestPercentOperation:
    """Tests for percentage operation."""
    
    def test_percent_positive_numbers(self):
        """Test percentage calculation."""
        op = PercentOperation()
        assert op.execute(25, 100) == 25.0
    
    def test_percent_partial(self):
        """Test percentage calculation with partial."""
        op = PercentOperation()
        assert op.execute(1, 4) == 25.0
    
    def test_percent_zero_denominator(self):
        """Test percentage with zero denominator raises error."""
        op = PercentOperation()
        with pytest.raises(OperationError):
            op.execute(25, 0)


class TestAbsDiffOperation:
    """Tests for absolute difference operation."""
    
    def test_abs_diff_positive_numbers(self):
        """Test absolute difference with positive numbers."""
        op = AbsDiffOperation()
        assert op.execute(10, 5) == 5.0
    
    def test_abs_diff_reversed_order(self):
        """Test absolute difference order doesn't matter."""
        op = AbsDiffOperation()
        assert op.execute(5, 10) == 5.0
    
    def test_abs_diff_negative_numbers(self):
        """Test absolute difference with negative numbers."""
        op = AbsDiffOperation()
        assert op.execute(-10, -5) == 5.0


class TestOperationFactory:
    """Tests for operation factory."""
    
    @pytest.mark.parametrize("op_name,expected_class", [
        ('add', AddOperation),
        ('subtract', SubtractOperation),
        ('multiply', MultiplyOperation),
        ('divide', DivideOperation),
        ('power', PowerOperation),
        ('root', RootOperation),
        ('modulus', ModulusOperation),
        ('int_divide', IntDivideOperation),
        ('percent', PercentOperation),
        ('abs_diff', AbsDiffOperation),
    ])
    def test_create_operation(self, op_name, expected_class):
        """Test creating operations by name."""
        op = OperationFactory.create_operation(op_name)
        assert isinstance(op, expected_class)
    
    def test_create_unknown_operation(self):
        """Test creating unknown operation raises error."""
        with pytest.raises(OperationError):
            OperationFactory.create_operation('unknown')
    
    def test_create_operation_case_insensitive(self):
        """Test operation creation is case insensitive."""
        op = OperationFactory.create_operation('ADD')
        assert isinstance(op, AddOperation)
    
    def test_get_available_operations(self):
        """Test getting available operations."""
        ops = OperationFactory.get_available_operations()
        assert 'add' in ops
        assert 'subtract' in ops
        assert len(ops) >= 10
    
    def test_operation_names(self):
        """Test operation names match."""
        assert AddOperation().get_name() == 'add'
        assert SubtractOperation().get_name() == 'subtract'
        assert PowerOperation().get_name() == 'power'
        assert RootOperation().get_name() == 'root'
        assert ModulusOperation().get_name() == 'modulus'
        assert IntDivideOperation().get_name() == 'int_divide'
        assert PercentOperation().get_name() == 'percent'
        assert AbsDiffOperation().get_name() == 'abs_diff'

