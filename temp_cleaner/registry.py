"""
Handles the registration and creation of Action, Filter, and Trigger objects.
This is the core of the Strategy and Factory patterns.
"""
from typing import Dict, Type, Any

# Import concrete strategy classes
from .actions import Action, TrashAction, DeleteAction
from .filters import Filter, AgeFilter
from .triggers import Trigger, ScheduleTrigger

#--- Triggers ---
# Note: on_startup and on_shutdown are "marker" triggers. They don't need a class.
# Their logic is handled directly in the engine based on the config key.

# The 'Registry' is a simple dictionary mapping config strings to classes.
ACTION_REGISTRY: Dict[str, Type[Action]] = {
    'trash': TrashAction,
    'delete': DeleteAction,
}

FILTER_REGISTRY: Dict[str, Type[Filter]] = {
    'age': AgeFilter,
}

TRIGGER_REGISTRY: Dict[str, Type[Trigger]] = {
    "schedule": ScheduleTrigger,
    # These are marker keys. They will be converted to simple string identifiers.
    "on_startup": str,
    "on_shutdown": str,
}

# The 'Factory' functions use the registry to create instances.
def create_action(action_config: Dict[str, Any]) -> Action:
    """
    Factory function to create an Action instance from its config dict.
    
    Args:
        action_config: The configuration dict for the action (e.g., {'trash': {}}).

    Returns:
        An instance of a concrete Action subclass.
    """
    action_type = list(action_config.keys())[0]
    action_args = action_config[action_type]

    ActionClass = ACTION_REGISTRY.get(action_type)
    if not ActionClass:
        raise ValueError(f"Unknown action type: {action_type}")
    
    # In the future, if actions have args, they can be passed here:
    # return ActionClass(**action_args)
    return ActionClass()

def create_filter(filter_config: Dict[str, Any]) -> Filter:
    """
    Factory function to create a Filter instance from its config dict.

    Args:
        filter_config: The configuration dict for the filter (e.g., {'age': {'older_than': '30d'}}).

    Returns:
        An instance of a concrete Filter subclass.
    """
    filter_type = list(filter_config.keys())[0]
    filter_args = filter_config[filter_type]

    FilterClass = FILTER_REGISTRY.get(filter_type)
    if not FilterClass:
        raise ValueError(f"Unknown filter type: {filter_type}")
    
    # Pass the arguments to the constructor of the filter class.
    return FilterClass(filter_args)

def create_trigger(trigger_config: Any) -> Trigger:
    """
    Factory function to create a Trigger instance from its config.
    It supports both dicts for complex triggers and simple strings for marker triggers.

    Args:
        trigger_config: The config, e.g., {'schedule': '0 0 * * *'} or 'on_startup'.

    Returns:
        An instance of a concrete Trigger subclass or a string for marker triggers.
    """
    if isinstance(trigger_config, str):
        trigger_type = trigger_config
        value = None # No value for simple string triggers
        if trigger_type not in TRIGGER_REGISTRY:
             raise ValueError(f"Unknown trigger type: '{trigger_type}'")
        return trigger_type # Return the string itself as the "trigger"

    if isinstance(trigger_config, dict):
        if len(trigger_config) != 1:
            raise ValueError(f"Invalid trigger configuration format: {trigger_config}")
        
        trigger_type, value = next(iter(trigger_config.items()))
        TriggerClass = TRIGGER_REGISTRY.get(trigger_type)
        
        if not TriggerClass:
            raise ValueError(f"Unknown trigger type: '{trigger_type}'")

        if TriggerClass is str: # Handle marker triggers defined as dicts, e.g., {'on_startup': True}
            return trigger_type

        return TriggerClass(value)

    raise ValueError(f"Unsupported trigger format: {trigger_config}")