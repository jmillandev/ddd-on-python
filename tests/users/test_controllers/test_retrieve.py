import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.users.factories import UserFactory
from mercury.config import settings

from tests.support.auth import AuthAsUser

pytestmark = pytest.mark.anyio

class TestRetrieve:

    async def test_success(self, client: AsyncClient, db_session: AsyncSession) -> None:
        user = await UserFactory()

        response = await client.post(f"{settings.API_PREFIX}/v1/users/{user.public_id}", auth=AuthAsUser(user))

        assert response.status_code == status.HTTP_200_OK, response.text

        json_response = response.json()
        assert json_response['email']
        assert json_response['name']
        assert json_response['last_name']
        assert json_response['id']

    async def test_user_not_found(self, client: AsyncClient, db_session: AsyncSession) -> None:
        user = await UserFactory()

        response = await client.post(f"{settings.API_PREFIX}/v1/users/1", auth=AuthAsUser(user))

        assert response.status_code == status.HTTP_403_FORBIDDEN, response.text

        json_response = response.json()
        assert len(json_response['detail']) == 1
        error_response = json_response['detail'][0]
        assert error_response['msg'] == 'You do not have permission to perform this action'
        assert error_response['source'] == 'credentials'

    async def test_forbidden(self, client: AsyncClient, db_session: AsyncSession) -> None:
        user = await UserFactory()

        response = await client.post(f"{settings.API_PREFIX}/v1/users/{user.public_id}", auth=AuthAsUser(await UserFactory()))

        assert response.status_code == status.HTTP_403_FORBIDDEN, response.text

        json_response = response.json()
        assert len(json_response['detail']) == 1
        error_response = json_response['detail'][0]
        assert error_response['msg'] == 'You do not have permission to perform this action'
        assert error_response['source'] == 'credentials'

    async def test_unauthorized(self, client: AsyncClient, db_session: AsyncSession) -> None:
        user = await UserFactory()

        response = await client.post(f"{settings.API_PREFIX}/v1/users/{user.public_id}")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text

        json_response = response.json()
        assert len(json_response['detail']) == 1
        error_response = json_response['detail'][0]
        assert error_response['msg'] == 'Invalid authentication credentials'
        assert error_response['source'] == 'credentials'

    async def test_unactive_user(self, client: AsyncClient, db_session: AsyncSession) -> None:
        user = await UserFactory(is_active=False)

        response = await client.post(f"{settings.API_PREFIX}/v1/users/{user.public_id}", auth=AuthAsUser(user))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text

        json_response = response.json()
        assert len(json_response['detail']) == 1
        error_response = json_response['detail'][0]
        assert error_response['msg'] == 'Invalid authentication credentials'
        assert error_response['source'] == 'credentials'