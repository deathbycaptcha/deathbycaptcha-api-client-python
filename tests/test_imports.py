"""Test module imports and basic functionality."""

import unittest
import sys


class TestImports(unittest.TestCase):
    """Test that all modules can be imported successfully."""

    def test_deathbycaptcha_import(self):
        """Test importing the main deathbycaptcha module."""
        try:
            import deathbycaptcha
            self.assertIsNotNone(deathbycaptcha)
        except ImportError as e:
            self.fail(f"Failed to import deathbycaptcha: {e}")

    def test_fast_imghdr_import(self):
        """Test importing the fast_imghdr module."""
        try:
            from deathbycaptcha import fast_imghdr
            self.assertIsNotNone(fast_imghdr)
        except ImportError as e:
            self.fail(f"Failed to import fast_imghdr: {e}")

    def test_client_classes(self):
        """Test that client classes are accessible."""
        from deathbycaptcha import (
            HttpClient,
            SocketClient,
            Client,
            AccessDeniedException
        )
        self.assertIsNotNone(HttpClient)
        self.assertIsNotNone(SocketClient)
        self.assertIsNotNone(Client)
        self.assertIsNotNone(AccessDeniedException)

    def test_api_version(self):
        """Test that API_VERSION is correctly defined."""
        from deathbycaptcha import API_VERSION
        self.assertIsNotNone(API_VERSION)
        self.assertIn("4.7.0", API_VERSION)

    def test_python_version_compatibility(self):
        """Test that module works with required Python versions."""
        # Should work with Python 3.6+
        self.assertGreaterEqual(sys.version_info.major, 3)
        self.assertGreaterEqual(sys.version_info.minor, 6)


class TestClientInstantiation(unittest.TestCase):
    """Test client class instantiation."""

    def test_http_client_instantiation(self):
        """Test creating an HttpClient instance."""
        from deathbycaptcha import HttpClient
        
        client = HttpClient("test_user", "test_pass")
        self.assertIsNotNone(client)
        self.assertEqual(client.userpwd['username'], "test_user")
        self.assertEqual(client.userpwd['password'], "test_pass")

    def test_http_client_with_authtoken(self):
        """Test creating an HttpClient with authtoken."""
        from deathbycaptcha import HttpClient
        
        client = HttpClient("test_user", "test_pass", "test_token")
        self.assertIsNotNone(client)
        self.assertEqual(client.authtoken['authtoken'], "test_token")

    def test_socket_client_instantiation(self):
        """Test creating a SocketClient instance."""
        from deathbycaptcha import SocketClient
        
        client = SocketClient("test_user", "test_pass")
        self.assertIsNotNone(client)
        self.assertEqual(client.userpwd['username'], "test_user")
        self.assertEqual(client.userpwd['password'], "test_pass")

    def test_socket_client_with_authtoken(self):
        """Test creating a SocketClient with authtoken."""
        from deathbycaptcha import SocketClient
        
        client = SocketClient("test_user", "test_pass", "test_token")
        self.assertIsNotNone(client)
        self.assertEqual(client.authtoken['authtoken'], "test_token")

    def test_client_get_auth_with_credentials(self):
        """Test get_auth() method with username/password."""
        from deathbycaptcha import HttpClient
        
        client = HttpClient("user", "pass")
        auth = client.get_auth()
        self.assertEqual(auth['username'], "user")
        self.assertEqual(auth['password'], "pass")

    def test_client_get_auth_with_token(self):
        """Test get_auth() method with authtoken."""
        from deathbycaptcha import HttpClient
        
        client = HttpClient("user", "pass", "token123")
        auth = client.get_auth()
        self.assertEqual(auth['authtoken'], "token123")


class TestFastImghdr(unittest.TestCase):
    """Test fast_imghdr module functionality."""

    def test_fast_imghdr_what_function(self):
        """Test that fast_imghdr.what function exists."""
        from deathbycaptcha import fast_imghdr
        self.assertTrue(hasattr(fast_imghdr, 'what'))
        self.assertTrue(callable(fast_imghdr.what))

    def test_fast_imghdr_with_none(self):
        """Test fast_imghdr.what with None returns None."""
        from deathbycaptcha import fast_imghdr
        result = fast_imghdr.what(None, b'')
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
