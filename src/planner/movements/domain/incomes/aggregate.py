from dataclasses import dataclass
from typing import Self

from src.planner.movements.domain.aggregate import Movement
from src.planner.movements.domain.value_objects.amount import MovementAmount
from src.planner.movements.domain.value_objects.date import MovementDate
from src.planner.movements.domain.value_objects.id import MovementId
from src.planner.shared.domain.accounts import AccountId
from src.planner.shared.domain.movements.events import IncomeMovementAdded


@dataclass
class IncomeMovement(Movement):
    account_id: AccountId

    @classmethod
    def add(
        cls,
        id: MovementId,
        amount: MovementAmount,
        account_id: AccountId,
        date: MovementDate,
    ) -> Self:
        income = cls(id=id, amount=amount, account_id=account_id, date=date)
        income._record_event(
            IncomeMovementAdded.make(
                income.id.primitive,
                date=income.date.primitive,
                amount=income.amount.primitive,
                account_id=income.account_id.primitive,
            )
        )
        return income
