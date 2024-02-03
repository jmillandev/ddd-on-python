from src.planner.shared.domain.value_objects.base import ValueObject
from datetime import date, datetime

DATE_FORMAT = "%d-%m-%Y"

class DateValueObject(ValueObject[date]):
    BASE_TYPE = date

    def _cast(self, value: str) -> date:
        if value is None:
            raise self._fail("Is required")
        if isinstance(value, self.BASE_TYPE):
            return value
        try:
            return datetime.strptime(value, DATE_FORMAT).date()
        except Exception:
            self._fail(f"Invalid {self.BASE_TYPE.__name__}")
            return None  # type: ignore[return-value]
