from typing import AsyncGenerator

import pytest
from faker import Faker
from motor.core import AgnosticDatabase

from src.planner.shared.infrastructure.persistence.motor.db import database
from src.shared.infrastructure.dependency_injector import init as init_dependencies
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
async def sqlalchemy_sessionmaker() -> AsyncGenerator:
    sessionmaker = SqlalchemyAutoRollbackSession()
    await sessionmaker.begin()
    yield sessionmaker
    await sessionmaker.roolback()


@pytest.mark.asyncio
@pytest.fixture(scope="function")
def motor_database() -> AgnosticDatabase:
    return database("mercury_test")
