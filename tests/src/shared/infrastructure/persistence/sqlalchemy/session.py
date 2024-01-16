from kink import di
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.persistence.sqlalchemy.session import SqlAlchemySession, engine


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
        if self._connection is not None:
            raise RuntimeError('Already exists a connection!')

        self._connection = await engine.connect()
        self._transaction = await self._connection.begin()
        self._session = SqlAlchemySession(bind=self._connection, join_transaction_mode="create_savepoint")
        di[AsyncSession] = lambda _: self._session
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
