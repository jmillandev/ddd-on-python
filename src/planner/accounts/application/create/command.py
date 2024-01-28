from dataclasses import dataclass

from src.planner.shared.domain.bus.command import Command


@dataclass(frozen=True)
class CreateAccountCommand(Command):
    currency: str
    balance: int
    id: str
    name: str
    user_id: str
