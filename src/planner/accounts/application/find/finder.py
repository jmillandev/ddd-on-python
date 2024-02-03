from src.planner.accounts.domain.entity import Account
from src.planner.accounts.domain.exceptions.not_found import AccountNotFound
from src.planner.accounts.domain.repository import AccountRepository
from src.planner.shared.domain.accounts import AccountId
from src.planner.shared.domain.users import UserId


class AccountFinder:
    def __init__(self, repository: AccountRepository):
        self._repository = repository

    async def __call__(self, id: AccountId, owner_id: UserId) -> Account:
        account = await self._repository.search_by_id_and_owner_id(id, owner_id)
        if account is None:
            raise AccountNotFound

        return account
