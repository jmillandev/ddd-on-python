from src.planner.shared.domain.aggregates import AggregateRoot
from dataclasses import dataclass
from .value_objects.amount import ExpenseAmount
from .value_objects.date import ExpenseDate
from .value_objects.id import ExpenseId
from src.planner.shared.domain.accounts import AccountId
from .events.added import ExpenseAdded


@dataclass
class Expense(AggregateRoot):
    id: ExpenseId
    amount: ExpenseAmount
    account_id: AccountId
    date: ExpenseDate

    @classmethod
    def add(cls, id: ExpenseId, amount: ExpenseAmount, account_id: AccountId, date: ExpenseDate) -> None:
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
