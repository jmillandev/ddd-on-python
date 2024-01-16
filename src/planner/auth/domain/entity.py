from typing import Any, Optional
from dataclasses import dataclass
from kink import inject
from src.planner.auth.domain.encoder import AuthEncoder

from src.planner.auth.domain.value_objects import AuthAccessToken, AuthExpiresAt, AuthPassword, AuthUsername
from src.planner.shared.domain.users import UserId

@dataclass
@inject
class AuthToken:
    access_token: AuthAccessToken
    user_id: UserId
    expires_at: AuthExpiresAt

    def __init__(self, user_id: UserId, expires_at: AuthExpiresAt, encoder: AuthEncoder, access_token: Optional[AuthAccessToken] = None) -> None:
        self.encoder = encoder
        self.user_id = user_id
        self.expires_at = expires_at
        self.access_token = access_token or AuthAccessToken(self.encoder.encode(self.payload))

    @classmethod
    def create(cls, user_id: UserId) -> 'AuthToken':
        return cls(user_id=user_id, expires_at=AuthExpiresAt.create())

    @property
    def payload(self) -> dict[str, Any]:
        return {'sub': self.user_id.primitive, 'exp': self.expires_at.primitive}


@dataclass
class AuthCredential:
    user_id: UserId
    username: AuthUsername
    password: AuthPassword
