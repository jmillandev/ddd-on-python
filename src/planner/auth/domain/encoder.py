from typing import Any, Optional, Protocol, runtime_checkable


@runtime_checkable
class AuthEncoder(Protocol):
    """Token encoder protocol. Use to encrypt and decrypt tokens."""

    def encode(self, payload: dict[str, Any]) -> str:
        ...

    def decode(self, token: str) -> Optional[dict]:
        ...
