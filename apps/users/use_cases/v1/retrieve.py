from fastapi import status
from utils.interactors import Interactor


class RetrieveUser(Interactor):
    async def call(self):
        user = await self.context.respository.find(self.context.id)
        if not user:
            self.fail('User not found',
                      status_code=status.HTTP_404_NOT_FOUND,
                      source='id')
            return self.context

        self.context.user = user
