from typing import Annotated

from kink import di
from fastapi import Depends

from src.planner.users.application.command import CreateUserCommand
from src.planner.shared.domain.bus.command import CommandBus
from src.planner.users.application.responses import UserResponse
from src.planner.shared.domain.bus.query import QueryBus
from src.planner.users.application.query import FindUserQuery
from apps.planner.backend.shared.auth import oauth2_scheme
from src.planner.auth.application.query import FindAuthTokenQuery


async def sign_up(
    *,
    command_bus: Annotated[CommandBus, Depends(lambda: di[CommandBus])],
    command: CreateUserCommand
):
    """
    Create new user.
    """
    await command_bus.dispatch(command)


async def find(
    id: FindUserQuery.__annotations__["id"],
    query_bus: Annotated[QueryBus, Depends(lambda: di[QueryBus])],
    access_token: Annotated[str, Depends(oauth2_scheme)],
) -> UserResponse:
    auth_token = await query_bus.ask(FindAuthTokenQuery(access_token=access_token))
    return await query_bus.ask(FindUserQuery(id=id, user_id=auth_token.user_id))
