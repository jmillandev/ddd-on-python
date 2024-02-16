from kink import inject

from src.planner.accounts.domain.value_objects.delta_balance import AccountDeltaBalance
from src.planner.shared.domain.accounts import AccountId
from src.planner.shared.domain.movements.events import IncomeMovementAdded
from src.shared.domain.bus.event.domain_event import DomainEvent
from src.shared.domain.bus.event.domain_event_susbcriber import DomainEventSubscriber

from ..updater import AccountBalanceUpdater


@inject
class IncreaseAccountBalanceOnIncomeAdded(DomainEventSubscriber):
    def __init__(self, use_case: AccountBalanceUpdater) -> None:
        self.use_case = use_case

    async def __call__(self, event: DomainEvent) -> None:
        if isinstance(event, IncomeMovementAdded):
            await self.use_case(
                id=AccountId(event.account_id),
                delta_balance=AccountDeltaBalance(event.amount),
            )
            return
        raise RuntimeError

    @staticmethod
    def subscribed_to() -> type[DomainEvent]:
        return IncomeMovementAdded
