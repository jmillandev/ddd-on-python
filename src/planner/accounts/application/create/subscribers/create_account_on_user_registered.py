from kink import inject

from src.planner.accounts.domain.value_objects import (
    AccountBalance,
    AccountCurrency,
    AccountName,
)
from src.planner.accounts.domain.value_objects.currency import Currency
from src.planner.shared.domain.accounts import AccountId
from src.planner.shared.domain.generators.uuid import UuidGenerator
from src.planner.shared.domain.users import UserId
from src.planner.shared.domain.users.events import UserRegistered
from src.shared.domain.bus.event.domain_event import DomainEvent
from src.shared.domain.bus.event.domain_event_susbcriber import DomainEventSubscriber

from ..creator import AccountCreator


@inject
class CreateAccountOnUserRegistered(DomainEventSubscriber):
    def __init__(self, use_case: AccountCreator, uuid_generator: UuidGenerator) -> None:
        self.use_case = use_case
        self.uuid_generator = uuid_generator

    async def __call__(self, event: DomainEvent) -> None:
        if isinstance(event, UserRegistered):
            await self.use_case(
                id=AccountId(self.uuid_generator()),
                owner_id=UserId(event.aggregate_id),
                name=AccountName("Main"),
                currency=AccountCurrency(Currency.USD),
                balance=AccountBalance(0),
            )
            return
        raise RuntimeError

    @staticmethod
    def subscribed_to() -> type[DomainEvent]:
        return UserRegistered
