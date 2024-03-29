from dataclasses import dataclass
from typing import Any, Optional, Self

from kink import inject

from src.planner.auth_token.domain.encoder import AuthEncoder
from src.planner.auth_token.domain.value_objects import (
    AuthAccessToken,
    AuthExpiresAt,
    AuthPassword,
    AuthUsername,
)
from src.planner.shared.domain.aggregates import AggregateRoot
from src.planner.shared.domain.users import UserId


@inject
@dataclass
class AuthToken(AggregateRoot):
    access_token: AuthAccessToken
    user_id: UserId
    expires_at: AuthExpiresAt

    def __init__(
        self,
        user_id: UserId,
        expires_at: AuthExpiresAt,
        encoder: AuthEncoder,
        access_token: Optional[AuthAccessToken] = None,
    ) -> None:
        self.encoder = encoder
        self.user_id = user_id
        self.expires_at = expires_at
        self.access_token = access_token or AuthAccessToken(
            self.encoder.encode(self.payload)
        )

    @classmethod
    def create(cls, user_id: UserId) -> Self:
        return cls(user_id=user_id, expires_at=AuthExpiresAt.create())  # type: ignore[call-arg]

    @property
    def payload(self) -> dict[str, Any]:
        return {"sub": self.user_id.primitive, "exp": self.expires_at.primitive}

    def __str__(self) -> str:
        return f"[{self.user_id}] {self.access_token}"


@dataclass
class AuthCredential(AggregateRoot):
    user_id: UserId
    username: AuthUsername
    password: AuthPassword

    def __str__(self) -> str:
        return f"[{self.user_id}] {self.username}"
