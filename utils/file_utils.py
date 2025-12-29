"""
File Utilities - Functions for common file operations.
"""

import os
import shutil
import hashlib
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


def find_files(directory: str, pattern: str = "*") -> List[Path]:
    """
    Find files matching a pattern in a directory.

    Args:
        directory: Directory to search in
        pattern: Glob pattern (e.g., "*.py", "*.txt")

    Returns:
        List of matching file paths

    Example:
        >>> find_files("./src", "*.py")
        [Path('src/main.py'), Path('src/utils.py')]
    """
    path = Path(directory)
    return list(path.rglob(pattern))


def get_file_info(filepath: str) -> Dict:
    """
    Get detailed information about a file.

    Args:
        filepath: Path to the file

    Returns:
        Dictionary with file metadata

    Example:
        >>> get_file_info("example.txt")
        {'name': 'example.txt', 'size': 1024, 'size_human': '1.0 KB', ...}
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    stat = path.stat()
    size = stat.st_size

    # Human readable size
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            size_human = f"{size:.1f} {unit}"
            break
        size /= 1024
    else:
        size_human = f"{size:.1f} PB"

    return {
        "name": path.name,
        "path": str(path.absolute()),
        "extension": path.suffix,
        "size": stat.st_size,
        "size_human": size_human,
        "created": datetime.fromtimestamp(stat.st_ctime),
        "modified": datetime.fromtimestamp(stat.st_mtime),
        "is_file": path.is_file(),
        "is_dir": path.is_dir(),
    }


def batch_rename(directory: str, old_pattern: str, new_pattern: str, dry_run: bool = True) -> List[Dict]:
    """
    Batch rename files in a directory.

    Args:
        directory: Directory containing files
        old_pattern: Pattern to find in filenames
        new_pattern: Pattern to replace with
        dry_run: If True, only show what would be renamed

    Returns:
        List of rename operations (old_name, new_name)

    Example:
        >>> batch_rename("./images", "IMG_", "photo_", dry_run=True)
        [{'old': 'IMG_001.jpg', 'new': 'photo_001.jpg'}, ...]
    """
    results = []
    path = Path(directory)

    for file in path.iterdir():
        if file.is_file() and old_pattern in file.name:
            new_name = file.name.replace(old_pattern, new_pattern)
            new_path = file.parent / new_name

            results.append({
                "old": file.name,
                "new": new_name,
                "old_path": str(file),
                "new_path": str(new_path),
            })

            if not dry_run:
                file.rename(new_path)

    return results


def find_duplicates(directory: str, by_hash: bool = True) -> Dict[str, List[str]]:
    """
    Find duplicate files in a directory.

    Args:
        directory: Directory to search
        by_hash: If True, compare by content hash; else by size

    Returns:
        Dictionary mapping hash/size to list of duplicate file paths

    Example:
        >>> find_duplicates("./downloads")
        {'abc123...': ['file1.txt', 'file1_copy.txt'], ...}
    """
    files_map = {}
    path = Path(directory)

    for file in path.rglob("*"):
        if file.is_file():
            if by_hash:
                # Calculate MD5 hash
                hasher = hashlib.md5()
                with open(file, 'rb') as f:
                    for chunk in iter(lambda: f.read(8192), b''):
                        hasher.update(chunk)
                key = hasher.hexdigest()
            else:
                key = file.stat().st_size

            if key not in files_map:
                files_map[key] = []
            files_map[key].append(str(file))

    # Return only duplicates
    return {k: v for k, v in files_map.items() if len(v) > 1}


def organize_by_extension(source_dir: str, target_dir: Optional[str] = None, dry_run: bool = True) -> Dict[str, List[str]]:
    """
    Organize files into folders by their extension.

    Args:
        source_dir: Directory containing files to organize
        target_dir: Target directory (defaults to source_dir)
        dry_run: If True, only show what would be moved

    Returns:
        Dictionary mapping extensions to list of files

    Example:
        >>> organize_by_extension("./downloads")
        {'.pdf': ['doc1.pdf', 'doc2.pdf'], '.jpg': ['img1.jpg'], ...}
    """
    if target_dir is None:
        target_dir = source_dir

    source_path = Path(source_dir)
    target_path = Path(target_dir)

    organized = {}

    for file in source_path.iterdir():
        if file.is_file():
            ext = file.suffix.lower() or "no_extension"

            if ext not in organized:
                organized[ext] = []
            organized[ext].append(file.name)

            if not dry_run:
                # Create folder for extension
                ext_folder = target_path / ext.lstrip(".")
                ext_folder.mkdir(exist_ok=True)

                # Move file
                shutil.move(str(file), str(ext_folder / file.name))

    return organized


def safe_delete(filepath: str, to_trash: bool = True) -> bool:
    """
    Safely delete a file (optionally move to trash).

    Args:
        filepath: Path to file to delete
        to_trash: If True, move to trash instead of permanent delete

    Returns:
        True if successful
    """
    path = Path(filepath)
    if not path.exists():
        return False

    if to_trash:
        # Move to a .trash folder
        trash_dir = path.parent / ".trash"
        trash_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        trash_path = trash_dir / f"{path.stem}_{timestamp}{path.suffix}"
        shutil.move(str(path), str(trash_path))
    else:
        path.unlink()

    return True


def get_directory_size(directory: str) -> Dict:
    """
    Calculate total size of a directory.

    Args:
        directory: Directory path

    Returns:
        Dictionary with size info
    """
    total_size = 0
    file_count = 0

    path = Path(directory)
    for file in path.rglob("*"):
        if file.is_file():
            total_size += file.stat().st_size
            file_count += 1

    # Human readable
    size = total_size
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            size_human = f"{size:.1f} {unit}"
            break
        size /= 1024

    return {
        "total_bytes": total_size,
        "total_human": size_human,
        "file_count": file_count,
    }
