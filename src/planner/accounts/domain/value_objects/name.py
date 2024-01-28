from src.planner.shared.domain.value_objects.string import StringValueObject


class AccountName(StringValueObject):
    SIZE = 20
    NAME = "name"

    def _validate(self, value: str):
        super()._validate(value)
        if len(value) > self.SIZE:
            raise self._fail(f"{value} should be less than {self.SIZE} characters")
