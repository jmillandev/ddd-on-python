from utils.errors import BaseError


class AuthError(BaseError):
    def __init__(self, status_code: int, message: str):
        super().__init__(status_code, message, source='credentials')

class ForbiddenError(AuthError):
    def __init__(self):
        super().__init__(status_code=403, message='You do not have permission to perform this action')

class UnauthorizedError(AuthError):
    def __init__(self):
        super().__init__(status_code=401, message='Invalid authentication credentials')
