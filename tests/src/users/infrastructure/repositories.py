"""User respository"""
from typing import Optional

from apps.users.models import User
from db.base_repository import BaseRepository
from src.users.domain.value_objects import UserEmail, UserId


class InMemoryUserRepository(BaseRepository):
    def __init__(self, users: dict[UserId, User]):
        self._users = users

    async def find_by_email(self, email: UserEmail) -> User:
        """Find user by email"""
        for user in self._users.values():
            if user.email == email:
                return user

    async def find(self, id: UserId) -> Optional[User]:
        """Find object by id"""
        try:
            return self._users[id]
        except KeyError:
            pass

    async def create(self,  user: User) -> User:
        """Save user"""
        self._users[user.id] = user
        return user
