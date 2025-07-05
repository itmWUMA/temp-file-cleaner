"""
Defines the abstract base class for all triggers.
"""
import abc
from datetime import datetime

class Trigger(abc.ABC):
    """
    Abstract base class for all triggers.
    
    A trigger determines if a job should run at a given moment.
    """
    
    @abc.abstractmethod
    def should_run(self, current_time: datetime) -> bool:
        """
        Determines whether the job should run based on the trigger's logic.

        Args:
            current_time: The current timestamp to check against.

        Returns:
            True if the job should run, False otherwise.
        """
        raise NotImplementedError
