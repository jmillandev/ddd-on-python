from typing import Protocol, runtime_checkable

from src.planner.auth_token.domain.entity import AuthCredential
from src.planner.auth_token.domain.value_objects import AuthUsername


@runtime_checkable
class AuthCredentialRepository(Protocol):
    async def search(self, username: AuthUsername) -> AuthCredential:
        ...
