from kink import inject

from src.auth.domain.encoder import AuthEncoder
from src.auth.domain.entity import AuthToken
from src.auth.domain.repository import AuthCredentialRepository
from src.auth.domain.value_objects import (AuthUsername, AuthExpiresAt,
                                           AuthPassword)
from src.auth.domain.exceptions.invalid_credentials import InvalidCredentials


@inject
class AuthTokenCreator:
    def __init__(self, repository: AuthCredentialRepository, encoder: AuthEncoder):
        self._repository = repository
        self._encoder = encoder
        # TODO-Events: add event bus
        # self._event_bus = EventBus()

    async def create(self, username: AuthUsername, password: AuthPassword) -> AuthToken:
        credential = await self._repository.search(username)
        # TODO: Use QueryBus instead Repository? https://pro.codely.com/library/cqrs-command-query-responsibility-segregation-29074/62554/path/step/33532843/discussion/79379/
        if not (credential or credential.verify_password(password)):
            raise InvalidCredentials()

        expires_at = AuthExpiresAt.create()
        token_payload = AuthToken.payload(credential.user_id, expires_at)
        auth_token = AuthToken.create(
            user_id=credential.user_id,
            access_token=self._encoder.encode(token_payload),
            expires_at=expires_at
        )
        # TODO-Events: publish events
        # self._event_bus.publish(*auth_token.pull_domain_events())
        return auth_token
