from kink import inject

from src.planner.shared.domain.exceptions.forbidden import ForbiddenAccess
from src.planner.shared.domain.users import UserId
from src.planner.users.domain.entity import User
from src.planner.users.domain.exceptions.not_found import UserNotFound
from src.planner.users.domain.repository import UserRepository


@inject
class UserFinder:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def find(self, id: UserId, current_user_id: UserId) -> User:
        if id != current_user_id:
            raise ForbiddenAccess
        user = await self._repository.search(id)
        if not user:
            raise UserNotFound

        return user
