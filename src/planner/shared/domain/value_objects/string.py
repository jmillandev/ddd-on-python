from src.planner.shared.domain.value_objects.base import ValueObject


class StringValueObject(ValueObject[str]):
    BASE_TYPE = str

    @property
    def primitive(self) -> str:
        return self.value
