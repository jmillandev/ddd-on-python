from datetime import datetime

from src.shared.domain.value_objects.base import ValueObject


class DatetimeValueObject(ValueObject):
    BASE_TYPE = datetime

    def _name(self):
        return "datetime"
    
    @classmethod
    def now(cls):
        return cls(datetime.utcnow())
