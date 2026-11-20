"""Minimal spider that runs behind DeathByCaptchaMiddleware.

Point ``start_urls`` at the protected page you own or are allowed to crawl.
The middleware handles the challenge and retries the request.
"""

import scrapy


class ProtectedSpider(scrapy.Spider):
    name = "protected"
    start_urls = ["https://example.com/protected"]

    def parse(self, response):
        self.logger.info("Status %s for %s", response.status, response.url)
        yield {
            "url": response.url,
            "status": response.status,
            "title": response.css("title::text").get(),
        }
