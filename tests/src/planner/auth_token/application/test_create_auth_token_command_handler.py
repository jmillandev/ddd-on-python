from datetime import datetime
from unittest.mock import Mock

import pytest

from src.planner.auth_token.application.create.command import CreateAuthTokenCommand
from src.planner.auth_token.application.create.command_handler import (
    CreateAuthTokenCommandHandler,
)
from src.planner.auth_token.application.create.creator import AuthTokenCreator
from src.planner.auth_token.application.shared.response import AuthTokenResponse
from src.planner.auth_token.domain.exceptions.invalid_credentials import (
    InvalidCredentials,
)
from src.planner.auth_token.domain.repository import AuthCredentialRepository
from src.planner.shared.domain.exceptions.base import DomainException
from tests.src.planner.auth_token.factories import AuthCredentialFactory

pytestmark = pytest.mark.anyio


class TestCreateAuthTokenCommandHandler:
    def setup_method(self):
        self._repository = Mock(AuthCredentialRepository)
        use_case = AuthTokenCreator(self._repository)
        self.handler = CreateAuthTokenCommandHandler(use_case)

    async def test_should_create_a_token(self) -> None:
        params = AuthCredentialFactory.to_dict()
        credential = AuthCredentialFactory.build(**params)
        self._repository.search.return_value = credential
        command = CreateAuthTokenCommand(**params)

        token = await self.handler(command)
        assert isinstance(token, AuthTokenResponse)

        assert token.access_token is not None
        assert token.expires_at > datetime.now().timestamp()
        assert token.user_id == credential.user_id.primitive

    async def test_should_raise_error_invalid_username(self) -> None:
        params = AuthCredentialFactory.to_dict()
        command = CreateAuthTokenCommand(**params)
        self._repository.search.return_value = None

        with pytest.raises(InvalidCredentials) as excinfo:
            await self.handler(command)

        assert isinstance(excinfo.value, DomainException)
        assert excinfo.value.source == "credentials"

    async def test_should_raise_error_invalid_password(self, fake) -> None:
        params = AuthCredentialFactory.to_dict()
        command = CreateAuthTokenCommand(**params)
        params.update(password=fake.password())
        self._repository.search.return_value = AuthCredentialFactory.build(**params)

        with pytest.raises(InvalidCredentials) as excinfo:
            await self.handler(command)

        assert isinstance(excinfo.value, DomainException)
        assert excinfo.value.source == "credentials"
