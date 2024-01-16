from typing import Protocol, runtime_checkable

from src.planner.auth.domain.value_objects import AuthUsername
from src.planner.auth.domain.entity import AuthCredential

@runtime_checkable
class AuthCredentialRepository(Protocol):
    async def search(self, username: AuthUsername) -> AuthCredential:
        ...
