# GitHub Actions Configuration

## Required Secrets

The GitHub Actions workflows in this repository require the following secrets to be configured:

### DBC_USERNAME
Your DeathByCaptcha account username for running integration tests.

### DBC_PASSWORD
Your DeathByCaptcha account password for running integration tests.

## Setting Up Secrets

To configure these secrets in your GitHub repository:

1. Go to your repository on GitHub
2. Click on **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret:
   - Name: `DBC_USERNAME`
   - Value: Your DBC account username
   
   - Name: `DBC_PASSWORD`
   - Value: Your DBC account password

## How Secrets Are Used

The secrets are passed as environment variables to the test runner:

```yaml
- name: Run tests with coverage
  env:
    DBC_TEST_USERNAME: ${{ secrets.DBC_USERNAME }}
    DBC_TEST_PASSWORD: ${{ secrets.DBC_PASSWORD }}
  run: python -m pytest tests/ -v --cov=src/deathbycaptcha
```

The integration tests in `tests/test_integration_balance.py` will use these environment variables to authenticate with the DeathByCaptcha API.

## Workflows

##### 1. **test** - Full test matrix (Python 3.10-3.14)
- Runs standard test suite on all supported Python versions
- Full code coverage reporting:
  - Coverage percentage of entire codebase
  - HTML and XML coverage reports
  - JUnit test results
- Uploads coverage artifacts for 30 days

##### 2. **test-python3-15** - RC version compatibility
- Python 3.15 RC (release candidate)
- Allow-failure: doesn't block PRs if it fails
- Tests compatibility with upcoming Python versions

##### 3. **test-image-captcha-python3-14** - Python 3.14 coverage badge generation ⭐

**Purpose:** Generate comprehensive coverage badge from full test suite on Python 3.14

**What it tests:**
- Runs complete test suite (all test files)
- Generates coverage report for entire codebase
- Creates and commits coverage badge SVG
- Both HTTP and Socket client implementations
- Critical features:
  - Client initialization and authentication
  - Error handling (HTTP codes, socket errors)
  - Image detection and validation
  - Balance and user info retrieval
  - CAPTCHA upload and polling
  - Integration tests with real API

**Badge Generation:**
- Parses `coverage.xml` to calculate line coverage percentage
- Generates SVG badge with color coding:
  - Green (≥90%)
  - Yellow-green (≥75%)
  - Orange (≥60%)
  - Red (<60%)
- Commits badge to `.github/badges/coverage.svg`
- Displayed in README.md

**Coverage metrics:**
- Focuses on API interaction and polling code paths
- Modules covered:
  - `deathbycaptcha.HttpClient` - full polling flow
  - `deathbycaptcha.SocketClient` - socket-based polling
  - `deathbycaptcha.client` - core client logic
- Generates detailed coverage reports:
  - **coverage.xml** - Machine-readable coverage data (Cobertura format)
  - **htmlcov/** - Interactive HTML report with line-by-line coverage
  - **report.xml** - Test results (JUnit XML format)

**Why Python 3.14 specifically?**
- Newest stable Python version available at test time
- Validates that polling and async operations work on latest Python
- Tests for potential compatibility issues early
- Ensures edge cases in timing and backoff work correctly
- Canary test for upcoming Python releases

**Artifacts retained for 30 days:**
- Coverage reports enable tracking coverage trends
- Useful for identifying regressions in polling logic
- Can be analyzed if integration tests fail
- Async operations and timeouts correctly
## Coverage Reporting

The GitHub Actions workflows generate and upload coverage reports:

### Main Test Job Coverage
- Full coverage of entire test suite
- All modules analyzed
- Available in: `coverage-reports-py{version}` artifacts

### Python 3.14 Integration Coverage
- Specialized coverage focusing on API polling code
- Detailed metrics for HttpClient and SocketClient
- HTML report useful for identifying untested code paths
- Available in: `text-captcha-test-results-py3.14` artifact

**How to view coverage:**
1. Go to **Actions** → Select workflow run
2. Under **Artifacts**, download `text-captcha-test-results-py3.14`
3. Extract and open `htmlcov/index.html` in browser
4. View line-by-line coverage analysis
- Exponential backoff retry logic
- API polling and response handling

## Security Notes
## Additional Resources

- **[COVERAGE-GUIDE.md](COVERAGE-GUIDE.md)** - Detailed guide on understanding and interpreting coverage reports
  - How to download and view HTML coverage reports
  - Coverage metrics and what they mean
  - Tracking coverage trends over time
  - Integration with CI/CD tools

## Security Notes
- Never commit credentials directly to the repository
- Secrets are encrypted and only exposed to workflow runs
- Secret values are not visible in logs or to users without repository admin access
- Use test accounts with minimal balance for CI/CD testing
