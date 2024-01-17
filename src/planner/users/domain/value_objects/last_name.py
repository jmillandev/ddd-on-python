from src.planner.shared.domain.value_objects.string import StringValueObject


class UserLastName(StringValueObject):
    SIZE = 50
    NAME = "last_name"

    def _validate(self):
        super()._validate()
        if len(self.value) > self.SIZE:
            raise self._fail(f"{self.value} should be less than {self.SIZE} characters")
