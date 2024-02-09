from kink import inject

from src.planner.accounts.domain.exceptions.not_found import AccountNotFound
from src.planner.accounts.domain.repository import AccountRepository
from src.planner.accounts.domain.value_objects.delta_balance import AccountDeltaBalance
from src.planner.shared.domain.accounts import AccountId
from src.shared.domain.bus.event.event_bus import EventBus


@inject
class AccountBalanceUpdater:
    def __init__(self, repository: AccountRepository, event_bus: EventBus):
        self._repository = repository
        self._event_bus = event_bus

    async def __call__(self, id: AccountId, delta_balance: AccountDeltaBalance) -> None:
        account = await self._repository.search(id)
        if account is None:
            raise AccountNotFound

        account.update_balance(delta_balance)
        await self._repository.save(account)
        await self._event_bus.publish(*account.pull_domain_events())
