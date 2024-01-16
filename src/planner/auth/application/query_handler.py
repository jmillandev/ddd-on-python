from kink import inject

from src.planner.auth.domain.entity import AuthToken
from src.planner.auth.domain.value_objects import AuthAccessToken

from .finder import AuthTokenFinder
from .query import FindAuthTokenQuery
from .response import AuthTokenResponse


@inject
class FindAuthTokenQueryHandler:
    def __init__(self, finder: AuthTokenFinder) -> None:
        self.finder = finder

    async def __call__(self, query: FindAuthTokenQuery) -> AuthToken:
        auth_token = await self.finder.find(
            access_token=AuthAccessToken(query.access_token)
        )
        return AuthTokenResponse.build(auth_token)
