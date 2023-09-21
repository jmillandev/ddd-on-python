import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from utils.passwords import password_context
from apps.users.repositories import UserRepository
from mercury.config import settings

fake = Faker()

pytestmark = pytest.mark.anyio


async def test_success(client: AsyncClient, db_session: AsyncSession) -> None:
    params = {
        'name': fake.name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'password': fake.password(),
        'pronoun': 'he'
    }
    response = await client.post(f"{settings.API_PREFIX}/v1/sign-up", json=params)

    assert response.status_code == status.HTTP_201_CREATED, response.text
    created_user = response.json()

    user = await UserRepository(db_session).find_by_email(params['email'])
    assert user
    assert user.id
    assert user.public_id
    assert user.email == created_user.get('email') == params['email']
    assert user.name == created_user.get('name') == params['name']
    assert user.last_name == created_user.get('last_name') == params['last_name']
    assert created_user.get('public_id')
    assert user.password == None
    assert user.hashed_password != params['password'] 
    assert user.verify_password(params['password']) == password_context.verify(params['password'], user.hashed_password) == True
    assert user.is_active
    assert user.pronoun == params['pronoun']

    users = await UserRepository(db_session).all(limit=None)
    assert len(users) == 1


async def test_email_already_exists(client: AsyncClient, db_session: AsyncSession) -> None:
    params = {
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

    users = await UserRepository(db_session).all(limit=None)
    assert len(users) == 1


async def test_required_field(client: AsyncClient, db_session: AsyncSession) -> None:
    params = {
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

    users = await UserRepository(db_session).all(limit=None)
    assert len(users) == 0


async def test_invalid_email(client: AsyncClient, db_session: AsyncSession) -> None:
    params = {
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

    users = await UserRepository(db_session).all(limit=None)
    assert len(users) == 0
