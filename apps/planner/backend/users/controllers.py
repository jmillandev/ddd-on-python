from typing import Annotated

from fastapi import Depends, File
from kink import di

from apps.planner.backend.shared.auth import oauth2_scheme
from src.planner.auth_token.application.find.query import FindAuthTokenQuery
from src.planner.shared.domain.bus.command import CommandBus
from src.planner.shared.domain.bus.query import QueryBus
from src.planner.users.application.find.query import FindUserQuery
from src.planner.users.application.find.responses import UserResponse
from src.planner.users.application.register.command import RegisterUserCommand
from src.planner.users.application.update_avatar.command import UpdateUserAvatarCommand


async def sign_up(
    *,
    command_bus: Annotated[CommandBus, Depends(lambda: di[CommandBus])],
    command: RegisterUserCommand
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

async def update_avatar(
    id: str,
    avatar: Annotated[bytes | None, File()],
    access_token: Annotated[str, Depends(oauth2_scheme)],
    command_bus: Annotated[CommandBus, Depends(lambda: di[CommandBus])],
    query_bus: Annotated[QueryBus, Depends(lambda: di[QueryBus])]
):
    auth_token = await query_bus.ask(FindAuthTokenQuery(access_token=access_token))
    command = UpdateUserAvatarCommand(id=id, avatar=avatar, user_id=auth_token.user_id)
    await command_bus.dispatch(command)
