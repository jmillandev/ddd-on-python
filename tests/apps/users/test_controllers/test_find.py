import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from mercury.config import settings
from src.users.domain.repository import UserRepository
from kink import di
from tests.src.users.factories import UserFactory

fake = Faker()

pytestmark = pytest.mark.anyio

class TestFindController:

    def setup(self):
        self._user = UserFactory.build()

    async def test_success(self, client: AsyncClient, sqlalchemy_session: AsyncSession) -> None:
        await di[UserRepository].create(self._user)
        response = await client.get(f"{settings.API_PREFIX}/v1/users/{self._user.id.primitive}")

        assert response.status_code == status.HTTP_200_OK, response.text
        assert response.json() == {
            'id': self._user.id.primitive,
            'name': self._user.name.primitive,
            'email': self._user.email.primitive,
            'last_name': self._user.last_name.primitive,
            'pronoun': self._user.pronoun.primitive,
        }

    # TODO: Add Test case for unauthorized error
    # async def test_should_return_unauthorized_error(self, client: AsyncClient, sqlalchemy_session: AsyncSession) -> None:
        # user = await UserFactory()

        # response = await client.post(f"{settings.API_PREFIX}/v1/users/{user.public_id}")

        # assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text

        # json_response = response.json()
        # assert len(json_response['detail']) == 1
        # error_response = json_response['detail'][0]
        # assert error_response['msg'] == 'Invalid authentication credentials'
        # assert error_response['source'] == 'credentials'
