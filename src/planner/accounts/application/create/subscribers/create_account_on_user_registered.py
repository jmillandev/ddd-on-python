from typing import Set

from kink import inject

from src.planner.accounts.domain.value_objects import (
    AccountBalance,
    AccountCurrency,
    AccountId,
    AccountName,
)
from src.planner.accounts.domain.value_objects.currency import Currency
from src.planner.shared.domain.generators.uuid import UuidGenerator
from src.planner.shared.domain.users import UserId
from src.planner.shared.domain.users.events import UserRegistered
from src.shared.domain.bus.event.domain_event import DomainEvent
from src.shared.domain.bus.event.domain_event_susbcriber import DomainEventSubscriber

from ..creator import AccountCreator


@inject
class CreateAccountOnUserRegistered(DomainEventSubscriber):
    # TODO: Add test case
    def __init__(
        self, user_case: AccountCreator, uuid_generator: UuidGenerator
    ) -> None:
        self.user_case = user_case
        self.uuid_generator = uuid_generator

    async def __call__(self, event: DomainEvent) -> None:
        if isinstance(event, UserRegistered):
            await self.user_case(
                id=AccountId(self.uuid_generator()),
                user_id=UserId(event.aggregate_id),
                name=AccountName("Main"),
                currency=AccountCurrency(Currency.USD),
                balance=AccountBalance(0),
            )
            return
        raise RuntimeError

    @staticmethod
    def subscribed_to() -> Set[type[DomainEvent]]:
        return {UserRegistered}
