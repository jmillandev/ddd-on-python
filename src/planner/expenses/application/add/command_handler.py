from kink import inject

from src.planner.shared.domain.accounts import AccountId
from src.planner.expenses.domain.value_objects import (
    ExpenseId,
    ExpenseAmount,
    ExpenseDate
)
from src.planner.shared.domain.users import UserId
from .command import AddExpenseCommand
from .adder import ExpenseAdder


@inject
class AddExpenseCommandHandler:
    def __init__(self, user_case: ExpenseAdder) -> None:
        self.user_case = user_case

    async def __call__(self, command: AddExpenseCommand) -> None:
        await self.user_case(
            id=ExpenseId(command.id),
            amount=ExpenseAmount(command.amount),
            account_id=AccountId(command.account_id),
            date=ExpenseDate(command.date),
            user_id=UserId(command.user_id)
        )
