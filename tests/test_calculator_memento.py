"""Tests for calculator memento pattern."""

from app.calculator_memento import (
    CalculatorMemento,
    CalculatorOriginator,
    CalculatorCaretaker
)
from app.calculation import Calculation


class TestCalculatorMemento:
    """Tests for CalculatorMemento class."""
    
    def test_memento_creation(self):
        """Test creating a memento."""
        history = [Calculation('add', 1, 2, 3)]
        memento = CalculatorMemento(history)
        assert len(memento.history) == 1


class TestCalculatorOriginator:
    """Tests for CalculatorOriginator class."""
    
    def test_save_state(self):
        """Test saving state."""
        originator = CalculatorOriginator()
        calc = Calculation('add', 1, 2, 3)
        originator.add_calculation(calc)
        memento = originator.save_state()
        assert len(memento.history) == 1
    
    def test_restore_state(self):
        """Test restoring state."""
        originator = CalculatorOriginator()
        calc = Calculation('add', 1, 2, 3)
        originator.add_calculation(calc)
        memento = originator.save_state()
        
        originator.add_calculation(Calculation('subtract', 5, 2, 3))
        assert len(originator.get_history()) == 2
        
        originator.restore_state(memento)
        assert len(originator.get_history()) == 1


class TestCalculatorCaretaker:
    """Tests for CalculatorCaretaker class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.originator = CalculatorOriginator()
        self.caretaker = CalculatorCaretaker(self.originator)
        self.caretaker.save_state()
    
    def test_save_state(self):
        """Test saving state."""
        calc = Calculation('add', 1, 2, 3)
        self.originator.add_calculation(calc)
        self.caretaker.save_state()
        assert self.caretaker.can_undo()
    
    def test_undo(self):
        """Test undo functionality."""
        calc1 = Calculation('add', 1, 2, 3)
        self.originator.add_calculation(calc1)
        self.caretaker.save_state()
        
        calc2 = Calculation('subtract', 5, 2, 3)
        self.originator.add_calculation(calc2)
        
        assert len(self.originator.get_history()) == 2
        assert self.caretaker.undo()
        assert len(self.originator.get_history()) == 1
        assert self.caretaker.can_redo()
    
    def test_undo_empty(self):
        """Test undo when nothing to undo."""
        caretaker = CalculatorCaretaker(CalculatorOriginator())
        assert not caretaker.undo()
    
    def test_redo(self):
        """Test redo functionality."""
        # Save initial empty state
        self.caretaker.save_state()

        calc = Calculation('add', 1, 2, 3)
        self.originator.add_calculation(calc)
        self.caretaker.save_state()
        
        assert self.caretaker.undo()
        assert len(self.originator.get_history()) == 0
        assert self.caretaker.redo() # Redo to state with 1 calc
        assert len(self.originator.get_history()) == 1
    
    def test_redo_empty(self):
        """Test redo when nothing to redo."""
        assert not self.caretaker.redo()
    
    def test_redo_stack_cleared_on_new_operation(self):
        """Test that redo stack is cleared on new operation."""
        calc1 = Calculation('add', 1, 2, 3)
        self.originator.add_calculation(calc1)
        self.caretaker.save_state()
        
        assert self.caretaker.undo()
        assert self.caretaker.can_redo()
        
        calc2 = Calculation('subtract', 5, 2, 3)
        self.originator.add_calculation(calc2)
        self.caretaker.save_state()
        
        assert not self.caretaker.can_redo()
