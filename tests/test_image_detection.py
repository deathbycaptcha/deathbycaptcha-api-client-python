"""Test image detection functionality."""

import unittest
import os
from deathbycaptcha import fast_imghdr


class TestImageDetection(unittest.TestCase):
    """Test image format detection."""

    def test_png_detection(self):
        """Test PNG image detection."""
        # PNG magic bytes
        png_data = b'\x89PNG\r\n\x1a\n'
        result = fast_imghdr.what(None, png_data)
        self.assertEqual(result, 'png')

    def test_jpeg_detection_jfif(self):
        """Test JPEG with JFIF header detection."""
        # JPEG JFIF magic bytes: FFD8 FFE0 ... JFIF
        jpeg_data = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01'
        result = fast_imghdr.what(None, jpeg_data)
        self.assertEqual(result, 'jpeg')

    def test_jpeg_detection_exif(self):
        """Test JPEG with Exif header detection."""
        # JPEG Exif magic bytes: FFD8 FFE1 ... Exif
        jpeg_data = b'\xff\xd8\xff\xe1\x00\x10Exif\x00\x00'
        result = fast_imghdr.what(None, jpeg_data)
        self.assertEqual(result, 'jpeg')

    def test_gif87_detection(self):
        """Test GIF87a detection."""
        gif_data = b'GIF87a'
        result = fast_imghdr.what(None, gif_data)
        self.assertEqual(result, 'gif')

    def test_gif89_detection(self):
        """Test GIF89a detection."""
        gif_data = b'GIF89a'
        result = fast_imghdr.what(None, gif_data)
        self.assertEqual(result, 'gif')

    def test_bmp_detection(self):
        """Test BMP detection."""
        bmp_data = b'BM'
        result = fast_imghdr.what(None, bmp_data)
        self.assertEqual(result, 'bmp')

    def test_webp_detection(self):
        """Test WebP detection."""
        webp_data = b'RIFF' + b'\x00' * 4 + b'WEBP'
        result = fast_imghdr.what(None, webp_data)
        self.assertEqual(result, 'webp')

    def test_unknown_format(self):
        """Test that unknown format returns None."""
        unknown_data = b'UNKNOWN_FORMAT'
        result = fast_imghdr.what(None, unknown_data)
        self.assertIsNone(result)

    def test_empty_data(self):
        """Test with empty data."""
        result = fast_imghdr.what(None, b'')
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
