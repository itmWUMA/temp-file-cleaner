"""
Encapsulates all filesystem-related operations, such as path resolving,
finding files, and performing actions like delete or trash.
"""
import os
import glob
from pathlib import Path
from typing import List

import send2trash

def resolve_path(path_str: str) -> Path:
    """
    Resolves a path string, expanding user home directory ('~') and environment variables.

    Args:
        path_str: The path string from the config (e.g., '~/Downloads', '$TEMP/logs').

    Returns:
        An absolute Path object.
    """
    # Expand '~' to user's home directory
    expanded_path = os.path.expanduser(path_str)
    # Expand environment variables like $TEMP or %TEMP%
    expanded_path = os.path.expandvars(expanded_path)
    return Path(expanded_path).resolve()


def find_files(base_path: Path, pattern: str) -> List[Path]:
    """
    Finds all files and directories matching a glob pattern within a base path.

    Args:
        base_path: The absolute path to search in.
        pattern: The glob pattern to match (e.g., '*.log', '**/*.tmp').

    Returns:
        A list of Path objects for all matches.
    """
    if not base_path.is_dir():
        return []
    
    # Use recursive glob search
    # The pattern should be relative to the base_path, but glob works by joining them.
    # The '/**/' syntax is crucial for recursive searching.
    search_pattern = str(base_path / pattern)
    
    # glob.glob with recursive=True will handle '**' correctly.
    return [Path(p) for p in glob.glob(search_pattern, recursive=True)]


def trash_item(path: Path, dry_run: bool = False):
    """
    Moves a file or directory to the system's trash.

    Args:
        path: The path to the item to trash.
        dry_run: If True, only prints the action without executing it.
    """
    print(f"[DRY-RUN] Trashing: {path}" if dry_run else f"Trashing: {path}")
    if not dry_run:
        send2trash.send2trash(path)


def delete_item(path: Path, dry_run: bool = False):
    """
    Permanently deletes a file or directory.

    Args:
        path: The path to the item to delete.
        dry_run: If True, only prints the action without executing it.
    """
    print(f"[DRY-RUN] Deleting: {path}" if dry_run else f"Deleting: {path}")
    if not dry_run:
        if path.is_dir():
            # For simplicity, we'll recursively delete directories.
            # A more robust solution might require shutil.rmtree for non-empty dirs.
            # However, for many build artifacts, os.rmdir might be sufficient if they are empty
            # or we delete contents first. Let's use a safer recursive delete.
            import shutil
            shutil.rmtree(path)
        else:
            path.unlink()