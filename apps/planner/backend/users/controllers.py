from typing import Annotated

from fastapi import Depends
from kink import di

from apps.planner.backend.shared.auth import oauth2_scheme
from src.planner.auth_token.application.find.query import FindAuthTokenQuery
from src.planner.shared.domain.bus.command import CommandBus
from src.planner.shared.domain.bus.query import QueryBus
from src.planner.users.application.create.command import CreateUserCommand
from src.planner.users.application.find.query import FindUserQuery
from src.planner.users.application.find.responses import UserResponse


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
    id: str,
    query_bus: Annotated[QueryBus, Depends(lambda: di[QueryBus])],
    access_token: Annotated[str, Depends(oauth2_scheme)],
) -> UserResponse:
    auth_token = await query_bus.ask(FindAuthTokenQuery(access_token=access_token))
    find_user_query = FindUserQuery(id=id, user_id=auth_token.user_id)  # type: ignore[union-attr]
    return await query_bus.ask(find_user_query)  # type: ignore[return-value]
