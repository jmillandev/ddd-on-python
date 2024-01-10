from typing import Any
from dataclasses import dataclass

from src.auth.domain.value_objects import AuthAccessToken, AuthTokenType, AuthExpiresAt, AuthPassword, AuthUsername
from src.shared.domain.users import UserId
from src.auth.domain.encoder import AuthEncoder


@dataclass
class AuthToken:
    access_token: AuthAccessToken
    user_id: UserId
    token_type: AuthTokenType
    expires_at: AuthExpiresAt


    @classmethod
    def create(cls, user_id: UserId, access_token: AuthAccessToken, expires_at: AuthExpiresAt) -> 'Auth':
        return cls(
            access_token=access_token,
            user_id=user_id,
            token_type=AuthTokenType.bearer(),
            expires_at=expires_at
        )
    
    @staticmethod
    def payload(user_id: UserId, expires_at: AuthExpiresAt) -> dict[str, Any]:
        return {'sub': user_id.primitive(), 'exp': expires_at.primitive()}


@dataclass
class AuthCredential:
    user_id: UserId
    username: AuthUsername
    password: AuthPassword

    def verify_password(self, password: AuthPassword) -> bool:
        return self.password == password.hash()
