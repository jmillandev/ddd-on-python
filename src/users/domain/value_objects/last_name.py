from src.shared.domain.exceptions.invalid_value import InvalidValueException
from src.shared.domain.value_objects.string import StringValueObject


class UserLastName(StringValueObject):
    SIZE = 50

    def _validate(self) -> None:
        super()._validate()
        if len(self.value) > self.SIZE:
            raise InvalidValueException(f"{self.value} should be less than {self.SIZE} characters")
