from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.planner.shared.config import settings

engine = create_async_engine(
    str(settings.DATABASE_URI), echo=True, poolclass=pool.NullPool
)


def sessionmaker():
    return async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


SqlAlchemySession = sessionmaker()
