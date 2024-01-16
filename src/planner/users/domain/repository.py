from typing import Protocol, runtime_checkable

from src.planner.shared.domain.users import UserId
from src.planner.users.domain.entity import User


@runtime_checkable
class UserRepository(Protocol):
    async def create(self, user: User)-> None:
        ...

    async def search(self, user_id: UserId) -> User:
        ...

    async def search_by_email(self, email: UserId) -> User:
        ...
