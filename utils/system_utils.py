"""
System Utilities - Functions for system-related operations.
"""

import os
import sys
import platform
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


def get_disk_usage(path: str = "/") -> Dict:
    """
    Get disk usage information for a path.

    Args:
        path: Path to check (defaults to root)

    Returns:
        Dictionary with disk usage info

    Example:
        >>> get_disk_usage("C:/")
        {'total': '500 GB', 'used': '250 GB', 'free': '250 GB', 'percent': 50.0}
    """
    try:
        if sys.platform == 'win32':
            import ctypes
            free_bytes = ctypes.c_ulonglong(0)
            total_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                ctypes.c_wchar_p(path),
                None,
                ctypes.pointer(total_bytes),
                ctypes.pointer(free_bytes)
            )
            total = total_bytes.value
            free = free_bytes.value
            used = total - free
        else:
            stat = os.statvfs(path)
            total = stat.f_blocks * stat.f_frsize
            free = stat.f_bavail * stat.f_frsize
            used = total - free

        percent = (used / total) * 100 if total > 0 else 0

        return {
            "total": _format_size(total),
            "total_bytes": total,
            "used": _format_size(used),
            "used_bytes": used,
            "free": _format_size(free),
            "free_bytes": free,
            "percent": round(percent, 1),
        }
    except Exception as e:
        return {"error": str(e)}


def get_system_info() -> Dict:
    """
    Get comprehensive system information.

    Returns:
        Dictionary with system info

    Example:
        >>> get_system_info()
        {'os': 'Windows', 'version': '10', 'machine': 'AMD64', ...}
    """
    return {
        "os": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "hostname": platform.node(),
        "architecture": platform.architecture()[0],
    }


def find_large_files(directory: str, min_size_mb: float = 100, top_n: int = 10) -> List[Dict]:
    """
    Find largest files in a directory.

    Args:
        directory: Directory to search
        min_size_mb: Minimum file size in MB
        top_n: Number of files to return

    Returns:
        List of file info dictionaries sorted by size

    Example:
        >>> find_large_files("./", min_size_mb=50)
        [{'path': 'bigfile.zip', 'size': '150 MB'}, ...]
    """
    min_size_bytes = min_size_mb * 1024 * 1024
    large_files = []

    path = Path(directory)
    try:
        for file in path.rglob("*"):
            if file.is_file():
                try:
                    size = file.stat().st_size
                    if size >= min_size_bytes:
                        large_files.append({
                            "path": str(file),
                            "name": file.name,
                            "size_bytes": size,
                            "size": _format_size(size),
                            "modified": datetime.fromtimestamp(file.stat().st_mtime),
                        })
                except (PermissionError, OSError):
                    continue
    except PermissionError:
        pass

    # Sort by size descending
    large_files.sort(key=lambda x: x["size_bytes"], reverse=True)
    return large_files[:top_n]


def get_environment_variable(name: str, default: Optional[str] = None) -> Optional[str]:
    """
    Get environment variable value.

    Args:
        name: Variable name
        default: Default value if not found

    Returns:
        Variable value or default
    """
    return os.environ.get(name, default)


def set_environment_variable(name: str, value: str) -> None:
    """
    Set environment variable for current process.

    Args:
        name: Variable name
        value: Variable value
    """
    os.environ[name] = value


def get_all_environment_variables() -> Dict[str, str]:
    """
    Get all environment variables.

    Returns:
        Dictionary of all environment variables
    """
    return dict(os.environ)


def run_command(command: str, timeout: Optional[int] = None, capture_output: bool = True) -> Dict:
    """
    Run a shell command and return results.

    Args:
        command: Command to run
        timeout: Timeout in seconds
        capture_output: Capture stdout/stderr

    Returns:
        Dictionary with command results

    Example:
        >>> run_command("echo Hello")
        {'success': True, 'stdout': 'Hello', 'returncode': 0}
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=capture_output,
            text=True,
            timeout=timeout
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip() if result.stdout else "",
            "stderr": result.stderr.strip() if result.stderr else "",
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Command timed out",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


def get_current_directory() -> str:
    """Get current working directory."""
    return os.getcwd()


def change_directory(path: str) -> bool:
    """
    Change current working directory.

    Args:
        path: New directory path

    Returns:
        True if successful
    """
    try:
        os.chdir(path)
        return True
    except Exception:
        return False


def get_home_directory() -> str:
    """Get user's home directory."""
    return str(Path.home())


def path_exists(path: str) -> bool:
    """Check if path exists."""
    return Path(path).exists()


def is_file(path: str) -> bool:
    """Check if path is a file."""
    return Path(path).is_file()


def is_directory(path: str) -> bool:
    """Check if path is a directory."""
    return Path(path).is_dir()


def get_file_extension(filepath: str) -> str:
    """Get file extension."""
    return Path(filepath).suffix


def get_filename(filepath: str, with_extension: bool = True) -> str:
    """
    Get filename from path.

    Args:
        filepath: Full file path
        with_extension: Include extension

    Returns:
        Filename
    """
    path = Path(filepath)
    return path.name if with_extension else path.stem


def ensure_directory(path: str) -> bool:
    """
    Create directory if it doesn't exist.

    Args:
        path: Directory path

    Returns:
        True if directory exists or was created
    """
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False


def get_temp_directory() -> str:
    """Get system temporary directory."""
    import tempfile
    return tempfile.gettempdir()


def create_temp_file(suffix: str = "", prefix: str = "tmp") -> str:
    """
    Create a temporary file and return its path.

    Args:
        suffix: File suffix/extension
        prefix: File prefix

    Returns:
        Path to temporary file
    """
    import tempfile
    fd, path = tempfile.mkstemp(suffix=suffix, prefix=prefix)
    os.close(fd)
    return path


def _format_size(size: int) -> str:
    """Format bytes to human readable size."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"
