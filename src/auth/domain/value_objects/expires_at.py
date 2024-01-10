from datetime import datetime, timedelta
from mercury.config import settings

from src.shared.domain.value_objects.datetime import DateTimeValueObject


class AuthExpiresAt(DateTimeValueObject):
    NAME = 'expires_at'

    @classmethod
    def create(cls) -> 'AuthExpiresAt':
        return cls(datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    
    def primitive(self) -> int:
        return int(self.value.timestamp())
