from kink import inject

from src.planner.auth.domain.encoder import AuthEncoder
from src.planner.auth.domain.entity import AuthToken
from src.planner.auth.domain.exceptions.invalid_credentials import InvalidCredentials
from src.planner.auth.domain.repository import AuthCredentialRepository
from src.planner.auth.domain.value_objects import AuthPassword, AuthUsername


@inject
class AuthTokenCreator:
    def __init__(self, repository: AuthCredentialRepository, encoder: AuthEncoder):
        self._repository = repository
        self._encoder = encoder
        # TODO-Events: add event bus
        # self._event_bus = EventBus()

    async def create(self, username: AuthUsername, password: AuthPassword) -> AuthToken:
        credential = await self._repository.search(username)
        # TODO: Use QueryBus instead Repository? https://pro.codely.com/library/cqrs-command-query-responsibility-segregation-29074/62554/path/step/33532843/discussion/79379/  # noqa:E501
        if not credential or credential.password != password:
            raise InvalidCredentials()

        auth_token = AuthToken.create(user_id=credential.user_id)
        # TODO-Events: publish events
        # self._event_bus.publish(*auth_token.pull_domain_events())
        return auth_token
