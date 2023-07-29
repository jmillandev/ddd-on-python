from typing import Generator

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from db.session import make_session
from main import app


@pytest.mark.anyio
@pytest.fixture(scope="session")
async def db() -> AsyncSession:
    async with make_session() as session:
        yield session


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'
