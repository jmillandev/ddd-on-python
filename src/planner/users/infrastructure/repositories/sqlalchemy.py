"""User respository"""
from typing import Optional

from sqlalchemy import UUID, Boolean, Column, DateTime, Enum, String, select

from src.planner.shared.infrastructure.persistence.sqlalchemy.models import Base
from src.planner.shared.infrastructure.persistence.sqlalchemy.repositories import (
    SqlAlcheamyCreateMixin,
    SqlAlcheamyFindMixin,
    SqlAlcheamyRepository,
)
from src.planner.users.domain.entity import User
from src.planner.users.domain.value_objects import UserEmail, pronoun


class SqlAlcheamyUser(Base):
    id = Column(UUID, primary_key=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    email = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    pronoun = Column(
        Enum(
            pronoun.Pronoun,
            values_callable=lambda _: pronoun.Pronoun.keys(),
            name="pronouns",
        )
    )

    __tablename__ = "users"


class SqlAlcheamyUserRepository(
    SqlAlcheamyRepository, SqlAlcheamyCreateMixin, SqlAlcheamyFindMixin
):
    model_class = SqlAlcheamyUser
    entity_class = User

    async def search_by_email(self, email: UserEmail) -> Optional[User]:
        """Search user by email"""
        stmt = (
            select(SqlAlcheamyUser).where(SqlAlcheamyUser.email == email.value).limit(1)
        )
        return await self._search(stmt)
