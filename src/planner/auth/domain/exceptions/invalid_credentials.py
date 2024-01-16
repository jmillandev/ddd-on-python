from src.planner.shared.domain.exceptions.base import DomainException


class InvalidCredentials(DomainException):
    def __init__(self):
        # TODO: Use I18n To translations
        message = 'Invalid credentials'
        super().__init__(401, message, 'credentials')
