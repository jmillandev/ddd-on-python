from typing import Set
from uuid import uuid4

from kink import inject

from src.planner.accounts.domain.value_objects import (
    AccountBalance,
    AccountCurrency,
    AccountId,
    AccountName,
)
from src.planner.accounts.domain.value_objects.currency import Currency
from src.planner.shared.domain.users import UserId
from src.planner.shared.domain.users.events import UserRegistered
from src.shared.domain.bus.event.domain_event import DomainEvent

from ..creator import AccountCreator
from src.shared.domain.bus.event.domain_event_susbcriber import DomainEventSubscriber


@inject
class CreateAccountOnUserRegistered(DomainEventSubscriber):
    def __init__(self, user_case: AccountCreator) -> None:
        self.user_case = user_case

    async def __call__(self, event: UserRegistered) -> None:
        await self.user_case(
            id=AccountId(uuid4()),
            user_id=UserId(event.aggregate_id),
            name=AccountName(event.name),
            currency=AccountCurrency(Currency.USD),
            balance=AccountBalance(0),
        )

    @staticmethod
    def subscribed_to() -> Set[type[DomainEvent]]:
        return {UserRegistered}
