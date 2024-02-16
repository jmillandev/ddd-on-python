from dataclasses import dataclass

from src.planner.shared.domain.bus.command import Command


@dataclass(frozen=True)
class UpdateUserAvatarCommand(Command):
    id: str
    avatar: bytes
    user_id: str
