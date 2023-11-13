"""User respository"""
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from apps.users.models import User
from db.base_repository import BaseRepository
from src.users.domain.value_objects import UserEmail, UserId


class UserSqlAlcheamyRepository(BaseRepository):
    """
    CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    For more information on how to create new methods, see:
        https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
    """

    def __init__(self, session: async_sessionmaker[AsyncSession]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `session`: A SQLAlchemy database session object.
        """
        self.session = session

    async def find_by_email(self, email: UserEmail) -> User:
        """Find user by email"""
        stmt = select(User).where(User.email == email).limit(1)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def find(self, public_id: UserId) -> Optional[User]:
        """Find object by id"""
        try:
            stmt = select(User).where(User.public_id == public_id).limit(1)
            result = await self.session.execute(stmt)
        except Exception:
            return None

        data = result.scalars()
        return data.first()

    async def create(self,  user: User) -> User:
        # async with self.session.begin():
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
