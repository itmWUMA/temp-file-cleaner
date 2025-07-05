"""
Defines the abstract base class for all Filter strategies.
"""
import abc
from pathlib import Path

class Filter(abc.ABC):
    """Abstract base class for all secondary filters."""

    @abc.abstractmethod
    def matches(self, file_path: Path) -> bool:
        """
        Checks if a file path matches the filter's criteria.

        Args:
            file_path: The path to the file to check.

        Returns:
            True if the file matches, False otherwise.
        """
        pass