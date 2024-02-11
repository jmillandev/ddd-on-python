from dataclasses import dataclass

from src.planner.shared.domain.bus.command import Command


@dataclass(frozen=True)
class AddTransferMovementCommand(Command):
    id: str
    amount: int
    date: str
    user_id: str
    origin_id: str
    destination_id: str
