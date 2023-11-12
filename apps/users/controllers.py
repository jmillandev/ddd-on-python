from typing import Annotated, Any

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from apps.users.contracts import UserCreateContract, OAuth2Contract
from apps.users.use_cases.v1.create import CreateUser
from apps.users.use_cases.v1.login import Login
from apps.users.use_cases.v1.retrieve import RetrieveUser
from apps.users.repositories import UserRepository
from apps.users.schemas import Token
from apps.users.schemas import User as UserSchema
from db.session import get_db
from apps.users.models import User
from utils.auth import get_current_user
from apps.users.policies import UserPolicy

async def sign_up(*, db_session: Annotated[AsyncSession, Depends(get_db)], params: UserCreateContract) -> UserSchema:
    """
    Create new user.
    """
    respository = UserRepository(db_session)
    context = await CreateUser.exec(respository=respository, params=params)
    return UserSchema.from_orm(context.user)


async def sign_in(*, db_session: Annotated[AsyncSession, Depends(get_db)], params: OAuth2Contract) -> Token:
    respository = UserRepository(db_session)
    context = await Login.exec(respository=respository, params=params)
    return Token(access_token=context.access_token, token_type="bearer", user=UserSchema.from_orm(context.user))


async def retrieve(
    id: str,
    db_session: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
) -> UserSchema:
    UserPolicy(current_user).retrieve(id)
    respository = UserRepository(db_session)
    context = await RetrieveUser.exec(respository=respository, id=id)
    return UserSchema.from_orm(context.user)
