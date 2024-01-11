"""User respository"""
from typing import Optional

from sqlalchemy import Column, String, select, UUID

from src.auth.domain.entity import AuthCredential
from src.auth.domain.value_objects import AuthUsername
from src.shared.infrastructure.persistence.sqlalchemy.models import Base
from src.shared.infrastructure.persistence.sqlalchemy.repositories import (
    SqlAlcheamyFindMixin, SqlAlcheamyRepository)


class SqlAlcheamyAuthCredential(Base):
    user_id = Column(UUID, primary_key=True)
    username = Column(String)
    password = Column(String)
    __tablename__ = 'auth_credentials'


class SqlAlcheamyAuthCredentialRepository(SqlAlcheamyRepository, SqlAlcheamyFindMixin):

    model_class = SqlAlcheamyAuthCredential
    entity_class = AuthCredential

    async def find(self, username: AuthUsername) -> Optional[AuthCredential]:
        """Find credential by username"""
        stmt = select(SqlAlcheamyAuthCredential).where(SqlAlcheamyAuthCredential.username == username.value).limit(1)
        return await self._find(stmt)
