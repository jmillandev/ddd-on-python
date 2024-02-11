from kink import inject

from src.planner.movements.domain.value_objects import (
    MovementAmount,
    MovementDate,
    MovementId,
)
from src.planner.shared.domain.accounts import AccountId
from src.planner.shared.domain.users import UserId

from .adder import TransferMovementAdder
from .command import AddTransferMovementCommand


@inject
class AddTransferMovementCommandHandler:
    def __init__(self, use_case: TransferMovementAdder) -> None:
        self.use_case = use_case

    async def __call__(self, command: AddTransferMovementCommand) -> None:
        await self.use_case(
            id=MovementId(command.id),
            amount=MovementAmount(command.amount),
            origin_id=AccountId(command.origin_id),
            destination_id=AccountId(command.destination_id),
            date=MovementDate(command.date),
            user_id=UserId(command.user_id),
        )
