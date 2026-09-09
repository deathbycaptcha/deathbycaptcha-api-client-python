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
CAPTCHA_URL = os.getenv('AMAZON_WAF_URL', 'https://efw47fpad9.execute-api.us-east-1.amazonaws.com/latest')


def solve_waf_captcha(captcha: dict):
    json_captcha = json.dumps(captcha)
    client = deathbycaptcha.SocketClient(USERNAME, PASSWORD)

    try:
        balance = client.get_balance()
        print('Balance: %s' % balance)

        print('Solving Amazon WAF captcha...')
        client.is_verbose = True
        result = client.decode(type=16, waf_params=json_captcha)

        return result.get('text')

    except Exception as e:
        print(f'DeathByCaptcha error: {e}')
        return None


def extract_waf_params(page):
    sitekey = page.evaluate('''() => {
        const scripts = document.querySelectorAll('script');
        for (const script of scripts) {
            const text = script.textContent || '';
            const match = text.match(/key['":\s]+['"]([^'"]+)['"]/);
            if (match) return match[1];
        }
        const el = document.querySelector('[data-sitekey]');
        if (el) return el.getAttribute('data-sitekey');
        return null;
    }''')

    iv = page.evaluate('''() => {
        const scripts = document.querySelectorAll('script');
        for (const script of scripts) {
            const text = script.textContent || '';
            const match = text.match(/iv['":\s]+['"]([^'"]+)['"]/);
            if (match) return match[1];
        }
        return null;
    }''')

    context = page.evaluate('''() => {
        const scripts = document.querySelectorAll('script');
        for (const script of scripts) {
            const text = script.textContent || '';
            const match = text.match(/context['":\s]+['"]([^'"]+)['"]/);
            if (match) return match[1];
        }
        return null;
    }''')

    return sitekey, iv, context


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

            time.sleep(3)

            print('Extracting WAF parameters from page...')
            sitekey, iv, context_val = extract_waf_params(page)

            print('SiteKey: %s' % sitekey)
            print('IV: %s' % iv)
            print('Context: %s' % (context_val[:50] + '...' if context_val and len(context_val) > 50 else context_val))

            if not sitekey or not iv or not context_val:
                print('ERROR: Could not extract all required WAF parameters from page')
                print('Make sure the page contains Amazon WAF captcha')
                return

            captcha = {
                'sitekey': sitekey,
                'pageurl': CAPTCHA_URL,
                'iv': iv,
                'context': context_val
            }

            solution = solve_waf_captcha(captcha)
            if not solution:
                print('No captcha solution (maybe implement retry)...closing')
                return

            print('Solution: %s' % (solution[:50] + '...' if len(solution) > 50 else solution))

            page.context.add_cookies([{
                'name': 'aws-waf-token',
                'value': solution,
                'domain': page.url.split('/')[2],
                'path': '/'
            }])

            print('Token cookie set. Reloading page...')
            page.reload(timeout=60000)

            time.sleep(3)

            page_content = page.content()
            if 'captcha' not in page_content.lower():
                print('SUCCESS: Page loaded without captcha')
            else:
                print('Page still shows captcha - token may need retry')

        except PlaywrightTimeout as e:
            print(f'Timeout error: {e}')
        except Exception as e:
            print(f'Error: {e}')
        finally:
            browser.close()


if __name__ == '__main__':
    main()
