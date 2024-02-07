from dataclasses import dataclass

from src.planner.shared.domain.aggregates import AggregateRoot

from .value_objects.amount import ExpenseAmount
from .value_objects.date import ExpenseDate
from .value_objects.id import ExpenseId


@dataclass
class Movement(AggregateRoot):
    id: ExpenseId
    amount: ExpenseAmount
    date: ExpenseDate

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"
