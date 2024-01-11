from typing import TypeVar
from pydantic import BaseModel

Entity = TypeVar('Entity')

class Response(BaseModel):

    @classmethod
    def build(cls, entity: Entity) -> Entity:
        attributes = {key: getattr(entity, key).primitive for key in cls.__annotations__.keys()}
        return cls(**attributes)
