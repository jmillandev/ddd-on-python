from typing import Any

from src.planner.shared.domain.exceptions.invalid_value import InvalidValueException
from src.planner.shared.domain.value_objects.string import StringValueObject


class AuthAccessToken(StringValueObject):
    NAME = "access_token"

    def _set_value(self, value: Any) -> None:
        try:
            super()._set_value(value)
        except InvalidValueException as e:
            e.code = 401
            raise e
