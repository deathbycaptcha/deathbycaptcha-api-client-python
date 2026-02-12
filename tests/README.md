# Testing

This directory contains unit tests for the DeathByCaptcha Python client library.

## Running Tests Locally

### Prerequisites

```bash
pip install -e ".[dev]"
```

This installs the package in editable mode with development dependencies including `pytest` and `coverage`.

### Using unittest (built-in)

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```

### Using pytest (recommended)

```bash
pytest tests/ -v
pytest tests/ -v --cov=src/deathbycaptcha --cov-report=html
```

## Test Coverage

Current test coverage includes:

- **test_imports.py** - Module imports and client initialization
  - `TestImports` - Verifies all modules can be imported
  - `TestClientInstantiation` - Tests client class instantiation
  - `TestFastImghdr` - Tests fast_imghdr module functions

- **test_image_detection.py** - Image format detection
  - Tests for PNG, JPEG, GIF, BMP, WebP and unknown formats
  - Validates magic byte detection

- **test_constants.py** - Configuration constants
  - Validates API version, timeouts, and other constants
  - Ensures configuration values are within expected ranges

## CI/CD Integration

### GitLab CI

The project includes a `.gitlab-ci.yml` file that automatically runs tests on:

- Python 3.11
- Python 3.12
- Python 3.13
- Python 3.14
- Python 3.15 (RC)

Tests are run with:
- Code coverage reports
- Multiple dependency versions

To run locally the same way GitLab would:

```bash
# Create a clean Python 3.13 environment
python3.13 -m venv test_venv
source test_venv/bin/activate
pip install -e ".[dev]"
python -m pytest tests/ -v --cov=src/deathbycaptcha
```

## Writing New Tests

1. Create a new test file in the `tests/` directory with prefix `test_`
2. Import unittest and required modules
3. Create test classes inheriting from `unittest.TestCase`
4. Write test methods prefixed with `test_`

Example:

```python
import unittest
from deathbycaptcha.deathbycaptcha import HttpClient

class TestMyFeature(unittest.TestCase):
    def test_something(self):
        client = HttpClient("user", "pass")
        self.assertIsNotNone(client)
```

Then run with:
```bash
python -m unittest tests.test_myfeature -v
```

## Coverage Reports

After running tests with pytest and coverage:

```bash
pytest tests/ --cov=src/deathbycaptcha --cov-report=html
open htmlcov/index.html  # View coverage report in browser
```

## Troubleshooting

### "No module named 'deathbycaptcha'"

Install the package in editable mode:
```bash
pip install -e .
```

### Tests failing with import errors

Make sure you're running from the project root:
```bash
cd /path/to/deathbycaptcha-api-client-python
python -m unittest discover -s tests -p 'test_*.py'
```

### Module not found when running individual test files

Run using the module syntax instead:
```bash
python -m unittest tests.test_imports -v
```

Not:
```bash
python tests/test_imports.py  # This may fail
```
