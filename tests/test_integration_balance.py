"""Integration tests for get_balance and get_user with real API requests.

This test module contains realistic tests that make actual HTTP and Socket API
requests to the Death by Captcha service. These tests use a test account with
no real balance.

Test account credentials:
    Username: dbcpiptests
    Password: KFJiugf.d432.3uyf
"""

import unittest
import time
from deathbycaptcha import (
    HttpClient,
    SocketClient,
    AccessDeniedException,
    API_VERSION
)


class TestHttpClientRealBalance(unittest.TestCase):
    """Test HttpClient get_balance and get_user with real API requests."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures for HTTP client tests."""
        cls.username = 'dbcpiptests'
        cls.password = 'KFJiugf.d432.3uyf'
        cls.client = None

    def setUp(self):
        """Create a fresh HttpClient instance for each test."""
        self.client = HttpClient(self.username, self.password)

    def tearDown(self):
        """Clean up after each test."""
        if self.client:
            try:
                self.client.close()
            except Exception:
                pass

    def test_http_get_balance_returns_number(self):
        """Test that get_balance returns a numeric value (int or float)."""
        balance = self.client.get_balance()
        self.assertIsNotNone(balance)
        self.assertIsInstance(balance, (int, float))
        # Test account balance should be 0 or small value
        self.assertGreaterEqual(balance, 0)

    def test_http_get_balance_is_callable_multiple_times(self):
        """Test that get_balance can be called multiple times."""
        balance1 = self.client.get_balance()
        time.sleep(0.5)
        balance2 = self.client.get_balance()
        
        self.assertIsNotNone(balance1)
        self.assertIsNotNone(balance2)
        # Balance should be consistent across calls
        self.assertEqual(balance1, balance2)

    def test_http_get_user_returns_dict(self):
        """Test that get_user returns a proper dictionary."""
        user = self.client.get_user()
        self.assertIsNotNone(user)
        self.assertIsInstance(user, dict)

    def test_http_get_user_contains_required_fields(self):
        """Test that get_user response contains required fields."""
        user = self.client.get_user()
        
        # Must contain these keys
        required_keys = ['user', 'balance', 'rate', 'is_banned']
        for key in required_keys:
            self.assertIn(key, user, 
                         f"Missing required key '{key}' in user response")

    def test_http_get_user_user_id_is_positive(self):
        """Test that user ID is a positive integer."""
        user = self.client.get_user()
        user_id = user.get('user')
        self.assertIsNotNone(user_id)
        self.assertIsInstance(user_id, int)
        self.assertGreater(user_id, 0, 
                          "User ID should be positive for valid credentials")

    def test_http_get_user_balance_is_non_negative_number(self):
        """Test that balance in get_user response is a non-negative number."""
        user = self.client.get_user()
        balance = user.get('balance')
        self.assertIsNotNone(balance)
        self.assertIsInstance(balance, (int, float))
        self.assertGreaterEqual(balance, 0)

    def test_http_get_user_rate_is_positive(self):
        """Test that rate is a positive number."""
        user = self.client.get_user()
        rate = user.get('rate')
        self.assertIsNotNone(rate)
        self.assertIsInstance(rate, (int, float))
        self.assertGreater(rate, 0)

    def test_http_get_user_is_banned_is_boolean(self):
        """Test that is_banned is a boolean value."""
        user = self.client.get_user()
        is_banned = user.get('is_banned')
        self.assertIsNotNone(is_banned)
        self.assertIsInstance(is_banned, bool)

    def test_http_get_balance_matches_get_user_balance(self):
        """Test that get_balance equals the balance from get_user."""
        balance = self.client.get_balance()
        user = self.client.get_user()
        user_balance = user.get('balance')
        
        self.assertEqual(balance, user_balance,
                        "get_balance() should match balance from get_user()")





    def test_http_multiple_concurrent_operations(self):
        """Test that multiple operations work in sequence."""
        # First get user
        user1 = self.client.get_user()
        self.assertGreater(user1.get('user'), 0)
        
        # Then get balance
        balance = self.client.get_balance()
        self.assertIsInstance(balance, (int, float))
        
        # Get user again
        user2 = self.client.get_user()
        self.assertEqual(user1.get('user'), user2.get('user'))
        
        # Verify consistency
        self.assertEqual(user1.get('balance'), balance)
        self.assertEqual(user1.get('balance'), user2.get('balance'))


class TestSocketClientRealBalance(unittest.TestCase):
    """Test SocketClient get_balance and get_user with real API requests."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures for Socket client tests."""
        cls.username = 'dbcpiptests'
        cls.password = 'KFJiugf.d432.3uyf'
        cls.client = None

    def setUp(self):
        """Create a fresh SocketClient instance for each test."""
        self.client = SocketClient(self.username, self.password)

    def tearDown(self):
        """Clean up socket connection after each test."""
        if self.client:
            try:
                self.client.close()
            except Exception:
                pass

    def test_socket_get_balance_returns_number(self):
        """Test that get_balance returns a numeric value (int or float) via socket."""
        balance = self.client.get_balance()
        self.assertIsNotNone(balance)
        self.assertIsInstance(balance, (int, float))
        # Test account balance should be 0 or small value
        self.assertGreaterEqual(balance, 0)

    def test_socket_get_balance_is_callable_multiple_times(self):
        """Test that get_balance can be called multiple times via socket."""
        balance1 = self.client.get_balance()
        time.sleep(0.5)
        balance2 = self.client.get_balance()
        
        self.assertIsNotNone(balance1)
        self.assertIsNotNone(balance2)
        # Balance should be consistent across calls
        self.assertEqual(balance1, balance2)

    def test_socket_get_user_returns_dict(self):
        """Test that get_user returns a proper dictionary via socket."""
        user = self.client.get_user()
        self.assertIsNotNone(user)
        self.assertIsInstance(user, dict)

    def test_socket_get_user_contains_required_fields(self):
        """Test that get_user response contains required fields via socket."""
        user = self.client.get_user()
        
        # Must contain these keys
        required_keys = ['user', 'balance', 'rate', 'is_banned']
        for key in required_keys:
            self.assertIn(key, user,
                         f"Missing required key '{key}' in user response")

    def test_socket_get_user_user_id_is_positive(self):
        """Test that user ID is a positive integer via socket."""
        user = self.client.get_user()
        user_id = user.get('user')
        self.assertIsNotNone(user_id)
        self.assertIsInstance(user_id, int)
        self.assertGreater(user_id, 0,
                          "User ID should be positive for valid credentials")

    def test_socket_get_user_balance_is_non_negative_number(self):
        """Test that balance in get_user response is non-negative via socket."""
        user = self.client.get_user()
        balance = user.get('balance')
        self.assertIsNotNone(balance)
        self.assertIsInstance(balance, (int, float))
        self.assertGreaterEqual(balance, 0)

    def test_socket_get_user_rate_is_positive(self):
        """Test that rate is a positive number via socket."""
        user = self.client.get_user()
        rate = user.get('rate')
        self.assertIsNotNone(rate)
        self.assertIsInstance(rate, (int, float))
        self.assertGreater(rate, 0)

    def test_socket_get_user_is_banned_is_boolean(self):
        """Test that is_banned is a boolean value via socket."""
        user = self.client.get_user()
        is_banned = user.get('is_banned')
        self.assertIsNotNone(is_banned)
        self.assertIsInstance(is_banned, bool)

    def test_socket_get_balance_matches_get_user_balance(self):
        """Test that get_balance equals the balance from get_user via socket."""
        balance = self.client.get_balance()
        user = self.client.get_user()
        user_balance = user.get('balance')
        
        self.assertEqual(balance, user_balance,
                        "get_balance() should match balance from get_user()")





    def test_socket_multiple_concurrent_operations(self):
        """Test that multiple operations work in sequence via socket."""
        # First get user
        user1 = self.client.get_user()
        self.assertGreater(user1.get('user'), 0)
        
        # Then get balance
        balance = self.client.get_balance()
        self.assertIsInstance(balance, (int, float))
        
        # Get user again
        user2 = self.client.get_user()
        self.assertEqual(user1.get('user'), user2.get('user'))
        
        # Verify consistency
        self.assertEqual(user1.get('balance'), balance)
        self.assertEqual(user1.get('balance'), user2.get('balance'))

    def test_socket_persistent_connection_reuse(self):
        """Test that socket connection is reused across multiple calls."""
        # Make multiple calls without reconnecting
        balance1 = self.client.get_balance()
        balance2 = self.client.get_balance()
        user = self.client.get_user()
        balance3 = self.client.get_balance()
        
        # All should succeed and be consistent
        self.assertEqual(balance1, balance2)
        self.assertEqual(balance1, balance3)
        self.assertEqual(balance1, user.get('balance'))


class TestHttpVsSocketConsistency(unittest.TestCase):
    """Test that HTTP and Socket clients return consistent results."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.username = 'dbcpiptests'
        cls.password = 'KFJiugf.d432.3uyf'

    def test_http_and_socket_balance_consistency(self):
        """Test that both HTTP and Socket clients return the same balance."""
        http_client = HttpClient(self.username, self.password)
        socket_client = SocketClient(self.username, self.password)
        
        try:
            http_balance = http_client.get_balance()
            socket_balance = socket_client.get_balance()
            
            self.assertEqual(http_balance, socket_balance,
                           "HTTP and Socket clients should return same balance")
        finally:
            http_client.close()
            socket_client.close()

    def test_http_and_socket_user_consistency(self):
        """Test that both HTTP and Socket clients return the same user data."""
        http_client = HttpClient(self.username, self.password)
        socket_client = SocketClient(self.username, self.password)
        
        try:
            http_user = http_client.get_user()
            socket_user = socket_client.get_user()
            
            # Check critical fields match
            self.assertEqual(http_user.get('user'), socket_user.get('user'),
                           "User IDs should match between HTTP and Socket")
            self.assertEqual(http_user.get('balance'), socket_user.get('balance'),
                           "Balances should match between HTTP and Socket")
            self.assertEqual(http_user.get('rate'), socket_user.get('rate'),
                           "Rates should match between HTTP and Socket")
            self.assertEqual(http_user.get('is_banned'), socket_user.get('is_banned'),
                           "Ban status should match between HTTP and Socket")
        finally:
            http_client.close()
            socket_client.close()

    def test_http_and_socket_user_id_validity(self):
        """Test that both clients return a valid user ID."""
        http_client = HttpClient(self.username, self.password)
        socket_client = SocketClient(self.username, self.password)
        
        try:
            http_user_id = http_client.get_user().get('user')
            socket_user_id = socket_client.get_user().get('user')
            
            # Both should be positive
            self.assertGreater(http_user_id, 0)
            self.assertGreater(socket_user_id, 0)
            # And they should match
            self.assertEqual(http_user_id, socket_user_id)
        finally:
            http_client.close()
            socket_client.close()



if __name__ == '__main__':
    unittest.main()
