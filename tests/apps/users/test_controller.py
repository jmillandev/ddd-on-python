import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from mercury.config import settings
from src.users.infrastructure.repositories.sqlalchemy import SqlAlcheamyUserRepository as UserRepository

fake = Faker()

pytestmark = pytest.mark.anyio


async def test_success(client: AsyncClient) -> None:
    params = {
        'id': fake.uuid4(),
        'name': fake.name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'password': fake.password(),
        'pronoun': 'he'
    }
    response = await client.post(f"{settings.API_PREFIX}/v1/sign-up", json=params)

    assert response.status_code == status.HTTP_201_CREATED, response.text
