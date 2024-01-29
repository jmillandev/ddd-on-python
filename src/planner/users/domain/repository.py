from typing import Optional, Protocol, runtime_checkable

from src.planner.shared.domain.users import UserId
from src.planner.users.domain.entity import User
from src.planner.users.domain.value_objects.email import UserEmail


@runtime_checkable
class UserRepository(Protocol):
    async def create(self, user: User) -> None:
        ...

    async def search(self, user_id: UserId) -> Optional[User]:
        ...

    async def search_by_email(self, email: UserEmail) -> Optional[User]:
        ...
