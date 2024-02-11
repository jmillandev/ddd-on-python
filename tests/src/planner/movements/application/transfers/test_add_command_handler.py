from unittest.mock import ANY, Mock, call

import pytest

from src.planner.movements.application.auth import MovementAuthorizationService
from src.planner.movements.application.transfers.add.adder import TransferMovementAdder
from src.planner.movements.application.transfers.add.command import (
    AddTransferMovementCommand,
)
from src.planner.movements.application.transfers.add.command_handler import (
    AddTransferMovementCommandHandler,
)
from src.planner.movements.domain.repository import MovementRepository
from src.planner.shared.application.accounts.query import FindAccountQuery
from src.planner.shared.application.accounts.response import AccountResponse
from src.planner.shared.application.mappers import entity_to_response
from src.planner.shared.domain.bus.query import QueryBus
from src.planner.shared.domain.exceptions.base import DomainException
from src.planner.shared.domain.movements.events import TransferMovementAdded
from src.shared.domain.bus.event.event_bus import EventBus
from src.shared.domain.exceptions.not_found import NotFound
from tests.src.planner.movements.factories import TransferMovementFactory
from tests.src.planner.shared.factories.accounts import AccountFactory
from tests.src.planner.users.factories import UserFactory  # TODO: Move to shared

pytestmark = pytest.mark.anyio


class TestAddTransferMovementCommandHandler:
    def setup_method(self) -> None:
        # Mocks
        self._repository = Mock(spec=MovementRepository)
        self._event_bus = Mock(EventBus)
        self._query_bus = Mock(QueryBus)
        self._auth_service = MovementAuthorizationService(self._query_bus)

        # Use case And Handler
        use_case = TransferMovementAdder(
            self._repository, self._event_bus, self._auth_service
        )
        self.handler = AddTransferMovementCommandHandler(use_case)

        # Arrange
        self.owner = UserFactory.build()
        self.origin = AccountFactory.build(owner_id=self.owner.id.primitive)
        self.destination = AccountFactory.build(owner_id=self.owner.id.primitive)
        transfer_factory = TransferMovementFactory(
            origin_id=self.origin.id.primitive,
            destination_id=self.destination.id.primitive,
        )
        self.transfer = transfer_factory.aggregate()
        self.transfer_attrs = transfer_factory.to_dict()

        self.origin_response = entity_to_response(self.origin, AccountResponse)
        self.destination_response = entity_to_response(
            self.destination, AccountResponse
        )

    async def test_should_create_an_transfer(self, faker) -> None:
        command = AddTransferMovementCommand.from_dict(
            dict(self.transfer_attrs, user_id=self.owner.id.primitive)
        )
        origin_query = FindAccountQuery(id=command.origin_id, owner_id=command.user_id)
        destination_query = FindAccountQuery(
            id=command.destination_id, owner_id=command.user_id
        )
        self._query_bus.ask.side_effect = [origin_query, destination_query]
        transfer_added = TransferMovementAdded.make(
            self.transfer.id.primitive,
            event_id=ANY,
            ocurrend_at=ANY,
            origin_id=self.transfer.origin_id.primitive,
            destination_id=self.transfer.destination_id.primitive,
            amount=self.transfer.amount.primitive,
            date=self.transfer.date.primitive,
        )

        await self.handler(command)

        self._query_bus.ask.assert_has_calls(
            [call(origin_query), call(destination_query)]
        )
        assert self._query_bus.ask.call_count == 2
        self._repository.save.assert_called_once_with(self.transfer)
        self._event_bus.publish.assert_called_once_with(transfer_added)

    async def test_should_raise_error_not_found_if_account_belong_to_another_user(
        self, faker
    ) -> None:
        command = AddTransferMovementCommand.from_dict(
            dict(self.transfer_attrs, user_id=self.owner.id.primitive)
        )
        origin_query = FindAccountQuery(id=command.origin_id, owner_id=command.user_id)
        destination_query = FindAccountQuery(
            id=command.destination_id, owner_id=command.user_id
        )
        self._query_bus.ask.side_effect = [destination_query, NotFound("On Query Bus")]
        with pytest.raises(NotFound) as excinfo:
            await self.handler(command)

        assert isinstance(excinfo.value, DomainException)
        assert excinfo.value.message == "On Query Bus"

        self._query_bus.ask.assert_has_calls(
            [call(origin_query), call(destination_query)]
        )
        assert self._query_bus.ask.call_count == 2
        assert self._repository.save.call_count == 0
        assert self._event_bus.publish.call_count == 0
