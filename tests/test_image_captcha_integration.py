"""Integration test for image CAPTCHA (type=0) uploading and polling.

This test demonstrates:
1. Uploading a normal image CAPTCHA (type=0)
2. Polling for the solution with exponential backoff
3. Handling timeout scenarios

This test is included in the Python 3.14 verification job to ensure
compatibility with the latest Python version.
"""

import unittest
import os
import time
from pathlib import Path
from deathbycaptcha import HttpClient, SocketClient, AccessDeniedException

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class TestTextCaptchaIntegration(unittest.TestCase):
    """Integration tests for image CAPTCHA solving (type=0)."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.username = os.getenv('DBC_TEST_USERNAME')
        cls.password = os.getenv('DBC_TEST_PASSWORD')
        cls.authtoken = os.getenv('DBC_TEST_AUTHTOKEN')

        if not cls.authtoken and not (cls.username and cls.password):
            raise unittest.SkipTest(
                "Skipping image CAPTCHA integration tests: missing DBC_TEST_AUTHTOKEN or DBC_TEST_USERNAME/DBC_TEST_PASSWORD"
            )
        cls.image_captcha_path = (
            Path(__file__).resolve().parents[1] / 'examples' / 'images' / 'normal.jpg'
        )
        if not cls.image_captcha_path.exists():
            raise FileNotFoundError(f"Sample CAPTCHA image not found: {cls.image_captcha_path}")

    def _skip_if_insufficient_funds(self, err: Exception):
        message = str(err).lower()
        if 'insufficient-funds' in message or 'low balance' in message or 'check your credentials and/or balance' in message:
            self.skipTest('Skipping image CAPTCHA integration test: insufficient funds')
        raise err

    def test_image_captcha_upload_and_poll_http(self):
        """Test uploading a type=0 image CAPTCHA and polling for solution.
        
        This test:
        1. Creates an HttpClient
        2. Uploads a normal image CAPTCHA (type=0)
        3. Polls the API multiple times with backoff until solved
        4. Verifies the solution exists
        """
        client = HttpClient(authtoken=self.authtoken) if self.authtoken else HttpClient(self.username, self.password)
        
        try:
            # Upload a normal image CAPTCHA (type=0)
            try:
                uploaded = client.upload(str(self.image_captcha_path), type=0)
            except AccessDeniedException as err:
                self._skip_if_insufficient_funds(err)
            self.assertIsNotNone(uploaded)
            self.assertIn('captcha', uploaded)
            
            captcha_id = uploaded['captcha']
            self.assertGreater(captcha_id, 0, "Captcha ID should be positive")
            
            # Poll for solution with exponential backoff
            max_attempts = 10
            backoff_base = 0.5
            solution = None
            
            for attempt in range(max_attempts):
                # Wait before polling (exponential backoff)
                wait_time = backoff_base * (2 ** attempt)
                time.sleep(min(wait_time, 5))  # Cap at 5 seconds
                
                # Get CAPTCHA status
                captcha = client.get_captcha(captcha_id)
                self.assertIsNotNone(captcha)
                self.assertEqual(captcha['captcha'], captcha_id)
                
                # Check if solved
                if captcha.get('text'):
                    solution = captcha['text']
                    break
            
            # Verify we got a solution
            self.assertIsNotNone(solution, 
                                f"Could not get solution after {max_attempts} attempts")
            self.assertIsInstance(solution, str)
            self.assertGreater(len(solution), 0, "Solution should not be empty")
            
        finally:
            if hasattr(client, 'close'):
                try:
                    client.close()
                except Exception:
                    pass

    def test_image_captcha_upload_and_poll_socket(self):
        """Test socket client polling for a type=0 image CAPTCHA.
        
        Similar to HTTP test but using SocketClient for faster polling.
        """
        client = SocketClient(authtoken=self.authtoken) if self.authtoken else SocketClient(self.username, self.password)
        
        try:
            # Upload a normal image CAPTCHA (type=0)
            try:
                uploaded = client.upload(str(self.image_captcha_path), type=0)
            except AccessDeniedException as err:
                self._skip_if_insufficient_funds(err)
            self.assertIsNotNone(uploaded)
            self.assertIn('captcha', uploaded)
            
            captcha_id = uploaded['captcha']
            
            # Poll with shorter timeout for socket (usually faster)
            max_attempts = 8
            solution = None
            
            for attempt in range(max_attempts):
                time.sleep(0.3 * (2 ** attempt))  # Shorter backoff for socket
                
                captcha = client.get_captcha(captcha_id)
                if captcha and captcha.get('text'):
                    solution = captcha['text']
                    break
            
            # Verify solution obtained
            self.assertIsNotNone(solution, "Could not get solution via socket client")
            self.assertIsInstance(solution, str)
            
        finally:
            if hasattr(client, 'close'):
                try:
                    client.close()
                except Exception:
                    pass


if __name__ == '__main__':
    unittest.main()
