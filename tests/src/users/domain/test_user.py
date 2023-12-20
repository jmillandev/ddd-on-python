import pytest
from unittest.mock import Mock
from faker import Faker
from src.users.application.creator import UserCreator
from src.users.domain.repository import UserRepository
from tests.src.users.factories import UserFactory

fake = Faker()

pytestmark = pytest.mark.anyio

class TestUser:
    def setup(self):
        self._repository = Mock(UserRepository)

    async def test_create_a_user(self) -> None:
        user = UserFactory.build()

        await UserCreator(self._repository).create(
            id=user.id,
            email=user.email,
            name=user.name,
            last_name=user.last_name,
            pronoun=user.pronoun,
            password=user.password
        )

        self._repository.create.assert_called_once_with(user)
