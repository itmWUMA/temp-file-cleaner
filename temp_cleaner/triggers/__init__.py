"""
This package contains the implementations for various trigger strategies.

The concrete classes are registered and instantiated via the factory
in `temp_cleaner.registry`.
"""
from .base import Trigger
from .schedule import ScheduleTrigger