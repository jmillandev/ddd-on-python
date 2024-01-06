from src.shared.domain.value_objects.base import ValueObject


class BooleanValueObject(ValueObject):
    BASE_TYPE = bool

    def _name(self):
      return "boolean"