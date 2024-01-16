from src.planner.shared.domain.exceptions.base import DomainException
from src.planner.users.domain.value_objects.email import UserEmail


class EmailAlreadyUsed(DomainException):
    def __init__(self, email: UserEmail):
        # TODO: Use I18n To translations
        message = 'The user with this username already exists in the system.'
        super().__init__(400, message, 'email')