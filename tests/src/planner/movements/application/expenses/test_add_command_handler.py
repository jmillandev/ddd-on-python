from unittest.mock import ANY, Mock

import pytest

from src.planner.movements.application.auth import MovementAuthorizationService
from src.planner.movements.application.expenses.add.adder import ExpenseMovementAdder
from src.planner.movements.application.expenses.add.command import (
    AddExpenseMovementCommand,
)
from src.planner.movements.application.expenses.add.command_handler import (
    AddExpenseMovementCommandHandler,
)
from src.planner.shared.domain.movements.events import ExpenseMovementAdded
from src.planner.movements.domain.repository import MovementRepository
from src.planner.shared.application.accounts.query import FindAccountQuery
from src.planner.shared.application.accounts.response import AccountResponse
from src.planner.shared.application.mappers import entity_to_response
from src.planner.shared.domain.bus.query import QueryBus
from src.planner.shared.domain.exceptions.base import DomainException
from src.shared.domain.bus.event.event_bus import EventBus
from src.shared.domain.exceptions.not_found import NotFound
from tests.src.planner.movements.factories import ExpenseMovementFactory
from tests.src.planner.shared.factories.accounts import AccountFactory

pytestmark = pytest.mark.anyio


class TestAddExpenseMovementCommandHandler:
    def setup_method(self) -> None:
        # Mocks
        self._repository = Mock(spec=MovementRepository)
        self._event_bus = Mock(EventBus)
        self._query_bus = Mock(QueryBus)
        self._auth_service = MovementAuthorizationService(self._query_bus)

        # Use case And Handler
        use_case = ExpenseMovementAdder(
            self._repository, self._event_bus, self._auth_service
        )
        self.handler = AddExpenseMovementCommandHandler(use_case)

        # Arrange
        self.account = AccountFactory.build()
        self.params = ExpenseMovementFactory(
            account_id=self.account.id.primitive
        ).to_dict()
        self.expense = ExpenseMovementFactory.build(**self.params)

    async def test_should_create_an_expenses(self) -> None:
        command = AddExpenseMovementCommand.from_dict(
            dict(self.params, user_id=self.account.owner_id.primitive)
        )
        account_query = FindAccountQuery(
            id=command.account_id, owner_id=command.user_id
        )
        account_response = entity_to_response(self.account, AccountResponse)
        self._query_bus.ask.return_value = account_response
        expense_added = ExpenseMovementAdded.make(
            self.expense.id.primitive,
            event_id=ANY,
            ocurrend_at=ANY,
            account_id=self.expense.account_id.primitive,
            amount=self.expense.amount.primitive,
            date=self.expense.date.primitive,
        )

        await self.handler(command)

        self._query_bus.ask.assert_called_once_with(account_query)
        self._repository.save.assert_called_once_with(self.expense)
        self._event_bus.publish.assert_called_once_with(expense_added)

    async def test_should_raise_error_not_found_if_account_belong_to_another_user(
        self, faker
    ) -> None:
        command = AddExpenseMovementCommand.from_dict(
            dict(self.params, user_id=str(faker.uuid4()))
        )
        account_query = FindAccountQuery(
            id=command.account_id, owner_id=command.user_id
        )
        self._query_bus.ask.side_effect = NotFound("On Query Bus")

        with pytest.raises(NotFound) as excinfo:
            await self.handler(command)

        assert isinstance(excinfo.value, DomainException)
        assert excinfo.value.message == "On Query Bus"

        self._query_bus.ask.assert_called_once_with(account_query)
        assert self._repository.save.call_count == 0
        assert self._event_bus.publish.call_count == 0
