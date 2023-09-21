# from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from mercury.config import settings
from sqlalchemy import pool

engine = create_async_engine(settings.DATABASE_URI, echo=True, poolclass=pool.NullPool)
LocalSession = async_sessionmaker(
    engine, autoflush=False, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with LocalSession() as session:
        yield session
