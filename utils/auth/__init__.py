from apps.users.repositories import UserRepository
from datetime import timedelta, datetime
from mercury.config import settings
from apps.users.models import User
from jose.jwt import encode


async def authenticate_user(respository: UserRepository, email: str, password: str) -> User:
    user = await respository.find_by_email(email)
    if not user:
        return
    if not user.verify_password(password):
        return
    return user

def create_access_token(user: User, expires_delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    payload = { 'sub': str(user.public_id), 'exp': datetime.utcnow() + expires_delta }
    return encode(payload, settings.SECRET_KEY, algorithm='HS256')
