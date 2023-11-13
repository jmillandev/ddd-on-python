import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from mercury.config import settings
from tests.users.factories import UserFactory

fake = Faker()

pytestmark = pytest.mark.anyio

class TestSignIn:
    def teardown_success(self):
        pass

    def setup_success(self):
        pass

    async def test_success(self, client: AsyncClient, db_session: AsyncSession) -> None:
        password = fake.password()
        user = await UserFactory(password=password)
        params = {'username': user.email, 'password': password, 'grant_type': 'password'}

        response = await client.post(f"{settings.API_PREFIX}/v1/sign-in", json=params)

        assert response.status_code == status.HTTP_200_OK, response.text

        json_response = response.json()
        assert json_response['access_token']
        assert json_response['user']
        json_user = json_response['user']
        assert json_user['id'] == str(user.public_id)
        assert json_user['email'] == user.email
        assert json_user['name'] == user.name
        assert json_user['full_name'] == user.full_name
        assert json_user['pronoun'] == user.pronoun

    async def test_email_doesnt_exists(self, client: AsyncClient, db_session: AsyncSession) -> None:
        params = {'username': fake.email(), 'password': fake.password(), 'grant_type': 'password'}

        response = await client.post(f"{settings.API_PREFIX}/v1/sign-in", json=params)

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text

        json_response = response.json()
        assert len(json_response['detail']) == 1
        error_response = json_response['detail'][0]
        assert error_response['msg'] == 'Incorrect username or password'
        assert error_response['source'] == 'unknown'

    async def test_invalid_password(self, client: AsyncClient, db_session: AsyncSession) -> None:
        password = fake.password()
        user = await UserFactory(password=password)
        params = {'username': user.email, 'password': 'Superpass', 'grant_type': 'password'}

        response = await client.post(f"{settings.API_PREFIX}/v1/sign-in", json=params)

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text

        json_response = response.json()
        assert len(json_response['detail']) == 1
        error_response = json_response['detail'][0]
        assert error_response['msg'] == 'Incorrect username or password'
        assert error_response['source'] == 'unknown'