from src.shared.application.response import Response

class AuthTokenResponse(Response):
    access_token: str
    token_type: str
