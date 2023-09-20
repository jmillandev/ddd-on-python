from typing import Any

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession 

from apps.users.contracts import UserCreateContract
from apps.users.schemas import User as UserSchema
from apps.users.repositories import UserRepository
from apps.users.interactors.v1.create import UserCreate
from db.session import get_db


async def sign_up(*, db_session: AsyncSession = Depends(get_db), params: UserCreateContract) -> Any:
    """
    Create new user.
    """
    respository = UserRepository(db_session)
    context = await UserCreate.exec(respository=respository, params=params)
    if context.error:
        raise HTTPException(
            status_code=context.error.status_code,
            detail=dict(context.error),
        )

    return UserSchema(
        public_id=str(context.user.public_id),
        email=context.user.email, 
        name=context.user.name,
        last_name=context.user.last_name
    )
