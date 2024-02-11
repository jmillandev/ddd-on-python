from kink import inject

from src.planner.accounts.domain.entity import Account
from src.planner.accounts.domain.exceptions.name_already_registered import (
    NameAlreadyRegistered,
)
from src.planner.accounts.domain.repository import AccountRepository
from src.planner.accounts.domain.value_objects import (
    AccountBalance,
    AccountCurrency,
    AccountName,
)
from src.planner.shared.domain.accounts import AccountId
from src.planner.shared.domain.users import UserId
from src.shared.domain.bus.event.event_bus import EventBus


@inject(use_factory=True)
class AccountCreator:
    def __init__(self, repository: AccountRepository, event_bus: EventBus):
        self._repository = repository
        self._event_bus = event_bus

    async def __call__(
        self,
        id: AccountId,
        owner_id: UserId,
        name: AccountName,
        currency: AccountCurrency,
        balance: AccountBalance,
    ) -> None:
        if await self._repository.search_by_name_and_owner_id(name, owner_id):
            raise NameAlreadyRegistered(name)

        account = Account.create(id, owner_id, name, currency, balance)
        await self._repository.save(account)
        await self._event_bus.publish(*account.pull_domain_events())
