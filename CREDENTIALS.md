# Credentials Configuration Guide

This guide explains how to configure credentials for running tests in different environments.

## Quick Summary

| Environment | Credentials File | Method |
|------------|------------------|--------|
| **Local Development** | `.env` (local, not committed) | Environment variables from .env file |
| **gitlab-ci-local** | `.env` (local, not committed) | Load .env and pipe to gitlab-ci-local |
| **GitHub Actions** | Repository Secrets | `DBC_USERNAME`, `DBC_PASSWORD` secrets |
| **GitLab CI** | Project CI/CD Variables | `DBC_USERNAME`, `DBC_PASSWORD` variables |

## Local Development Setup

### Prerequisites
```bash
pip install python-dotenv
# Optional: gitlab-ci-local (for testing CI pipeline locally)
npm install -g @ezbz/gitlab-ci-local
```

### Configuration
1. Copy the sample file:
   ```bash
   cp .env.sample .env
   ```

2. Edit `.env` with your credentials:
   ```bash
   DBC_TEST_USERNAME=your_username
   DBC_TEST_PASSWORD=your_password
   ```

3. The `.env` file is in `.gitignore` - it won't be committed to git

4. Run tests:
   ```bash
   python -m pytest tests/ -v
   ```

### What happens
- `python-dotenv` loads variables from `.env` into environment
- Tests read `DBC_TEST_USERNAME` and `DBC_TEST_PASSWORD` from environment
- If credentials are missing, tests raise a clear error

## Testing GitLab CI Pipeline Locally

### Prerequisites
```bash
npm install -g @ezbz/gitlab-ci-local
```

### Quick Start

For testing the GitLab CI pipeline locally before pushing:

#### Recommended: Use the convenience script ⭐
```bash
./run-gitlab-ci-local.sh
```

This script:
- Loads credentials from `.env` file
- Passes them to `gitlab-ci-local` using `--variable` flags (required for Docker)
- Runs all jobs in the pipeline
- Shows logs in real-time

#### Alternative: Manual command with proper variable passing
```bash
# Load .env and export credentials for GitLab CI
set -a
source .env
set +a

# Pass variables using --variable flags (important for Docker!)
gitlab-ci-local \
  --file ./.gitlab-ci.yml \
  --variable "DBC_USERNAME=$DBC_TEST_USERNAME" \
  --variable "DBC_PASSWORD=$DBC_TEST_PASSWORD"
```

### Why --variable flags?

`gitlab-ci-local` runs jobs in Docker containers by default. Simply exporting environment variables in your shell won't pass them to the container. The `--variable` flag explicitly injects variables into the GitLab CI pipeline context, making them available inside the containers.

### What happens
- `gitlab-ci-local` simulates the GitLab CI environment locally
- Credentials are read from `.env` file and passed via `--variable` flags
- Pipeline jobs run in Docker containers (more accurate simulation)
- Artifacts and logs are saved locally for inspection
- You can see exactly what would happen on the real GitLab CI server

## GitHub Actions Setup

### Prerequisites
Already configured in `.github/workflows/tests.yml`

### Configuration
1. Go to your GitHub repository
2. **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add:
   - Name: `DBC_USERNAME`, Value: `your_username`
   - Name: `DBC_PASSWORD`, Value: `your_password`

### What happens
- GitHub Actions exposes secrets as environment variables
- Workflow passes them as `DBC_TEST_USERNAME` and `DBC_TEST_PASSWORD`
- Tests read from environment variables

## GitLab CI Setup

### Prerequisites
Configured in `.gitlab-ci.yml` variables section

### Configuration

#### Step 1: Set GitLab CI/CD Variables

1. Go to your GitLab project
2. **Settings** → **CI/CD** → **Variables**
3. Click **Add variable**

#### Step 2: Add DBC_USERNAME Variable
- **Key**: `DBC_USERNAME`
- **Value**: `your_username`
- **Type**: Variable
- **Scope**: All (or select specific branches)
- **Protect variable**: ✓ (Recommended)
- **Mask variable**: ✓ (Hides in logs)

#### Step 3: Add DBC_PASSWORD Variable
- **Key**: `DBC_PASSWORD`
- **Value**: `your_password`
- **Type**: Variable
- **Scope**: All
- **Protect variable**: ✓
- **Mask variable**: ✓

### What happens
- `.gitlab-ci.yml` defines `DBC_TEST_USERNAME: ${DBC_USERNAME}` etc.
- GitLab CI injects these variables into all jobs
- Tests read `DBC_TEST_USERNAME` and `DBC_TEST_PASSWORD` from environment

### Verification
1. Go to CI/CD → Pipelines
2. Click a job
3. Check "Logs" - variables should be masked if you checked "Mask variable"

## Environment Variable Mapping

The tests always expect these variable names:
- `DBC_TEST_USERNAME` - Account username
- `DBC_TEST_PASSWORD` - Account password

Each CI/CD platform maps its credentials to these:

**GitHub Actions:**
```yaml
env:
  DBC_TEST_USERNAME: ${{ secrets.DBC_USERNAME }}
  DBC_TEST_PASSWORD: ${{ secrets.DBC_PASSWORD }}
```

**GitLab CI:**
```yaml
variables:
  DBC_TEST_USERNAME: ${DBC_USERNAME}
  DBC_TEST_PASSWORD: ${DBC_PASSWORD}
```

**Local:**
```bash
# .env file
DBC_TEST_USERNAME=...
DBC_TEST_PASSWORD=...
```

## Testing Your Configuration

### Local Test
```bash
# Should work with .env configured
python -m pytest tests/test_integration_balance.py -v
```

### GitHub Actions Test
Push to branch and check **Actions** tab

### GitLab CI Test
1. Push to branch
2. Go to **CI/CD** → **Pipelines**
3. Check job logs for your test results

## Troubleshooting

### "Missing credentials" error

**Cause**: Environment variables `DBC_TEST_USERNAME` and `DBC_TEST_PASSWORD` are not set

**Solution for local:**
- Ensure `.env` file exists and is readable
- Check credentials are correct
- Verify `python-dotenv` is installed

**Solution for GitHub Actions:**
- Go to **Settings** → **Secrets and variables** → **Actions**
- Verify `DBC_USERNAME` and `DBC_PASSWORD` are configured
- Trigger a new workflow run

**Solution for GitLab CI:**
- Go to **Settings** → **CI/CD** → **Variables**
- Verify `DBC_USERNAME` and `DBC_PASSWORD` are configured
- Check variable scope (should include current branch)
- Manually trigger pipeline in **CI/CD** → **Pipelines** → **Run pipeline**

### Tests pass locally but fail in CI

This usually means:
1. Local `.env` has different (valid) credentials than CI variables
2. Check both `.env` and CI/CD variables have same values
3. Or CI credentials are missing/empty

### Variables not appearing in CI logs

This is normal behavior when **Mask variable** is enabled. This is secure - values are hidden from logs.

## Security Best Practices

1. **Use test accounts** - Never use production accounts in CI
2. **Limit balance** - Use test accounts with minimal balance to prevent accidents
3. **Rotate regularly** - Change credentials periodically
4. **Use protected branches** - Restrict secret usage to protected branches only
5. **Mask secrets** - Always check "Mask variable" in CI/CD settings
6. **GitIgnore local secrets** - Never commit `.env` to git
7. **Review logs** - Check that variable values are masked in CI output

## Files Reference

- [`.env.sample`](.env.sample) - Template for local credentials
- [`.env`](.env) - Local credentials (in `.gitignore`, not committed)
- [`.github/workflows/tests.yml`](.github/workflows/tests.yml) - GitHub Actions config
- [`.gitlab-ci.yml`](.gitlab-ci.yml) - GitLab CI config
- [`.github/ACTIONS.md`](.github/ACTIONS.md) - GitHub Actions documentation
- [`.gitlab/README.md`](.gitlab/README.md) - GitLab CI documentation
- [`tests/README.md`](tests/README.md) - Testing documentation

## Support

For issues with credentials or CI/CD setup:
1. Check the appropriate README in `.github/` or `.gitlab/`
2. Verify credentials are configured in the right place
3. Check environment variable names match exactly
4. Review CI/CD logs for error messages
