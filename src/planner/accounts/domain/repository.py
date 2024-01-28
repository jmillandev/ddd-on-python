from typing import Protocol, runtime_checkable, Optional

from src.planner.accounts.domain.value_objects import AccountId, AccountName
from src.planner.accounts.domain.entity import Account
from src.planner.shared.domain.users.id import UserId


@runtime_checkable
class AccountRepository(Protocol):
    async def create(self, account: Account) -> None:
        ...

    async def search(self, account_id: AccountId) -> Optional[Account]:
        ...

    async def search_by_name_and_user_id(self, name: AccountName, user_id: UserId) -> Optional[Account]:
        ...
