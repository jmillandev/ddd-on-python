import enum

from src.shared.domain.exceptions.invalid_value import InvalidValueException
from src.shared.domain.value_objects.string import StringValueObject


class Pronoun(str, enum.Enum):
    HE = 'he'
    SHE = 'she'

    @staticmethod
    def keys():
        return [c.value for c in Pronoun]


class UserPronoun(StringValueObject):
    def _validate(self) -> None:
        super()._validate()
        if self.value not in Pronoun.keys():
            raise InvalidValueException(f"{self.value} is not a valid pronoun")
