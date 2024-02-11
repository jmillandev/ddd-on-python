from unittest.mock import ANY, Mock

import pytest

from src.planner.movements.application.auth import MovementAuthorizationService
from src.planner.movements.application.incomes.add.adder import IncomeMovementAdder
from src.planner.movements.application.incomes.add.command import (
    AddIncomeMovementCommand,
)
from src.planner.movements.application.incomes.add.command_handler import (
    AddIncomeMovementCommandHandler,
)
from src.planner.movements.domain.repository import MovementRepository
from src.planner.shared.application.accounts.query import FindAccountQuery
from src.planner.shared.application.accounts.response import AccountResponse
from src.planner.shared.application.mappers import entity_to_response
from src.planner.shared.domain.bus.query import QueryBus
from src.planner.shared.domain.exceptions.base import DomainException
from src.planner.shared.domain.movements.events import IncomeMovementAdded
from src.shared.domain.bus.event.event_bus import EventBus
from src.shared.domain.exceptions.not_found import NotFound
from tests.src.planner.movements.factories import IncomeMovementFactory
from tests.src.planner.shared.factories.accounts import AccountFactory

pytestmark = pytest.mark.anyio


class TestAddIncomeMovementCommandHandler:
    def setup_method(self) -> None:
        # Mocks
        self._repository = Mock(spec=MovementRepository)
        self._event_bus = Mock(EventBus)
        self._query_bus = Mock(QueryBus)
        self._auth_service = MovementAuthorizationService(self._query_bus)

        # Use case And Handler
        use_case = IncomeMovementAdder(
            self._repository, self._event_bus, self._auth_service
        )
        self.handler = AddIncomeMovementCommandHandler(use_case)

        # Arrange
        self.account = AccountFactory.build()
        income_factory = IncomeMovementFactory(account_id=self.account.id.primitive)
        self.income = income_factory.aggregate()
        self.income_attrs = income_factory.to_dict()

    async def test_should_create_an_income(self) -> None:
        command = AddIncomeMovementCommand.from_dict(
            dict(self.income_attrs, user_id=self.account.owner_id.primitive)
        )
        account_query = FindAccountQuery(
            id=command.account_id, owner_id=command.user_id
        )
        account_response = entity_to_response(self.account, AccountResponse)
        self._query_bus.ask.return_value = account_response
        income_added = IncomeMovementAdded.make(
            self.income.id.primitive,
            event_id=ANY,
            ocurrend_at=ANY,
            account_id=self.income.account_id.primitive,
            amount=self.income.amount.primitive,
            date=self.income.date.primitive,
        )

        await self.handler(command)

        self._query_bus.ask.assert_called_once_with(account_query)
        self._repository.save.assert_called_once_with(self.income)
        self._event_bus.publish.assert_called_once_with(income_added)

    async def test_should_raise_error_not_found_if_account_belong_to_another_user(
        self, faker
    ) -> None:
        command = AddIncomeMovementCommand.from_dict(
            dict(self.income_attrs, user_id=str(faker.uuid4()))
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
