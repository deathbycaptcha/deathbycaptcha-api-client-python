"""Scrapy downloader middleware example for DeathByCaptcha.

Copy this file into your project, or add this directory to PYTHONPATH, and
enable the class in ``DOWNLOADER_MIDDLEWARES``.

Scope: cookie-based challenges. The example handles Amazon WAF (type 16);
DataDome (type 21) follows the same shape with ``datadome_params``. Scrapy
does not execute JavaScript, so reCAPTCHA and GeeTest need a browser: the
middleware raises ``EscalationRequired`` instead of pretending to solve them.

The token is never logged.
"""

import json
import re

import deathbycaptcha
from scrapy import signals


class EscalationRequired(Exception):
    """Raised when the challenge needs a browser, which Scrapy does not have."""


class DeathByCaptchaMiddleware:
    def __init__(
        self,
        username=None,
        password=None,
        authtoken=None,
        proxy=None,
        proxytype=None,
        max_retries=2,
    ):
        if authtoken:
            self.client = deathbycaptcha.HttpClient(None, None, authtoken)
        else:
            self.client = deathbycaptcha.HttpClient(username, password)

        # Never dump credentials or tokens to the crawl log.
        self.client.is_verbose = False
        self.proxy = proxy
        self.proxytype = proxytype
        self.max_retries = max_retries

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        middleware = cls(
            username=settings.get("DBC_USERNAME"),
            password=settings.get("DBC_PASSWORD"),
            authtoken=settings.get("DBC_AUTHTOKEN"),
            proxy=settings.get("DBC_PROXY"),
            proxytype=settings.get("DBC_PROXYTYPE"),
            max_retries=settings.getint("DBC_MAX_RETRIES", 2),
        )
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    def spider_closed(self, spider):
        self.client.close()

    def process_response(self, request, response, spider):
        retries = request.meta.get("dbc_retries", 0)
        if retries >= self.max_retries:
            return response

        if self._is_recaptcha_or_geetest(response):
            raise EscalationRequired(
                "This challenge needs JavaScript: use the Playwright samples "
                "or a browser-based spider instead of Scrapy's middleware."
            )

        if not self._is_waf_challenge(response):
            return response

        params = self._waf_params(response)
        if not params:
            raise EscalationRequired(
                "Amazon WAF markers found, but sitekey/iv/context could not be extracted"
            )

        payload = {
            "sitekey": params["sitekey"],
            "pageurl": response.url,
            "iv": params["iv"],
            "context": params["context"],
        }
        if self.proxy:
            payload["proxy"] = self.proxy
            if self.proxytype:
                payload["proxytype"] = self.proxytype

        captcha = self.client.decode(type=16, waf_params=json.dumps(payload))
        if not captcha or not captcha.get("text"):
            spider.logger.warning("DBC returned no WAF token for %s", response.url)
            return response

        spider.logger.info(
            "DBC solved WAF challenge %s for %s", captcha.get("captcha"), response.url
        )
        retry = request.replace(
            dont_filter=True,
            meta={**request.meta, "dbc_retries": retries + 1},
        )
        retry.cookies["aws-waf-token"] = captcha["text"]
        return retry

    @staticmethod
    def _body(response):
        try:
            return response.text[:50000]
        except AttributeError:
            return ""

    def _is_waf_challenge(self, response):
        body = self._body(response)
        return (
            response.status in (403, 429, 503)
            and ("aws-waf" in body or "captchacharacters" in body)
        ) or "aws-waf-token" in body

    def _is_recaptcha_or_geetest(self, response):
        body = self._body(response)
        return any(marker in body for marker in ("g-recaptcha", "geetest", "grecaptcha"))

    def _waf_params(self, response):
        body = self._body(response)
        match = re.search(
            r"(?:key|sitekey)['\"]?\s*[:=]\s*['\"]([^'\"]+)['\"]", body
        )
        iv = re.search(r"\biv['\"]?\s*[:=]\s*['\"]([^'\"]+)['\"]", body)
        context = re.search(r"\bcontext['\"]?\s*[:=]\s*['\"]([^'\"]+)['\"]", body)

        if not match or not iv or not context:
            return None
        return {
            "sitekey": match.group(1),
            "iv": iv.group(1),
            "context": context.group(1),
        }
