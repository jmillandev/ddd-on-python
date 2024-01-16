from typing import Annotated

from kink import di
from fastapi import Depends

from src.users.application.command import CreateUserCommand
from src.shared.domain.bus.command import CommandBus
from src.users.application.responses import UserResponse
from src.shared.domain.bus.query import QueryBus
from src.users.application.query import FindUserQuery


async def sign_up(*, command_bus: Annotated[CommandBus, Depends(lambda: di[CommandBus])], command: CreateUserCommand):
    """
    Create new user.
    """
    await command_bus.dispatch(command)


async def find(id: FindUserQuery.__annotations__['id'], query_bus: Annotated[QueryBus, Depends(lambda: di[QueryBus])]) -> UserResponse:
    return await query_bus.ask(FindUserQuery(id))
