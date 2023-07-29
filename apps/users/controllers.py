from typing import Any

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession 

from apps.users.contracts import UserCreateContract
from apps.users.models import User
from apps.users.schemas import User as UserSchema
from apps.users.repositories import UserRepository
from mercury.dependencies import get_db


async def sign_up(*, session: AsyncSession = Depends(get_db), params: UserCreateContract) -> Any:
    """
    Create new user.
    """
    respository = UserRepository(session)
    user = await respository.find_by_email(params.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail='The user with this username already exists in the system.',
        )
    validated_data = params.dict()
    validated_data['hashed_password'] = validated_data.pop('password')
    user = User(**validated_data)
    respository.create(user)

    return UserSchema(
        email=user.email, 
        is_active=True,
        is_superuser=False,
        name=user.name,
        last_name=user.last_name
    )
