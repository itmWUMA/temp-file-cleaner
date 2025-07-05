"""
Contains the logic for different types of filters (e.g., age, pattern).
"""
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any

def _parse_duration(duration_str: str) -> timedelta:
    """
    Parses a duration string (e.g., "30d", "2h", "5m") into a timedelta object.
    """
    unit = duration_str[-1].lower()
    value = int(duration_str[:-1])
    if unit == 'd':
        return timedelta(days=value)
    if unit == 'h':
        return timedelta(hours=value)
    if unit == 'm':
        return timedelta(minutes=value)
    if unit == 's':
        return timedelta(seconds=value)
    raise ValueError(f"Invalid duration unit: {unit}. Must be one of 'd', 'h', 'm', 's'.")


class AgeFilter:
    """Filters files based on their last modification time."""

    def __init__(self, args: Dict[str, Any]):
        if 'older_than' in args:
            self.mode = 'older_than'
            duration_str = args['older_than']
        # 'newer_than' is not in P0 scope but good to have the structure
        # elif 'newer_than' in args:
        #     self.mode = 'newer_than'
        #     duration_str = args['newer_than']
        else:
            raise ValueError("AgeFilter requires 'older_than' parameter.")
        
        self.delta = _parse_duration(duration_str)
        self.threshold_timestamp = datetime.now() - self.delta

    def matches(self, file_path: Path) -> bool:
        """
        Checks if a file's age matches the filter criteria.

        Args:
            file_path: The path to the file to check.

        Returns:
            True if the file matches the age criteria, False otherwise.
        """
        try:
            file_mod_time = file_path.stat().st_mtime
            
            if self.mode == 'older_than':
                # If the file's modification timestamp is less than the threshold, it's older.
                return file_mod_time < self.threshold_timestamp.timestamp()
            
            # Placeholder for future 'newer_than' implementation
            # if self.mode == 'newer_than':
            #     return file_mod_time > self.threshold_timestamp.timestamp()

        except FileNotFoundError:
            # If file doesn't exist during check, it can't match.
            return False
            
        return False

def apply_filters(files: List[Path], filter_configs: List[Dict[str, Any]]) -> List[Path]:
    """
    Applies a series of filters to a list of files.
    Note: 'pattern' filter is handled by `filesystem.find_files`, this handles the rest.
    """
    filtered_files = files
    
    for f_config in filter_configs:
        if f_config.type == 'age':
            age_filter = AgeFilter(f_config.args)
            filtered_files = [f for f in filtered_files if age_filter.matches(f)]
        # Add other filters like 'size' here in the future
        # elif f_config.type == 'size':
        #     ...
            
    return filtered_files