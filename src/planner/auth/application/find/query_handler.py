from kink import inject

from src.planner.auth.domain.value_objects import AuthAccessToken
from src.planner.shared.application.mappers import entity_to_response

from ..shared.response import AuthTokenResponse
from .finder import AuthTokenFinder
from .query import FindAuthTokenQuery


@inject
class FindAuthTokenQueryHandler:
    def __init__(self, finder: AuthTokenFinder) -> None:
        self.finder = finder

    async def __call__(self, query: FindAuthTokenQuery) -> AuthTokenResponse:
        auth_token = await self.finder.find(
            access_token=AuthAccessToken(query.access_token)
        )
        return entity_to_response(auth_token, AuthTokenResponse)
