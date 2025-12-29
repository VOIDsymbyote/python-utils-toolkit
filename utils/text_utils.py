"""
Text Utilities - Functions for text processing and manipulation.
"""

import re
import unicodedata
from typing import List, Dict, Optional
from collections import Counter


def extract_emails(text: str) -> List[str]:
    """
    Extract all email addresses from text.

    Args:
        text: Input text to search

    Returns:
        List of email addresses found

    Example:
        >>> extract_emails("Contact us at hello@example.com or support@test.org")
        ['hello@example.com', 'support@test.org']
    """
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(pattern, text)


def extract_urls(text: str) -> List[str]:
    """
    Extract all URLs from text.

    Args:
        text: Input text to search

    Returns:
        List of URLs found

    Example:
        >>> extract_urls("Visit https://example.com or http://test.org")
        ['https://example.com', 'http://test.org']
    """
    pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    return re.findall(pattern, text)


def extract_phone_numbers(text: str, country_code: str = "US") -> List[str]:
    """
    Extract phone numbers from text.

    Args:
        text: Input text to search
        country_code: Country code for pattern matching

    Returns:
        List of phone numbers found
    """
    patterns = {
        "US": r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4}',
        "UK": r'[\+]?[0-9]{2}[-\s]?[0-9]{4}[-\s]?[0-9]{6}',
    }
    pattern = patterns.get(country_code, patterns["US"])
    return re.findall(pattern, text)


def word_frequency(text: str, top_n: Optional[int] = None, ignore_case: bool = True) -> Dict[str, int]:
    """
    Count word frequency in text.

    Args:
        text: Input text
        top_n: Return only top N words (None for all)
        ignore_case: If True, treat words case-insensitively

    Returns:
        Dictionary of word counts

    Example:
        >>> word_frequency("hello world hello", top_n=2)
        {'hello': 2, 'world': 1}
    """
    if ignore_case:
        text = text.lower()

    # Extract words (alphanumeric only)
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    counter = Counter(words)

    if top_n:
        return dict(counter.most_common(top_n))
    return dict(counter)


def slugify(text: str, separator: str = "-", max_length: Optional[int] = None) -> str:
    """
    Convert text to URL-friendly slug.

    Args:
        text: Input text
        separator: Character to use as separator
        max_length: Maximum length of slug

    Returns:
        URL-friendly slug

    Example:
        >>> slugify("Hello World! How are you?")
        'hello-world-how-are-you'
    """
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')

    # Convert to lowercase
    text = text.lower()

    # Replace non-alphanumeric with separator
    text = re.sub(r'[^a-z0-9]+', separator, text)

    # Remove leading/trailing separators
    text = text.strip(separator)

    # Truncate if needed
    if max_length:
        text = text[:max_length].rstrip(separator)

    return text


def validate_email(email: str) -> bool:
    """
    Validate email format.

    Args:
        email: Email address to validate

    Returns:
        True if valid format

    Example:
        >>> validate_email("test@example.com")
        True
        >>> validate_email("invalid-email")
        False
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to specified length with suffix.

    Args:
        text: Input text
        max_length: Maximum length (including suffix)
        suffix: String to append when truncated

    Returns:
        Truncated text

    Example:
        >>> truncate_text("This is a long text", 10)
        'This is...'
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def remove_extra_whitespace(text: str) -> str:
    """
    Remove extra whitespace from text.

    Args:
        text: Input text

    Returns:
        Text with normalized whitespace

    Example:
        >>> remove_extra_whitespace("Hello   world  !")
        'Hello world !'
    """
    return ' '.join(text.split())


def count_words(text: str) -> int:
    """
    Count words in text.

    Args:
        text: Input text

    Returns:
        Number of words
    """
    words = re.findall(r'\b\w+\b', text)
    return len(words)


def count_sentences(text: str) -> int:
    """
    Count sentences in text.

    Args:
        text: Input text

    Returns:
        Number of sentences
    """
    sentences = re.split(r'[.!?]+', text)
    return len([s for s in sentences if s.strip()])


def extract_hashtags(text: str) -> List[str]:
    """
    Extract hashtags from text.

    Args:
        text: Input text

    Returns:
        List of hashtags (without #)

    Example:
        >>> extract_hashtags("Check out #python and #coding")
        ['python', 'coding']
    """
    return re.findall(r'#(\w+)', text)


def extract_mentions(text: str) -> List[str]:
    """
    Extract @mentions from text.

    Args:
        text: Input text

    Returns:
        List of mentions (without @)

    Example:
        >>> extract_mentions("Hey @john and @jane!")
        ['john', 'jane']
    """
    return re.findall(r'@(\w+)', text)


def mask_sensitive_data(text: str, mask_char: str = "*") -> str:
    """
    Mask sensitive data like emails and phone numbers.

    Args:
        text: Input text
        mask_char: Character to use for masking

    Returns:
        Text with masked sensitive data
    """
    # Mask emails
    text = re.sub(
        r'([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
        lambda m: mask_char * len(m.group(1)) + '@' + m.group(2),
        text
    )

    # Mask phone numbers (basic)
    text = re.sub(
        r'\b(\d{3})[-.]?(\d{3})[-.]?(\d{4})\b',
        lambda m: mask_char * 3 + '-' + mask_char * 3 + '-' + m.group(3)[-4:],
        text
    )

    return text


def is_palindrome(text: str, ignore_case: bool = True, ignore_spaces: bool = True) -> bool:
    """
    Check if text is a palindrome.

    Args:
        text: Input text
        ignore_case: Ignore case differences
        ignore_spaces: Ignore spaces

    Returns:
        True if palindrome
    """
    if ignore_case:
        text = text.lower()
    if ignore_spaces:
        text = text.replace(" ", "")

    # Keep only alphanumeric
    text = re.sub(r'[^a-zA-Z0-9]', '', text)

    return text == text[::-1]
