from typing import Any, Generic, TypeVar, Union

from src.planner.shared.domain.exceptions.invalid_value import InvalidValueException

T = TypeVar("T")


class ValueObject(Generic[T]):
    """
    Base class for value objects
    """

    NAME: str
    BASE_TYPE: type[T]
    _value: T

    def __init__(self, value: Any) -> None:
        self._set_value(value)

    def _cast(self, value: Any) -> T:
        if value is None:
            raise self._fail("Is required")
        if isinstance(value, self.BASE_TYPE):
            return value
        try:
            return self.BASE_TYPE(value)  # type: ignore[call-arg]
        except Exception:
            self._fail(f"Invalid {self.BASE_TYPE.__name__}")
            return None  # type: ignore[return-value]

    def _fail(self, message: str):
        raise InvalidValueException(message=message, source=self._name)

    @property
    def value(self) -> T:
        return self._value

    @property
    def primitive(self) -> Union[str, int, bool]:
        """
        Use this method to get the primitive value of the object. Useful for serialization
        """
        return self.value  # type: ignore[return-value]

    def _set_value(self, value: Any) -> None:
        casted_value = self._cast(value)
        self._validate(casted_value)
        self._value = casted_value

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

    def _validate(self, value: T):
        """
        Override this method to implement custom validations
        """
        if not isinstance(value, self.BASE_TYPE):
            raise self._fail(
                f"invalid type: Want {self.BASE_TYPE.__name__} got {type(value).__name__}"
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
