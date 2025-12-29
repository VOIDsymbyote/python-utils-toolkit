"""
Demo Scripts - Examples of how to use the utility functions.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime, timedelta
from utils.file_utils import find_files, get_file_info, get_directory_size
from utils.text_utils import extract_emails, extract_urls, slugify, word_frequency
from utils.date_utils import time_ago, format_duration, business_days_between
from utils.web_utils import is_url_valid, parse_url, build_url
from utils.system_utils import get_system_info, get_disk_usage


def demo_file_utils():
    """Demonstrate file utility functions."""
    print("\n" + "=" * 50)
    print("FILE UTILITIES DEMO")
    print("=" * 50)

    # Find Python files in current directory
    print("\n1. Finding Python files:")
    py_files = find_files(".", "*.py")
    for f in py_files[:5]:
        print(f"   - {f}")

    # Get file info
    print("\n2. Getting file info:")
    try:
        info = get_file_info(__file__)
        print(f"   Name: {info['name']}")
        print(f"   Size: {info['size_human']}")
        print(f"   Modified: {info['modified']}")
    except FileNotFoundError:
        print("   File not found")

    # Get directory size
    print("\n3. Directory size:")
    size_info = get_directory_size(".")
    print(f"   Total: {size_info['total_human']}")
    print(f"   Files: {size_info['file_count']}")


def demo_text_utils():
    """Demonstrate text utility functions."""
    print("\n" + "=" * 50)
    print("TEXT UTILITIES DEMO")
    print("=" * 50)

    sample_text = """
    Contact us at support@example.com or sales@company.org.
    Visit our website: https://www.example.com/products
    Check out our blog at http://blog.example.com
    """

    # Extract emails
    print("\n1. Extracting emails:")
    emails = extract_emails(sample_text)
    for email in emails:
        print(f"   - {email}")

    # Extract URLs
    print("\n2. Extracting URLs:")
    urls = extract_urls(sample_text)
    for url in urls:
        print(f"   - {url}")

    # Slugify
    print("\n3. Creating URL slugs:")
    titles = ["Hello World!", "Python 3.12 Release Notes", "What's New in 2024?"]
    for title in titles:
        print(f"   '{title}' -> '{slugify(title)}'")

    # Word frequency
    print("\n4. Word frequency:")
    text = "Python is great. Python is easy. Python is powerful."
    freq = word_frequency(text, top_n=3)
    for word, count in freq.items():
        print(f"   '{word}': {count}")


def demo_date_utils():
    """Demonstrate date utility functions."""
    print("\n" + "=" * 50)
    print("DATE UTILITIES DEMO")
    print("=" * 50)

    # Time ago
    print("\n1. Time ago formatting:")
    times = [
        datetime.now() - timedelta(minutes=5),
        datetime.now() - timedelta(hours=3),
        datetime.now() - timedelta(days=7),
        datetime.now() - timedelta(days=60),
    ]
    for t in times:
        print(f"   {t.strftime('%Y-%m-%d %H:%M')} -> {time_ago(t)}")

    # Format duration
    print("\n2. Duration formatting:")
    durations = [45, 3600, 86400, 90061]
    for d in durations:
        print(f"   {d} seconds -> {format_duration(d)}")

    # Business days
    print("\n3. Business days calculation:")
    from datetime import date
    start = date(2024, 1, 1)
    end = date(2024, 1, 15)
    days = business_days_between(start, end)
    print(f"   {start} to {end}: {days} business days")


def demo_web_utils():
    """Demonstrate web utility functions."""
    print("\n" + "=" * 50)
    print("WEB UTILITIES DEMO")
    print("=" * 50)

    # Parse URL
    print("\n1. Parsing URLs:")
    test_url = "https://api.example.com:8080/users/search?q=john&limit=10#results"
    parsed = parse_url(test_url)
    print(f"   URL: {test_url}")
    print(f"   Host: {parsed['host']}")
    print(f"   Port: {parsed['port']}")
    print(f"   Path: {parsed['path']}")
    print(f"   Params: {parsed['query_params']}")

    # Build URL
    print("\n2. Building URLs:")
    url = build_url("https://api.example.com", "/users", {"page": 1, "limit": 20})
    print(f"   Built URL: {url}")

    # Check URL validity (commented out to avoid network calls in demo)
    print("\n3. URL validation (checking format):")
    urls_to_check = [
        "https://google.com",
        "not-a-url",
        "http://localhost:8080",
    ]
    for url in urls_to_check:
        from utils.web_utils import is_valid_url
        valid = is_valid_url(url)
        print(f"   '{url}' -> {'Valid' if valid else 'Invalid'}")


def demo_system_utils():
    """Demonstrate system utility functions."""
    print("\n" + "=" * 50)
    print("SYSTEM UTILITIES DEMO")
    print("=" * 50)

    # System info
    print("\n1. System information:")
    info = get_system_info()
    print(f"   OS: {info['os']} {info['os_release']}")
    print(f"   Machine: {info['machine']}")
    print(f"   Python: {info['python_version']}")
    print(f"   Hostname: {info['hostname']}")

    # Disk usage
    print("\n2. Disk usage:")
    if sys.platform == 'win32':
        disk = get_disk_usage("C:\\")
    else:
        disk = get_disk_usage("/")

    if "error" not in disk:
        print(f"   Total: {disk['total']}")
        print(f"   Used: {disk['used']} ({disk['percent']}%)")
        print(f"   Free: {disk['free']}")


def main():
    """Run all demos."""
    print("\n" + "#" * 60)
    print("#" + " " * 58 + "#")
    print("#" + "     PYTHON UTILS TOOLKIT - DEMONSTRATION".center(58) + "#")
    print("#" + " " * 58 + "#")
    print("#" * 60)

    demo_file_utils()
    demo_text_utils()
    demo_date_utils()
    demo_web_utils()
    demo_system_utils()

    print("\n" + "=" * 50)
    print("Demo complete! Explore the utils/ folder for more functions.")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
