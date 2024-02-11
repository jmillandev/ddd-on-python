from dataclasses import asdict, dataclass

from src.planner.movements.application.incomes.add.command import (
    AddIncomeMovementCommand,
)


@dataclass(frozen=True)
class AddIncomeSchema:
    __annotations__ = {
        key: value
        for key, value in AddIncomeMovementCommand.__annotations__.items()
        if key not in ["id", "user_id"]
    }

    def to_dict(self):
        return asdict(self)
