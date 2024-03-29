from typing import Optional

from jose import JWTError, jwt
from jose.jwt import encode
from kink import inject

from src.planner.auth_token.domain.encoder import AuthEncoder
from src.planner.shared.config import settings


@inject(alias=AuthEncoder)
class JoseJwtEncoder:
    _ALGORITHM = "HS256"

    def encode(self, payload: dict) -> str:
        return encode(payload, settings.SECRET_KEY, algorithm=self._ALGORITHM)

    def decode(self, token: str) -> Optional[dict]:
        try:
            return jwt.decode(token, settings.SECRET_KEY, algorithms=[self._ALGORITHM])
        except JWTError:
            return None
