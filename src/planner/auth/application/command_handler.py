from kink import inject

from src.planner.auth.domain.value_objects import AuthPassword, AuthUsername
from src.planner.shared.application.mappers import entity_to_response

from .command import CreateAuthTokenCommand
from .creator import AuthTokenCreator
from .response import AuthTokenResponse


@inject
class CreateAuthTokenCommandHandler:
    def __init__(self, creator: AuthTokenCreator) -> None:
        self.creator = creator

    async def __call__(self, command: CreateAuthTokenCommand) -> AuthTokenResponse:
        auth_token = await self.creator.create(
            username=AuthUsername(command.username),
            password=AuthPassword(command.password),
        )
        return entity_to_response(auth_token, AuthTokenResponse)
