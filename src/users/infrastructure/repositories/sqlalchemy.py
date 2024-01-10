"""User respository"""
from typing import Optional

from sqlalchemy import Boolean, Column, Enum, String, select

from src.shared.infrastructure.persistence.sqlalchemy.models import Base
from src.shared.infrastructure.persistence.sqlalchemy.repositories import (
    SqlAlcheamyCreateMixin, SqlAlcheamyFindMixin, SqlAlcheamyRepository)
from src.users.domain.entity import User
from src.users.domain.value_objects import UserEmail, pronoun


class SqlAlcheamyUser(Base):
    email = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    pronoun = Column(
        Enum(pronoun.Pronoun, values_callable=lambda x: pronoun.Pronoun.keys(), name='pronouns'))

    __tablename__ = 'users'


class SqlAlcheamyUserRepository(SqlAlcheamyRepository, SqlAlcheamyCreateMixin, SqlAlcheamyFindMixin):

    model_class = SqlAlcheamyUser
    entity_class = User

    async def find_by_email(self, email: UserEmail) -> User:
        """Find user by email"""
        stmt = select(SqlAlcheamyUser).where(SqlAlcheamyUser.email == email.value).limit(1)
        return await self._find(stmt)
