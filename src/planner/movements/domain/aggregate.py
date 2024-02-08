from dataclasses import dataclass

from src.planner.shared.domain.aggregates import AggregateRoot

from .value_objects.amount import MovementAmount
from .value_objects.date import MovementDate
from .value_objects.id import MovementId


@dataclass
class Movement(AggregateRoot):
    id: MovementId
    amount: MovementAmount
    date: MovementDate

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"
