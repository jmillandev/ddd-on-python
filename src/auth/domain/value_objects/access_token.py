from src.shared.domain.exceptions.invalid_value import InvalidValueException
from src.shared.domain.value_objects.string import StringValueObject


class AuthAccessToken(StringValueObject):
    NAME = "access_token"

    def _validate(self) -> None:
        try:
            super()._validate()
        except InvalidValueException as e:
            e.code = 401
            raise e
