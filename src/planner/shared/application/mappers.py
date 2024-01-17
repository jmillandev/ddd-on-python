from typing import Any, Dict, TypeVar
from src.planner.shared.domain.aggregates import Aggregate
from src.planner.shared.domain.bus.query import QueryResponse


def dict_to_entity(data: Dict[str, Any], entity_class: type[Aggregate]):
    """Create a Entity from a dict.
    Used for deserialization of a Aggregate. Usually used in a Database.

    Args:
        data (dict[str, Any]): A dict with the attributes of a Entity
        entity_class (Aggregate): A Entity class(like User, AuthCredential, etc)

    Returns:
        Entity
    """
    annotations = entity_class.__annotations__
    attributes = {
        key: annotations[key](value)
        for key, value in data.items()
        if key in annotations
    }
    return entity_class(**attributes)


QR = TypeVar("QR", bound=QueryResponse)

def entity_to_response(entity: Aggregate, response: type[QR]) -> QR:
    attributes = {
            key: getattr(entity, key).primitive for key in response.__annotations__.keys()
        }
    return response(**attributes)
