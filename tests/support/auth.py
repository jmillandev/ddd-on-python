from httpx import Auth

from utils.auth import create_access_token


class AuthAsUser(Auth):
    def __init__(self, user):
        self.user = user

    def auth_flow(self, request):
        request.headers['Authorization'] = f'Bearer {create_access_token(self.user)}'
        yield request
