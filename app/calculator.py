"""Main Calculator class with REPL interface and Decorator Pattern for help."""

import sys
from typing import Optional
from colorama import init, Fore, Style
from app.calculator_config import CalculatorConfig
from app.input_validators import InputValidator
from app.operations import OperationFactory
from app.calculation import Calculation
from app.history import HistoryManager
from app.calculator_memento import CalculatorOriginator, CalculatorCaretaker
from app.observers import LoggingObserver, AutoSaveObserver
from app.exceptions import OperationError, ValidationError
from app.logger import Logger

# Initialize colorama
init(autoreset=True)


def help_decorator(func):
    """Decorator to register commands for dynamic help menu."""
    if not hasattr(help_decorator, 'commands'):
        help_decorator.commands = {}
    
    func_name = func.__name__.replace('_cmd_', '')
    help_decorator.commands[func_name] = func.__doc__ or "No description"
    return func


class Calculator:
    """Enhanced calculator with REPL interface."""
    
    def __init__(self):
        """Initialize calculator with all components."""
        self.config = CalculatorConfig()
        self.validator = InputValidator(self.config)
        self.history_manager = HistoryManager(self.config)
        self.logger = Logger()
        
        # Memento Pattern for undo/redo
        self.originator = CalculatorOriginator()
        self.caretaker = CalculatorCaretaker(self.originator)
        
        # Observer Pattern
        self.observers = []
        self._register_observers()
        
        # Load history from CSV if available
        try:
            self.history_manager.load_from_csv()
            self.originator.set_history(self.history_manager.get_history())
        except Exception as e:
            self.logger.log_warning(f"Could not load history: {e}")
    
    def _register_observers(self):
        """Register observers."""
        logging_observer = LoggingObserver()
        auto_save_observer = AutoSaveObserver(self.history_manager)
        
        self.observers.append(logging_observer)
        if self.config.auto_save:
            self.observers.append(auto_save_observer)
    
    def _notify_observers(self, calculation: Calculation):
        """Notify all observers of a new calculation."""
        for observer in self.observers:
            observer.on_calculation(calculation)
    
    def _perform_calculation(
        self,
        operation_name: str,
        a_str: str,
        b_str: str
    ) -> float:
        """
        Perform a calculation.
        
        Args:
            operation_name: Name of the operation
            a_str: First operand as string
            b_str: Second operand as string
            
        Returns:
            Calculation result
        """
        # Validate inputs
        a, b = self.validator.validate_two_numbers(a_str, b_str)
        
        # Create operation
        operation = OperationFactory.create_operation(operation_name)
        
        # Execute operation
        try:
            result = operation.execute(a, b)
            # Round result based on precision
            result = round(result, self.config.precision)
        except OperationError as e:
            self.logger.log_error(str(e))
            raise
        
        # Create calculation record
        calculation = Calculation(
            operation=operation_name,
            operand_a=a,
            operand_b=b,
            result=result
        )
        
        # Save state for undo
        self.caretaker.save_state()
        
        # Add to history
        self.history_manager.add_calculation(calculation)
        self.originator.add_calculation(calculation)
        
        # Notify observers
        self._notify_observers(calculation)
        
        return result
    
    @help_decorator
    def _cmd_add(self, args: list[str]) -> str:
        """Add two numbers. Usage: add <a> <b>"""
        if len(args) != 2:
            return Fore.RED + "Error: add requires 2 arguments"
        try:
            result = self._perform_calculation('add', args[0], args[1])
            return f"{Fore.GREEN}Result: {result}"
        except (OperationError, ValidationError) as e:
            return f"{Fore.RED}Error: {e}"
    
    @help_decorator
    def _cmd_subtract(self, args: list[str]) -> str:
        """Subtract b from a. Usage: subtract <a> <b>"""
        if len(args) != 2:
            return Fore.RED + "Error: subtract requires 2 arguments"
        try:
            result = self._perform_calculation('subtract', args[0], args[1])
            return f"{Fore.GREEN}Result: {result}"
        except (OperationError, ValidationError) as e:
            return f"{Fore.RED}Error: {e}"
    
    @help_decorator
    def _cmd_multiply(self, args: list[str]) -> str:
        """Multiply two numbers. Usage: multiply <a> <b>"""
        if len(args) != 2:
            return Fore.RED + "Error: multiply requires 2 arguments"
        try:
            result = self._perform_calculation('multiply', args[0], args[1])
            return f"{Fore.GREEN}Result: {result}"
        except (OperationError, ValidationError) as e:
            return f"{Fore.RED}Error: {e}"
    
    @help_decorator
    def _cmd_divide(self, args: list[str]) -> str:
        """Divide a by b. Usage: divide <a> <b>"""
        if len(args) != 2:
            return Fore.RED + "Error: divide requires 2 arguments"
        try:
            result = self._perform_calculation('divide', args[0], args[1])
            return f"{Fore.GREEN}Result: {result}"
        except (OperationError, ValidationError) as e:
            return f"{Fore.RED}Error: {e}"
    
    @help_decorator
    def _cmd_power(self, args: list[str]) -> str:
        """Raise a to the power of b. Usage: power <a> <b>"""
        if len(args) != 2:
            return Fore.RED + "Error: power requires 2 arguments"
        try:
            result = self._perform_calculation('power', args[0], args[1])
            return f"{Fore.GREEN}Result: {result}"
        except (OperationError, ValidationError) as e:
            return f"{Fore.RED}Error: {e}"
    
    @help_decorator
    def _cmd_root(self, args: list[str]) -> str:
        """Calculate the bth root of a. Usage: root <a> <b>"""
        if len(args) != 2:
            return Fore.RED + "Error: root requires 2 arguments"
        try:
            result = self._perform_calculation('root', args[0], args[1])
            return f"{Fore.GREEN}Result: {result}"
        except (OperationError, ValidationError) as e:
            return f"{Fore.RED}Error: {e}"
    
    @help_decorator
    def _cmd_modulus(self, args: list[str]) -> str:
        """Compute a modulo b. Usage: modulus <a> <b>"""
        if len(args) != 2:
            return Fore.RED + "Error: modulus requires 2 arguments"
        try:
            result = self._perform_calculation('modulus', args[0], args[1])
            return f"{Fore.GREEN}Result: {result}"
        except (OperationError, ValidationError) as e:
            return f"{Fore.RED}Error: {e}"
    
    @help_decorator
    def _cmd_int_divide(self, args: list[str]) -> str:
        """Integer division of a by b. Usage: int_divide <a> <b>"""
        if len(args) != 2:
            return Fore.RED + "Error: int_divide requires 2 arguments"
        try:
            result = self._perform_calculation('int_divide', args[0], args[1])
            return f"{Fore.GREEN}Result: {result}"
        except (OperationError, ValidationError) as e:
            return f"{Fore.RED}Error: {e}"
    
    @help_decorator
    def _cmd_percent(self, args: list[str]) -> str:
        """Calculate (a/b)*100. Usage: percent <a> <b>"""
        if len(args) != 2:
            return Fore.RED + "Error: percent requires 2 arguments"
        try:
            result = self._perform_calculation('percent', args[0], args[1])
            return f"{Fore.GREEN}Result: {result}"
        except (OperationError, ValidationError) as e:
            return f"{Fore.RED}Error: {e}"
    
    @help_decorator
    def _cmd_abs_diff(self, args: list[str]) -> str:
        """Absolute difference between a and b. Usage: abs_diff <a> <b>"""
        if len(args) != 2:
            return Fore.RED + "Error: abs_diff requires 2 arguments"
        try:
            result = self._perform_calculation('abs_diff', args[0], args[1])
            return f"{Fore.GREEN}Result: {result}"
        except (OperationError, ValidationError) as e:
            return f"{Fore.RED}Error: {e}"
    
    @help_decorator
    def _cmd_history(self, args: list[str]) -> str:
        """Display calculation history. Usage: history"""
        history = self.history_manager.get_history()
        if not history:
            return Fore.YELLOW + "No calculations in history."
        
        output = [Fore.CYAN + "Calculation History:"]
        for i, calc in enumerate(history, 1):
            output.append(f"{Fore.WHITE}{i}. {calc}")
        return "\n".join(output)
    
    @help_decorator
    def _cmd_clear(self, args: list[str]) -> str:
        """Clear calculation history. Usage: clear"""
        self.caretaker.save_state()
        self.history_manager.clear_history()
        self.originator.set_history([])
        return Fore.GREEN + "History cleared."
    
    @help_decorator
    def _cmd_undo(self, args: list[str]) -> str:
        """Undo the last calculation. Usage: undo"""
        if self.caretaker.undo():
            history = self.originator.get_history()
            self.history_manager.set_history(history)
            if history:
                last = history[-1]
                return f"{Fore.GREEN}Undone: {last}"
            return Fore.GREEN + "Undone: History cleared"
        return Fore.YELLOW + "Nothing to undo."
    
    @help_decorator
    def _cmd_redo(self, args: list[str]) -> str:
        """Redo the last undone calculation. Usage: redo"""
        if self.caretaker.redo():
            history = self.originator.get_history()
            self.history_manager.set_history(history)
            if history:
                last = history[-1]
                return f"{Fore.GREEN}Redone: {last}"
            return Fore.GREEN + "Redone: History cleared"
        return Fore.YELLOW + "Nothing to redo."
    
    @help_decorator
    def _cmd_save(self, args: list[str]) -> str:
        """Save calculation history to CSV. Usage: save"""
        try:
            self.history_manager.save_to_csv()
            return Fore.GREEN + f"History saved to {self.config.history_file}"
        except Exception as e:
            return f"{Fore.RED}Error saving history: {e}"
    
    @help_decorator
    def _cmd_load(self, args: list[str]) -> str:
        """Load calculation history from CSV. Usage: load"""
        try:
            if self.history_manager.load_from_csv():
                self.originator.set_history(self.history_manager.get_history())
                return Fore.GREEN + f"History loaded from {self.config.history_file}"
            return Fore.YELLOW + "No history file found."
        except Exception as e:
            return f"{Fore.RED}Error loading history: {e}"
    
    @help_decorator
    def _cmd_help(self, args: list[str]) -> str:
        """Display available commands. Usage: help"""
        output = [Fore.CYAN + "Available Commands:"]
        output.append("")
        
        # Use decorator-registered commands for dynamic help
        commands = help_decorator.commands
        for cmd_name, description in sorted(commands.items()):
            output.append(f"{Fore.YELLOW}{cmd_name:15} {Fore.WHITE}- {description}")
        
        return "\n".join(output)
    
    @help_decorator
    def _cmd_exit(self, args: list[str]) -> str:
        """Exit the calculator. Usage: exit"""
        return "EXIT"
    
    def _process_command(self, command: str) -> Optional[str]:
        """
        Process a command.
        
        Args:
            command: Command string to process
            
        Returns:
            Response string or None
        """
        command = command.strip()
        if not command:
            return None
        
        parts = command.split()
        cmd_name = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        # Map command to method
        method_name = f"_cmd_{cmd_name}"
        if not hasattr(self, method_name):
            return f"{Fore.RED}Unknown command: {cmd_name}. Type 'help' for available commands."
        
        method = getattr(self, method_name)
        return method(args)
    
    def run(self):
        """Run the REPL interface."""
        print(f"{Fore.CYAN}{Style.BRIGHT}Enhanced Calculator")
        print(f"{Fore.WHITE}Type 'help' for available commands or 'exit' to quit.\n")
        
        while True:
            try:
                command = input(f"{Fore.GREEN}> ")
                result = self._process_command(command)
                
                if result == "EXIT":
                    print(f"{Fore.YELLOW}Goodbye!")
                    break
                elif result:
                    print(result)
            except KeyboardInterrupt:  # pragma: no cover
                print(f"\n{Fore.YELLOW}Goodbye!")
                break
            except EOFError:  # pragma: no cover
                print(f"\n{Fore.YELLOW}Goodbye!")
                break
            except Exception as e:  # pragma: no cover
                print(f"{Fore.RED}Unexpected error: {e}")
                self.logger.log_error(f"Unexpected error in REPL: {e}")


def main():  # pragma: no cover
    """Main entry point."""
    try:
        calculator = Calculator()
        calculator.run()
    except Exception as e:
        print(f"{Fore.RED}Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover
    main()

