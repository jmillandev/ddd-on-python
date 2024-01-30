from dataclasses import dataclass

from src.planner.shared.domain.bus.command import Command


@dataclass(frozen=True)
class CreateAuthTokenCommand(Command):
    username: str
    password: str
