from unittest.mock import ANY, Mock

import pytest

from src.planner.shared.domain.exceptions.base import DomainException
from src.planner.shared.domain.exceptions.invalid_value import InvalidValueException
from src.planner.users.application.register.command import RegisterUserCommand
from src.planner.users.application.register.command_handler import (
    RegisterUserCommandHandler,
)
from src.planner.users.application.register.register import UserRegistrator
from src.planner.users.domain.events.registered import UserRegistered
from src.planner.users.domain.exceptions.email_already_used import EmailAlreadyUsed
from src.planner.users.domain.repository import UserRepository
from src.shared.domain.bus.event.event_bus import EventBus
from tests.src.planner.users.factories import UserFactory

pytestmark = pytest.mark.anyio


class TestCreateUserCommandHandler:
    def setup_method(self):
        self._repository = Mock(UserRepository)
        self._event_bus = Mock(EventBus)
        use_case = UserRegistrator(self._repository, self._event_bus)
        self.handler = RegisterUserCommandHandler(use_case)

    async def test_should_create_a_user(self) -> None:
        self._repository.search_by_email.return_value = None
        params = UserFactory.to_dict()
        user = UserFactory.build(**params)
        command = RegisterUserCommand.from_dict(params)
        # TODO: Use Factory Pattern
        user_registered = UserRegistered.make(
            user.id.value,
            event_id=ANY,
            ocurrend_at=ANY,
            email=user.email.primitive,
            pronoun=user.pronoun.primitive,
            name=user.name.primitive,
            last_name=user.last_name.primitive,
        )
        await self.handler(command)

        self._repository.create.assert_called_once_with(user)
        self._event_bus.publish.assert_called_once_with(user_registered)

    async def test_should_raise_error_email_already_exists(self) -> None:
        params = UserFactory.to_dict()
        self._repository.search_by_email.return_value = UserFactory.build(**params)
        command = RegisterUserCommand.from_dict(params)

        with pytest.raises(EmailAlreadyUsed) as excinfo:
            await self.handler(command)

        assert isinstance(excinfo.value, DomainException)

    async def test_should_raise_error_invalid_email(self, fake) -> None:
        params = UserFactory.to_dict(email=fake.name())
        command = RegisterUserCommand.from_dict(params)

        with pytest.raises(InvalidValueException) as excinfo:
            await self.handler(command)

        assert isinstance(excinfo.value, DomainException)
        assert excinfo.value.source == "email"
