from src.planner.shared.domain.exceptions.base import DomainException


class ForbiddenAccess(DomainException):
    def __init__(self):
        # TODO: Use I18N
        message = "You are not allowed to do this operation"
        super().__init__(403, message, "credentials")
