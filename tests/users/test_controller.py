import pytest
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from apps.users.repositories import UserRepository
from mercury.config import settings

fake = Faker()

pytestmark = pytest.mark.anyio

async def test_sign_up(client: TestClient, db: AsyncSession) -> None:
    params = {
        'name': fake.name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'password': fake.password()
    }
    response = client.post(f"{settings.API_PREFIX}/v1/sign-up/", json=params)

    assert response.status_code == 201, response.text
    created_user = response.json()
    user = await UserRepository(db).find_by_email(params['email'])
    assert user
    assert user.name == created_user['name']
