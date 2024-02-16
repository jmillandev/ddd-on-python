from contextlib import asynccontextmanager
from os import environ
from typing import Any

from kink import di
from sqlalchemy.ext.asyncio import AsyncSession

from src.planner.shared.infrastructure.persistence.sqlalchemy.session import (
    SqlAlchemySession,
    engine,
    sessionmaker,
)


class SqlalchemyAutoRollbackSession:
    def __init__(self):
        """
        Database dependency
        :param session: AsyncSession is used for testing
        """
        self._connection = None
        self._transaction = None

    async def begin(self):
        self._old_factory = di.factories[type[AsyncSession]]
        di.factories[type[AsyncSession]] = get_sessionmaker
        if self._connection is not None:
            raise RuntimeError("Already exists a connection!")
        self._connection = await engine.connect()
        di[current_test()] = self._connection
        self._transaction = await self._connection.begin()

    @asynccontextmanager
    async def __call__(self) -> Any:
        async with SqlAlchemySession(bind=self._connection) as session:
            yield session

    async def roolback(self):
        await self._transaction.rollback()
        self._transaction = None
        await self._connection.close()
        self._connection = None
        di.factories[type[AsyncSession]] = self._old_factory


def current_test() -> str:
    return environ["PYTEST_CURRENT_TEST"].split(" ")[0]


def get_session(di):
    test = current_test()
    return di[test]


def get_sessionmaker(di):
    test = current_test()
    LocalSession = sessionmaker()
    conection = di[test]
    LocalSession.configure(bind=conection)
    return LocalSession
