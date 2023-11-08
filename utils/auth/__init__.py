from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from jose.jwt import encode
from sqlalchemy.ext.asyncio import AsyncSession

from apps.users.models import User
from apps.users.repositories import UserRepository
from db.session import get_db
from mercury.config import settings

from utils.auth.errors import UnauthorizedError
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token', auto_error=False)
ALGORITHM = 'HS256'


async def authenticate_user(respository: UserRepository, email: str, password: str) -> User:
    user = await respository.find_by_email(email)
    if not user:
        return
    if not user.verify_password(password):
        return
    return user


def create_access_token(user: User, expires_delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    payload = {'sub': str(user.public_id),
               'exp': datetime.utcnow() + expires_delta}
    return encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db_session: AsyncSession = Depends(get_db)):
    if not token:
        raise UnauthorizedError()
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[ALGORITHM])
        public_id: str = payload.get("sub")
        if public_id is None:
            raise UnauthorizedError()
    except JWTError:
        raise UnauthorizedError()
    user = await UserRepository(db_session).find(public_id)
    if user is None:
        raise UnauthorizedError()
    return user
