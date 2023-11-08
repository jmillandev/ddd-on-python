from typing import Annotated, Any

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from apps.users.contracts import UserCreateContract, OAuth2Contract
from apps.users.interactors.v1.create import UserCreate
from apps.users.interactors.v1.login import Login
from apps.users.interactors.v1.retrieve import UserRetrieve
from apps.users.repositories import UserRepository
from apps.users.schemas import Token
from apps.users.schemas import User as UserSchema
from db.session import get_db
from apps.users.models import User
from utils.auth import get_current_user


async def sign_up(*, db_session: Annotated[AsyncSession, Depends(get_db)], params: UserCreateContract) -> UserSchema:
    """
    Create new user.
    """
    respository = UserRepository(db_session)
    context = await UserCreate.exec(respository=respository, params=params)
    if context.error:
        # TODO: Refactor this and raise error from Interactor
        raise HTTPException(
            status_code=context.error.status_code,
            detail=[dict(context.error)],
        )

    return UserSchema.from_orm(context.user)


async def sign_in(*, db_session: Annotated[AsyncSession, Depends(get_db)], params: OAuth2Contract) -> Token:
    respository = UserRepository(db_session)
    context = await Login.exec(respository=respository, params=params)
    if context.error:
        # TODO: Refactor this and raise error from Interactor
        raise HTTPException(
            status_code=context.error.status_code,
            detail=[dict(context.error)],
        )
    return Token(access_token=context.access_token, token_type="bearer", user=UserSchema.from_orm(context.user))


async def retrieve(
    id: str,
    db_session: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
) -> UserSchema:
    respository = UserRepository(db_session)
    context = await UserRetrieve.exec(respository=respository, id=id)
    if context.error:
        # TODO: Refactor this and raise error from Interactor
        raise HTTPException(
            status_code=context.error.status_code,
            detail=[dict(context.error)],
        )

    return UserSchema.from_orm(context.user)
