from datetime import datetime
from src.shared.domain.value_objects.datetime import DatetimeValueObject


class UserCreatedAt(DatetimeValueObject):
    NAME = "created_at"

    @classmethod
    def now(cls):
        return cls(datetime.utcnow())
