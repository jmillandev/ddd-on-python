from kink import inject

from src.planner.auth.domain.encoder import AuthEncoder
from src.planner.auth.domain.entity import AuthToken
from src.planner.auth.domain.exceptions.invalid_credentials import InvalidCredentials
from src.planner.auth.domain.value_objects import AuthAccessToken, AuthExpiresAt
from src.planner.shared.domain.users import UserId


@inject
class AuthTokenFinder:
    def __init__(self, encoder: AuthEncoder):
        self._encoder = encoder
        # TODO-Events: add event bus
        # self._event_bus = EventBus()

    async def find(self, access_token: AuthAccessToken) -> AuthToken:
        payload = self._encoder.decode(access_token.primitive)
        if not payload:
            raise InvalidCredentials()
        auth_token =  AuthToken(
            access_token=access_token,
            user_id=UserId(payload['sub']),
            expires_at=AuthExpiresAt(payload['exp'])
        )
        if auth_token.expires_at.expired:
            raise InvalidCredentials()

        return auth_token
