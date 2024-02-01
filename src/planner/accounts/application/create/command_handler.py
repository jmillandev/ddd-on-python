from kink import inject

from src.planner.accounts.domain.value_objects import (
    AccountBalance,
    AccountCurrency,
    AccountName,
)
from src.planner.shared.domain.accounts import AccountId
from src.planner.shared.domain.users import UserId

from .command import CreateAccountCommand
from .creator import AccountCreator


@inject
class CreateAccountCommandHandler:
    def __init__(self, user_case: AccountCreator) -> None:
        self.user_case = user_case

    async def __call__(self, command: CreateAccountCommand) -> None:
        await self.user_case(
            id=AccountId(command.id),
            user_id=UserId(command.user_id),
            name=AccountName(command.name),
            currency=AccountCurrency(command.currency),
            balance=AccountBalance(command.balance),
        )
