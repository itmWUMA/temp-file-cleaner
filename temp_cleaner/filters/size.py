"""
Filter for files based on their size.
"""

from pathlib import Path
from typing import Dict
from .base import Filter

class SizeFilter(Filter):
    """Filters files based on their size. (byte)"""

    def __init__(self, args: Dict[str, int]):
        if 'greater_than' in args:
            self.mode = 'greater_than'
            self.limit_size = args['greater_than']
        else:
            raise ValueError("SizeFilter requires 'greater_than' parameter.")
        
    def matches(self, file_path : Path) -> bool:
        """
        Checks if a file's size matches the filter criteria.
        """
        try:
            file_size = file_path.stat().st_size
            if self.mode == 'greater_than':
                return self.limit_size < file_size
        except FileNotFoundError:
            return False
        return False