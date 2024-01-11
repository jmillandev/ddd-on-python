from unittest.mock import Mock

import pytest

from src.auth.application.command import CreateAuthTokenCommand
from src.auth.application.command_handler import CreateAuthTokenCommandHandler
from src.auth.application.creator import AuthTokenCreator
from src.auth.domain.exceptions.invalid_credentials import InvalidCredentials
from src.auth.domain.repository import AuthCredentialRepository
from src.shared.domain.exceptions.base import DomainException
from tests.src.auth.factories import AuthCredentialFactory

pytestmark = pytest.mark.anyio


class TestCreateAuthTokenCommandHandler:

    def setup(self):
        self._repository = Mock(AuthCredentialRepository)
        use_case = AuthTokenCreator(self._repository)
        self.handler = CreateAuthTokenCommandHandler(use_case)

    async def test_should_create_a_token(self) -> None:
        params = AuthCredentialFactory.to_dict()
        self._repository.search.return_value = AuthCredentialFactory.build(**params)
        command = CreateAuthTokenCommand(**params)

        await self.handler(command)

    async def test_should_raise_error_invalid_username(self) -> None:
        params = AuthCredentialFactory.to_dict()
        command = CreateAuthTokenCommand(**params)
        self._repository.search.return_value = None

        with pytest.raises(InvalidCredentials) as excinfo:
            await self.handler(command)

        assert isinstance(excinfo.value, DomainException)
        assert excinfo.value.source == 'credentials'

    async def test_should_raise_error_invalid_password(self, fake) -> None:
        params = AuthCredentialFactory.to_dict()
        command = CreateAuthTokenCommand(**params)
        params.update(password=fake.password())
        self._repository.search.return_value = AuthCredentialFactory.build(**params)

        with pytest.raises(InvalidCredentials) as excinfo:
            await self.handler(command)

        assert isinstance(excinfo.value, DomainException)
        assert excinfo.value.source == 'credentials'
