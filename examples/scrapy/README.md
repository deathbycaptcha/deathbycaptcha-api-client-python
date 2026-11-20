# Scrapy downloader middleware example

This example shows how to intercept a cookie-based challenge in a Scrapy
spider, solve it with DeathByCaptcha and retry the request with the token
as a cookie.

It is an example to copy, not an installed package. Copy `middleware.py`
into your project (or add this directory to `PYTHONPATH`) and enable it in
your settings.

## Scope

- **Works without a browser:** Amazon WAF (type 16) and DataDome (type 21)
  when the service returns a cookie value.
- **Does not work without a browser:** reCAPTCHA and GeeTest. Scrapy does
  not execute JavaScript, so the middleware raises `EscalationRequired`
  and points to the Playwright samples.
- The token is never written to the crawl log; verbose mode stays off.

## Install

From the repository root:

```bash
pip install -e .
pip install -r examples/scrapy/requirements.txt
```

## Configure

In your Scrapy project's `settings.py`:

```python
DOWNLOADER_MIDDLEWARES = {
    "middleware.DeathByCaptchaMiddleware": 543,
}

DBC_USERNAME = "your_username"
DBC_PASSWORD = "your_password"
# or: DBC_AUTHTOKEN = "your_authtoken"

# Required for challenges tied to the exit IP: the crawler and the service
# must use the same proxy.
DBC_PROXY = "http://user:pass@127.0.0.1:1234"
DBC_PROXYTYPE = "HTTP"

DBC_MAX_RETRIES = 2
```

Put `middleware.py` where Python can import it, or add the directory to
`PYTHONPATH` and use the module path you chose.

## Run

```bash
scrapy runspider spider.py
```

The sample spider points at `https://example.com/protected`; change it to a
page you own or are allowed to crawl.

## How it works

1. `process_response` sees a 403/429/503 with Amazon WAF markers.
2. It extracts `sitekey`, `iv` and `context` from the page.
3. It calls `client.decode(type=16, waf_params=...)`.
4. It retries the request with `aws-waf-token` set as a cookie.
5. Retries are capped by `DBC_MAX_RETRIES`; there is no unbounded loop.

For DataDome, keep the same shape and send `datadome_params` instead.

## Limitations

- Do not use this middleware for token types that need a real browser;
  use the Playwright samples.
- The proxy is not optional for IP-bound challenges, even though the API
  accepts a request without one.
- A challenge that keeps coming back after the retries is dropped with a
  log line; it is not retried forever.
