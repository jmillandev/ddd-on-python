from unittest.mock import ANY, Mock

import pytest

from src.planner.accounts.application.create.command import CreateAccountCommand
from src.planner.accounts.application.create.command_handler import (
    CreateAccountCommandHandler,
)
from src.planner.accounts.application.create.creator import AccountCreator
from src.planner.accounts.domain.events.created import AccountCreated
from src.planner.accounts.domain.exceptions.name_already_registered import (
    NameAlreadyRegistered,
)
from src.planner.accounts.domain.repository import AccountRepository
from src.planner.shared.domain.exceptions.base import DomainException
from src.shared.domain.bus.event.event_bus import EventBus
from tests.src.planner.shared.factories.accounts import AccountFactory

pytestmark = pytest.mark.anyio


class TestCreateAccountCommandHandler:
    def setup_method(self):
        self._repository = Mock(AccountRepository)
        self._event_bus = Mock(EventBus)
        use_case = AccountCreator(self._repository, self._event_bus)
        self.handler = CreateAccountCommandHandler(use_case)

    async def test_should_create_an_account(self) -> None:
        self._repository.search_by_name_and_owner_id.return_value = None
        params = AccountFactory().to_dict()
        account = AccountFactory.build(**params)
        command = CreateAccountCommand.from_dict(params)
        account_created = AccountCreated.make(
            account.id.primitive,
            event_id=ANY,
            ocurrend_at=ANY,
            owner_id=account.owner_id.primitive,
            name=account.name.primitive,
            currency=account.currency.primitive,
            balance=account.balance.primitive,
        )

        await self.handler(command)

        self._repository.save.assert_called_once_with(account)
        self._event_bus.publish.assert_called_once_with(account_created)

    async def test_should_raise_error_name_already_registered(self) -> None:
        params = AccountFactory().to_dict()
        self._repository.search_by_name_and_owner_id.return_value = (
            AccountFactory.build(**params)
        )
        command = CreateAccountCommand.from_dict(params)

        with pytest.raises(NameAlreadyRegistered) as excinfo:
            await self.handler(command)

        assert isinstance(excinfo.value, DomainException)
        assert excinfo.value.source == "name"
        assert self._repository.save.call_count == 0
        assert self._event_bus.publish.call_count == 0
