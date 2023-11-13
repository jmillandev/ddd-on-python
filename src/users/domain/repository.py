from typing import Protocol, runtime_checkable

from src.users.domain.user import User
from src.users.domain.value_objects import UserEmail, UserId


@runtime_checkable
class UserRepository(Protocol):
    async def create(self, user: User)-> None:
        ...

    async def find(self, user_id: UserId) -> User:
        ...

    async def find_by_email(self, email: UserId) -> User:
        ...
