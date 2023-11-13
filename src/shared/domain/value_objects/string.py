from src.shared.domain.exceptions.invalid_value import InvalidValueException
from src.shared.domain.value_objects.base import ValueObject


class StringValueObject(ValueObject):
    BASE_TYPE = str

    @property
    def _name(self) -> str:
        return "string"
