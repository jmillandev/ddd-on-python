from typing import Generic, TypeVar

from pydantic import BaseModel

from src.planner.shared.domain.bus.query import QueryResponse

Entity = TypeVar('Entity')


class Response(BaseModel, Generic[QueryResponse]):

    @classmethod
    def build(cls, entity: Entity) -> Entity:
        attributes = {key: getattr(entity, key).primitive for key in cls.__annotations__.keys()}
        return cls(**attributes)
