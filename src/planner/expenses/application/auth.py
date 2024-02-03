from typing import cast

from kink import inject

from src.planner.shared.application.accounts.query import FindAccountQuery
from src.planner.shared.application.accounts.response import AccountResponse
from src.planner.shared.domain.accounts import AccountId
from src.planner.shared.domain.bus.query import QueryBus
from src.planner.shared.domain.exceptions.forbidden import ForbiddenAccess
from src.planner.shared.domain.users import UserId


@inject
class ExpenseAuthorizationService:
    def __init__(self, query_bus: QueryBus) -> None:
        self.query_bus = query_bus

    async def ensure_user_is_account_owner(
        self, account_id: AccountId, user_id: UserId
    ) -> None:
        account = await self.query_bus.ask(
            FindAccountQuery(id=account_id.primitive, owner_id=user_id.primitive)
        )
        account = cast(AccountResponse, account)
        if account.owner_id != user_id.primitive:
            raise ForbiddenAccess
