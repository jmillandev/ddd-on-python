from src.planner.shared.domain.exceptions.base import DomainException
# TODO: Move to src/shared/domain/exceptions/base.py

class NotFound(DomainException):
    def __init__(self, message: str, source: str = None):
        super().__init__(404, message, source)
