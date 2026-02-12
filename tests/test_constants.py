"""Test module constants and configuration."""

import unittest
from deathbycaptcha import (
    API_VERSION,
    DEFAULT_TIMEOUT,
    DEFAULT_TOKEN_TIMEOUT,
    POLLS_INTERVAL,
    DFLT_POLL_INTERVAL,
    HTTP_BASE_URL,
    HTTP_RESPONSE_TYPE,
    SOCKET_HOST,
    SOCKET_PORTS
)


class TestConstants(unittest.TestCase):
    """Test module constants."""

    def test_api_version_format(self):
        """Test API_VERSION is correctly formatted."""
        self.assertIsInstance(API_VERSION, str)
        self.assertIn("DBC/Python", API_VERSION)
        self.assertIn("4.7.0", API_VERSION)

    def test_timeouts_are_positive(self):
        """Test timeout constants are positive integers."""
        self.assertIsInstance(DEFAULT_TIMEOUT, int)
        self.assertGreater(DEFAULT_TIMEOUT, 0)
        self.assertIsInstance(DEFAULT_TOKEN_TIMEOUT, int)
        self.assertGreater(DEFAULT_TOKEN_TIMEOUT, 0)

    def test_polls_interval_is_list(self):
        """Test POLLS_INTERVAL is a list of integers."""
        self.assertIsInstance(POLLS_INTERVAL, list)
        for interval in POLLS_INTERVAL:
            self.assertIsInstance(interval, int)
            self.assertGreater(interval, 0)

    def test_default_poll_interval(self):
        """Test DFLT_POLL_INTERVAL is a positive integer."""
        self.assertIsInstance(DFLT_POLL_INTERVAL, int)
        self.assertGreater(DFLT_POLL_INTERVAL, 0)

    def test_http_base_url(self):
        """Test HTTP_BASE_URL is properly formatted."""
        self.assertIsInstance(HTTP_BASE_URL, str)
        self.assertTrue(HTTP_BASE_URL.startswith('http://'))
        self.assertIn('api.dbcapi.me', HTTP_BASE_URL)

    def test_http_response_type(self):
        """Test HTTP_RESPONSE_TYPE is set to JSON."""
        self.assertEqual(HTTP_RESPONSE_TYPE, 'application/json')

    def test_socket_host(self):
        """Test SOCKET_HOST is correctly set."""
        self.assertEqual(SOCKET_HOST, 'api.dbcapi.me')

    def test_socket_ports_range(self):
        """Test SOCKET_PORTS contains expected port range."""
        self.assertIsInstance(SOCKET_PORTS, list)
        self.assertGreater(len(SOCKET_PORTS), 0)
        # Port range should be between 8123 and 8130
        self.assertEqual(SOCKET_PORTS[0], 8123)
        self.assertEqual(SOCKET_PORTS[-1], 8130)

    def test_timeout_relationships(self):
        """Test that TOKEN_TIMEOUT is greater than regular TIMEOUT."""
        self.assertGreater(DEFAULT_TOKEN_TIMEOUT, DEFAULT_TIMEOUT)


if __name__ == '__main__':
    unittest.main()
