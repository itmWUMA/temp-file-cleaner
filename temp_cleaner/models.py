"""
Defines the data structures for jobs, filters, and actions.
"""
import dataclasses
from typing import List, Dict, Any, Optional

from .actions import Action
from .filters import Filter
from .triggers import Trigger


@dataclasses.dataclass
class Job:
    """
    Represents a single cleanup job, holding strategy objects for filters and actions.
    """
    name: str
    paths: List[str]
    pattern: Optional[str]  # The primary pattern filter is treated specially
    filters: List[Filter]   # List of secondary filter objects (e.g., AgeFilter)
    actions: List[Action]   # List of action objects (e.g., TrashAction)
    triggers: List[Trigger]   # List of trigger objects (e.g., ScheduleTrigger)

@dataclasses.dataclass
class Config:
    """Represents the entire config.yaml structure."""
    jobs: List[Job]