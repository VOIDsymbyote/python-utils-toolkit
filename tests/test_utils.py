"""
Unit Tests for Python Utils Toolkit
"""

import sys
import unittest
from pathlib import Path
from datetime import datetime, date, timedelta

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.text_utils import (
    extract_emails,
    extract_urls,
    slugify,
    validate_email,
    word_frequency,
    truncate_text,
    is_palindrome,
)
from utils.date_utils import (
    time_ago,
    format_duration,
    business_days_between,
    get_week_dates,
    is_weekend,
    get_age,
    get_quarter,
)
from utils.web_utils import (
    url_encode,
    url_decode,
    parse_url,
    build_url,
    is_valid_url,
    extract_domain,
)
from utils.system_utils import (
    get_system_info,
    path_exists,
    get_filename,
    get_file_extension,
)


class TestTextUtils(unittest.TestCase):
    """Tests for text_utils module."""

    def test_extract_emails(self):
        text = "Contact: test@example.com and admin@test.org"
        emails = extract_emails(text)
        self.assertEqual(len(emails), 2)
        self.assertIn("test@example.com", emails)
        self.assertIn("admin@test.org", emails)

    def test_extract_urls(self):
        text = "Visit https://example.com and http://test.org/path"
        urls = extract_urls(text)
        self.assertEqual(len(urls), 2)

    def test_slugify(self):
        self.assertEqual(slugify("Hello World!"), "hello-world")
        self.assertEqual(slugify("Python 3.12 Release"), "python-3-12-release")
        self.assertEqual(slugify("  Spaces  Everywhere  "), "spaces-everywhere")

    def test_slugify_max_length(self):
        result = slugify("This is a very long title", max_length=10)
        self.assertLessEqual(len(result), 10)

    def test_validate_email(self):
        self.assertTrue(validate_email("test@example.com"))
        self.assertTrue(validate_email("user.name@domain.co.uk"))
        self.assertFalse(validate_email("invalid-email"))
        self.assertFalse(validate_email("@nodomain.com"))

    def test_word_frequency(self):
        text = "python python java python java ruby"
        freq = word_frequency(text)
        self.assertEqual(freq["python"], 3)
        self.assertEqual(freq["java"], 2)
        self.assertEqual(freq["ruby"], 1)

    def test_word_frequency_top_n(self):
        text = "a b b c c c"
        freq = word_frequency(text, top_n=2)
        self.assertEqual(len(freq), 2)
        self.assertIn("c", freq)

    def test_truncate_text(self):
        self.assertEqual(truncate_text("Hello World", 20), "Hello World")
        self.assertEqual(truncate_text("Hello World", 8), "Hello...")

    def test_is_palindrome(self):
        self.assertTrue(is_palindrome("racecar"))
        self.assertTrue(is_palindrome("A man a plan a canal Panama"))
        self.assertFalse(is_palindrome("hello"))


class TestDateUtils(unittest.TestCase):
    """Tests for date_utils module."""

    def test_time_ago(self):
        now = datetime.now()
        self.assertEqual(time_ago(now - timedelta(seconds=30), now), "30 seconds ago")
        self.assertEqual(time_ago(now - timedelta(minutes=5), now), "5 minutes ago")
        self.assertEqual(time_ago(now - timedelta(hours=2), now), "2 hours ago")
        self.assertEqual(time_ago(now - timedelta(days=1), now), "1 day ago")

    def test_format_duration(self):
        self.assertEqual(format_duration(45), "45 seconds")
        self.assertEqual(format_duration(90), "1 minute, 30 seconds")
        self.assertEqual(format_duration(3600), "1 hour")
        self.assertEqual(format_duration(3661, granularity=2), "1 hour, 1 minute")

    def test_business_days_between(self):
        # Monday to Friday = 4 business days
        start = date(2024, 1, 1)  # Monday
        end = date(2024, 1, 5)    # Friday
        self.assertEqual(business_days_between(start, end), 4)

    def test_get_week_dates(self):
        test_date = date(2024, 1, 3)  # Wednesday
        week = get_week_dates(test_date)
        self.assertEqual(len(week), 7)
        self.assertEqual(week[0].weekday(), 0)  # Monday

    def test_is_weekend(self):
        saturday = date(2024, 1, 6)
        sunday = date(2024, 1, 7)
        monday = date(2024, 1, 8)
        self.assertTrue(is_weekend(saturday))
        self.assertTrue(is_weekend(sunday))
        self.assertFalse(is_weekend(monday))

    def test_get_age(self):
        today = date(2024, 6, 15)
        birth = date(2000, 6, 15)
        self.assertEqual(get_age(birth, today), 24)

        # Birthday not yet
        birth_later = date(2000, 12, 25)
        self.assertEqual(get_age(birth_later, today), 23)

    def test_get_quarter(self):
        self.assertEqual(get_quarter(date(2024, 1, 15)), 1)
        self.assertEqual(get_quarter(date(2024, 4, 1)), 2)
        self.assertEqual(get_quarter(date(2024, 9, 30)), 3)
        self.assertEqual(get_quarter(date(2024, 12, 31)), 4)


class TestWebUtils(unittest.TestCase):
    """Tests for web_utils module."""

    def test_url_encode(self):
        params = {"name": "John Doe", "age": 30}
        encoded = url_encode(params)
        self.assertIn("name=John", encoded)
        self.assertIn("age=30", encoded)

    def test_url_decode(self):
        query = "name=John+Doe&age=30"
        decoded = url_decode(query)
        self.assertEqual(decoded["name"], "John Doe")
        self.assertEqual(decoded["age"], "30")

    def test_parse_url(self):
        url = "https://example.com:8080/path?q=test"
        parsed = parse_url(url)
        self.assertEqual(parsed["scheme"], "https")
        self.assertEqual(parsed["host"], "example.com")
        self.assertEqual(parsed["port"], 8080)
        self.assertEqual(parsed["path"], "/path")

    def test_build_url(self):
        url = build_url("https://api.example.com", "/users", {"page": 1})
        self.assertEqual(url, "https://api.example.com/users?page=1")

    def test_is_valid_url(self):
        self.assertTrue(is_valid_url("https://example.com"))
        self.assertTrue(is_valid_url("http://localhost:8080"))
        self.assertFalse(is_valid_url("not-a-url"))
        self.assertFalse(is_valid_url("ftp://example.com"))

    def test_extract_domain(self):
        self.assertEqual(extract_domain("https://www.example.com/path"), "example.com")
        self.assertEqual(extract_domain("http://api.test.org"), "api.test.org")


class TestSystemUtils(unittest.TestCase):
    """Tests for system_utils module."""

    def test_get_system_info(self):
        info = get_system_info()
        self.assertIn("os", info)
        self.assertIn("python_version", info)
        self.assertIn("machine", info)

    def test_path_exists(self):
        self.assertTrue(path_exists(__file__))
        self.assertFalse(path_exists("/nonexistent/path/file.txt"))

    def test_get_filename(self):
        self.assertEqual(get_filename("/path/to/file.txt"), "file.txt")
        self.assertEqual(get_filename("/path/to/file.txt", with_extension=False), "file")

    def test_get_file_extension(self):
        self.assertEqual(get_file_extension("/path/to/file.txt"), ".txt")
        self.assertEqual(get_file_extension("/path/to/file.tar.gz"), ".gz")


if __name__ == "__main__":
    unittest.main(verbosity=2)
