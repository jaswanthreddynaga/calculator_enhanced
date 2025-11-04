"""Memento Pattern implementation for undo/redo functionality."""

from typing import Optional
from app.calculation import Calculation


class CalculatorMemento:
    """Memento class to store calculator state."""
    
    def __init__(self, history: list[Calculation]):
        """
        Initialize memento with calculator history.
        
        Args:
            history: List of calculations representing the state
        """
        self.history = history.copy()  # Deep copy to preserve state


class CalculatorOriginator:
    """Originator class that creates and restores mementos."""
    
    def __init__(self):
        """Initialize the originator."""
        self._history: list[Calculation] = []
    
    def save_state(self) -> CalculatorMemento:
        """Create a memento with current state."""
        return CalculatorMemento(self._history)
    
    def restore_state(self, memento: CalculatorMemento):
        """Restore state from a memento."""
        self._history = memento.history.copy()
    
    def add_calculation(self, calculation: Calculation):
        """Add a calculation to history."""
        self._history.append(calculation)
    
    def get_history(self) -> list[Calculation]:
        """Get current history."""
        return self._history.copy()
    
    def set_history(self, history: list[Calculation]):
        """Set the history."""
        self._history = history.copy()


class CalculatorCaretaker:
    """Caretaker class that manages mementos for undo/redo."""
    
    def __init__(self, originator: CalculatorOriginator):
        """
        Initialize caretaker with originator.
        
        Args:
            originator: The originator to manage
        """
        self.originator = originator
        self._undo_stack: list[CalculatorMemento] = []
        self._redo_stack: list[CalculatorMemento] = []
    
    def save_state(self):
        """Save current state for undo."""
        memento = self.originator.save_state()
        self._undo_stack.append(memento)
        # Clear redo stack when new operation is performed
        self._redo_stack.clear()
    
    def undo(self) -> bool:
        """
        Undo the last operation.
        
        Returns:
            True if undo was successful, False if nothing to undo
        """
        if not self.can_undo():
            return False

        # Move the current state memento to the redo stack
        current_state_memento = self._undo_stack.pop()
        self._redo_stack.append(current_state_memento)

        # Restore the previous state
        previous_memento = self._undo_stack[-1] # Peek
        self.originator.restore_state(previous_memento)

        return True
    
    def redo(self) -> bool:
        """
        Redo the last undone operation.
        
        Returns:
            True if redo was successful, False if nothing to redo
        """
        if not self.can_redo():
            return False

        # Pop from redo stack and restore
        next_memento = self._redo_stack.pop()
        self.originator.restore_state(next_memento)

        # Push the restored state's memento back to the undo stack
        self._undo_stack.append(next_memento)

        return True
    
    def can_undo(self) -> bool:
        """Check if undo is possible."""
        return len(self._undo_stack) > 1
    
    def can_redo(self) -> bool:
        """Check if redo is possible."""
        return len(self._redo_stack) > 0

