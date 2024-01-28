import enum

from src.planner.shared.domain.value_objects.string import StringValueObject


class Currency(str, enum.Enum):
    USD = "USD"
    VES = "VES"

    @staticmethod
    def keys():
        return [c.value for c in Currency]


class AccountCurrency(StringValueObject):
    NAME = "currency"

    def _validate(self, value: str):
        super()._validate(value)
        if value not in Currency.keys():
            raise self._fail(f"{value} is not a valid currency")
