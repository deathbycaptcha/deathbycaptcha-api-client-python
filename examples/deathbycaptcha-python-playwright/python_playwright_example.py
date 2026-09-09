import json
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

try:
    import deathbycaptcha
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
    import deathbycaptcha

load_dotenv(dotenv_path=Path(__file__).with_name('.env'))

USERNAME = os.getenv('DBC_USERNAME')
PASSWORD = os.getenv('DBC_PASSWORD')
CAPTCHA_URL = 'https://www.google.com/recaptcha/api2/demo'


def solve_captcha(captcha: dict):
    json_captcha = json.dumps(captcha)
    client = deathbycaptcha.SocketClient(USERNAME, PASSWORD)

    try:
        balance = client.get_balance()
        print('Balance: %s' % balance)

        print('Solving captcha...')
        client.is_verbose = True
        result = client.decode(type=4, token_params=json_captcha)

        return result.get('text')

    except Exception as e:
        print(f'DeathByCaptcha error: {e}')
        return None


def main():
    if not USERNAME or not PASSWORD:
        print('Missing credentials. Please set DBC_USERNAME and DBC_PASSWORD in .env')
        return

    is_github_actions = os.getenv('GITHUB_ACTIONS') == 'true'
    force_headless = os.getenv('HEADLESS', '0') == '1'
    run_headless = is_github_actions or force_headless

    wait_timeout = 30000 if run_headless else 10000
    print(f'Using wait timeout: {wait_timeout} ms')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=run_headless)
        context = browser.new_context()
        page = context.new_page()

        try:
            print(f'Navigating to {CAPTCHA_URL}...')
            page.goto(CAPTCHA_URL, timeout=60000)

            print('Looking for recaptcha-demo element...')
            page.wait_for_selector('#recaptcha-demo', timeout=wait_timeout)
            print('Element found')

            googlekey = page.get_attribute('#recaptcha-demo', 'data-sitekey')

            if not googlekey:
                print('Trying alternative method to get sitekey...')
                googlekey = page.evaluate(
                    "document.getElementById('recaptcha-demo').getAttribute('data-sitekey')"
                )

            print('GoogleKey: %s' % googlekey)

            if not googlekey:
                print('ERROR: Could not extract sitekey from page')
                return

            captcha = {
                'googlekey': googlekey,
                'pageurl': CAPTCHA_URL
            }

            solution = solve_captcha(captcha)
            if not solution:
                print('No captcha solution (maybe implement retry)...closing')
                return

            print('Solution: %s' % solution)
            page.evaluate(
                "document.getElementById('g-recaptcha-response').value='%s'" % solution
            )

            page.click('#recaptcha-demo-submit')

            time.sleep(2)

            try:
                success_element = page.query_selector('.recaptcha-success')
                if success_element:
                    print('SUCCESS: %s' % success_element.inner_text())
                else:
                    print('Success message not found')
            except Exception as e:
                print('Success message not found: %s' % str(e))

        except PlaywrightTimeout as e:
            print(f'Timeout error: {e}')
        except Exception as e:
            print(f'Error: {e}')
        finally:
            browser.close()


if __name__ == '__main__':
    main()
