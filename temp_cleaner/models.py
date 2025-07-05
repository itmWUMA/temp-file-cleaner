"""
Defines the data structures for jobs, filters, and actions.
"""
import dataclasses
from typing import List, Dict, Any

@dataclasses.dataclass(frozen=True)
class ActionConfig:
    """
    Represents an action configuration from the YAML file.
    For P0, it's just a string like 'delete' or 'trash'.
    """
    type: str

@dataclasses.dataclass(frozen=True)
class FilterConfig:
    """
    Represents a filter configuration from the YAML file.
    e.g., {'pattern': '**/*.log'} or {'age': 'older_than: "30d"'}
    """
    type: str
    args: Dict[str, Any]


@dataclasses.dataclass
class Job:
    """Represents a single cleanup job."""
    name: str
    paths: List[str]
    filters: List[FilterConfig]
    actions: List[ActionConfig]
    # Triggers are parsed but not used by the engine in P0
    triggers: List[Dict[str, Any]]

@dataclasses.dataclass
class Config:
    """Represents the entire config.yaml structure."""
    jobs: List[Job]