"""User respository"""
from typing import Optional

from sqlalchemy import select
from sqlalchemy import Boolean, Column, Enum, String
from db.base_class import Base # TODO: Move to share infrastructure
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from db.base_repository import BaseRepository
from src.users.domain.value_objects import UserEmail, UserId, pronoun
from src.users.domain.entity import User


class UserModel(Base):
    email = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    pronoun = Column(
        Enum(pronoun.Pronoun, values_callable=lambda x: pronoun.Pronoun.keys(), name='pronouns'))

    __tablename__ = 'users'


class SqlAlcheamyUserRepository(BaseRepository):
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
        stmt = select(UserModel).where(UserModel.email == email.value).limit(1)
        result = await self.session.execute(stmt)
        data = result.scalars().first()
        if data:
            return User(**data)

    async def find(self, id: UserId) -> Optional[User]:
        """Find object by id"""
        try:
            stmt = select(User).where(User.id == id).limit(1)
            result = await self.session.execute(stmt)
        except Exception:
            return None

        data = result.scalars().first()
        if data:
            return User(**data)

    async def create(self,  user: User) -> User:
        user_object = UserModel.from_entity(user)
        self.session.add(user_object)
        await self.session.commit()
        # await self.session.refresh(user)
        return user
