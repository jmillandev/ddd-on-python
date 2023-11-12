from apps.users.models import User
from utils.interactors import Interactor


class CreateUser(Interactor):
    async def call(self):
        user = await self.context.respository.find_by_email(self.context.params.email)
        if user:
            self.fail('The user with this username already exists in the system.', source='email')

        self.context.user = User(**self.validated_data)
        await self.context.respository.create(self.context.user)
