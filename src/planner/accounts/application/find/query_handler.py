from kink import inject

from src.planner.shared.application.accounts.query import FindAccountQuery
from src.planner.shared.application.accounts.response import AccountResponse
from src.planner.shared.application.mappers import entity_to_response
from src.planner.shared.domain.accounts import AccountId
from src.planner.shared.domain.users import UserId

from .finder import AccountFinder


@inject
class FindAccountQueryHandler:
    def __init__(self, use_case: AccountFinder) -> None:
        self.use_case = use_case

    async def __call__(self, query: FindAccountQuery) -> AccountResponse:
        account = await self.use_case(AccountId(query.id), UserId(query.owner_id))
        return entity_to_response(account, AccountResponse)
