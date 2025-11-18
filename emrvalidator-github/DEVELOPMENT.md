# Getting Started with EMRValidator Development

Complete guide for setting up EMRValidator for development and publishing to GitHub/PyPI.

## Quick Start for Users

```bash
# Install from PyPI (when published)
pip install emrvalidator

# Use the library
python
>>> from emrvalidator import DataValidator
>>> validator = DataValidator("My Validation")
```

## For Contributors

### 1. Clone and Setup

```bash
# Clone repository
git clone https://github.com/yourusername/emrvalidator.git
cd emrvalidator

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

### 2. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=emrvalidator --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
xdg-open htmlcov/index.html  # Linux
```

### 3. Code Formatting

```bash
# Format code
black emrvalidator tests examples

# Sort imports
isort emrvalidator tests examples

# Check with flake8
flake8 emrvalidator tests
```

### 4. Run Examples

```bash
# Run comprehensive examples
python examples/basic_usage.py

# Interactive testing
python
>>> from emrvalidator import DataValidator, DataProfiler
>>> import pandas as pd
>>> df = pd.read_csv('your_data.csv')
>>> validator = DataValidator("Test")
>>> validator.load_data(df)
```

## Project Structure

```
emrvalidator/
│
├── emrvalidator/              # Main package
│   ├── __init__.py           # Package initialization
│   ├── validator.py          # DataValidator class
│   ├── profiler.py           # DataProfiler class
│   ├── reporters.py          # Report generators
│   ├── rules.py              # Rules and expectations
│   └── py.typed             # Type hints marker
│
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── test_validator.py
│   ├── test_profiler.py
│   └── test_reporters.py
│
├── examples/                  # Usage examples
│   └── basic_usage.py
│
├── docs/                      # Documentation
│   ├── QUICKSTART.md
│   ├── COMPARISON.md
│   └── ...
│
├── .github/                   # GitHub specific
│   └── workflows/
│       ├── ci.yml            # CI pipeline
│       └── publish.yml       # PyPI publishing
│
├── .gitignore                # Git ignore rules
├── LICENSE                   # MIT License
├── README.md                 # Main documentation
├── CONTRIBUTING.md           # Contribution guide
├── CHANGELOG.md              # Version history
├── PUBLISHING.md             # PyPI publishing guide
├── pyproject.toml           # Package configuration
├── requirements.txt         # Dependencies
└── MANIFEST.in              # Package manifest
```

## Publishing to GitHub

### Initial Setup

1. **Create GitHub Repository**
   ```bash
   # On GitHub.com, create new repository: emrvalidator
   ```

2. **Push Code**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: EMRValidator v1.0.0"
   git branch -M main
   git remote add origin https://github.com/yourusername/emrvalidator.git
   git push -u origin main
   ```

3. **Add Repository Secrets**
   - Go to Settings → Secrets and variables → Actions
   - Add `PYPI_API_TOKEN`
   - Add `TEST_PYPI_API_TOKEN`

### Making Releases

1. **Update Version**
   ```bash
   # Edit pyproject.toml
   version = "1.1.0"
   
   # Update CHANGELOG.md
   ```

2. **Commit and Tag**
   ```bash
   git add pyproject.toml CHANGELOG.md
   git commit -m "Bump version to 1.1.0"
   git tag v1.1.0
   git push origin main --tags
   ```

3. **Create Release on GitHub**
   - Go to Releases → Create new release
   - Choose tag: v1.1.0
   - Add release notes from CHANGELOG.md
   - Publish release
   - GitHub Actions will automatically publish to PyPI

## Development Workflow

### Adding New Features

1. **Create Branch**
   ```bash
   git checkout -b feature/new-validator
   ```

2. **Make Changes**
   - Add feature code
   - Write tests
   - Update documentation

3. **Test**
   ```bash
   pytest
   black --check emrvalidator tests
   isort --check-only emrvalidator tests
   flake8 emrvalidator tests
   ```

4. **Commit and Push**
   ```bash
   git add .
   git commit -m "Add: New healthcare validator"
   git push origin feature/new-validator
   ```

5. **Create Pull Request**
   - Go to GitHub repository
   - Create Pull Request
   - Wait for CI checks to pass
   - Merge when approved

### Fixing Bugs

1. **Create Branch**
   ```bash
   git checkout -b fix/issue-123
   ```

2. **Fix and Test**
   ```bash
   # Make fix
   pytest tests/test_validator.py::test_specific_case
   ```

3. **Commit and PR**
   ```bash
   git add .
   git commit -m "Fix: Resolve issue #123"
   git push origin fix/issue-123
   ```

## CI/CD Pipeline

GitHub Actions automatically runs on:
- Push to `main` or `develop`
- Pull requests
- Release creation

### CI Pipeline (`ci.yml`)
- Runs on: Linux, macOS, Windows
- Python versions: 3.8, 3.9, 3.10, 3.11, 3.12
- Steps:
  1. Lint with flake8
  2. Check formatting (black, isort)
  3. Run tests with coverage
  4. Upload coverage to Codecov
  5. Security checks (bandit, safety)

### Publish Pipeline (`publish.yml`)
- Triggered on: Release publication
- Steps:
  1. Build package
  2. Check package (twine check)
  3. Publish to TestPyPI
  4. Publish to PyPI

## Common Tasks

### Update Dependencies

```bash
# Check for outdated packages
pip list --outdated

# Update specific package
pip install --upgrade pandas

# Update requirements
pip freeze > requirements.txt
```

### Generate Documentation

```bash
# Install sphinx (optional)
pip install sphinx sphinx-rtd-theme

# Generate docs
cd docs
sphinx-quickstart
sphinx-build -b html . _build
```

### Performance Testing

```python
import pandas as pd
import numpy as np
from emrvalidator import DataValidator
import time

# Create large dataset
n = 1_000_000
df = pd.DataFrame({
    'id': range(n),
    'value': np.random.rand(n)
})

# Time validation
start = time.time()
validator = DataValidator("Performance Test")
validator.load_data(df)
validator.expect_column_not_null('value')
end = time.time()

print(f"Validation time: {end - start:.2f}s")
```

## Troubleshooting

### Import Errors

```bash
# Reinstall in development mode
pip install -e ".[dev]"

# Check installation
pip show emrvalidator
```

### Test Failures

```bash
# Run specific test
pytest tests/test_validator.py::TestDataValidator::test_method

# Run with verbose output
pytest -v -s

# Run with pdb on failure
pytest --pdb
```

### Formatting Issues

```bash
# Auto-fix with black
black emrvalidator tests

# Auto-fix imports
isort emrvalidator tests
```

## Resources

- [GitHub Repository](https://github.com/yourusername/emrvalidator)
- [PyPI Package](https://pypi.org/project/emrvalidator/)
- [Issue Tracker](https://github.com/yourusername/emrvalidator/issues)
- [Discussions](https://github.com/yourusername/emrvalidator/discussions)

## Support

- **Bug Reports**: [GitHub Issues](https://github.com/yourusername/emrvalidator/issues)
- **Feature Requests**: [GitHub Issues](https://github.com/yourusername/emrvalidator/issues)
- **Questions**: [GitHub Discussions](https://github.com/yourusername/emrvalidator/discussions)
- **Email**: your-email@example.com

---


