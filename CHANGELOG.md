# Changelog

All notable changes to this project will be documented in this file.

## [4.7.1] - 2026-03-09

### Added
- Integrated Selenium reCAPTCHA v2 sample from `deathbycaptcha-python-selenium` repository
  - Located at `examples/deathbycaptcha-python-selenium/`
  - Includes improved script with browser selection (Firefox/Chrome) and headless mode support
  - Dedicated README with setup and usage instructions
- GitHub Actions workflow for Selenium sample validation (`.github/workflows/selenium-sample.yml`)
  - Validates syntax and imports on every push/PR
  - Runs live Selenium test when DBC secrets are configured
  - Uploads debug artifacts (screenshots, logs)
- GitHub Actions workflow for automatic PyPI publishing (`.github/workflows/publish.yml`)
  - Triggers on GitHub releases
  - Verifies version tag matches `pyproject.toml`
  - Publishes package to PyPI using API token
- Table of contents (index) in main README for easier navigation
- Featured section in README highlighting Selenium sample with quick start instructions
- Documentation for `PYPI_API_TOKEN` secret in `CREDENTIALS.md`

### Changed
- README badges section now includes:
  - Selenium Sample workflow status
  - Publish to PyPI workflow status
- Selenium sample script enhanced with:
  - Automatic fallback to import from `src/` if package not installed
  - Environment variable support for `BROWSER` and `HEADLESS` mode
  - Improved error handling and missing import fixes

## [4.7.0] - 2026-02-11

### Added
- Support for Python 3.13
- Support for Python 3.14
- Support for Python 3.15
- `.env.sample` template for integration-test credentials
- Local helper script `run-gitlab-ci-local.sh` for running GitLab CI jobs with credentials from `.env`
- Agent and CI documentation for credentials setup:
	- `CREDENTIALS.md`
	- `.github/ACTIONS.md`
	- `.gitlab/README.md`
	- `.github/COVERAGE-GUIDE.md`
- Python 3.14 specialized image CAPTCHA integration test (`type=0`) with polling flow validation
- Repository-hosted coverage badge SVG at `.github/badges/coverage.svg`

### Changed
- Integration tests now load credentials from environment variables (`DBC_TEST_USERNAME` / `DBC_TEST_PASSWORD`) instead of hardcoded values
- GitHub Actions test workflow updated to:
	- consume repository secrets (`DBC_USERNAME` / `DBC_PASSWORD`)
	- run Python 3.14 image CAPTCHA integration coverage job
	- generate and publish coverage badge without external services
- GitLab CI updated to map CI variables into test variables for credential-based integration tests
- Test documentation updated to reflect env-based credentials and CI behavior
