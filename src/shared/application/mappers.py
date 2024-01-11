from typing import Any, TypeVar

Entity = TypeVar('Entity')

def dict_to_entity(data: dict[str, Any], entity: Entity):
    """Create a Entity from a dict.
    Used for deserialization of a Entity. Usually used in a Database.

    Args:
        data (dict[str, Any]): A dict with the attributes of a Entity
        entity (Entity): A Entity class(like User, AuthCredential, etc)

    Returns:
        Entity
    """
    annotations = entity.__annotations__
    attributes = { key: annotations[key](value) for key, value in data.items() if key in annotations }
    return entity(**attributes)
