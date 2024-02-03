from src.shared.domain.exceptions.not_found import NotFound


class AccountNotFound(NotFound):
    def __init__(self) -> None:
        # TODO: Use I18n To translations
        message = "Account not found"
        super().__init__(message)
