from typing import AsyncGenerator

import pytest
from faker import Faker

from src.planner.shared.infrastructure.dependency_injector import (
    init as init_dependencies,
)
from src.planner.shared.infrastructure.persistence.motor.db import database
from tests.src.planner.shared.infrastructure.persistence.sqlalchemy.session import (
    SqlalchemyAutoRollbackSession,
)

init_dependencies()


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
def fake() -> Faker:
    return Faker()


@pytest.mark.asyncio
@pytest.fixture(scope="function")
async def sqlalchemy_session() -> AsyncGenerator:
    async with SqlalchemyAutoRollbackSession() as session:
        yield session


@pytest.mark.asyncio
@pytest.fixture(scope="function")
async def motor_database() -> AsyncGenerator:
    yield database("mercury_test")
