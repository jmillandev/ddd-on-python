from src.planner.accounts.domain.entity import Account
from src.planner.accounts.domain.exceptions.name_already_registered import (
    NameAlreadyRegistered,
)
from src.planner.accounts.domain.repository import AccountRepository
from src.planner.accounts.domain.value_objects import (
    AccountBalance,
    AccountCurrency,
    AccountId,
    AccountName,
)
from kink import inject
from src.planner.shared.domain.users import UserId
from src.shared.domain.bus.event.event_bus import EventBus


@inject
class AccountCreator:
    def __init__(self, repository: AccountRepository, event_bus: EventBus):
        self._repository = repository
        self._event_bus = event_bus

    async def __call__(
        self,
        id: AccountId,
        user_id: UserId,
        name: AccountName,
        currency: AccountCurrency,
        balance: AccountBalance,
    ) -> None:
        if await self._repository.search_by_name_and_user_id(
            name, user_id
        ):  # TODO: Implement Criteria
            raise NameAlreadyRegistered(name)

        account = Account.create(id, user_id, name, currency, balance)
        await self._repository.create(account)
        await self._event_bus.publish(*account.pull_domain_events())
