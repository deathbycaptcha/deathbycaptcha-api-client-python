#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Test client functionality and error handling
"""

import io
import os
import unittest
from unittest.mock import Mock, MagicMock, patch, mock_open
import deathbycaptcha


class TestLoadImage(unittest.TestCase):
    """Test the _load_image function"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_image_path = os.path.join(
            os.path.dirname(__file__), '..', 'examples', 'images', 'normal.jpg'
        )
        # Read actual image for tests
        with open(self.test_image_path, 'rb') as f:
            self.valid_image_data = f.read()

    def test_load_image_from_file_path(self):
        """Test loading image from file path"""
        img = deathbycaptcha._load_image(self.test_image_path)
        self.assertIsInstance(img, bytes)
        self.assertGreater(len(img), 0)

    def test_load_image_from_file_like_object(self):
        """Test loading image from file-like object"""
        file_obj = io.BytesIO(self.valid_image_data)
        img = deathbycaptcha._load_image(file_obj)
        self.assertIsInstance(img, bytes)
        self.assertEqual(img, self.valid_image_data)

    def test_load_image_empty_raises_value_error(self):
        """Test that empty image raises ValueError"""
        empty_file = io.BytesIO(b'')
        with self.assertRaises(ValueError) as context:
            deathbycaptcha._load_image(empty_file)
        self.assertIn('empty', str(context.exception).lower())

    def test_load_image_invalid_type_raises_type_error(self):
        """Test that invalid image type raises TypeError"""
        invalid_file = io.BytesIO(b'not an image')
        with self.assertRaises(TypeError) as context:
            deathbycaptcha._load_image(invalid_file)
        self.assertIn('unknown', str(context.exception).lower())

    def test_load_image_nonexistent_file_raises_exception(self):
        """Test that nonexistent file raises exception"""
        with self.assertRaises(Exception):
            deathbycaptcha._load_image('/nonexistent/path/to/image.jpg')


class TestClientBase(unittest.TestCase):
    """Test base Client class functionality"""

    def test_client_with_username_password(self):
        """Test client initialization with username and password"""
        client = deathbycaptcha.Client('testuser', 'testpass')
        auth = client.get_auth()
        self.assertEqual(auth['username'], 'testuser')
        self.assertEqual(auth['password'], 'testpass')
        self.assertIsNone(client.authtoken)

    def test_client_with_authtoken(self):
        """Test client initialization with authtoken"""
        client = deathbycaptcha.Client(None, None, 'test_token_12345')
        auth = client.get_auth()
        self.assertEqual(auth['authtoken'], 'test_token_12345')
        self.assertIsNotNone(client.authtoken)

    def test_client_verbose_logging(self):
        """Test that verbose logging works"""
        client = deathbycaptcha.Client('test', 'test')
        client.is_verbose = True
        # Should not raise exception
        client._log('TEST', 'test message')

    def test_client_silent_mode(self):
        """Test that silent mode works"""
        client = deathbycaptcha.Client('test', 'test')
        client.is_verbose = False
        # Should not raise exception
        client._log('TEST', 'test message')

    def test_client_close_method(self):
        """Test client close method"""
        client = deathbycaptcha.Client('test', 'test')
        # Should not raise exception
        client.close()

    def test_client_connect_method(self):
        """Test client connect method"""
        client = deathbycaptcha.Client('test', 'test')
        # Should not raise exception
        client.connect()

    def test_client_get_user_not_implemented(self):
        """Test that get_user raises NotImplementedError for base class"""
        client = deathbycaptcha.Client('test', 'test')
        with self.assertRaises(NotImplementedError):
            client.get_user()

    def test_client_get_captcha_not_implemented(self):
        """Test that get_captcha raises NotImplementedError for base class"""
        client = deathbycaptcha.Client('test', 'test')
        with self.assertRaises(NotImplementedError):
            client.get_captcha(123)

    def test_client_report_not_implemented(self):
        """Test that report raises NotImplementedError for base class"""
        client = deathbycaptcha.Client('test', 'test')
        with self.assertRaises(NotImplementedError):
            client.report(123)

    def test_client_upload_not_implemented(self):
        """Test that upload raises NotImplementedError for base class"""
        client = deathbycaptcha.Client('test', 'test')
        with self.assertRaises(NotImplementedError):
            client.upload('test.jpg')

    def test_get_text_returns_none_when_not_solved(self):
        """Test that get_text returns None when captcha not solved"""
        client = deathbycaptcha.HttpClient('test', 'test')
        with patch.object(client, 'get_captcha', return_value={'captcha': 123, 'text': None}):
            result = client.get_text(123)
            self.assertIsNone(result)

    def test_get_text_returns_text_when_solved(self):
        """Test that get_text returns text when captcha solved"""
        client = deathbycaptcha.HttpClient('test', 'test')
        with patch.object(client, 'get_captcha', return_value={'captcha': 123, 'text': 'solved text'}):
            result = client.get_text(123)
            self.assertEqual(result, 'solved text')


class TestHttpClientErrorHandling(unittest.TestCase):
    """Test HttpClient error handling"""

    def setUp(self):
        """Set up test client"""
        self.client = deathbycaptcha.HttpClient('test', 'test')
        self.client.is_verbose = False

    @patch('deathbycaptcha.requests.post')
    def test_http_client_403_raises_access_denied(self, mock_post):
        """Test that 403 status raises AccessDeniedException"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_post.return_value = mock_response

        with self.assertRaises(deathbycaptcha.AccessDeniedException) as context:
            self.client._call('test', payload={'test': 'data'})
        self.assertIn('denied', str(context.exception).lower())

    @patch('deathbycaptcha.requests.post')
    def test_http_client_400_raises_value_error(self, mock_post):
        """Test that 400 status raises ValueError"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        with self.assertRaises(ValueError) as context:
            self.client._call('test', payload={'test': 'data'})
        self.assertIn('rejected', str(context.exception).lower())

    @patch('deathbycaptcha.requests.post')
    def test_http_client_413_raises_value_error(self, mock_post):
        """Test that 413 status raises ValueError"""
        mock_response = Mock()
        mock_response.status_code = 413
        mock_post.return_value = mock_response

        with self.assertRaises(ValueError) as context:
            self.client._call('test', payload={'test': 'data'})
        self.assertIn('rejected', str(context.exception).lower())

    @patch('deathbycaptcha.requests.post')
    def test_http_client_503_raises_overflow_error(self, mock_post):
        """Test that 503 status raises OverflowError"""
        mock_response = Mock()
        mock_response.status_code = 503
        mock_post.return_value = mock_response

        with self.assertRaises(OverflowError) as context:
            self.client._call('test', payload={'test': 'data'})
        self.assertIn('overload', str(context.exception).lower())

    @patch('deathbycaptcha.requests.post')
    def test_http_client_invalid_json_raises_runtime_error(self, mock_post):
        """Test that invalid JSON response raises RuntimeError"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.text = 'not valid json'
        mock_post.return_value = mock_response

        with self.assertRaises(RuntimeError) as context:
            self.client._call('test', payload={'test': 'data'})
        self.assertIn('invalid', str(context.exception).lower())

    @patch('deathbycaptcha.requests.post')
    def test_http_client_not_ok_raises_runtime_error(self, mock_post):
        """Test that non-OK response raises RuntimeError"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.ok = False
        mock_post.return_value = mock_response

        with self.assertRaises(RuntimeError) as context:
            self.client._call('test', payload={'test': 'data'})
        self.assertIn('invalid', str(context.exception).lower())

    @patch('deathbycaptcha.requests.get')
    def test_http_client_get_without_payload(self, mock_get):
        """Test that GET is used when no payload"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.text = '{"test": "response"}'
        mock_get.return_value = mock_response

        result = self.client._call('test')
        mock_get.assert_called_once()
        self.assertEqual(result, {"test": "response"})


class TestHttpClientReport(unittest.TestCase):
    """Test HttpClient report functionality"""

    def setUp(self):
        """Set up test client"""
        self.client = deathbycaptcha.HttpClient('test', 'test')
        self.client.is_verbose = False

    @patch('deathbycaptcha.requests.post')
    def test_report_correctly_solved_returns_false(self, mock_post):
        """Test that report returns False when captcha was correctly solved"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.text = '{"is_correct": true}'
        mock_post.return_value = mock_response

        result = self.client.report(12345)
        self.assertFalse(result)

    @patch('deathbycaptcha.requests.post')
    def test_report_incorrectly_solved_returns_true(self, mock_post):
        """Test that report returns True when captcha was incorrectly solved"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.text = '{"is_correct": false}'
        mock_post.return_value = mock_response

        result = self.client.report(12345)
        self.assertTrue(result)


class TestDecodeMethod(unittest.TestCase):
    """Test decode method with various timeout scenarios"""

    def setUp(self):
        """Set up test client and fixtures"""
        self.client = deathbycaptcha.HttpClient('test', 'test')
        self.client.is_verbose = False
        self.test_image_path = os.path.join(
            os.path.dirname(__file__), '..', 'examples', 'images', 'normal.jpg'
        )

    @patch('deathbycaptcha.time.sleep')
    @patch('deathbycaptcha.time.time')
    def test_decode_with_custom_timeout(self, mock_time, mock_sleep):
        """Test decode with custom timeout"""
        # Simulate time progression
        mock_time.side_effect = [0, 0, 1, 2, 3, 4]  # Start time, deadline check, sleep intervals

        # Mock upload to return captcha
        with patch.object(self.client, 'upload', return_value={'captcha': 123, 'text': None}):
            # Mock get_captcha to return solved after a few polls
            with patch.object(self.client, 'get_captcha', side_effect=[
                {'captcha': 123, 'text': None, 'is_correct': False},
                {'captcha': 123, 'text': 'SOLVED', 'is_correct': True}
            ]):
                result = self.client.decode(self.test_image_path, timeout=10)
                self.assertIsNotNone(result)
                self.assertEqual(result['text'], 'SOLVED')

    @patch('deathbycaptcha.time.sleep')
    @patch('deathbycaptcha.time.time')
    def test_decode_timeout_expires(self, mock_time, mock_sleep):
        """Test decode when timeout expires before solving"""
        # Simulate timeout expiration
        mock_time.side_effect = [0, 0, 11]  # Start time, then past deadline

        # Mock upload to return captcha
        with patch.object(self.client, 'upload', return_value={'captcha': 123, 'text': None}):
            # Mock get_captcha to never return solved
            with patch.object(self.client, 'get_captcha', return_value={'captcha': 123, 'text': None}):
                result = self.client.decode(self.test_image_path, timeout=10)
                self.assertIsNone(result)

    @patch('deathbycaptcha.time.sleep')
    @patch('deathbycaptcha.time.time')
    def test_decode_without_timeout_uses_default(self, mock_time, mock_sleep):
        """Test decode without timeout uses DEFAULT_TIMEOUT"""
        mock_time.side_effect = [0, 0, 1]

        with patch.object(self.client, 'upload', return_value={'captcha': 123, 'text': None}):
            with patch.object(self.client, 'get_captcha', return_value={'captcha': 123, 'text': 'SOLVED', 'is_correct': True}):
                result = self.client.decode(self.test_image_path)
                self.assertIsNotNone(result)

    @patch('deathbycaptcha.time.sleep')
    @patch('deathbycaptcha.time.time')
    def test_decode_with_token_uses_token_timeout(self, mock_time, mock_sleep):
        """Test decode without captcha uses DEFAULT_TOKEN_TIMEOUT"""
        mock_time.side_effect = [0, 0, 1]

        with patch.object(self.client, 'upload', return_value={'captcha': 123, 'text': None}):
            with patch.object(self.client, 'get_captcha', return_value={'captcha': 123, 'text': 'SOLVED', 'is_correct': True}):
                # Pass None for captcha to trigger token timeout path
                result = self.client.decode(captcha=None, type='recaptcha')
                self.assertIsNotNone(result)

    def test_decode_upload_failure_returns_none(self):
        """Test decode returns None when upload fails"""
        with patch.object(self.client, 'upload', return_value=None):
            result = self.client.decode(self.test_image_path)
            self.assertIsNone(result)


class TestGetPollInterval(unittest.TestCase):
    """Test _get_poll_interval method"""

    def setUp(self):
        """Set up test client"""
        self.client = deathbycaptcha.HttpClient('test', 'test')

    def test_poll_interval_within_range(self):
        """Test poll interval returns values from POLLS_INTERVAL"""
        for idx in range(len(deathbycaptcha.POLLS_INTERVAL)):
            interval, next_idx = self.client._get_poll_interval(idx)
            self.assertEqual(interval, deathbycaptcha.POLLS_INTERVAL[idx])
            self.assertEqual(next_idx, idx + 1)

    def test_poll_interval_beyond_range(self):
        """Test poll interval returns default when index beyond range"""
        idx = len(deathbycaptcha.POLLS_INTERVAL) + 5
        interval, next_idx = self.client._get_poll_interval(idx)
        self.assertEqual(interval, deathbycaptcha.DFLT_POLL_INTERVAL)
        self.assertEqual(next_idx, idx + 1)


class TestSocketClientErrorHandling(unittest.TestCase):
    """Test SocketClient error handling"""

    def setUp(self):
        """Set up test client"""
        self.client = deathbycaptcha.SocketClient('test', 'test')
        self.client.is_verbose = False

    def test_socket_client_close(self):
        """Test socket client close method"""
        # Should not raise even if no socket
        self.client.close()

    @patch('deathbycaptcha.socket.socket')
    def test_socket_client_connect(self, mock_socket):
        """Test socket client connect method"""
        mock_sock = Mock()
        mock_socket.return_value = mock_sock

        sock = self.client.connect()
        self.assertIsNotNone(sock)

    def test_socket_error_not_logged_in_raises_access_denied(self):
        """Test that socket error 'not-logged-in' raises AccessDeniedException"""
        with patch.object(self.client, '_sendrecv', return_value='{"error": "not-logged-in"}'):
            with patch.object(self.client, 'connect', return_value=Mock()):
                with self.assertRaises(deathbycaptcha.AccessDeniedException):
                    self.client._call('test')

    def test_socket_error_invalid_credentials_raises_access_denied(self):
        """Test that socket error 'invalid-credentials' raises AccessDeniedException"""
        with patch.object(self.client, '_sendrecv', return_value='{"error": "invalid-credentials"}'):
            with patch.object(self.client, 'connect', return_value=Mock()):
                with self.assertRaises(deathbycaptcha.AccessDeniedException):
                    self.client._call('test')

    def test_socket_error_banned_raises_access_denied(self):
        """Test that socket error 'banned' raises AccessDeniedException"""
        with patch.object(self.client, '_sendrecv', return_value='{"error": "banned"}'):
            with patch.object(self.client, 'connect', return_value=Mock()):
                with self.assertRaises(deathbycaptcha.AccessDeniedException):
                    self.client._call('test')

    def test_socket_error_insufficient_funds_raises_access_denied(self):
        """Test that socket error 'insufficient-funds' raises AccessDeniedException"""
        with patch.object(self.client, '_sendrecv', return_value='{"error": "insufficient-funds"}'):
            with patch.object(self.client, 'connect', return_value=Mock()):
                with self.assertRaises(deathbycaptcha.AccessDeniedException):
                    self.client._call('test')

    def test_socket_error_invalid_captcha_raises_value_error(self):
        """Test that socket error 'invalid-captcha' raises ValueError"""
        with patch.object(self.client, '_sendrecv', return_value='{"error": "invalid-captcha"}'):
            with patch.object(self.client, 'connect', return_value=Mock()):
                with self.assertRaises(ValueError):
                    self.client._call('test')

    def test_socket_error_service_overload_raises_overflow_error(self):
        """Test that socket error 'service-overload' raises OverflowError"""
        with patch.object(self.client, '_sendrecv', return_value='{"error": "service-overload"}'):
            with patch.object(self.client, 'connect', return_value=Mock()):
                with self.assertRaises(OverflowError):
                    self.client._call('test')

    def test_socket_error_unknown_raises_runtime_error(self):
        """Test that unknown socket error raises RuntimeError"""
        with patch.object(self.client, '_sendrecv', return_value='{"error": "unknown-error"}'):
            with patch.object(self.client, 'connect', return_value=Mock()):
                with self.assertRaises(RuntimeError):
                    self.client._call('test')

    def test_socket_invalid_json_raises_runtime_error(self):
        """Test that invalid JSON from socket raises RuntimeError"""
        with patch.object(self.client, '_sendrecv', return_value='not valid json'):
            with patch.object(self.client, 'connect', return_value=Mock()):
                with self.assertRaises(RuntimeError):
                    self.client._call('test')


if __name__ == '__main__':
    unittest.main()
