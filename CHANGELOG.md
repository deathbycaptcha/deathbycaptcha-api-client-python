# Changelog

All notable changes to this project will be documented in this file.

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
