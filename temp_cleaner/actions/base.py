"""
Defines the abstract base class for all Action strategies.
"""
import abc
from pathlib import Path

class Action(abc.ABC):
    """Abstract base class for all actions."""
    
    @abc.abstractmethod
    def execute(self, file_path: Path, dry_run: bool = False):
        """
        Executes the action on a given file path.

        Args:
            file_path: The path to the file or directory to act upon.
            dry_run: If True, simulates the action without making changes.
        """
        pass