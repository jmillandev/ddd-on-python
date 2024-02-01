from dataclasses import dataclass

from src.planner.shared.domain.bus.command import Command


@dataclass(frozen=True)
class AddExpenseCommand(Command):
    id: str
    amount: int
    account_id: str
    date: str
