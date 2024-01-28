import enum

from src.planner.shared.domain.value_objects.string import StringValueObject


class Pronoun(str, enum.Enum):
    HE = "he"
    SHE = "she"

    @staticmethod
    def keys():
        return [c.value for c in Pronoun]


class UserPronoun(StringValueObject):
    NAME = "pronoun"

    def _validate(self, value: str):
        super()._validate(value)
        if value not in Pronoun.keys():
            raise self._fail(f"{value} is not a valid pronoun")
