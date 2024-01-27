from kink import inject

from src.planner.shared.application.mappers import entity_to_response
from src.planner.shared.domain.users import UserId

from .finder import UserFinder
from .query import FindUserQuery
from .responses import UserResponse


@inject
class FindUserQueryHandler:
    def __init__(self, use_case: UserFinder) -> None:
        self.use_case = use_case

    async def __call__(self, query: FindUserQuery) -> UserResponse:
        user = await self.use_case(
            id=UserId(query.id), current_user_id=UserId(query.user_id)
        )
        return entity_to_response(user, UserResponse)
