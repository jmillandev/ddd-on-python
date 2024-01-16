from kink import inject

from src.auth.domain.value_objects import AuthAccessToken
from .query import FindAuthTokenQuery
from .finder import AuthTokenFinder
from .response import AuthTokenResponse
from src.auth.domain.entity import AuthToken

@inject
class FindAuthTokenQueryHandler:

    def __init__(self, finder: AuthTokenFinder) -> None:
        self.finder = finder

    async def __call__(self, query: FindAuthTokenQuery) -> AuthToken:
        return await self.finder.find(access_token=AuthAccessToken(query.access_token))
