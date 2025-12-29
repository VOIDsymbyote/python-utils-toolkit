"""
Python Utils Toolkit - A collection of reusable utility functions.
"""

from .file_utils import (
    find_files,
    get_file_info,
    batch_rename,
    find_duplicates,
    organize_by_extension,
)

from .text_utils import (
    extract_emails,
    extract_urls,
    word_frequency,
    slugify,
    validate_email,
)

from .date_utils import (
    time_ago,
    business_days_between,
    format_duration,
    get_week_dates,
)

from .web_utils import (
    download_file,
    is_url_valid,
    get_page_title,
)

from .system_utils import (
    get_disk_usage,
    get_system_info,
    find_large_files,
)

__version__ = "1.0.0"
__author__ = "Your Name"
