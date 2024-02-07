from dataclasses import dataclass
from typing import Self

from src.planner.shared.domain.accounts import AccountId
from src.planner.shared.domain.users import UserId
from src.planner.shared.domain.aggregates import AggregateRoot

from .events.added import ExpenseAdded
from .value_objects.amount import ExpenseAmount
from .value_objects.date import ExpenseDate
from .value_objects.id import ExpenseId


@dataclass
class Expense(AggregateRoot):
    id: ExpenseId
    amount: ExpenseAmount
    account_id: AccountId
    date: ExpenseDate

    def __str__(self) -> str:
        return f"Expense(id={self.id}, account_id={self.account_id})"

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
            ExpenseAdded.make(
                expense.id.primitive,
                date=expense.date.primitive,
                amount=expense.amount.primitive,
                account_id=expense.account_id.primitive,
            )
        )
        return expense


# TODO: Add to Expense
@dataclass
class Account:
    id: AccountId
    owner_id: UserId
