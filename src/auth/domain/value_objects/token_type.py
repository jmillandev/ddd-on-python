import enum

from src.shared.domain.value_objects.string import StringValueObject


class TokenType(str, enum.Enum):
    BEARER = 'bearer'

    @staticmethod
    def keys():
        return [c.value for c in TokenType]


class AuthTokenType(StringValueObject):
    NAME = 'token_type'

    def _validate(self) -> None:
        super()._validate()
        if self.value not in TokenType.keys():
            raise self._fail(f"{self.value} is not a valid token type")

    @classmethod
    def bearer(cls):
        return cls(TokenType.BEARER.value)
