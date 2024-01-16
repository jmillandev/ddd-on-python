from src.planner.shared.application.response import Response


class AuthTokenResponse(Response):
    access_token: str
    expires_at: int
    user_id: str
