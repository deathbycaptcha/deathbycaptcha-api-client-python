"""Integration test for Playwright reCAPTCHA v2 solving.

This test demonstrates:
1. Launching a browser with Playwright
2. Extracting the reCAPTCHA sitekey from the page
3. Requesting a token from DeathByCaptcha API
4. Injecting the token and submitting the form
5. Verifying successful verification
"""

import json
import os
import time
import unittest

from deathbycaptcha import HttpClient, SocketClient, AccessDeniedException

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    raise unittest.SkipTest("Playwright not installed: pip install playwright")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class TestPlaywrightIntegration(unittest.TestCase):
    """Integration tests for Playwright reCAPTCHA v2 solving."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.username = os.getenv('DBC_TEST_USERNAME')
        cls.password = os.getenv('DBC_TEST_PASSWORD')
        if not cls.username or not cls.password:
            raise unittest.SkipTest(
                "Skipping Playwright integration tests: missing DBC_TEST_USERNAME/DBC_TEST_PASSWORD"
            )

    def _skip_if_insufficient_funds(self, err: Exception):
        message = str(err).lower()
        if 'insufficient-funds' in message or 'low balance' in message or 'check your credentials and/or balance' in message:
            self.skipTest('Skipping Playwright integration test: insufficient funds')
        raise err

    def _run_playwright_test(self, client_class):
        """Run the Playwright reCAPTCHA v2 test with the given client class."""
        page_url = os.getenv('DBC_PLAYWRIGHT_PAGE_URL',
                             'https://www.google.com/recaptcha/api2/demo')
        headless = os.getenv('DBC_PLAYWRIGHT_HEADLESS', 'true').lower() in ('true', '1', 'yes')

        print(f"[PLAYWRIGHT-IT] pageUrl={page_url}")
        print(f"[PLAYWRIGHT-IT] headless={headless}")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless)
            context = browser.new_context()
            page = context.new_page()

            try:
                print("[PLAYWRIGHT-IT] navigating to page...")
                page.goto(page_url, timeout=60000)

                print("[PLAYWRIGHT-IT] looking for recaptcha-demo element...")
                page.wait_for_selector('#recaptcha-demo', timeout=20000)
                print("[PLAYWRIGHT-IT] recaptcha container found")

                googlekey = page.get_attribute('#recaptcha-demo', 'data-sitekey')
                if not googlekey:
                    googlekey = page.evaluate(
                        "document.getElementById('recaptcha-demo').getAttribute('data-sitekey')"
                    )

                self.assertIsNotNone(googlekey, "Could not extract sitekey from page")
                self.assertGreater(len(googlekey), 0, "Sitekey should not be empty")
                print(f"[PLAYWRIGHT-IT] sitekey-length={len(googlekey)}")

                captcha_params = json.dumps({
                    'googlekey': googlekey,
                    'pageurl': page_url
                })

                client = client_class(self.username, self.password)
                try:
                    print("[PLAYWRIGHT-IT] requesting token from DBC")
                    try:
                        solution = client.decode(
                            timeout=90,
                            type=4,
                            token_params=captcha_params
                        )
                    except AccessDeniedException as err:
                        self._skip_if_insufficient_funds(err)

                    self.assertIsNotNone(solution)
                    token = solution.get('text', '')
                    self.assertGreater(len(token), 0, "Token should not be empty")
                    print(f"[PLAYWRIGHT-IT] token received captchaId={solution.get('captcha')} token-length={len(token)}")

                    page.evaluate(
                        "value => document.getElementById('g-recaptcha-response').value = value",
                        token
                    )
                    print("[PLAYWRIGHT-IT] token injected into g-recaptcha-response")

                    page.click('#recaptcha-demo-submit')
                    print("[PLAYWRIGHT-IT] submit clicked")

                    page.wait_for_selector('.recaptcha-success', timeout=15000)
                    success_text = page.text_content('.recaptcha-success') or ''
                    self.assertIn('Verification Success', success_text)
                    print(f"[PLAYWRIGHT-IT] successText='{success_text}'")
                    print("[PLAYWRIGHT-IT] PASS")

                finally:
                    client.close()
                    print("[PLAYWRIGHT-IT] END")

            finally:
                browser.close()

    def test_playwright_recaptcha_v2_http(self):
        """Test reCAPTCHA v2 solving using HTTP client with Playwright."""
        self._run_playwright_test(HttpClient)

    def test_playwright_recaptcha_v2_socket(self):
        """Test reCAPTCHA v2 solving using Socket client with Playwright."""
        self._run_playwright_test(SocketClient)


if __name__ == '__main__':
    unittest.main()
