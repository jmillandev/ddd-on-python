from typing import Annotated, Any

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from apps.users.contracts import OAuth2Contract, UserCreateContract
from apps.users.models import User
from apps.users.policies import UserPolicy
from apps.users.schemas import Token
from apps.users.schemas import User as UserSchema
from apps.users.use_cases.v1.create import CreateUser
from apps.users.use_cases.v1.login import Login
from apps.users.use_cases.v1.retrieve import RetrieveUser
from db.session import get_db
from src.users.infrastructure.repositories import SqlAlcheamyUserRepository
from utils.auth import get_current_user


async def sign_up(*, db_session: Annotated[AsyncSession, Depends(get_db)], params: UserCreateContract) -> UserSchema:
    """
    Create new user.
    """
    respository = SqlAlcheamyUserRepository(db_session)
    UserCreator(respository).create(
        email=params.email,
        name=params.name,
        last_name=params.last_name,
        pronoun=params.pronoun,
        password=params.password
    )
    context = await CreateUser.exec(respository=respository, params=params)
    return UserSchema.from_orm(context.user)


async def sign_in(*, db_session: Annotated[AsyncSession, Depends(get_db)], params: OAuth2Contract) -> Token:
    respository = SqlAlcheamyUserRepository(db_session)
    context = await Login.exec(respository=respository, params=params)
    return Token(access_token=context.access_token, token_type="bearer", user=UserSchema.from_orm(context.user))


async def retrieve(
    id: str,
    db_session: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
) -> UserSchema:
    UserPolicy(current_user).retrieve(id)
    respository = SqlAlcheamyUserRepository(db_session)
    context = await RetrieveUser.exec(respository=respository, id=id)
    return UserSchema.from_orm(context.user)
