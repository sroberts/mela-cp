# Contributing to mela-cp

Thank you for your interest in contributing to mela-cp! This document provides guidelines for contributing to the project.

## Development Setup

### Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer that avoids externally managed environment issues.

1. Install uv if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Clone the repository:
```bash
git clone https://github.com/sroberts/mela-cp.git
cd mela-cp
```

3. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate  # On macOS/Linux
# Or on Windows: .venv\Scripts\activate
```

4. Install in development mode with test dependencies:
```bash
uv pip install -e ".[test]"
```

### Using pip

If you prefer to use pip:

1. Clone the repository:
```bash
git clone https://github.com/sroberts/mela-cp.git
cd mela-cp
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# Or on Windows: .venv\Scripts\activate
```

3. Install in development mode with test dependencies:
```bash
pip install -e ".[test]"
```

## Testing

### Running Tests

Run the full test suite:
```bash
pytest tests/ -v
```

Run specific test files:
```bash
pytest tests/test_database.py -v
pytest tests/test_server.py -v
```

Run tests with coverage:
```bash
# Using uv (recommended)
uv pip install pytest-cov
pytest tests/ --cov=src/mela_cp --cov-report=term-missing

# Or using pip
pip install pytest-cov
pytest tests/ --cov=src/mela_cp --cov-report=term-missing
```

### Writing Tests

- Place new tests in the `tests/` directory
- Follow the existing test structure and naming conventions
- Use pytest fixtures from `tests/conftest.py` for test databases
- Write descriptive test names that explain what is being tested
- Test both success and error cases
- Aim for high test coverage of new code

### Test Structure

- `tests/conftest.py` - Shared fixtures (test databases)
- `tests/test_database.py` - Tests for database operations
- `tests/test_server.py` - Tests for MCP server functionality

## Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Add docstrings to all public functions and classes
- Keep functions focused and single-purpose

## Continuous Integration

Tests run automatically on:
- Push to main branch or copilot/** branches
- Pull requests to main
- Python versions: 3.10, 3.11, 3.12
- Operating systems: Ubuntu, macOS

All tests must pass before merging.

## Submitting Changes

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Run tests to ensure nothing breaks: `pytest tests/ -v`
5. Submit a pull request with a clear description of the changes

## Reporting Issues

If you encounter any issues or have suggestions for improvements:

1. Check if the issue already exists
2. Create a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, etc.)

## Questions

For questions about the project, please open an issue or discussion on GitHub.
