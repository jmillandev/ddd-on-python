from typing import Any, TypeVar, Generic, Optional

from src.planner.shared.domain.exceptions.invalid_value import InvalidValueException

T = TypeVar("T")

class ValueObject(Generic[T]):
    """
    Base class for value objects
    """
    BASE_TYPE: Any
    _value: T

    def __init__(self, value: Any) -> None:
        self._set_value(self._cast(value))

    def _cast(self, value: Any) -> Optional[T]:
        if value is None:
            return None
        if isinstance(value, self.BASE_TYPE):
            return value
        try:
            return self.BASE_TYPE(value)
        except Exception:
            self._fail(f"Invalid {self.BASE_TYPE.__name__}")
            return None

    def _fail(self, message: str):
        raise InvalidValueException(message=message, source=self._name)

    @property
    def value(self) -> T:
        return self._value

    @property
    def primitive(self) -> Any:
        """
        Use this method to get the primitive value of the object. Useful for serialization
        """
        return self.value

    def _set_value(self, value: T):
        self._value = self._cast(value)
        self._validate()

    def is_none(self) -> bool:
        return self.value is None

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, self.__class__):
            return False
        return self.value == o.value

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}('{self.value}')>"

    def __hash__(self) -> int:
        return hash(self.value)

    def _validate(self):
        """
        Override this method to implement custom validations
        """
        if self.is_none():
            raise self._fail("Is required")
        if not isinstance(self.value, self.BASE_TYPE):
            raise self._fail(
                f"invalid type: Want {self.BASE_TYPE.__name__} got {type(self.value).__name__}"
            )

    @property
    def _name(self) -> str:
        """
        Override this method to implement a name that final users can understand in case of error
        """
        if hasattr(self, "NAME"):
            return self.NAME

        raise NotImplementedError(
            "You must implement _name or define NAME in the {self.__class__.__name__}"
        )
