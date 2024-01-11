from src.shared.application.response import Response

class AuthTokenResponse(Response):
    access_token: str
    token_type: str
    expires_at: int
    user_id: str
