from dataclasses import dataclass
from pydantic import BaseModel, ConfigDict


class AuthTokenResponse(BaseModel):
    model_config = ConfigDict()
    access_token: str
    expires_at: int
    user_id: str
