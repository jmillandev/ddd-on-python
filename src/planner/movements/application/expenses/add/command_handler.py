from kink import inject

from src.planner.movements.domain.value_objects import (
    ExpenseAmount,
    ExpenseDate,
    ExpenseId,
)
from src.planner.shared.domain.accounts import AccountId
from src.planner.shared.domain.users import UserId

from .adder import ExpenseMovementAdder
from .command import AddExpenseMovementCommand


@inject
class AddExpenseMovementCommandHandler:
    def __init__(self, user_case: ExpenseMovementAdder) -> None:
        self.user_case = user_case

    async def __call__(self, command: AddExpenseMovementCommand) -> None:
        await self.user_case(
            id=ExpenseId(command.id),
            amount=ExpenseAmount(command.amount),
            account_id=AccountId(command.account_id),
            date=ExpenseDate(command.date),
            user_id=UserId(command.user_id),
        )
