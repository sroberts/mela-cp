# Contributing to mela-cp

Thank you for your interest in contributing to mela-cp! This document provides guidelines for contributing to the project.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/sroberts/mela-cp.git
cd mela-cp
```

2. Install in development mode:
```bash
pip install -e .
```

3. Create a test database (for testing without actual Mela data):
```bash
python create_test_db.py
```

## Testing

Run the test suite:
```bash
python test_mcp_server.py
python test_server_setup.py
```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Add docstrings to all public functions and classes
- Keep functions focused and single-purpose

## Submitting Changes

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Test your changes thoroughly
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
