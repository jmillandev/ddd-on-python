from typing import TypeVar
from pydantic import BaseModel

Entity = TypeVar('Entity')

class Response(BaseModel):

    def __init__(self, entity: Entity):
        attributes = {key: getattr(entity, key).primitive for key in self.__annotations__.keys()}
        super().__init__(**attributes)
