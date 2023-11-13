from re import match

from src.shared.domain.exceptions.invalid_value import InvalidValueException
from src.shared.domain.value_objects.string import StringValueObject


class UserEmail(StringValueObject):
    EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    def _validate(self) -> None:
        super()._validate()
        if not match(self.EMAIL_REGEX, self.value):
            raise InvalidValueException(
                f"{self.value} is not a valid email")
