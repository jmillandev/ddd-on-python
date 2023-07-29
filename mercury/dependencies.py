from typing import Generator

from db.session import make_session


async def get_db() -> Generator:
    async with make_session() as session:
        yield session
