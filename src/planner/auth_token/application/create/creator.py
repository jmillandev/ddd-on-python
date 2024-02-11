from kink import inject

from src.planner.auth_token.domain.encoder import AuthEncoder
from src.planner.auth_token.domain.entity import AuthToken
from src.planner.auth_token.domain.exceptions.invalid_credentials import (
    InvalidCredentials,
)
from src.planner.auth_token.domain.repository import AuthCredentialRepository
from src.planner.auth_token.domain.value_objects import AuthPassword, AuthUsername
from src.shared.domain.bus.event.event_bus import EventBus


@inject(use_factory=True)
class AuthTokenCreator:
    def __init__(
        self,
        repository: AuthCredentialRepository,
        event_bus: EventBus,
        encoder: AuthEncoder,
    ):
        self._repository = repository
        self._encoder = encoder
        self._event_bus = event_bus

    async def __call__(
        self, username: AuthUsername, password: AuthPassword
    ) -> AuthToken:
        credential = await self._repository.search(username)
        if not credential or credential.password != password:
            raise InvalidCredentials()

        auth_token = AuthToken.create(user_id=credential.user_id)
        # TODO-Events: publish events
        # self._event_bus.publish(*auth_token.pull_domain_events())
        return auth_token
