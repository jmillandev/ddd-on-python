from typing import Optional, Protocol, runtime_checkable

from src.planner.accounts.domain.entity import Account
from src.planner.accounts.domain.value_objects import AccountName
from src.planner.shared.domain.accounts.id import AccountId
from src.planner.shared.domain.users.id import UserId


@runtime_checkable
class AccountRepository(Protocol):
    async def save(self, account: Account) -> None:
        ...

    async def search_by_name_and_owner_id(
        self, name: AccountName, owner_id: UserId
    ) -> Optional[Account]:
        ...

    async def search_by_id_and_owner_id(
        self, id: AccountId, owner_id: UserId
    ) -> Optional[Account]:
        ...

    async def search(self, id: AccountId) -> Optional[Account]:
        ...
