from passlib.context import CryptContext

context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasslibUnidirectionalEncryptor:
   
    def encrypt(self, value: str) -> str:
        return context.hash(value)

    def compare(self, value: str, encrypted_value: str) -> bool:
        return context.verify(value, encrypted_value)
