import pytest
from unittest.mock import ANY, Mock

from src.planner.expenses.domain.repository import ExpenseRepository
from src.planner.shared.domain.bus.query import QueryBus
from src.shared.domain.bus.event.event_bus import EventBus
from src.planner.expenses.application.auth import ExpenseAuthorizationService
from src.planner.expenses.application.add.command_handler import AddExpenseCommandHandler
from src.planner.expenses.application.add.command import AddExpenseCommand
from src.planner.expenses.application.add.adder import ExpenseAdder

from tests.src.planner.shared.factories.accounts import AccountFactory
from tests.src.planner.expenses.factories import ExpenseFactory

from src.planner.shared.application.accounts import AccountResponse, FindAccountQuery
from src.planner.expenses.domain.events.added import ExpenseAdded
from src.planner.shared.domain.exceptions.base import DomainException
from src.shared.domain.exceptions.not_found import NotFound


pytestmark = pytest.mark.anyio

class TestAddExpenseCommandHandler:
    def setup_method(self) -> None:
        # Mocks
        self._repository = Mock(spec=ExpenseRepository)
        self._event_bus = Mock(EventBus)
        self._query_bus = Mock(QueryBus)
        self._auth_service = ExpenseAuthorizationService(self._query_bus)

        # Use case And Handler
        use_case = ExpenseAdder(self._repository, self._event_bus, self._auth_service)
        self.handler = AddExpenseCommandHandler(use_case)

        # Arrange
        self.account = AccountFactory.build()
        self.params = ExpenseFactory().to_dict(account_id=self.account.id.primitive)
        self.expense = ExpenseFactory.build(**self.params)

    async def test_should_create_an_expenses(self) -> None:
        command = AddExpenseCommand.from_dict(self.params.update(user_id=self.account.owner_id.primitive))
        account_query = FindAccountQuery(id=command.id, user_id=command.user_id)
        account_response = AccountResponse.from_dict(self.account)
        self._query_bus.ask.return_value = account_response
        expense_added = ExpenseAdded.make(
            self.expense.id.primitive,
            event_id=ANY,
            ocurrend_at=ANY,
            account_id=self.expense.account_id.primitive,
            amount=self.expense.amount.primitive,
            date=self.expense.date.primitive,
        )

        command = AddExpenseCommand.from_dict(self.params.update(user_id=self.account.owner_id.primitive))

        await self.handler(command)
        
        self._query_bus.ask.assert_called_once_with(account_query)
        self._repository.create.assert_called_once_with(self.expense)
        self._event_bus.publish.assert_called_once_with(expense_added)

    async def test_should_raise_error_not_found_if_account_belong_to_another_user(self, faker) -> None:
        command = AddExpenseCommand.from_dict(self.params.update(user_id=str(faker.uuid4())))
        account_query = FindAccountQuery(id=command.id, user_id=command.user_id)
        self._query_bus.ask.side_effect = NotFound("On Query Bus")

        with pytest.raises(NotFound) as excinfo:
            await self.handler(command)

        assert isinstance(excinfo.value, DomainException)
        assert excinfo.value.message == "On Query Bus"

        self._query_bus.ask.assert_called_once_with(account_query)
        assert self._repository.create.call_count == 0
        assert self._repository.publish.call_count == 0
