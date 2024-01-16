from typing import AsyncGenerator

import pytest
from main import app # noqa - Used to load d
from faker import Faker

from tests.src.shared.infrastructure.persistence.sqlalchemy.session import \
    SqlalchemyAutoRollbackSession


@pytest.fixture(scope='session')
def anyio_backend()-> str:
    return 'asyncio'


@pytest.fixture(scope='session')
def fake() -> Faker:
    return Faker()


@pytest.mark.asyncio
@pytest.fixture(scope="function")
async def sqlalchemy_session() -> AsyncGenerator:
    async with SqlalchemyAutoRollbackSession() as session:
        yield session
