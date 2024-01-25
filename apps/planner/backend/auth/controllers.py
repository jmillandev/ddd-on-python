from src.planner.auth.application.create.command import CreateAuthTokenCommand
from src.planner.auth.application.create.command_handler import (
    CreateAuthTokenCommandHandler,
)


async def sign_in(*, command: CreateAuthTokenCommand):
    """
    Return a token to access to the API
    """
    response = await CreateAuthTokenCommandHandler()(command)  # type: ignore[call-arg]
    return response
