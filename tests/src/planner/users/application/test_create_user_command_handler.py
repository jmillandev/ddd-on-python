from unittest.mock import Mock

import pytest

from src.planner.shared.domain.exceptions.base import DomainException
from src.planner.shared.domain.exceptions.invalid_value import InvalidValueException
from src.planner.users.application.command import CreateUserCommand
from src.planner.users.application.command_handler import CreateUserCommandHandler
from src.planner.users.application.creator import UserCreator
from src.planner.users.domain.exceptions.email_already_used import EmailAlreadyUsed
from src.planner.users.domain.repository import UserRepository
from tests.src.planner.users.factories import UserFactory

pytestmark = pytest.mark.anyio


class TestCreateUserCommandHandler:
    def setup(self):
        self._repository = Mock(UserRepository)
        use_case = UserCreator(self._repository)
        self.handler = CreateUserCommandHandler(use_case)

    async def test_should_create_a_user(self) -> None:
        self._repository.search_by_email.return_value = None

        params = UserFactory.to_dict()
        user = UserFactory.build(**params)
        command = CreateUserCommand(**params)
        await self.handler(command)

        self._repository.create.assert_called_once_with(user)

    async def test_should_raise_error_email_already_exists(self) -> None:
        params = UserFactory.to_dict()
        self._repository.search_by_email.return_value = UserFactory.build(**params)
        command = CreateUserCommand(**params)

        with pytest.raises(EmailAlreadyUsed) as excinfo:
            await self.handler(command)

        assert isinstance(excinfo.value, DomainException)

    async def test_should_raise_error_invalid_email(self, fake) -> None:
        params = UserFactory.to_dict(email=fake.name())
        command = CreateUserCommand(**params)

        with pytest.raises(InvalidValueException) as excinfo:
            await self.handler(command)

        assert isinstance(excinfo.value, DomainException)
        assert excinfo.value.source == "email"
