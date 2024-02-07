from dataclasses import asdict, dataclass

from src.planner.movements.application.expenses.add.command import (
    AddExpenseMovementCommand,
)


@dataclass(frozen=True)
class AddExpenseSchema:
    __annotations__ = {
        key: value
        for key, value in AddExpenseMovementCommand.__annotations__.items()
        if key not in ["id", "user_id"]
    }

    def to_dict(self):
        return asdict(self)
