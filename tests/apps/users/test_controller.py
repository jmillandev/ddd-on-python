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


async def test_email_already_exists(client: AsyncClient, db_session: AsyncSession) -> None:
    # TODO: Move to Application layer Test Cases
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

    response = await client.post(f"{settings.API_PREFIX}/v1/sign-up", json=params)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response = response.json()['detail'][0]
    assert response['msg'] == 'The user with this username already exists in the system.'
    assert response['source'] == 'email'
    assert response['status_code'] == status.HTTP_400_BAD_REQUEST


async def test_required_field(client: AsyncClient, db_session: AsyncSession) -> None:
    # TODO: Add similar to Application layer Test Cases
    params = {
        'id': fake.uuid4(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'password': fake.password(),
        'pronoun': 'xd'
    }
    response = await client.post(f"{settings.API_PREFIX}/v1/sign-up", json=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = response.json()['detail']

    assert response[0]['source'] == 'name'
    assert response[0]['msg'] == 'field required'
    assert response[1]['source'] == 'pronoun'
    assert response[1]['msg'] == "value is not a valid enumeration member; permitted: 'he', 'she'"


async def test_invalid_email(client: AsyncClient, db_session: AsyncSession) -> None:
    # TODO: Add similar Move to Application layer Test Cases
    params = {
        'id': fake.uuid4(),
        'last_name': fake.last_name(),
        'email': fake.name(),
        'password': fake.password(),
        'pronoun': 'she'
    }
    response = await client.post(f"{settings.API_PREFIX}/v1/sign-up", json=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = response.json()['detail']

    assert response[0]['source'] == 'email'
    assert response[0]['msg'] == 'value is not a valid email address'
