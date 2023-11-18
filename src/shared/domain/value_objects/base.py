from typing import Any
from src.shared.domain.exceptions.invalid_value import InvalidValueException


class ValueObject:
    """
    Base class for value objects
    """
    OPTIONAL = False
    BASE_TYPE = Any
    _value: BASE_TYPE

    def __init__(self, value: BASE_TYPE) -> None:
        self.value = self._cast(value)

    def _cast(self, value: Any) -> BASE_TYPE:
        if value is None:
            return
        if isinstance(value, self.BASE_TYPE):
            return value
        try:
            return self.BASE_TYPE(value)
        except Exception:
            raise InvalidValueException(f"Invalid {self.BASE_TYPE.__name__}")

    @property
    def value(self) -> BASE_TYPE:
        return self._value

    @value.setter
    def value(self, value: BASE_TYPE) -> None:
        self._value = self._cast(value)
        if self.OPTIONAL and self.is_none():
            return
        self._validate()

    def is_none(self) -> bool:
        return self.value is None

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, self.__class__):
            return False
        return self.value == o.value

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __str__(self):
        return str(self.value)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}('{self.value}')>"

    def __hash__(self) -> int:
        return hash(self.value)

    def _validate(self) -> None:
        """
        Override this method to implement custom validations
        """
        if not isinstance(self.value, self.BASE_TYPE):
            raise ValueError(f"invalid type")

    @property
    def _name(self) -> str:
        """
        Override this method to implement a name that final users can understand
        """
        raise NotImplementedError
