from typing import Protocol, runtime_checkable

from users.domain.entity import User
from src.users.domain.value_objects import UserId


@runtime_checkable
class UserRepository(Protocol):
    async def create(self, user: User)-> None:
        ...

    async def find(self, user_id: UserId) -> User:
        ...

    async def find_by_email(self, email: UserId) -> User:
        ...
