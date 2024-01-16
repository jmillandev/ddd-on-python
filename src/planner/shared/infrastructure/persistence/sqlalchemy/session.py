from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.planner.shared.config import settings

engine = create_async_engine(settings.DATABASE_URI, echo=True, poolclass=pool.NullPool)
SqlAlchemySession = async_sessionmaker(
    engine, autoflush=False, expire_on_commit=False)
