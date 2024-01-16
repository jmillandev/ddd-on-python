import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from mercury.config import settings
from src.users.infrastructure.repositories.sqlalchemy import \
    SqlAlcheamyUserRepository
from tests.src.users.factories import UserFactory

fake = Faker()

pytestmark = pytest.mark.anyio


async def test_success_login(client: AsyncClient, fake, sqlalchemy_session: AsyncSession) -> None:
    password = fake.password()
    # TODO: Create DB table for Credentials
    user = UserFactory.build(password=password)
    # TODO: Use dependency injection instead of repository implementation
    await SqlAlcheamyUserRepository(sqlalchemy_session).create(user)
    params = {'username': user.email.value, 'password': password, 'grant_type': 'password'}

    response = await client.post(f"{settings.API_PREFIX}/v1/sign-in", json=params)

    assert response.status_code == status.HTTP_200_OK, response.text

    json_response = response.json()
    assert json_response['user_id'] == user.id.primitive
    assert json_response['access_token'] is not None
    assert json_response['expires_at'] is not None
