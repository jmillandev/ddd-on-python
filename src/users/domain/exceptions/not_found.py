from src.shared.domain.exceptions.base import DomainException


class UserNotFound(DomainException):
    def __init__(self):
        # TODO: Use I18n To translations
        message = 'The user does not exist.'
        super().__init__(400, message)