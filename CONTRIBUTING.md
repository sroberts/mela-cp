# Contributing to mela-cp

Thank you for your interest in contributing to mela-cp! This document provides guidelines for contributing to the project.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/sroberts/mela-cp.git
cd mela-cp
```

2. Install in development mode with test dependencies:
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
