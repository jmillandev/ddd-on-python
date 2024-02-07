from dataclasses import dataclass
from typing import Self

from src.planner.movements.domain.aggregate import Movement
from src.planner.movements.domain.value_objects.amount import ExpenseAmount
from src.planner.movements.domain.value_objects.date import ExpenseDate
from src.planner.movements.domain.value_objects.id import ExpenseId
from src.planner.shared.domain.accounts import AccountId

from .events.added import ExpenseMovementAdded


@dataclass
class ExpenseMovement(Movement):
    account_id: AccountId

    @classmethod
    def add(
        cls,
        id: ExpenseId,
        amount: ExpenseAmount,
        account_id: AccountId,
        date: ExpenseDate,
    ) -> Self:
        expense = cls(id=id, amount=amount, account_id=account_id, date=date)
        expense._record_event(
            ExpenseMovementAdded.make(
                expense.id.primitive,
                date=expense.date.primitive,
                amount=expense.amount.primitive,
                account_id=expense.account_id.primitive,
            )
        )
        return expense
