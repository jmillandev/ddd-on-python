from kink import inject

from src.auth.domain.value_objects import AuthUsername, AuthPassword
from .command import CreateAuthTokenCommand
from .creator import AuthTokenCreator
from .response import AuthTokenResponse


@inject
class CreateAuthTokenCommandHandler:

    def __init__(self, creator: AuthTokenCreator) -> None:
        self.creator = creator

    async def __call__(self, command: CreateAuthTokenCommand) -> None:
        auth_token = await self.creator.create(
            username=AuthUsername(command.username),
            password=AuthPassword(command.password)
        )
        return AuthTokenResponse(auth_token)
