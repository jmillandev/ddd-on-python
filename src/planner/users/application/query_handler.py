from kink import inject

from src.planner.shared.domain.users import UserId
from src.planner.shared.application.mappers import entity_to_response

from .finder import UserFinder
from .query import FindUserQuery
from .responses import UserResponse


@inject
class FindUserQueryHandler:
    def __init__(self, finder: UserFinder) -> None:
        self.finder = finder

    async def __call__(self, query: FindUserQuery) -> UserResponse:
        user = await self.finder.find(
            id=UserId(query.id), current_user_id=UserId(query.user_id)
        )
        return entity_to_response(user, UserResponse)
