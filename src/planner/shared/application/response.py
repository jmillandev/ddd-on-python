from pydantic import BaseModel

from src.planner.shared.domain.bus.query import QueryResponse
from src.planner.shared.domain.aggregates import Aggregate


class Response(BaseModel, QueryResponse):

    # TODO: Use entity_to_response
    @classmethod
    def build(cls, entity: Aggregate) -> 'Response':
        attributes = {
            key: getattr(entity, key).primitive for key in cls.__annotations__.keys()
        }
        return cls(**attributes)
