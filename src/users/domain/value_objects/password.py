from src.shared.domain.value_objects.secret import SecretValueObject


class UserPassword(SecretValueObject):
    NAME = "password"
