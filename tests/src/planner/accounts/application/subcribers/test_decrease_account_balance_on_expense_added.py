from unittest.mock import ANY, Mock

import pytest
from faker import Faker

from src.planner.accounts.application.update_balance.subscribers import (
    DecreaseAccountBalanceOnExpenseAdded,
)
from src.planner.accounts.application.update_balance.updater import (
    AccountBalanceUpdater,
)
from src.planner.accounts.domain.events.balance_updated import AccountBalanceUpdated
from src.planner.accounts.domain.repository import AccountRepository
from src.shared.domain.bus.event.event_bus import EventBus
from tests.src.planner.movements.factories import ExpenseMovementAddedFactory
from tests.src.planner.shared.factories.accounts import AccountFactory

faker = Faker()
pytestmark = pytest.mark.anyio


class TestDecreaseAccountBalanceOnExpenseAdded:
    def setup_method(self):
        self._repository = Mock(AccountRepository)
        self._event_bus = Mock(EventBus)
        self.event = ExpenseMovementAddedFactory.build()
        use_case = AccountBalanceUpdater(self._repository, self._event_bus)
        self.subscriber = DecreaseAccountBalanceOnExpenseAdded(use_case)

    async def test_should_decreaser_balance_account_on_expense_added(self) -> None:
        account_factory = AccountFactory(id=self.event.account_id)
        account = account_factory.aggregate()
        balance_updated_event = AccountBalanceUpdated.make(
            account.id.primitive,
            event_id=ANY,
            ocurrend_at=ANY,
            owner_id=account.owner_id.primitive,
            balance=account.balance.primitive - self.event.amount,
            currency=account.currency.primitive,
            name=account.name.primitive,
        )
        self._repository.search.return_value = account

        assert self.event.__class__ is self.subscriber.subscribed_to()

        await self.subscriber(self.event)

        assert account.balance.primitive == account_factory.balance - self.event.amount
        self._repository.search.assert_called_once_with(account.id)
        self._repository.save.assert_called_once_with(account)
        self._event_bus.publish.assert_called_once_with(balance_updated_event)
