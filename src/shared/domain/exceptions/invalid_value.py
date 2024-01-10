from src.shared.domain.exceptions.base import DomainException


class InvalidValueException(DomainException):
    def __init__(self, message: str, source: str):
        super().__init__(422, message, source)
