"""
Date/Time Utilities - Functions for date and time operations.
"""

from datetime import datetime, timedelta, date
from typing import List, Optional, Tuple
import calendar


def time_ago(dt: datetime, now: Optional[datetime] = None) -> str:
    """
    Convert datetime to human-readable "time ago" format.

    Args:
        dt: The datetime to convert
        now: Current time (defaults to now)

    Returns:
        Human-readable string like "2 hours ago"

    Example:
        >>> time_ago(datetime.now() - timedelta(hours=2))
        '2 hours ago'
    """
    if now is None:
        now = datetime.now()

    diff = now - dt

    seconds = diff.total_seconds()
    if seconds < 0:
        return "in the future"

    intervals = [
        (31536000, "year"),
        (2592000, "month"),
        (604800, "week"),
        (86400, "day"),
        (3600, "hour"),
        (60, "minute"),
        (1, "second"),
    ]

    for seconds_in_interval, name in intervals:
        count = int(seconds // seconds_in_interval)
        if count >= 1:
            plural = "s" if count != 1 else ""
            return f"{count} {name}{plural} ago"

    return "just now"


def time_until(dt: datetime, now: Optional[datetime] = None) -> str:
    """
    Convert datetime to human-readable "time until" format.

    Args:
        dt: The future datetime
        now: Current time (defaults to now)

    Returns:
        Human-readable string like "in 2 hours"
    """
    if now is None:
        now = datetime.now()

    diff = dt - now

    seconds = diff.total_seconds()
    if seconds < 0:
        return "already passed"

    intervals = [
        (31536000, "year"),
        (2592000, "month"),
        (604800, "week"),
        (86400, "day"),
        (3600, "hour"),
        (60, "minute"),
        (1, "second"),
    ]

    for seconds_in_interval, name in intervals:
        count = int(seconds // seconds_in_interval)
        if count >= 1:
            plural = "s" if count != 1 else ""
            return f"in {count} {name}{plural}"

    return "now"


def business_days_between(start_date: date, end_date: date, holidays: Optional[List[date]] = None) -> int:
    """
    Calculate business days between two dates.

    Args:
        start_date: Start date
        end_date: End date
        holidays: List of holiday dates to exclude

    Returns:
        Number of business days

    Example:
        >>> business_days_between(date(2024, 1, 1), date(2024, 1, 8))
        5
    """
    if holidays is None:
        holidays = []

    business_days = 0
    current = start_date

    while current < end_date:
        # Monday = 0, Sunday = 6
        if current.weekday() < 5 and current not in holidays:
            business_days += 1
        current += timedelta(days=1)

    return business_days


def add_business_days(start_date: date, days: int, holidays: Optional[List[date]] = None) -> date:
    """
    Add business days to a date.

    Args:
        start_date: Starting date
        days: Number of business days to add
        holidays: List of holiday dates to skip

    Returns:
        Resulting date
    """
    if holidays is None:
        holidays = []

    current = start_date
    added = 0

    while added < days:
        current += timedelta(days=1)
        if current.weekday() < 5 and current not in holidays:
            added += 1

    return current


def format_duration(seconds: float, granularity: int = 2) -> str:
    """
    Format seconds into human-readable duration.

    Args:
        seconds: Number of seconds
        granularity: Number of time units to show

    Returns:
        Formatted duration string

    Example:
        >>> format_duration(3661)
        '1 hour, 1 minute'
        >>> format_duration(90061, granularity=3)
        '1 day, 1 hour, 1 minute'
    """
    intervals = [
        ('day', 86400),
        ('hour', 3600),
        ('minute', 60),
        ('second', 1),
    ]

    result = []
    for name, count in intervals:
        value = int(seconds // count)
        if value:
            seconds -= value * count
            plural = "s" if value != 1 else ""
            result.append(f"{value} {name}{plural}")

    if not result:
        return "0 seconds"

    return ', '.join(result[:granularity])


def get_week_dates(dt: Optional[date] = None, start_monday: bool = True) -> List[date]:
    """
    Get all dates in the week containing the given date.

    Args:
        dt: Date in the week (defaults to today)
        start_monday: If True, week starts Monday; else Sunday

    Returns:
        List of 7 dates in the week

    Example:
        >>> get_week_dates(date(2024, 1, 3))
        [date(2024, 1, 1), date(2024, 1, 2), ..., date(2024, 1, 7)]
    """
    if dt is None:
        dt = date.today()

    if start_monday:
        start = dt - timedelta(days=dt.weekday())
    else:
        start = dt - timedelta(days=(dt.weekday() + 1) % 7)

    return [start + timedelta(days=i) for i in range(7)]


def get_month_dates(year: int, month: int) -> List[date]:
    """
    Get all dates in a month.

    Args:
        year: Year
        month: Month (1-12)

    Returns:
        List of all dates in the month
    """
    _, num_days = calendar.monthrange(year, month)
    return [date(year, month, day) for day in range(1, num_days + 1)]


def is_weekend(dt: date) -> bool:
    """
    Check if date is a weekend.

    Args:
        dt: Date to check

    Returns:
        True if Saturday or Sunday
    """
    return dt.weekday() >= 5


def is_leap_year(year: int) -> bool:
    """
    Check if year is a leap year.

    Args:
        year: Year to check

    Returns:
        True if leap year
    """
    return calendar.isleap(year)


def get_age(birth_date: date, reference_date: Optional[date] = None) -> int:
    """
    Calculate age in years.

    Args:
        birth_date: Date of birth
        reference_date: Date to calculate age at (defaults to today)

    Returns:
        Age in years
    """
    if reference_date is None:
        reference_date = date.today()

    age = reference_date.year - birth_date.year

    # Adjust if birthday hasn't occurred yet this year
    if (reference_date.month, reference_date.day) < (birth_date.month, birth_date.day):
        age -= 1

    return age


def get_quarter(dt: date) -> int:
    """
    Get the quarter (1-4) for a date.

    Args:
        dt: Date

    Returns:
        Quarter number (1-4)
    """
    return (dt.month - 1) // 3 + 1


def get_quarter_dates(year: int, quarter: int) -> Tuple[date, date]:
    """
    Get start and end dates of a quarter.

    Args:
        year: Year
        quarter: Quarter (1-4)

    Returns:
        Tuple of (start_date, end_date)
    """
    start_month = (quarter - 1) * 3 + 1
    end_month = start_month + 2
    _, last_day = calendar.monthrange(year, end_month)

    return date(year, start_month, 1), date(year, end_month, last_day)


def parse_date(date_string: str, formats: Optional[List[str]] = None) -> Optional[datetime]:
    """
    Parse date string trying multiple formats.

    Args:
        date_string: String to parse
        formats: List of formats to try

    Returns:
        Parsed datetime or None if no format matches
    """
    if formats is None:
        formats = [
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%m/%d/%Y",
            "%Y/%m/%d",
            "%d-%m-%Y",
            "%B %d, %Y",
            "%b %d, %Y",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S",
        ]

    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue

    return None
