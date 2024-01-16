from httpx import Auth

from src.planner.auth.domain.entity import AuthToken
from src.planner.shared.domain.users import UserId


class AuthAsUser(Auth):
    def __init__(self, user_id: UserId):
        self.user_id = user_id
        self._auth_token = None

    def auth_flow(self, request):
        request.headers[
            "Authorization"
        ] = f"Bearer {self.auth_token.access_token.primitive}"
        yield request

    @property
    def auth_token(self):
        if not self._auth_token:
            self._auth_token = AuthToken.create(user_id=self.user_id)
        return self._auth_token
