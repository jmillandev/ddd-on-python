from dataclasses import dataclass


@dataclass(frozen=True)
class AuthTokenResponse:
    access_token: str
    expires_at: int
    user_id: str
