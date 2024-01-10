from src.shared.domain.value_objects.string import StringValueObject


class AuthPassword(StringValueObject):
    NAME = 'password'

    def hash(self) -> str:
        # TODO: Implement password hashing
        return self.value