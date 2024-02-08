from typing import Set

from kink import inject

from src.planner.accounts.domain.value_objects.delta_balance import AccountDeltaBalance
from src.planner.shared.domain.accounts import AccountId
from src.planner.shared.domain.movements.events import ExpenseMovementAdded
from src.shared.domain.bus.event.domain_event import DomainEvent
from src.shared.domain.bus.event.domain_event_susbcriber import DomainEventSubscriber

from ..updater import AccountBalanceUpdater


@inject
class DecreaseAccountBalanceOnExpenseAdded(DomainEventSubscriber):
    def __init__(
        self, user_case: AccountBalanceUpdater
    ) -> None:
        self.user_case = user_case

    async def __call__(self, event: DomainEvent) -> None:
        if isinstance(event, ExpenseMovementAdded):
            await self.user_case(
                id=AccountId(event.account_id),
                delta_balance=AccountDeltaBalance(event.amount * -1),
            )
            return
        raise RuntimeError

    @staticmethod
    def subscribed_to() -> Set[type[DomainEvent]]:
        return {ExpenseMovementAdded}
