from kink import inject

from src.planner.accounts.domain.value_objects.delta_balance import AccountDeltaBalance
from src.planner.shared.domain.accounts import AccountId
from src.planner.shared.domain.movements.events import TransferMovementAdded
from src.shared.domain.bus.event.domain_event import DomainEvent
from src.shared.domain.bus.event.domain_event_susbcriber import DomainEventSubscriber

from ..updater import AccountBalanceUpdater


@inject
class IncreaseAccountBalanceOnTransferAdded(DomainEventSubscriber):
    def __init__(self, use_case: AccountBalanceUpdater) -> None:
        self.use_case = use_case

    async def __call__(self, event: DomainEvent) -> None:
        if isinstance(event, TransferMovementAdded):
            await self.use_case(
                id=AccountId(event.destination_id),
                delta_balance=AccountDeltaBalance(event.amount),
            )
            return
        raise RuntimeError

    @staticmethod
    def subscribed_to() -> type[DomainEvent]:
        return TransferMovementAdded
