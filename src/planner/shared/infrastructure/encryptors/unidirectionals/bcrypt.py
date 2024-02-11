from bcrypt import checkpw, gensalt, hashpw
from kink import inject

from src.planner.shared.domain.encryptors.unidirectional import UnidirectionalEncryptor


@inject(alias=UnidirectionalEncryptor)
class BcryptUnidirectionalEncryptor:
    def encrypt(self, value: str) -> str:
        return hashpw(value.encode(), gensalt()).decode()

    def compare(self, value: str, encrypted_value: str) -> bool:
        # try:
        return checkpw(value.encode(), encrypted_value.encode())
        # except UnknownHashError:
        # return False
