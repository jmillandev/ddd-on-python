from kink import di
from sqlalchemy.ext.asyncio import AsyncSession
from os import environ
from src.planner.shared.infrastructure.persistence.sqlalchemy.session import SqlAlchemySession, engine


class SqlalchemyAutoRollbackSession:

    def __init__(self):
        """
        Database dependency
        :param session: AsyncSession is used for testing
        """
        self._session = None
        self._connection = None
        self._transaction = None

    async def __aenter__(self) -> AsyncSession:
        self._old_factory = di.factories[AsyncSession]
        di.factories[AsyncSession] = get_session
        if self._connection is not None:
            raise RuntimeError('Already exists a connection!')

        self._connection = await engine.connect()
        self._transaction = await self._connection.begin()
        self._session = SqlAlchemySession(bind=self._connection, join_transaction_mode="create_savepoint")
        di[current_test()] = self._session
        return self._session

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self._session.close()
        self._session = None
        await self._transaction.rollback()
        self._transaction = None
        await self._connection.close()
        self._connection = None
        di.factories[AsyncSession] = self._old_factory


def current_test() -> str:
    return environ['PYTEST_CURRENT_TEST'].split(' ')[0]


def get_session(di):
    test = current_test()
    return di[test]
