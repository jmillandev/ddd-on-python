from src.shared.domain.value_objects.string import StringValueObject
from utils.passwords import password_context


class UserPassword(StringValueObject):

    def set_value(self, value):
        super().set_value(value)
        self._value = self._hash_password(value)

    def _hash_password(self, password):
        # TODO: Refactor and use a adapter
        return password_context.hash(password)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, self.__class__):
            return self.value == o.value
        if isinstance(o, StringValueObject):
            return self.value == self._hash_password(o.value)
        return False
