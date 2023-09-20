from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession
import pytest
from httpx import AsyncClient

from db.session import engine, LocalSession, get_db

from main import app

class TestDatabaseSession:

    def __init__(self):
        """
        Database dependency
        :param session: AsyncSession is used for testing
        """
        self._session = None
        self._connection = None
        self._transaction = None

    async def __aenter__(self) -> AsyncSession:
        if self._connection is not None:
            raise RuntimeError('Already exists a connection!')

        self._connection = await engine.connect()
        self._transaction = await self._connection.begin()
        self._session = LocalSession(bind=self._connection, join_transaction_mode="create_savepoint")
        return self._session

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self._session.close()
        self._session = None
        await self._transaction.rollback()
        self._transaction = None
        await self._connection.close()
        self._connection = None

    async def __call__(self) -> AsyncSession:
        if self._session is None:
            raise RuntimeError('Database needs connect first!')

        yield self._session


database = TestDatabaseSession()
app.dependency_overrides[get_db] = database


@pytest.mark.asyncio
@pytest.fixture(scope="function")
async def db_session() -> Generator:
    async with database as session:
        yield session


@pytest.fixture(scope="module")
async def client() -> Generator:
    async with AsyncClient(app=app, base_url="http://testserver") as ac:    
        yield ac


@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'
