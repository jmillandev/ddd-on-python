from typing import Annotated

from fastapi import Depends
from kink import di
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from db.session import get_db
from src.auth.application.command import CreateAuthTokenCommand
from src.auth.application.command_handler import CreateAuthTokenCommandHandler


async def sign_in(*, command: CreateAuthTokenCommand, db_session: Annotated[AsyncSession, Depends(get_db)]):
    """
    Return a token to access to the API
    """
    # TODO: This is a problem because we are using the same db_session for all the requests
    di[async_sessionmaker[AsyncSession]] = db_session
    response = await CreateAuthTokenCommandHandler()(command)
    return response
