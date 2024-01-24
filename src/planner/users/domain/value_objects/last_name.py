from src.planner.shared.domain.value_objects.string import StringValueObject


class UserLastName(StringValueObject):
    SIZE = 50
    NAME = "last_name"

    def _validate(self, value: str):
        super()._validate(value)
        if len(value) > self.SIZE:
            raise self._fail(f"{value} should be less than {self.SIZE} characters")
