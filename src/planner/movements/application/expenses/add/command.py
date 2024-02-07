from dataclasses import dataclass

from src.planner.shared.domain.bus.command import Command


@dataclass(frozen=True)
class AddExpenseMovementCommand(Command):
    id: str
    amount: int
    account_id: str
    date: str
    user_id: str
