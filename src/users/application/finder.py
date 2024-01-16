from kink import inject

from src.shared.domain.users import UserId
from src.users.domain.entity import User
from src.users.domain.exceptions.not_found import UserNotFound
from src.users.domain.repository import UserRepository


@inject
class UserFinder:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def find(self, id: UserId) -> User:
        user = await self._repository.search(id)
        if not user:
            raise UserNotFound

        return user
