import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from test.users.factories import UserFactory
from mercury.config import settings

fake = Faker()

pytestmark = pytest.mark.anyio

class TestSignIn:
    def teardown_success(self):
        pass

    def setup_success(self):
        pass

    async def test_success(self, client: AsyncClient, db_session: AsyncSession) -> None:
        password = fake.password()
        user = UserFactory(password=password)
        params = {'username': user.email, 'password': password, 'grant_type': 'password'}

        response = await client.post(f"{settings.API_PREFIX}/v1/sign-in", json=params)

        assert response.status_code == status.HTTP_200_OK, response.text

        json_response = response.json()
        assert json_response['token']
        assert json_response['user']
        json_user = json_response['user']
        assert json_user['id'] == user.id
        assert json_user['email'] == user.email
        assert json_user['name'] == user.name
        assert json_user['full_name'] == user.full_name
        assert json_user['pronoun'] == user.pronoun
