import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient
from kink import di
from sqlalchemy.ext.asyncio import AsyncSession

from apps.planner.backend.config import settings
from src.planner.users.domain.repository import UserRepository
from tests.src.planner.users.factories import UserFactory

fake = Faker()

pytestmark = pytest.mark.anyio


async def test_success_login(
    client: AsyncClient, fake, sqlalchemy_sessionmaker: type[AsyncSession]
) -> None:
    password = fake.password()
    user = UserFactory.build(password=password)
    await di[UserRepository].create(user)  # type:ignore [type-abstract]
    params = {
        "username": user.email.value,
        "password": password,
        "grant_type": "password",
    }

    response = await client.post(f"{settings.API_PREFIX}/v1/sign-in", json=params)

    assert response.status_code == status.HTTP_200_OK, response.text

    json_response = response.json()
    assert json_response["user_id"] == user.id.primitive
    assert json_response["access_token"] is not None
    assert json_response["expires_at"] is not None
