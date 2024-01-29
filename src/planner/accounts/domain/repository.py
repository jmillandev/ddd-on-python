from typing import Optional, Protocol, runtime_checkable

from src.planner.accounts.domain.entity import Account
from src.planner.accounts.domain.value_objects import AccountName
from src.planner.shared.domain.users.id import UserId


@runtime_checkable
class AccountRepository(Protocol):
    async def create(self, account: Account) -> None:
        ...

    async def search_by_name_and_user_id(
        self, name: AccountName, user_id: UserId
    ) -> Optional[Account]:
        ...
