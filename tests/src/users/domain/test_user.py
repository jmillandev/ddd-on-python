import pytest
from unittest.mock import Mock

from src.users.domain.exceptions.email_already_used import EmailAlreadyUsed
from src.users.application.creator import UserCreator
from src.users.domain.repository import UserRepository
from tests.src.users.factories import UserFactory


pytestmark = pytest.mark.anyio

class TestUser:
    def setup(self):
        self._repository = Mock(UserRepository)

    async def test_create_a_user(self) -> None:
        self._repository.find_by_email.return_value = None

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

    async def test_fail_because_email_already_exists(self) -> None:
        user = UserFactory.build()
        self._repository.find_by_email.return_value = user

        with pytest.raises(EmailAlreadyUsed):
            await UserCreator(self._repository).create(
                id=user.id,
                email=user.email,
                name=user.name,
                last_name=user.last_name,
                pronoun=user.pronoun,
                password=user.password
            )
