import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient

from mercury.config import settings
from src.users.infrastructure.repositories.sqlalchemy import SqlAlcheamyUserRepository as UserRepository
from kink import di
from tests.users.factories import UserFactory
fake = Faker()

pytestmark = pytest.mark.anyio


async def test_success(client: AsyncClient, fake) -> None:
    password = fake.password()
    # TODO: Create DB table for Credentials
    user = UserFactory.build(password=password)
    await di[UserRepository].create(user)
    params = {'username': fake.email(), 'password': fake.password(), 'grant_type': 'password'}

    response = await client.post(f"{settings.API_PREFIX}/v1/sign-in", json=params)

    assert response.status_code == status.HTTP_200_OK, response.text

    json_response = response.json()
    assert json_response['access_token']
    assert json_response['user']
    json_user = json_response['user']
    assert json_user['user_id'] == user.id.primitive
    assert json_user['access_token'] is not None
    assert json_user['expired_at'] is not None
    assert json_user['token_type'] == 'bearer'
