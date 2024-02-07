from dataclasses import asdict, dataclass

from src.planner.expenses.application.add.command import AddExpenseCommand


@dataclass(frozen=True)
class AddExpenseSchema:
    __annotations__ = {
        key: value
        for key, value in AddExpenseCommand.__annotations__.items()
        if key not in ["id", "user_id"]
    }

    def to_dict(self):
        return asdict(self)
