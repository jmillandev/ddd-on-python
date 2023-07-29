from fastapi import APIRouter, Depends, HTTPException

from apps.users import schemas
from sqlalchemy.orm import Session
from apps.users.contracts import UserCreateContract
from typing import Any
from apps.users.repositories import UserRepository
from mercury.dependencies import get_db

router = APIRouter()


def signup(*, db: Session = Depends(get_db), params: UserCreateContract) -> Any:
    """
    Create new user.
    """
    respository = UserRepository(db)
    user = respository.get_by_email(db, email=params.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail='The user with this username already exists in the system.',
        )
    user = respository.create(params)
    return user


router.add_api_route(
    '/v1/sign-up', methods=['POST'], response_model=schemas.User, endpoint=signup, tags=['sign-up'])
