# GitLab CI/CD Configuration Guide

This project uses GitLab CI/CD for automated testing. To run the tests successfully, you need to configure certain variables.

## Quick Start with gitlab-ci-local

If you want to test the CI pipeline locally before pushing:

### Option 1: Using the convenience script (Recommended) ⭐

```bash
./run-gitlab-ci-local.sh
```

This script automatically:
- ✓ Loads credentials from `.env`
- ✓ Verifies credentials are set
- ✓ Passes them to GitLab CI pipeline using `--variable` flags
- ✓ Runs pipeline jobs in Docker containers (if Docker available)
- ✓ Shows real-time logs and test outputs

**Note:** The script uses `--variable` flag because `gitlab-ci-local` runs jobs in Docker, and environment variables set in the host shell won't automatically pass to the container.

### Option 2: Manual command with --variable flags

```bash
# Load .env and export
set -a
source .env
set +a

# Run with --variable flags
gitlab-ci-local \
  --file ./.gitlab-ci.yml \
  --variable "DBC_USERNAME=$DBC_TEST_USERNAME" \
  --variable "DBC_PASSWORD=$DBC_TEST_PASSWORD"
```

### Option 3: Advanced - using gitlab-ci-local directly

```bash
# If you prefer to set variables differently
export DBC_USERNAME=your_username
export DBC_PASSWORD=your_password
gitlab-ci-local --file ./.gitlab-ci.yml
```

**Note:** Option 3 may not work reliably with Docker since environment variables from the host shell may not reach the container. Use Option 1 or 2 instead.

## Required CI/CD Variables

The following variables must be configured in your GitLab project:

### DBC_USERNAME
Your DeathByCaptcha account username for running integration tests.

### DBC_PASSWORD
Your DeathByCaptcha account password for running integration tests.

## Setting Up Variables in GitLab

### Method 1: Via GitLab Web UI (Recommended)

1. Go to your GitLab project
2. Navigate to **Settings** → **CI/CD** → **Variables**
3. Click **Add variable**
4. For each variable:
   - **Key**: `DBC_USERNAME` (or `DBC_PASSWORD`)
   - **Value**: Your credentials
   - **Type**: Variable
   - **Scope**: All (or specific branch)
   - **Protect variable**: ✓ (Recommended for security)
   - **Mask variable**: ✓ (Hides value in CI/CD logs)

### Method 2: Via `.gitlab-ci.yml`

⚠️ **NOT RECOMMENDED** - Don't commit credentials to git!

## How Variables Are Used

The `.gitlab-ci.yml` file automatically passes these variables to all test jobs:

```yaml
variables:
  DBC_TEST_USERNAME: ${DBC_USERNAME}
  DBC_TEST_PASSWORD: ${DBC_PASSWORD}
```

These are then used by the tests in `tests/test_integration_balance.py`:

```python
username = os.getenv('DBC_TEST_USERNAME')
password = os.getenv('DBC_TEST_PASSWORD')
```

## CI/CD Pipeline

The pipeline runs:
- **test:python3.11** - Primary Python version
- **test:python3.12** - LTS version
- **test:python3.13** - Latest stable
- **test:python3.14** - Beta version (allow failure)
- **test:python3.15** - RC version (allow failure)
- **unittest** - Alternative test runner
- **test:minimal_deps** - Tests with minimal dependency versions

Each job:
- Runs the full test suite with coverage
- Uploads coverage reports (HTML, XML, Cobertura)
- Stores test artifacts for 30 days

## Running Tests Locally

For local testing, create a `.env` file:

```bash
cp .env.sample .env
# Edit .env with your credentials
python -m pytest tests/ -v
```

The `.env` file is in `.gitignore` and won't be committed.

## Security Best Practices

- ✅ Use **Protected** variables to restrict to protected branches only
- ✅ **Mask** sensitive variables to hide them in logs
- ✅ Use test accounts with minimal balance
- ✅ Rotate credentials regularly
- ✅ Review CI/CD logs carefully before sharing

## Troubleshooting

### Tests fail with "Missing credentials" error

This means `DBC_USERNAME` and `DBC_PASSWORD` environment variables are not set. Check:
1. Variables are configured in **Settings → CI/CD → Variables**
2. Variable scope includes the current branch
3. Pipeline was run after variables were configured (may need to re-run)

### Variables not appearing in logs

This is expected if you checked **Mask variable**. This is the secure behavior.

### Local tests work but CI tests fail

Check that:
1. `.env` file exists locally (not committed to git)
2. Same credentials are configured in GitLab CI/CD variables
3. Credentials are valid and have sufficient balance

## Notes

- Integration tests that require credentials are in `tests/test_integration_balance.py`
- Other unit tests don't require credentials and always run
- GitLab CI runs all tests; failures are reported but don't block the pipeline if marked `allow_failure: true`
