from dataclasses import dataclass


@dataclass
class AuthTokenResponse:
    access_token: str
    expires_at: int
    user_id: str
