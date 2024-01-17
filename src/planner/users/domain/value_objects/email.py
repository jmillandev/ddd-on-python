from re import match

from src.planner.shared.domain.value_objects.string import StringValueObject


class UserEmail(StringValueObject):
    EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    NAME = "email"

    def _validate(self):
        super()._validate()
        if not match(self.EMAIL_REGEX, self.value):
            raise self._fail(f"{self.value} is not a valid email")
