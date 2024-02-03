from datetime import datetime

from src.planner.shared.domain.value_objects.base import ValueObject


class DatetimeValueObject(ValueObject):
    BASE_TYPE = datetime

    @property
    def primitive(self) -> int:
        """
        Returns:
            int: Unix timestamp
        """
        return int(self.value.utcnow().timestamp())
