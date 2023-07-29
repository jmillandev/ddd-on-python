"""User respository"""

from db.base_repository import BaseRepository

from apps.users.models import User

class UserRepository(BaseRepository):
    """User repository"""
    model = User

    def find_by_email(self, email: str) -> User:
        """Find user by email"""
        return self.db.query(self.model).filter(self.model.email == email).first()
