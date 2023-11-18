from src.shared.domain.value_objects.uuid import UuidValueObject
from uuid import uuid4

class UserId(UuidValueObject):
    
    @classmethod
    def generate(cls):
        return cls(uuid4())
