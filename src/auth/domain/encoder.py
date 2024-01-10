from typing import Protocol, Any

class AuthEncoder(Protocol):
    """Token encoder protocol. Use to encrypt and decrypt tokens.
    """

    def encode(self, payload: dict[str, Any]) -> str:
        ...
