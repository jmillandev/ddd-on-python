from dataclasses import asdict, dataclass

from src.planner.movements.application.transfers.add.command import (
    AddTransferMovementCommand,
)


@dataclass(frozen=True)
class AddTransferSchema:
    __annotations__ = {
        key: value
        for key, value in AddTransferMovementCommand.__annotations__.items()
        if key not in ["id", "user_id"]
    }

    def to_dict(self):
        return asdict(self)
