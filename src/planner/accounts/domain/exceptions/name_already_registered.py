from src.planner.accounts.domain.value_objects import AccountName
from src.planner.shared.domain.exceptions.base import DomainException


class NameAlreadyRegistered(DomainException):
    def __init__(self, name: AccountName) -> None:
        # TODO: Use I18n To translations
        message = f"You already have an account named {name}"
        super().__init__(400, message, name.NAME)
