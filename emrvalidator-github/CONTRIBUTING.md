# Contributing to EMRValidator

Thank you for your interest in contributing to EMRValidator! This document provides guidelines and steps for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/yourusername/emrvalidator/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Python version and OS
   - Sample code if applicable

### Suggesting Features

1. Check [existing feature requests](https://github.com/yourusername/emrvalidator/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement)
2. Create a new issue with:
   - Clear description of the feature
   - Use case and benefits
   - Possible implementation approach

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/emrvalidator.git
   cd emrvalidator
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

4. **Make your changes**
   - Write clear, documented code
   - Follow existing code style
   - Add tests for new features
   - Update documentation as needed

5. **Run tests**
   ```bash
   # Run all tests
   pytest

   # Run with coverage
   pytest --cov=emrvalidator --cov-report=html

   # Check code style
   black emrvalidator tests
   isort emrvalidator tests
   flake8 emrvalidator tests
   ```

6. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

   Commit message format:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for updates to existing features
   - `Docs:` for documentation changes
   - `Test:` for test additions or changes
   - `Refactor:` for code refactoring

7. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a Pull Request on GitHub

## Development Guidelines

### Code Style

- Follow PEP 8 style guide
- Use type hints where appropriate
- Maximum line length: 100 characters
- Use descriptive variable names
- Add docstrings to all functions and classes

Example:
```python
def expect_column_not_null(
    self, 
    column: str, 
    threshold: float = 1.0, 
    critical: bool = True
) -> 'DataValidator':
    """
    Check for null values in column
    
    Args:
        column: Column name to check
        threshold: Minimum non-null percentage (0.0 to 1.0)
        critical: Whether this is a critical validation
        
    Returns:
        Self for method chaining
    """
```

### Testing

- Write tests for all new features
- Maintain or improve code coverage
- Use pytest fixtures for common test data
- Test edge cases and error conditions

Example test:
```python
def test_expect_column_not_null(sample_data):
    """Test null value check"""
    validator = DataValidator("Test")
    validator.load_data(sample_data)
    
    validator.expect_column_not_null('mrn', threshold=1.0)
    
    results = validator.get_results()
    assert results['summary']['passed'] == 1
```

### Documentation

- Update README.md for user-facing changes
- Add docstrings to all new functions/classes
- Update examples if API changes
- Add entries to CHANGELOG.md

### Healthcare-Specific Features

When adding healthcare validators:
- Follow HIPAA compliance guidelines
- Use industry-standard formats (ICD, CPT, etc.)
- Document healthcare-specific terminology
- Add examples with synthetic healthcare data

## Project Structure

```
emrvalidator/
├── emrvalidator/           # Main package
│   ├── __init__.py
│   ├── validator.py        # Core validator
│   ├── profiler.py         # Data profiler
│   ├── reporters.py        # Report generators
│   └── rules.py           # Rules and expectations
├── tests/                  # Test suite
├── examples/              # Usage examples
├── docs/                  # Documentation
└── .github/               # GitHub Actions
```

## Adding New Validators

To add a new validation method to DataValidator:

```python
def expect_your_validation(
    self, 
    column: str, 
    threshold: float = 1.0, 
    critical: bool = True
) -> 'DataValidator':
    """Your validation description"""
    
    if column not in self.data.columns:
        result = {
            "rule": "your_validation",
            "column": column,
            "critical": critical,
            "passed": False,
            "message": f"Column '{column}' does not exist"
        }
        self._record_result(result)
        return self
    
    # Your validation logic here
    valid_mask = ...  # Create boolean mask
    valid_pct = valid_mask.sum() / len(self.data)
    passed = valid_pct >= threshold
    
    result = {
        "rule": "your_validation",
        "column": column,
        "critical": critical,
        "passed": passed,
        "valid_percentage": round(valid_pct * 100, 2),
        "threshold": threshold * 100,
        "message": f"Your message: {valid_pct*100:.2f}%"
    }
    self._record_result(result)
    return self
```

Don't forget to:
1. Add tests in `tests/test_validator.py`
2. Update README.md with usage example
3. Add to `__all__` if creating new classes

## Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md with changes
3. Create release on GitHub
4. GitHub Actions will automatically publish to PyPI

## Questions?

- Open an issue for questions
- Join discussions on GitHub Discussions
- Email: your-email@example.com

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to EMRValidator! 🎉
