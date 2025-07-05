"""
Filter for files based on their age (last modification time).
"""
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any

from .base import Filter

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


class AgeFilter(Filter):
    """Filters files based on their last modification time."""

    def __init__(self, args: Dict[str, Any]):
        if 'older_than' in args:
            self.mode = 'older_than'
            duration_str = args['older_than']
        else:
            raise ValueError("AgeFilter requires 'older_than' parameter.")
        
        self.delta = _parse_duration(duration_str)
        self.threshold_timestamp = datetime.now() - self.delta

    def matches(self, file_path: Path) -> bool:
        """
        Checks if a file's age matches the filter criteria.
        """
        try:
            file_mod_time = file_path.stat().st_mtime
            if self.mode == 'older_than':
                return file_mod_time < self.threshold_timestamp.timestamp()
        except FileNotFoundError:
            return False
        return False