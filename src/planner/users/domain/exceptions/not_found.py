from src.shared.domain.exceptions.not_found import NotFound


class UserNotFound(NotFound):
    def __init__(self):
        # TODO: Use I18n To translations
        message = "The user does not exist."
        super().__init__(message)
