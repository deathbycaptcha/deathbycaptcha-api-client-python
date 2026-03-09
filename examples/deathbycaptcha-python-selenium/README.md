# Selenium reCAPTCHA v2 Sample (Integrated)

This sample demonstrates how to solve Google reCAPTCHA v2 with Selenium using the `deathbycaptcha-official` client from this repository.

## What this sample does

- Opens Google's reCAPTCHA v2 demo page
- Extracts `data-sitekey`
- Requests a token from DeathByCaptcha (`type=4`)
- Injects the token into `g-recaptcha-response`
- Submits and validates the result

## Files

- `python_selenium_example.py` - runnable Selenium example
- `.env.example` - credentials template
- `requirements.txt` - Selenium-specific dependencies

## Prerequisites

- Python virtual environment active
- This package installed (`pip install -e .`)
- Browser + WebDriver installed
  - Firefox + geckodriver, or
  - Chrome + chromedriver

## Setup

From repo root:

```bash
pip install -e .
pip install -r examples/deathbycaptcha-python-selenium/requirements.txt
cp examples/deathbycaptcha-python-selenium/.env.example examples/deathbycaptcha-python-selenium/.env
```

Edit `examples/deathbycaptcha-python-selenium/.env` and set:

```dotenv
DBC_USERNAME=your_username
DBC_PASSWORD=your_password
```

## Run

```bash
cd examples/deathbycaptcha-python-selenium
python python_selenium_example.py
```

## Optional environment variables

- `BROWSER=firefox|chrome` (default: `firefox`)
- `HEADLESS=1` to force headless mode locally

Example:

```bash
BROWSER=chrome HEADLESS=1 python python_selenium_example.py
```

## Notes

- This is a functional sample for testing/integration workflows.
- Never commit real credentials in `.env`.
