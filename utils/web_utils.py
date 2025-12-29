"""
Web Utilities - Functions for web-related operations.
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import re
from typing import Optional, Dict, Any
from pathlib import Path


def download_file(url: str, destination: str, chunk_size: int = 8192, show_progress: bool = True) -> Dict:
    """
    Download a file from URL with progress tracking.

    Args:
        url: URL to download from
        destination: Local path to save file
        chunk_size: Size of chunks to download
        show_progress: Print progress to console

    Returns:
        Dictionary with download info

    Example:
        >>> download_file("https://example.com/file.zip", "./file.zip")
        {'success': True, 'path': './file.zip', 'size': 1024}
    """
    try:
        with urllib.request.urlopen(url) as response:
            total_size = response.headers.get('Content-Length')
            total_size = int(total_size) if total_size else None

            downloaded = 0
            dest_path = Path(destination)

            with open(dest_path, 'wb') as f:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)

                    if show_progress and total_size:
                        percent = (downloaded / total_size) * 100
                        print(f"\rDownloading: {percent:.1f}%", end="", flush=True)

            if show_progress:
                print()  # New line after progress

            return {
                "success": True,
                "path": str(dest_path),
                "size": downloaded,
                "size_human": _format_size(downloaded),
            }

    except urllib.error.URLError as e:
        return {
            "success": False,
            "error": str(e),
        }


def is_url_valid(url: str, timeout: int = 10) -> Dict:
    """
    Check if a URL is accessible.

    Args:
        url: URL to check
        timeout: Request timeout in seconds

    Returns:
        Dictionary with status info

    Example:
        >>> is_url_valid("https://google.com")
        {'valid': True, 'status_code': 200, 'url': 'https://google.com'}
    """
    try:
        request = urllib.request.Request(url, method='HEAD')
        request.add_header('User-Agent', 'Mozilla/5.0')

        with urllib.request.urlopen(request, timeout=timeout) as response:
            return {
                "valid": True,
                "status_code": response.status,
                "url": response.url,
                "content_type": response.headers.get('Content-Type'),
            }
    except urllib.error.HTTPError as e:
        return {
            "valid": False,
            "status_code": e.code,
            "error": str(e),
        }
    except urllib.error.URLError as e:
        return {
            "valid": False,
            "status_code": None,
            "error": str(e),
        }
    except Exception as e:
        return {
            "valid": False,
            "error": str(e),
        }


def get_page_title(url: str, timeout: int = 10) -> Optional[str]:
    """
    Get the title of a webpage.

    Args:
        url: URL of the page
        timeout: Request timeout

    Returns:
        Page title or None

    Example:
        >>> get_page_title("https://example.com")
        'Example Domain'
    """
    try:
        request = urllib.request.Request(url)
        request.add_header('User-Agent', 'Mozilla/5.0')

        with urllib.request.urlopen(request, timeout=timeout) as response:
            content = response.read().decode('utf-8', errors='ignore')
            match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
            if match:
                return match.group(1).strip()
            return None
    except Exception:
        return None


def fetch_json(url: str, timeout: int = 10, headers: Optional[Dict] = None) -> Dict:
    """
    Fetch JSON data from a URL.

    Args:
        url: URL to fetch
        timeout: Request timeout
        headers: Optional headers to include

    Returns:
        Dictionary with response data

    Example:
        >>> fetch_json("https://api.example.com/data")
        {'success': True, 'data': {...}}
    """
    try:
        request = urllib.request.Request(url)
        request.add_header('User-Agent', 'Mozilla/5.0')
        request.add_header('Accept', 'application/json')

        if headers:
            for key, value in headers.items():
                request.add_header(key, value)

        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = json.loads(response.read().decode('utf-8'))
            return {
                "success": True,
                "data": data,
                "status_code": response.status,
            }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"Invalid JSON: {e}",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


def url_encode(params: Dict[str, Any]) -> str:
    """
    Encode dictionary to URL query string.

    Args:
        params: Dictionary of parameters

    Returns:
        URL-encoded query string

    Example:
        >>> url_encode({"name": "John Doe", "age": 30})
        'name=John+Doe&age=30'
    """
    return urllib.parse.urlencode(params)


def url_decode(query_string: str) -> Dict[str, str]:
    """
    Decode URL query string to dictionary.

    Args:
        query_string: URL-encoded query string

    Returns:
        Dictionary of parameters

    Example:
        >>> url_decode("name=John+Doe&age=30")
        {'name': 'John Doe', 'age': '30'}
    """
    return dict(urllib.parse.parse_qsl(query_string))


def parse_url(url: str) -> Dict:
    """
    Parse URL into components.

    Args:
        url: URL to parse

    Returns:
        Dictionary with URL components

    Example:
        >>> parse_url("https://example.com:8080/path?q=test")
        {'scheme': 'https', 'host': 'example.com', 'port': 8080, ...}
    """
    parsed = urllib.parse.urlparse(url)
    query_params = dict(urllib.parse.parse_qsl(parsed.query))

    return {
        "scheme": parsed.scheme,
        "host": parsed.hostname,
        "port": parsed.port,
        "path": parsed.path,
        "query": parsed.query,
        "query_params": query_params,
        "fragment": parsed.fragment,
        "username": parsed.username,
        "password": parsed.password,
    }


def build_url(base: str, path: str = "", params: Optional[Dict] = None) -> str:
    """
    Build URL from components.

    Args:
        base: Base URL
        path: Path to append
        params: Query parameters

    Returns:
        Complete URL

    Example:
        >>> build_url("https://api.example.com", "/users", {"page": 1})
        'https://api.example.com/users?page=1'
    """
    url = base.rstrip('/') + '/' + path.lstrip('/') if path else base

    if params:
        query = urllib.parse.urlencode(params)
        url = f"{url}?{query}"

    return url


def extract_domain(url: str) -> Optional[str]:
    """
    Extract domain from URL.

    Args:
        url: URL to parse

    Returns:
        Domain name

    Example:
        >>> extract_domain("https://www.example.com/path")
        'example.com'
    """
    try:
        parsed = urllib.parse.urlparse(url)
        domain = parsed.hostname or ""
        # Remove www prefix
        if domain.startswith("www."):
            domain = domain[4:]
        return domain
    except Exception:
        return None


def is_valid_url(url: str) -> bool:
    """
    Check if string is a valid URL format.

    Args:
        url: String to check

    Returns:
        True if valid URL format
    """
    pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(pattern.match(url))


def _format_size(size: int) -> str:
    """Format bytes to human readable size."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"
