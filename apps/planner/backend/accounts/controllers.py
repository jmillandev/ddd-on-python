from typing import Annotated, cast

from fastapi import Depends
from kink import di

from apps.planner.backend.shared.auth import oauth2_scheme
from src.planner.accounts.application.create.command import CreateAccountCommand
from src.planner.auth_token.application.find.query import FindAuthTokenQuery
from src.planner.auth_token.application.shared.response import AuthTokenResponse
from src.planner.shared.domain.bus.command import CommandBus
from src.planner.shared.domain.bus.query import QueryBus

from .schemas import CreateAccountSchema


async def create(
    id: str,
    query_bus: Annotated[QueryBus, Depends(lambda: di[QueryBus])],
    command_bus: Annotated[CommandBus, Depends(lambda: di[CommandBus])],
    access_token: Annotated[str, Depends(oauth2_scheme)],
    params: CreateAccountSchema,
):
    """
    Create new user.
    """
    auth_token = await query_bus.ask(FindAuthTokenQuery(access_token=access_token))
    auth_token = cast(AuthTokenResponse, auth_token)
    command = CreateAccountCommand(
        **params.to_dict(), id=id, owner_id=auth_token.user_id
    )
    await command_bus.dispatch(command)
