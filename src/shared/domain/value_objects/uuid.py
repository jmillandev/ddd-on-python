from uuid import UUID

from src.shared.domain.value_objects.base import ValueObject


class UuidValueObject(ValueObject):
    BASE_TYPE = UUID

    def _name(self):
        return "uuid"

    @property
    def primitive(self)->str:
        return str(self.value)