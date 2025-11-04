# Enhanced Calculator Application

A feature-rich calculator application implementing multiple design patterns including Factory, Observer, Memento, and Decorator patterns.

## Features

- **Additional Arithmetic Operations**: Power, Root, Modulus, Integer Division, Percentage, Absolute Difference
- **Undo/Redo Functionality**: Memento Pattern implementation
- **Observer Pattern**: Automatic logging and auto-save functionality
- **Configuration Management**: Environment-based configuration using .env file
- **Comprehensive Error Handling**: Custom exceptions and input validation
- **History Management**: CSV-based persistence using pandas
- **Command-Line Interface**: REPL-based interactive calculator
- **Unit Testing**: 90%+ test coverage with pytest
- **CI/CD**: GitHub Actions workflow for automated testing

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd calculator_enhanced
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration Setup

1. Create a `.env` file in the project root:
```bash
cp .env.example .env
```

2. Configure the `.env` file with your settings:
```
CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=10
CALCULATOR_MAX_INPUT_VALUE=1e308
CALCULATOR_DEFAULT_ENCODING=utf-8
```

The application will create necessary directories automatically.

## Usage

Run the calculator:
```bash
python -m app.calculator
```

### Available Commands

- `add <a> <b>` - Add two numbers
- `subtract <a> <b>` - Subtract b from a
- `multiply <a> <b>` - Multiply two numbers
- `divide <a> <b>` - Divide a by b
- `power <a> <b>` - Raise a to the power of b
- `root <a> <b>` - Calculate the bth root of a
- `modulus <a> <b>` - Compute a modulo b
- `int_divide <a> <b>` - Integer division of a by b
- `percent <a> <b>` - Calculate (a/b) * 100
- `abs_diff <a> <b>` - Absolute difference between a and b
- `history` - Display calculation history
- `clear` - Clear calculation history
- `undo` - Undo the last calculation
- `redo` - Redo the last undone calculation
- `save` - Manually save calculation history to CSV
- `load` - Load calculation history from CSV
- `help` - Display available commands
- `exit` - Exit the application

### Example Usage

```
> add 5 3
Result: 8.0

> power 2 8
Result: 256.0

> history
1. add(5, 3) = 8.0
2. power(2, 8) = 256.0

> undo
Undone: power(2, 8) = 256.0

> redo
Redone: power(2, 8) = 256.0
```

## Testing

Run tests with pytest:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=app --cov-report=html
```

View coverage report:
```bash
open htmlcov/index.html  # On macOS/Linux
```

## CI/CD

The project includes a GitHub Actions workflow (`.github/workflows/python-app.yml`) that:
- Runs tests on every push to main branch
- Runs tests on pull requests
- Enforces 90% test coverage threshold
- Automatically fails if coverage is below 90%

## Project Structure

```
calculator_enhanced/
├── app/
│   ├── __init__.py
│   ├── calculator.py          # Main Calculator class with REPL
│   ├── calculation.py          # Calculation data model
│   ├── calculator_config.py    # Configuration management
│   ├── calculator_memento.py   # Memento Pattern for Undo/Redo
│   ├── exceptions.py           # Custom exceptions
│   ├── history.py              # History management with pandas
│   ├── input_validators.py     # Input validation
│   ├── operations.py           # Operations with Factory Pattern
│   └── logger.py               # Logging functionality
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py
│   ├── test_calculation.py
│   ├── test_operations.py
│   └── ...
├── .env                        # Environment configuration
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── .github/
    └── workflows/
        └── python-app.yml      # CI/CD workflow
```

## Design Patterns

- **Factory Pattern**: Used for creating operation instances
- **Observer Pattern**: LoggingObserver and AutoSaveObserver for event handling
- **Memento Pattern**: Undo/Redo functionality
- **Decorator Pattern**: Dynamic help menu generation

## License

This project is for educational purposes.

