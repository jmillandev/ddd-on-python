from datetime import datetime, timedelta

from src.planner.shared.config import settings
from src.planner.shared.domain.value_objects.integer import IntegerValueObject


class AuthExpiresAt(IntegerValueObject):
    NAME = 'expires_at'

    @classmethod
    def create(cls) -> 'AuthExpiresAt':
        expires_at = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) 
        return cls(expires_at.timestamp())

    @property
    def expired(self) -> bool:
        return self.value < datetime.utcnow().timestamp()
