from kink import inject

from src.shared.domain.encryptors.unidirectional import UnidirectionalEncryptor
from src.shared.domain.value_objects.string import StringValueObject


@inject
class SecretValueObject(StringValueObject):

    def __init__(self, value: str, encryptor: UnidirectionalEncryptor, is_hashed: bool = False) -> None:
        self.encryptor = encryptor
        super().__init__(value)
        self._raw_value = None if is_hashed else value
        if is_hashed:
            self._value = value

    def set_value(self, value):
        super().set_value(value)
        self._raw_value = value
        self._value = self.encryptor.encrypt(value)

    def __eq__(self, o: object) -> bool:

        if isinstance(o, self.__class__):
            if o._raw_value:
                return self.encryptor.compare(o._raw_value, self.value) 
            return self.value == o.value
        if isinstance(o, StringValueObject):
            return self.encryptor.compare(o.value, self.value)
        return False
