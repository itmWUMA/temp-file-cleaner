"""
Handles the registration and creation of Action and Filter objects.
This is the core of the Strategy and Factory patterns.
"""
from typing import Dict, Type, Any

# Import concrete strategy classes
from .actions import Action, TrashAction, DeleteAction
from .filters import Filter, AgeFilter

# The 'Registry' is a simple dictionary mapping config strings to classes.
ACTION_REGISTRY: Dict[str, Type[Action]] = {
    'trash': TrashAction,
    'delete': DeleteAction,
}

FILTER_REGISTRY: Dict[str, Type[Filter]] = {
    'age': AgeFilter,
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