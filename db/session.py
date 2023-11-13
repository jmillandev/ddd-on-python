# from sqlalchemy import create_engine
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from mercury.config import settings

engine = create_async_engine(settings.DATABASE_URI, echo=True, poolclass=pool.NullPool)
LocalSession = async_sessionmaker(
    engine, autoflush=False, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with LocalSession() as session:
        yield session
