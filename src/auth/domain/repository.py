from typing import Protocol, runtime_checkable

from src.auth.domain.value_objects import AuthUsername
from src.auth.domain.entity import AuthCredential

@runtime_checkable
class AuthCredentialRepository(Protocol):
    async def search(self, username: AuthUsername) -> AuthCredential:
        ...
