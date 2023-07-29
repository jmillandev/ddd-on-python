# from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from mercury.config import settings

engine = create_async_engine(settings.DATABASE_URI, pool_pre_ping=True, echo=True)
SessionLocal = async_sessionmaker(engine, autocommit=False, autoflush=False, expire_on_commit=False)
