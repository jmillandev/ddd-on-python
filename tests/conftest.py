from typing import AsyncGenerator

import pytest
from faker import Faker
from httpx import AsyncClient

from main import app
from tests.src.shared.infrastructure.persistence.sqlalchemy.session import SqlalchemyAutoRollbackSession


@pytest.mark.asyncio
@pytest.fixture(scope="function")
async def sqlalchemy_session() -> AsyncGenerator:
    async with SqlalchemyAutoRollbackSession() as session:
        yield session


@pytest.fixture(scope="module")
async def client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://testserver") as ac:    
        yield ac


@pytest.fixture(scope='session')
def anyio_backend()-> str:
    return 'asyncio'


@pytest.fixture(scope='session')
def fake() -> Faker:
    return Faker()
