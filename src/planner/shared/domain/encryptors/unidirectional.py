from typing import Protocol, runtime_checkable


@runtime_checkable
class UnidirectionalEncryptor(Protocol):
    """
    Interface for unidirectional encryptors.

    Unidirectional encryptors are those that can encrypt a value but cannot decrypt it.
    """

    def encrypt(self, value: str) -> str:
        ...

    def compare(self, value: str, encrypted_value: str) -> bool:
        ...
