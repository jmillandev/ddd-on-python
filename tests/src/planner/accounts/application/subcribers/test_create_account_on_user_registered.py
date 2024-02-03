from unittest.mock import ANY, Mock

import pytest
from faker import Faker

from src.planner.accounts.application.create.creator import AccountCreator
from src.planner.accounts.application.create.subscribers.create_account_on_user_registered import (
    CreateAccountOnUserRegistered,
)
from src.planner.accounts.domain.events.created import AccountCreated
from src.planner.accounts.domain.repository import AccountRepository
from src.planner.shared.domain.generators.uuid import UuidGenerator
from src.planner.shared.domain.users.events import UserRegistered
from src.shared.domain.bus.event.event_bus import EventBus
from tests.src.planner.shared.factories.accounts import AccountFactory

faker = Faker()
pytestmark = pytest.mark.anyio


class TestCreateAccountOnUserRegistered:
    def setup_method(self):
        self._repository = Mock(AccountRepository)
        self._event_bus = Mock(EventBus)
        use_case = AccountCreator(self._repository, self._event_bus)
        self.uuid_generator = Mock(UuidGenerator)
        # TODO: Create a factory for UserRegistered
        self.event = UserRegistered.make(
            aggregate_id=str(faker.uuid4()),
            name=faker.name(),
            email=faker.email(),
            last_name=faker.last_name(),
            pronoun=faker.word(),
        )
        self.subscriber = CreateAccountOnUserRegistered(use_case, self.uuid_generator)

    async def test_should_create_an_account_on_user_registered(self) -> None:
        self._repository.search_by_name_and_owner_id.return_value = None
        uuid = faker.uuid4()
        self.uuid_generator.return_value = uuid
        account = AccountFactory.build(
            id=uuid,
            name="Main",
            currency="USD",
            owner_id=self.event.aggregate_id,
            balance=0,
        )
        account_created = AccountCreated.make(
            account.id.primitive,
            event_id=ANY,
            ocurrend_at=ANY,
            owner_id=account.owner_id.primitive,
            name=account.name.primitive,
            currency=account.currency.primitive,
            balance=account.balance.primitive,
        )

        assert self.event.__class__ in self.subscriber.subscribed_to()

        await self.subscriber(self.event)

        self._repository.create.assert_called_once_with(account)
        self._event_bus.publish.assert_called_once_with(account_created)
