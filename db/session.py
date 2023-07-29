# from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from mercury.config import settings


def make_session() -> AsyncSession:
    engine = create_async_engine(settings.DATABASE_URI, pool_pre_ping=True, echo=True)
    return async_sessionmaker(engine, autoflush=False, expire_on_commit=False)()
