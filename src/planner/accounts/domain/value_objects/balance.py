from src.planner.shared.domain.value_objects.integer import IntegerValueObject

class AccountBalance(IntegerValueObject):
    NAME = "balance"

    def _validate(self, value: int):
        super()._validate(value)
        if value < 0:
            raise self._fail(f"{value} should be greater than 0")