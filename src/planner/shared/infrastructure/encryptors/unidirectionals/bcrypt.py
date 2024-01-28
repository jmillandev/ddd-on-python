from bcrypt import checkpw, hashpw, gensalt


class BcryptUnidirectionalEncryptor:
    def encrypt(self, value: str) -> str:
        return hashpw(value.encode(), gensalt()).decode()

    def compare(self, value: str, encrypted_value: str) -> bool:
        # try:
        return checkpw(value.encode(), encrypted_value.encode())
        # except UnknownHashError:
            # return False
