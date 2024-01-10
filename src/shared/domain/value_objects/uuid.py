from uuid import UUID

from src.shared.domain.value_objects.base import ValueObject


class UuidValueObject(ValueObject):
    BASE_TYPE = UUID

    @property
    def primitive(self)->str:
        return str(self.value)