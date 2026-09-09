# Playwright reCAPTCHA v2 Sample (Integrated)

This sample demonstrates how to solve Google reCAPTCHA v2 with Playwright using the `deathbycaptcha-official` client from this repository.

## What this sample does

- Opens Google's reCAPTCHA v2 demo page
- Extracts `data-sitekey`
- Requests a token from DeathByCaptcha (`type=4`)
- Injects the token into `g-recaptcha-response`
- Submits and validates the result

## Files

- `python_playwright_example.py` - runnable Playwright example
- `.env.example` - credentials template
- `requirements.txt` - Playwright-specific dependencies

## Prerequisites

- Python virtual environment active
- This package installed (`pip install -e .`)
- Playwright browsers installed (`playwright install`)

## Setup

From repo root:

```bash
pip install -e .
pip install -r examples/deathbycaptcha-python-playwright/requirements.txt
playwright install
cp examples/deathbycaptcha-python-playwright/.env.example examples/deathbycaptcha-python-playwright/.env
```

Edit `examples/deathbycaptcha-python-playwright/.env` and set:

```dotenv
DBC_USERNAME=your_username
DBC_PASSWORD=your_password
```

## Run

```bash
cd examples/deathbycaptcha-python-playwright
python python_playwright_example.py
```

## Optional environment variables

- `HEADLESS=1` to force headless mode locally

Example:

```bash
HEADLESS=1 python python_playwright_example.py
```

## Notes

- This is a functional sample for testing/integration workflows.
- Never commit real credentials in `.env`.
