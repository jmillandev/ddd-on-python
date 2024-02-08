from dataclasses import dataclass
from typing import Self

from src.planner.movements.domain.aggregate import Movement
from src.planner.movements.domain.value_objects.amount import MovementAmount
from src.planner.movements.domain.value_objects.date import MovementDate
from src.planner.movements.domain.value_objects.id import MovementId
from src.planner.shared.domain.accounts import AccountId

from src.planner.shared.domain.movements.events import ExpenseMovementAdded


@dataclass
class ExpenseMovement(Movement):
    account_id: AccountId

    @classmethod
    def add(
        cls,
        id: MovementId,
        amount: MovementAmount,
        account_id: AccountId,
        date: MovementDate,
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
