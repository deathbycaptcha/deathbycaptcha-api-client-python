# Testing

This directory contains unit tests for the DeathByCaptcha Python client library.

## Running Tests Locally

### Prerequisites

```bash
pip install -e ".[dev]"
```

This installs the package in editable mode with development dependencies including `pytest` and `coverage`.

### Configuring Test Credentials

For integration tests that require API credentials:

1. **Copy the environment template:**
   ```bash
   cp .env.sample .env
   ```

2. **Edit `.env` and add your credentials:**
   ```bash
   DBC_TEST_USERNAME=your_username
   DBC_TEST_PASSWORD=your_password
   ```

3. **Alternative: Use environment variables directly:**
   ```bash
   export DBC_TEST_USERNAME=your_username
   export DBC_TEST_PASSWORD=your_password
   ```

⚠️ **Important:** The `.env` file is in `.gitignore` and will never be committed to version control. Keep your credentials secure!

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

- **test_integration_balance.py** - Integration tests (requires credentials)
  - Tests real API calls for get_balance() and get_user()
  - Tests both HTTP and Socket clients
  - Validates consistency between client types

- **test_image_captcha_integration.py** - Image CAPTCHA integration tests (requires credentials)
  - Uploads normal image CAPTCHAs (`type=0`) and polls for solutions
  - Tests both HTTP and Socket clients with polling backoff
  - Validates solution retrieval with exponential backoff
  - Runs only on Python 3.14 in GitHub Actions as a compatibility test

## CI/CD Integration

### GitHub Actions

The project includes `.github/workflows/tests.yml` which automatically runs tests on every push/PR:

#### Main Test Job
- Runs on Python versions: 3.10, 3.11, 3.12, 3.13, 3.14
- Runs full test suite with code coverage
- Uploads coverage reports

#### Special Test Jobs
- **test-python3-15**: Runs on Python 3.15 RC (continue-on-error)
- **test-image-captcha-python3-14**: Python 3.14 job that:
  - Runs complete test suite (all test files)
  - Generates comprehensive coverage report
  - Creates coverage badge for README
  - Tests all client functionality including:
    - Image CAPTCHA upload (type=0) with polling
    - Balance and user info retrieval
    - Error handling and edge cases
    - Both HTTP and Socket clients


The Python 3.14 job generates the coverage badge displayed in the README, showing overall test coverage across the entire codebase.

**Coverage Details for Python 3.14 Job:**
- Generates code coverage reports specifically for polling operations
- Coverage focus areas:
  - `deathbycaptcha.HttpClient.upload()` and polling loop
  - `deathbycaptcha.SocketClient.upload()` and polling loop  
  - Exponential backoff retry logic
  - Timeout and exception handling
  - Response parsing and data extraction

- Coverage artifacts generated:
  - **XML format** (coverage.xml) - for CI/CD integration
  - **HTML report** (htmlcov/) - for manual inspection
  - **Test report** (report.xml) - JUnit XML format

- Retained for **30 days** - allows tracking coverage trends over time

  **Why this coverage is valuable:**
  - Validates critical API interaction code
  - Ensures polling logic handles edge cases
  - Catches regressions in timeout handling
  - Tests async/timing operations thoroughly
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
from deathbycaptcha import HttpClient

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
