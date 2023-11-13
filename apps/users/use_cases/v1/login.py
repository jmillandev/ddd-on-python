from fastapi import status

from utils.auth import authenticate_user, create_access_token
from utils.interactors import Interactor


class Login(Interactor):
    async def call(self):
        self.context.user = await authenticate_user(self.context.respository, self.context.params.username, self.context.params.password)
        if not self.context.user:
            self.fail('Incorrect username or password', status_code=status.HTTP_400_BAD_REQUEST)
        self.context.access_token = create_access_token(self.context.user)
