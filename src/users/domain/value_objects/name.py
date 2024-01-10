from src.shared.domain.value_objects.string import StringValueObject


class UserName(StringValueObject):
    SIZE = 50
    NAME = "name"

    def _validate(self) -> None:
        super()._validate()
        if len(self.value) > self.SIZE:
            raise self._fail(f"{self.value} should be less than {self.SIZE} characters")
