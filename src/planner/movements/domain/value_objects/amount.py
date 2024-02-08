from src.planner.shared.domain.value_objects.integer import IntegerValueObject


class MovementAmount(IntegerValueObject):
    NAME = "amount"
    MIN_VALUE = 0

    def _validate(self, value: int):
        super()._validate(value)
        if self.MIN_VALUE >= value:
            raise self._fail(
                f"Your expense amount should be greater than {self.MIN_VALUE}."
            )
