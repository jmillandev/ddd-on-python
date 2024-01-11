"""User respository"""
from typing import Optional

from sqlalchemy import Column, String, select, UUID

from src.auth.domain.entity import AuthCredential
from src.auth.domain.value_objects import AuthUsername, AuthPassword
from src.shared.infrastructure.persistence.sqlalchemy.models import Base
from src.shared.infrastructure.persistence.sqlalchemy.repositories import SqlAlcheamyRepository
from src.shared.domain.users import UserId

class SqlAlcheamyAuthCredential(Base):
    user_id = Column(UUID, primary_key=True)
    username = Column(String)
    password = Column(String)
    __tablename__ = 'auth_credentials'


class SqlAlcheamyAuthCredentialRepository(SqlAlcheamyRepository):

    model_class = SqlAlcheamyAuthCredential
    entity_class = AuthCredential

    async def search(self, username: AuthUsername) -> Optional[AuthCredential]:
        """Find credential by username"""
        stmt = select(SqlAlcheamyAuthCredential).where(SqlAlcheamyAuthCredential.username == username.value).limit(1)
        result = await self.session.execute(stmt)
        data = result.scalars().first()
        if data:
            return AuthCredential(
                user_id=UserId(data.user_id),
                username=AuthUsername(data.username),
                password=AuthPassword(data.password, is_hashed=True)
            )
