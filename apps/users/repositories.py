"""User respository"""

from db.base_repository import BaseRepository
from sqlalchemy import select
from apps.users.models import User

class UserRepository(BaseRepository):
    """User repository"""
    model = User

    async def find_by_email(self, email: str) -> User:
        """Find user by email"""
        result = await self.session.execute(
            select(self.model).where(self.model.email == email).limit(1)
        )
        return result.first()
