"""User respository"""
from typing import Optional

from sqlalchemy import UUID, Column, String, select

from src.planner.auth_token.domain.entity import AuthCredential
from src.planner.auth_token.domain.value_objects import AuthPassword, AuthUsername
from src.planner.shared.domain.users import UserId
from src.planner.shared.infrastructure.persistence.sqlalchemy.models import Base
from src.planner.shared.infrastructure.persistence.sqlalchemy.repositories import (
    SqlAlchemyRepository,
)


class SqlAlchemyAuthCredential(Base):
    user_id = Column(UUID, primary_key=True)
    username = Column(String)
    password = Column(String)
    __tablename__ = "planner__auth_credentials"


class SqlAlchemyAuthCredentialRepository(SqlAlchemyRepository):
    model_class = SqlAlchemyAuthCredential
    entity_class = AuthCredential

    async def search(self, username: AuthUsername) -> Optional[AuthCredential]:
        """Find credential by username"""
        stmt = (
            select(SqlAlchemyAuthCredential)
            .where(SqlAlchemyAuthCredential.username == username.value)
            .limit(1)
        )
        result = await self.session.execute(stmt)
        data = result.scalars().first()
        if data:
            return AuthCredential(
                user_id=UserId(data.user_id),
                username=AuthUsername(data.username),
                password=AuthPassword(str(data.password), is_hashed=True),  # type: ignore[call-arg]
            )
        return None
