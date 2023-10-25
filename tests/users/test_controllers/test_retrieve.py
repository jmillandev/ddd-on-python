import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.users.factories import UserFactory
from mercury.config import settings

fake = Faker()

pytestmark = pytest.mark.anyio

class TestSignIn:
    async def test_success(self, client: AsyncClient, db_session: AsyncSession) -> None:
        user = await UserFactory()

        response = await client.post(f"{settings.API_PREFIX}/v1/users/{user.public_id}")

        assert response.status_code == status.HTTP_200_OK, response.text

        json_response = response.json()
        assert json_response['email']
        assert json_response['name']
        assert json_response['last_name']
        assert json_response['id']

    async def test_user_not_found(self, client: AsyncClient, db_session: AsyncSession) -> None:
        response = await client.post(f"{settings.API_PREFIX}/v1/users/1")

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.text

        json_response = response.json()
        assert len(json_response['detail']) == 1
        error_response = json_response['detail'][0]
        assert error_response['msg'] == 'User not found'
        assert error_response['source'] == 'id'
